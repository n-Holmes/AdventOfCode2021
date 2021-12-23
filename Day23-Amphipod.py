from functools import lru_cache
from heapq import heappop, heappush
from typing import List, Tuple
from timeit import default_timer as timer

TARGETS = dict(zip("ABCD", [0, 1, 2, 3]))
WEIGHTS = dict(zip("ABCD", [1, 10, 100, 1000]))
BLOCK_SPACES = {
    (0, 10): [11],
    (0, 11): [],
    (0, 12): [],
    (0, 13): [12],
    (0, 14): [12, 13],
    (0, 15): [12, 13, 14],
    (0, 16): [12, 13, 14, 15],
    (1, 10): [11, 12],
    (1, 11): [12],
    (1, 12): [],
    (1, 13): [],
    (1, 14): [13],
    (1, 15): [13, 14],
    (1, 16): [13, 14, 15],
    (2, 10): [11, 12, 13],
    (2, 11): [12, 13],
    (2, 12): [13],
    (2, 13): [],
    (2, 14): [],
    (2, 15): [14],
    (2, 16): [14, 15],
    (3, 10): [11, 12, 13, 14],
    (3, 11): [12, 13, 14],
    (3, 12): [13, 14],
    (3, 13): [14],
    (3, 14): [],
    (3, 15): [],
    (3, 16): [15],
}


class AmphiRoom:
    def __init__(
        self, rows=None, stacks=None, spaces=None, cost=0, parent=None
    ) -> None:
        if rows:
            self.stacks = [[], [], [], []]  # spaces 0 to 3
            self.spaces = [None] * 7  # spaces 10 to 16

            for row in rows[::-1]:
                for i, c in enumerate(row):
                    self.stacks[i].append(c)

            self.clear_stacks = []
            self.filled_stacks = []

        else:
            self.stacks = [stack[:] for stack in stacks]
            self.spaces = spaces[:]
            self.cost = cost

            self.clear_stacks = []
            self.filled_stacks = []
            for i, stack in enumerate(self.stacks):
                if all(TARGETS[a] == i for a in stack):
                    self.clear_stacks.append(i)
                    if len(stack) == 4:
                        self.filled_stacks.append(i)

        self.cost = cost
        self.parent = parent

    def copy(self):
        return AmphiRoom(
            stacks=self.stacks, spaces=self.spaces, cost=self.cost, parent=self
        )

    def at(self, pos: int) -> str:
        """Which amphi is at the given position?"""
        if pos < 10:
            return self.stacks[pos][-1] if self.stacks[pos] else None
        return self.spaces[pos - 10]

    def move(self, start, end):
        if start < 10:
            amphi = self.stacks[start].pop()
            if len(self.stacks[start]) == 0:
                self.clear_stacks.append(start)
        else:
            amphi = self.spaces[start - 10]
            self.spaces[start - 10] = None

        stack, space = sorted((start, end))
        score = AmphiRoom.score_move(stack, space, len(self.stacks[stack]), amphi)

        if end < 10:
            self.stacks[end].append(amphi)
            if len(self.stacks[end]) == 4:
                self.filled_stacks.append(start)
        else:
            self.spaces[end - 10] = amphi

        self.cost += score

    def valid_moves(self):
        for start in range(4):
            if start in self.clear_stacks or len(self.stacks[start]) == 0:
                continue  #  Never move anything out of a cleared stack
            for end in range(10, 17):
                if self.at(end):
                    continue  # something there
                if any(self.at(blocker) for blocker in BLOCK_SPACES[start, end]):
                    continue

                yield start, end

        for start in range(10, 17):
            amphi = self.at(start)
            if amphi is None:
                continue
            end = TARGETS[amphi]
            if end not in self.clear_stacks:
                continue
            if any(self.at(blocker) for blocker in BLOCK_SPACES[end, start]):
                continue

            yield start, end

    @property
    def is_complete(self):
        return len(self.filled_stacks) == 4

    @staticmethod
    @lru_cache(2000)
    def score_move(stack: int, space: int, stack_height: int, amphi: str) -> int:
        """How far to move from stack to space (or vice versa)
        Stack height excludes the current amphipod, if starting from stack.
        """
        stack_spaces = 4 - stack_height

        top_spaces = 2 * abs(space - (stack + 11.5))
        if space in (10, 16):
            top_spaces -= 1

        return int(stack_spaces + top_spaces) * WEIGHTS[amphi]

    def __lt__(self, other):
        return True

    def pretty_print(self):
        spaces = [x if x is not None else "." for x in self.spaces]
        rooms = [list("###.#.#.#.###")] + [list("  #.#.#.#.#  ") for _ in range(3)]
        for i, stack in enumerate(self.stacks):
            for j, item in enumerate(stack):
                rooms[3 - j][2 * i + 3] = item

        print("#" * 13)
        print(
            f"#{spaces[0]}{spaces[1]}.{spaces[2]}.{spaces[3]}.{spaces[4]}.{spaces[5]}{spaces[6]}#"
        )
        for line in rooms:
            print("".join(line))

        print("  #########\n")


if __name__ == "__main__":
    start = timer()
    with open("input23.txt") as f:
        lines = f.readlines()

    room = AmphiRoom(["ADCA", "DCBA", "DBAC", "CDBB"])
    print("Starting room:")
    room.pretty_print()

    heap = [(0, room)]

    best_score = float("inf")
    best_solution = None
    count = 0

    while heap:
        count += 1
        score, room = heappop(heap)
        if score > best_score:
            break  # we're done

        if room.is_complete:
            best_score = score
            best_solution = room
            continue

        for start, end in room.valid_moves():
            new_room = room.copy()
            new_room.move(start, end)
            heappush(heap, (new_room.cost, new_room))

    print(best_score)
    print(count, "moves tested")

    print("\nSolution:")
    path = [best_solution]
    while True:
        parent = path[-1].parent
        if parent is None:
            break
        path.append(parent)

    for state in path[::-1]:
        state.pretty_print()

    print(f"Solution took {timer() - start:.3}s to complete.")
