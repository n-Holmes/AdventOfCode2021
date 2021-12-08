# The segments turned on for each digit
DIGITS = [
    {0, 1, 2, 4, 5, 6},
    {2, 5},
    {0, 2, 3, 4, 6},
    {0, 2, 3, 5, 6},
    {1, 2, 3, 5},
    {0, 1, 3, 5, 6},
    {0, 1, 3, 4, 5, 6},
    {0, 2, 5},
    {0, 1, 2, 3, 4, 5, 6},
    {0, 1, 2, 3, 5, 6},
]

DIGIT_LENS = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]


def get_outputs(line):
    _, o = line.split("|")
    return o.strip()


def get_digits(line):
    return line.strip().replace("| ", "").split()


def part_1(outputs):
    count = sum(len(s) in [2, 3, 4, 7] for l in outputs for s in l.split())
    print(f"There are {count} identifiable output digits")


def decode_mapping(line):
    coded_digits = get_digits(line)

    valid_mappings = {c: set(range(7)) for c in range(ord("a"), ord("g") + 1)}

    for cd in coded_digits:
        pass

if __name__ == "__main__":
    with open("input8.txt") as f:
        lines = f.readlines()

    part_1(map(get_outputs, lines))
