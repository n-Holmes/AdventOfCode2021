def most_common_bit(entries, position):
    bitmask = 1 << position
    average = sum(entry & bitmask for entry in entries) / bitmask / len(entries)
    return average >= 0.5


def get_gamma(entries, bits):
    gamma = 0
    for i in range(bits):
        value = most_common_bit(entries, i)
        gamma += value << i

    return gamma


def get_support_value(entries, bits, target_most_common):
    remaining = entries[:]

    for bit in reversed(range(bits)):
        mcb = most_common_bit(remaining, bit)
        target_val = mcb if target_most_common else not mcb

        # print(bit, target_val, list(map(bin, remaining)))

        remaining = [x for x in remaining if ((x >> bit) & 1) == target_val]

        if len(remaining) <= 1:
            break

    return remaining.pop()


if __name__ == "__main__":
    with open("input3.txt") as f:
        str_entries = list(map(str.strip, f.readlines()))

    bits = len(str_entries[0])
    entries = [int(e, 2) for e in str_entries]

    # Part 1
    gamma = get_gamma(entries, bits)
    epsilon = 2 ** (bits - 1) - 1 - gamma
    print(bin(gamma), bin(epsilon), gamma * epsilon)

    # Part 2
    ox_val = get_support_value(entries, bits, True)
    co_val = get_support_value(entries, bits, False)
    print(bin(ox_val), bin(co_val), ox_val * co_val)
