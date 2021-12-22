from collections import Counter, defaultdict
from itertools import combinations
from timeit import default_timer as timer

# List of base elements of the group of 90 degree rotations, by axis
# Each element gives steps of rotation around x, then y, then z
# Each pair in the list represents rotating a different face of a cube towards +Z
ROTATIONS = [
    (a, b, c)
    for c in range(4)
    for a, b in ((0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (0, 3))
]


class Scanner:
    def __init__(self, lines):
        self.coords = [
            tuple(map(int, line.split(","))) for line in lines.splitlines()[1:]
        ]

        self._get_distances()
        self.all_dists = sorted(x for row in self.distances for x in row)

        self.center = (0, 0, 0)
        self._absolutes = None

    def _get_distances(self):
        """Get lists of the distance from each point to each other point."""
        self.distances = []
        for i, a in enumerate(self.coords):
            row = []
            for j, b in enumerate(self.coords):
                if i == j:
                    continue
                row.append(pyth2(a, b))

            self.distances.append(sorted(row))

    def is_similar(self, other):
        score = count_shared(self.all_dists, other.all_dists)
        # We should have at least 12 points sharing at least 11 distances
        return score >= 132

    def rotate(self, rotation):
        """Rotate all points by steps/4 turns around the given axis (CCW looking down)"""
        for i, p in enumerate(self.coords):
            self.coords[i] = rotate(p, rotation)

        self._absolutes = None  # invalidate cache

    def translate_to_match(self, coord_index, pos):
        """Translate the sensor position to put the given coordinate in the specified position."""
        x, y, z = self.coords[coord_index]
        self.center = (pos[0] - x, pos[1] - y, pos[2] - z)
        self._absolutes = None  # invalidate cache

    def rotate_to_match(self, i_1, i_2, i_3, v, w):
        """Let p, q, r be the coordinates in positions i_1, ...
        Rotate the sensor so that vectors v == p -> q and w == p -> r
        """

        v_current = vector(self.coords[i_1], self.coords[i_2])
        w_current = vector(self.coords[i_1], self.coords[i_3])

        for rot in ROTATIONS:
            if rotate(v_current, rot) == v and rotate(w_current, rot) == w:
                self.rotate(rot)
                return
        
        raise ValueError("Rotation not found")
    
    def align_to(self, other):
        """Aligns the sensor to another, adjecant sensor."""
        matches = {}
        for i in range(len(self.coords)):
            for j in range(len(other.coords)):
                if count_shared(self.distances[i], other.distances[j]) >= 11:
                    if i in matches:
                        raise ValueError("Unclear match - don't know what to do.")
                    matches[i] = j

                    
        a, b, c, *_ = matches # Get three matches (any will do)
        v = vector(other.coords[matches[a]], other.coords[matches[b]])
        w = vector(other.coords[matches[a]], other.coords[matches[c]])
        self.rotate_to_match(a, b, c, v, w)
        self.translate_to_match(a, other.absolute_coords[matches[a]])

    @property
    def absolute_coords(self):
        if self._absolutes is not None:
            return self._absolutes

        self._absolutes = []
        for coord in self.coords:
            self._absolutes.append(
                (
                    coord[0] + self.center[0],
                    coord[1] + self.center[1],
                    coord[2] + self.center[2],
                )
            )

        return self._absolutes


def pyth2(p, q):
    """Get the squared distance between two points"""
    return sum((a - b) ** 2 for a, b in zip(p, q))

def manhattan(p, q):
    """Get the manhattan distance between two points"""
    return sum(abs(a-b) for a, b in zip(p, q))

def count_shared(a, b):
    """Count the shared elements between two sorted lists"""
    i = j = 0
    n, m = len(a), len(b)

    count = 0
    while i < n and j < m:
        if a[i] == b[j]:
            count += 1
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1

    return count


def vector(p, q):
    """Gets the vector p->q."""
    return tuple(b - a for a, b in zip(p, q))


def rotate(v, rotations):
    x, y, z = v
    a, b, c = rotations
    for _ in range(a):
        # CCW around x: y -> z -> -y
        y, z = -z, y
    for _ in range(b):
        # CCW around y: z -> x -> -z
        x, z = -z, x
    for _ in range(c):
        # CCW around z: x -> y -> -x
        x, y = -y, x
    return (x, y, z)

def align_scanners(scanners, adj_map):
    aligned = {0}
    seen = {0}
    queue = [(x, 0) for x in adj_map[0]]

    count = 1
    for current, target in queue:
        if current in aligned:
            continue
        
        scanners[current].align_to(scanners[target])
        aligned.add(current)
        count += 1

        for other in adj_map[current]:
            if other not in seen:
                queue.append((other, current))
                seen.add(other)

    print(f"{count} scanners aligned")



if __name__ == "__main__":
    start = timer()
    with open("input19.txt") as f:
        chunks = f.read().split("\n\n")

    scanners = [Scanner(chunk) for chunk in chunks]

    adj = defaultdict(list)
    for (i, a), (j, b) in combinations(enumerate(scanners), 2):
        if a.is_similar(b):
            #print(f"Scanners {i} and {j} are similar.")
            adj[i].append(j)
            adj[j].append(i)

    total = sum(map(len, adj.values())) // 2
    print(f"{total} similar pairs between {len(scanners)} scanners.")
    
    align_scanners(scanners, adj)
    points = set()
    for scanner in scanners:
        points.update(scanner.absolute_coords)
    
    print(f"{len(points)} beacons represented by {sum(len(s.coords) for s in scanners)} pings.")

    max_dist = max(manhattan(a.center, b.center) for a, b in combinations(scanners, 2))
    print("The max distance (taxicab) between any two scanners is", max_dist)

    print(f"Solution took {timer() - start:.3}s to complete.")
