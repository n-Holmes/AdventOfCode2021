from itertools import permutations
from timeit import default_timer as timer

# The segments turned on for each digit
DIGITS = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]


def get_outputs(line):
    _, o = line.split("|")
    return o.strip().split()


def get_digits(line):
    """Get the coded digits from the input line.
    Return a list sorted by length as the shortest are the most useful.
    """
    return sorted(line.strip().replace("| ", "").split(), key=len)


def part_1(outputs):
    count = sum(len(s) in [2, 3, 4, 7] for l in outputs for s in l)
    print(f"There are {count} identifiable output digits")


def map_digit(coded_digit, encoding):
    """Maps a coded digit to a value, using the given encoding"""
    A = ord("a")

    uncoded = "".join(sorted(encoding[ord(c) - A] for c in coded_digit.strip()))
    try:
        return DIGITS.index(uncoded)
    except ValueError:
        return None


def decode_mapping(line):
    coded_digits = get_digits(line)

    for encoding in permutations("abcdefg", 7):
        if all(map_digit(cd, encoding) is not None for cd in coded_digits):
            # Found a valid encoding
            coded_output = get_outputs(line)
            output = int("".join(str(map_digit(cd, encoding)) for cd in coded_output))

            # print(coded_output, output)
            return output


def part_2(lines):
    print(sum(decode_mapping(line) for line in lines))


if __name__ == "__main__":
    start = timer()

    with open("input8.txt") as f:
        lines = f.readlines()

    part_1(map(get_outputs, lines))
    part_2(lines)

    print(f"Solution took {timer() - start}s") # 0.733s
