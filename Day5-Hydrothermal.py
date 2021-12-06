from collections import Counter
from timeit import default_timer as timer


def get_depths(lines, allow_diagonal=False):
    depths = Counter()
    for a, b in lines:
        # set a to be the lower of the pair, for simplicity
        a, b = sorted((a, b))

        if a[0] == b[0]:
            # Vertical
            i = a[0]
            for j in range(a[1], b[1] + 1):
                depths[i, j] += 1

        elif a[1] == b[1]:
            # Horizontal
            j = a[1]
            for i in range(a[0], b[0] + 1):
                depths[i, j] += 1

        elif allow_diagonal:
            if sum(a) == sum(b):
                # Minor diagonal
                cap = sum(a)
                for i in range(a[0], b[0] + 1):
                    j = cap - i
                    depths[i, j] += 1
            elif a[0] - a[1] == b[0] - b[1]:
                # Major diagonal
                for k in range(b[0] - a[0] + 1):
                    i = a[0] + k
                    j = a[1] + k
                    depths[i, j] += 1
            else:
                # Oh dear!
                print(f"Missed one: {a}, {b}")

    return depths


if __name__ == "__main__":
    start = timer()

    with open("input5.txt") as f:
        s_lines = f.readlines()

    to_coords = lambda s: tuple(map(int, s.split(",")))
    lines = []
    for line in s_lines:
        a, _, b = line.split()
        lines.append((to_coords(a), to_coords(b)))

    # Part 1
    depths = get_depths(lines)
    print("Number of points containing more than one vent:")
    print(sum(1 for x in depths.values() if x >= 2))

    # Part 2
    depths = get_depths(lines, True)
    print("\nNumber of points containing more than one vent (with diagonals):")
    print(sum(1 for x in depths.values() if x >= 2))

    print(f"\nSolution took {timer() - start:.4} seconds")
