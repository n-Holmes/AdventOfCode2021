from statistics import median
from timeit import default_timer as timer

OPENERS = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}


def score_invalid(line):
    """Gets the score of an invalid line.
    Returns 0 if the line is incomplete or valid.
    """
    SCORES = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    stack = []
    for char in line:
        if char in OPENERS:
            if not stack or not (stack.pop() == OPENERS[char]):
                return SCORES[char]
        else:
            stack.append(char)

    return 0


def score_incomplete(line):
    """Gets the completion score of an incomplete line.
    Returns 0 if the line is invalid or complete.
    """
    SCORES = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }

    stack = []
    for char in line:
        if char in OPENERS:
            if not stack or not (stack.pop() == OPENERS[char]):
                return 0
        else:
            stack.append(char)

    score = 0
    while stack:
        score = score * 5 + SCORES[stack.pop()]

    return score


if __name__ == "__main__":
    start = timer()

    with open("input10.txt") as f:
        lines = f.readlines()

    invalid = [x for x in (score_invalid(line) for line in lines) if x]
    count = len(invalid)
    total = sum(invalid)
    print(f"There were {count} invalid lines, with a total score of {total}.")

    completion = [x for x in (score_incomplete(line.strip()) for line in lines) if x]
    count = len(completion)
    middle = median(completion)
    print(f"There were {count} incomplete lines, with a median score of {middle}.")

    print(f"Solution took {timer() - start:.3}s")  # 1.6ms
