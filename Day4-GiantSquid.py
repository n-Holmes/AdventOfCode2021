class BingoGrid:
    def __init__(self, lines, id) -> None:
        self.id = id
        self.grid = {}  # indices stored by value
        for i, row in enumerate(lines.split("\n")):
            for j, val in enumerate(map(int, row.strip().split())):
                self.grid[val] = (i, j)

        self.seen = [[False] * 5 for _ in range(5)]
        self.has_line = False

    def play(self, n, allow_diagonals=False):
        try:
            i, j = self.grid[n]
            self.seen[i][j] = True

            # Check if we have formed a line
            if all(self.seen[i]) or all(self.seen[k][j] for k in range(5)):
                self.has_line = True

            if allow_diagonals:
                if i == j and all(self.seen[k][k] for k in range(5)):
                    self.has_line = True
                if i + j == 4 and all(self.seen[k][4 - k] for k in range(5)):
                    self.has_line = True

        except KeyError:
            pass

    def sum_unmarked(self):
        return sum(val for val, (i, j) in self.grid.items() if not self.seen[i][j])


class BingoGame:
    def __init__(self, contents) -> None:
        moves, *grids = contents.split("\n\n")
        self.moves = [int(s) for s in moves.split(",")][::-1]
        self.grids = [BingoGrid(s, i) for i, s in enumerate(grids, 1)]

    def play(self):
        while not any(grid.has_line for grid in self.grids):
            move = self.moves.pop()
            print("Calling ", move)
            for grid in self.grids:
                grid.play(move)

        for i, grid in enumerate(self.grids):
            if grid.has_line:
                print(f"grid {i+1} wins!")
                unmk = grid.sum_unmarked()
                print(unmk, move, unmk * move)

    def play_to_lose(self):
        remaining = self.grids[:]
        while remaining:
            move = self.moves.pop()
            for i in range(len(remaining) - 1, -1, -1):
                grid = remaining[i]
                grid.play(move)

                if grid.has_line:
                    if len(remaining) == 1:
                        print(f"Grid {grid.id} loses!")
                        unmk = grid.sum_unmarked()
                        print(unmk, move, unmk * move)

                    remaining.pop(i)


if __name__ == "__main__":
    with open("input4.txt") as f:
        contents = f.read().strip()

    # Part 1
    game = BingoGame(contents)
    game.play()

    # Part 2
    game = BingoGame(contents)
    game.play_to_lose()
