from itertools import product
from functools import lru_cache
from timeit import default_timer as timer


class OctopusCave:
    """A cave full of flashing dumbo octopus"""
    def __init__(self, lines) -> None:
        self.octopi = [[int(c) for c in line.strip()] for line in lines]

        self.flash_count = 0
        self.steps = 0

    @lru_cache
    def adj(self, i, j):
        """List the adjacent positions in the grid"""
        return [
            (i + d_i, j + d_j)
            for d_i, d_j in product((-1, 0, 1), repeat=2)
            if 0 <= i + d_i < 10 and 0 <= j + d_j < 10 and (d_i or d_j)
        ]

    def step(self):
        """Increase and flash some octopodes"""
        self.steps += 1

        flashers = []
        for i, row in enumerate(self.octopi):
            for j, val in enumerate(row):
                self.octopi[i][j] = val + 1
                if val == 9:
                    flashers.append((i, j))

        for i, j in flashers:
            self.octopi[i][j] = 0
            for a, b in self.adj(i, j):
                val = self.octopi[a][b]
                if val == 0:
                    continue # Already flashed
                if val == 9:
                    flashers.append((a, b))
                self.octopi[a][b] = val + 1

        self.flash_count += len(flashers)

    def progress(self, n):
        """Progress the octopi through n steps"""
        for _ in range(n):
            self.step()
        return self.flash_count

    def find_sync(self):
        """Find the step at which all octopuses flash"""
        while sum(sum(row) for row in self.octopi):
            self.step()
        return self.steps

    def print_grid(self):
        """Print off the octopus cave in the input format"""
        for row in self.octopi:
            print("".join(map(str, row)))


if __name__ == "__main__":
    start = timer()
    with open("input11.txt") as f:
        lines = f.readlines()

    cave = OctopusCave(lines)
    flashes = cave.progress(100)
    print(f"There were {flashes} flashes in the first 100 steps.")

    steps_to_sync = cave.find_sync()
    print(f"It took {steps_to_sync} steps to synchronise all the octopodes.")

    print(f"Solution took {timer() - start:.3}s")  # 5.6ms
