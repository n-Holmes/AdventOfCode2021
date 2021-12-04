class Submarine:
    DELTAS = {"forward": (1, 0), "down": (0, 1), "up": (0, -1)}

    def __init__(self) -> None:
        self.travel = 0
        self.depth = 0

    def move(self, instruction):
        direction, s_dist = instruction.strip().split()
        dist = int(s_dist)

        delta_t, delta_d = Submarine.DELTAS[direction]
        self.travel += delta_t * dist
        self.depth += delta_d * dist

    def run(self, instructions):
        for instr in instructions:
            self.move(instr)


class AimSubmarine:
    def __init__(self) -> None:
        self.travel = 0
        self.depth = 0
        self.aim = 0

    def move(self, instruction):
        direction, s_dist = instruction.strip().split()
        dist = int(s_dist)

        if direction == "down":
            self.aim += dist
        elif direction == "up":
            self.aim -= dist
        elif direction == "forward":
            self.travel += dist
            self.depth += dist * self.aim

    def run(self, instructions):
        for instr in instructions:
            self.move(instr)


if __name__ == "__main__":
    with open("input2.txt") as f:
        instructions = f.read().strip().split("\n")

    # Part 1
    sub = Submarine()
    sub.run(instructions)
    print(sub.travel, sub.depth, sub.travel * sub.depth)

    # Part 1
    sub = AimSubmarine()
    sub.run(instructions)
    print(sub.travel, sub.depth, sub.travel * sub.depth)
