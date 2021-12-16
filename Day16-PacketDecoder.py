from timeit import default_timer as timer


class BitStream:
    """Wraps a stream of binary data."""

    def __init__(self, data, base=16):
        data = data.strip()  # safety

        if base == 16:
            # convert to binary string first
            data = bin(int(data, 16))[2:].rjust(len(data) * 4, "0")

        self._bits = (int(c) for c in data)
        self._i = 0
        self._counters = []  # stack of counter indices

    def get(self, n_bits=1):
        """Get the value of the next (n) bit(s)."""
        val = 0
        for _ in range(n_bits):
            val = (val << 1) + next(self._bits)
            self._i += 1

        return val

    def start_count(self):
        """Adds a count index to the stack.  Make sure to call get_count!"""
        self._counters.append(self._i)

    def get_count(self):
        """Gets a count index from the stack."""
        return self._i - self._counters.pop()


class Packet:
    def __init__(self, stream: BitStream):
        self.version = stream.get(3)
        self.type = stream.get(3)

        self.literal_val = 0
        self.sub_packets = []

        if self.type == 4:
            self.literal_val = self.get_literal(stream)

        else:
            # operator packet
            self.sub_packets = list(self.get_subpackets(stream))
            # print(f"Operator v{self.version}. {len(self.sub_packets)} sub packets.")

    @staticmethod
    def get_literal(stream):
        """Gets the value of a literal packet from the stream."""
        cont = True
        val = 0
        while cont:
            cont = stream.get()
            val = (val << 4) + stream.get(4)

        return val

    @staticmethod
    def get_subpackets(stream):
        """Generates the sub packets of an operator packet from the stream."""
        sub_len = sub_count = 0
        content_type = stream.get()
        if content_type == 0:
            sub_len = stream.get(15)
        else:
            sub_count = stream.get(11)

        while sub_len > 0 or sub_count > 0:
            stream.start_count()
            yield Packet(stream)
            packet_bits = stream.get_count()

            sub_len -= packet_bits
            sub_count -= 1

    def evaluate(self):
        """Calculates the value of the packet, based on its type."""
        values = [p.evaluate() for p in self.sub_packets]

        if self.type == 0:  # SUM
            return sum(values)
        elif self.type == 1:  # PRODUCT
            val = 1
            for x in values:
                val *= x
            return val
        elif self.type == 2:  # MIN
            return min(values)
        elif self.type == 3:  # MAX
            return max(values)
        elif self.type == 4:  # VALUE
            return self.literal_val
        elif self.type == 5:  # GT?
            return int(values[0] > values[1])
        elif self.type == 6:  # LT?
            return int(values[0] < values[1])
        elif self.type == 7:  # EQ?
            return int(values[0] == values[1])
        else:
            raise ValueError(f"Invalid packet type: {self.type}")

    def version_sum(self):
        return self.version + sum(p.version_sum() for p in self.sub_packets)

    def tree_size(self):
        return 1 + sum(p.tree_size() for p in self.sub_packets)


if __name__ == "__main__":
    start = timer()
    with open("input16.txt") as f:
        lines = f.readlines()

    for line in lines:
        stream = BitStream(line, 16)
        packet = Packet(stream)

        print(
            f"Found {packet.tree_size()} total packets with version sum {packet.version_sum()}"
        )
        print(f"Packet evaluates to", packet.evaluate(), "\n")

    print(f"Solution took {timer() - start:.3}s to complete.")
