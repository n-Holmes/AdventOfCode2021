from timeit import default_timer as timer
from typing import Counter


def parse_lines(lines):
    for line in lines:
        switch, contents = line.strip().split()
        parts = []
        for section in contents.split(","):
            lower, upper = map(int, section[2:].split(".."))
            parts.append((lower, upper))

        yield switch == "on", tuple(parts)


class SmallCubeReactor:
    def __init__(self, size):
        self.size = size

        full_size = 2 * size + 1
        self.cubes = [
            [[False] * full_size for _ in range(full_size)] for _ in range(full_size)
        ]

    def switch_cubes(self, command):
        state, (x, y, z) = command

        low, high = -self.size, self.size
        for i in range(max(x[0], low), min(x[1], high) + 1):
            for j in range(max(y[0], low), min(y[1], high) + 1):
                for k in range(max(z[0], low), min(z[1], high) + 1):
                    self.cubes[i + self.size][j + self.size][k + self.size] = state

    def run_commands(self, commands):
        for command in commands:
            self.switch_cubes(command)

    def count_live(self):
        return sum(sum(sum(line) for line in plane) for plane in self.cubes)


class FullReactor:
    def __init__(self):
        self.on_cuboids = []

    def switch_cubes(self, command):
        state, cmd_cuboid = command

        new_on_cuboids = []
        for cuboid in self.on_cuboids:
            new_on_cuboids.extend(diff(cuboid, cmd_cuboid))
        if state == True:
            new_on_cuboids.append(cmd_cuboid)

        self.on_cuboids = [x for x in new_on_cuboids if x is not None]

    def run_commands(self, commands):
        for command in commands:
            self.switch_cubes(command)

    def count_live(self):
        return sum(volume(cuboid) for cuboid in self.on_cuboids)


def volume(cuboid):
    """Gets the volume of a cuboid"""
    x, y, z = cuboid
    if x[1] < x[0] or y[1] < y[0] or z[1] < z[0]:
        return 0
    return (x[1] - x[0] + 1) * (y[1] - y[0] + 1) * (z[1] - z[0] + 1)


def is_contained(inner, outer):
    """Tests if cuboid inner is fully contained in outer"""
    return all(b[0] <= a[0] <= a[1] <= b[1] for a, b in zip(inner, outer))


def intersection(first, second):
    """Gets the cuboid that is the intersection of two cuboids (or None if no intersection."""
    if any(a[1] < b[0] or b[1] < a[0] for a, b in zip(first, second)):
        return None

    intersect = []
    for a, b in zip(first, second):
        intersect.append((max(a[0], b[0]), min(a[1], b[1])))

    return intersect


def diff(initial, subtractor):
    """Yield cuboids representing the remains of initial when subtractor is negated."""
    
    # If the initial is contained in the subtractor, we get nothing
    if not is_contained(initial, subtractor):
        intersect = intersection(initial, subtractor)
        if intersect is None:
            yield initial

        else:
            new_cuboids = []
            on_x, on_y, on_z = initial
            sub_x, sub_y, sub_z = subtractor
            int_x, int_y, int_z = intersect

            # planes in front and behind the subtractor
            new_cuboids.append(((on_x[0], sub_x[0] - 1), on_y, on_z))
            new_cuboids.append(((sub_x[1] + 1, on_x[1]), on_y, on_z))

            # towers to either side of it
            new_cuboids.append((int_x, (on_y[0], sub_y[0] - 1), on_z))
            new_cuboids.append((int_x, (sub_y[1] + 1, on_y[1]), on_z))

            # blocks above and below
            new_cuboids.append((int_x, int_y, (on_z[0], sub_z[0] - 1)))
            new_cuboids.append((int_x, int_y, (sub_z[1] + 1, on_z[1])))

            for cuboid in new_cuboids:
                if volume(cuboid) > 0:
                    # bad cuboids will have 0 volume
                    yield cuboid


if __name__ == "__main__":
    start = timer()
    with open("input22.txt") as f:
        lines = f.read().splitlines()
    commands = list(parse_lines(lines))

    reactor = SmallCubeReactor(50)
    reactor.run_commands(commands)
    print(reactor.count_live())

    full_reactor = FullReactor()
    full_reactor.run_commands(commands)
    print(full_reactor.count_live())

    print(f"Solution took {timer() - start:.3}s to complete.")
