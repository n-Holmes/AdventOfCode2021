from itertools import permutations
from timeit import default_timer as timer

# The segments turned on for each digit
# Using a dict instead of a list of strings: 0.73s -> 0.54s
DIGITS = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def get_outputs(line):
    _, o = line.split("|")
    return o.strip().split()


def get_digits(line):
    """Get the coded digits from the input line.
    Return a list sorted by length as the shortest are the most useful.
    """

    # Sorting the digits by shortest first means that encodings should fail faster
    # Effect 1.03s unsorted -> 0.73s sorted
    return sorted(line.strip().replace("| ", "").split(), key=len)


def part_1(outputs):
    count = sum(len(s) in [2, 3, 4, 7] for l in outputs for s in l)
    print(f"There are {count} identifiable output digits")


def map_digit(coded_digit, encoding):
    """Maps a coded digit to a value, using the given encoding"""
    A = ord("a")

    uncoded = "".join(sorted(encoding[ord(c) - A] for c in coded_digit))

    return DIGITS.get(uncoded, None)


def decode_mapping(line):
    """Given a series of encoded seven-segment digits, find the integer written out by
    the unencoded digits following the '|'
    """
    coded_digits = get_digits(line)

    # Just brute force check every permutation.
    for encoding in permutations("abcdefg", 7):
        if all(map_digit(cd, encoding) is not None for cd in coded_digits):
            # Found a valid encoding
            coded_output = get_outputs(line)
            output = int("".join(str(map_digit(cd, encoding)) for cd in coded_output))

            # print(coded_output, output)
            return output


def part_2(lines):
    # Add up all the decoded values
    output_sum = sum(decode_mapping(line) for line in lines)
    print(f"The sum of the decoded outputs is {output_sum}")


if __name__ == "__main__":
    start = timer()

    with open("input8.txt") as f:
        lines = f.readlines()

    part_1(map(get_outputs, lines))
    part_2(lines)

    print(f"Solution took {timer() - start:.4}s")  # 0.55s
