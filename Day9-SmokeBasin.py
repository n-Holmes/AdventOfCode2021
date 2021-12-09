from timeit import default_timer as timer


def adj_points(i, j, height, width):
    """Generate the adjacent co-ordinates to a point in a grid with given dimensions."""
    if i > 0:
        yield (i - 1, j)
    if i < height - 1:
        yield (i + 1, j)
    if j > 0:
        yield (i, j - 1)
    if j < width - 1:
        yield (i, j + 1)


def find_minima(grid):
    """Find the minimum points in a grid"""
    n, m = len(grid), len(grid[0])

    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if all(grid[r][c] > val for r, c in adj_points(i, j, n, m)):
                # print(f"Minima at {i}, {j}: {val}")
                yield (i, j, val)


def get_basin_sizes(grid):
    """Generate sizes of basins found, in no particular order."""

    n, m = len(grid), len(grid[0])
    # Going to assume that all basins are bounded by 9s and use flood-fill

    unseen = {(i, j) for i in range(n) for j in range(m) if grid[i][j] != 9}

    while unseen:
        start = unseen.pop()
        basin = [start]
        for i, j in basin:
            for adj in adj_points(i, j, n, m):
                try:
                    unseen.remove(adj)
                    basin.append(adj)
                except KeyError:
                    pass
        yield len(basin)


if __name__ == "__main__":
    start = timer()

    with open("input9.txt") as f:
        grid = [[int(c) for c in row.strip()] for row in f.readlines()]

    minimasum = sum(1 + v for _, _, v in find_minima(grid))
    print(f"The sum of the risk levels is {minimasum}")

    basin_sizes = sorted(get_basin_sizes(grid))
    print(f"The largest basin sizes are: {basin_sizes[-3:]}")
    print("Product:", basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1])

    print(f"Solution took {timer() - start:.3}s")  # 17ms
