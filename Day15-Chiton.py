from queue import PriorityQueue
from timeit import default_timer as timer


def a_star(adj_func, start, end):
    """A* pathing algorithm implementation.
    Point evaluation function not made generic as it's the same for most cases.
    """

    def eval_point(a, pre_weight=0):
        """Get the minimum possible path value to the end, from a point.
        Value reduced by sum(end), to simplify - will effect all points equally,
        so no problem.
        """
        return pre_weight - sum(a)

    q = PriorityQueue()
    q.put((eval_point(start), 0, start))
    checked = set() # Set of all points we have tried pathing from
    while not q.empty():
        weight, part_sum, last_node = q.get()

        # Due to ordering, the first time we scan a node will always be the best
        if last_node in checked:
            continue
        checked.add(last_node)

        # Have we found it?
        if last_node == end:
            print(f"Checked {len(checked)} points to find path_weight {part_sum}.")
            return part_sum

        for target, weight in adj_func(last_node):
            if target not in checked:
                d = eval_point(target, part_sum + weight)
                q.put((d, part_sum + weight, target))

    raise ValueError(f"Cannot reach {end} from {start}.")


def find_path(cave_map):
    height, width = len(cave_map), len(cave_map[0])

    def adj_func(p):
        coords = []
        if p[0] > 0:
            coords.append((p[0] - 1, p[1]))
        if p[0] < height - 1:
            coords.append((p[0] + 1, p[1]))
        if p[1] > 0:
            coords.append((p[0], p[1] - 1))
        if p[1] < width - 1:
            coords.append((p[0], p[1] + 1))

        return (((i, j), cave_map[i][j]) for i, j in coords)

    start = (0, 0)
    target = (height - 1, width - 1)
    return a_star(adj_func, start, target)


def find_path_wrapped(cave_map, repeats):
    height, width = len(cave_map), len(cave_map[0])
    t_height, t_width = height * repeats - 1, width * repeats - 1

    def adj_func(p):
        coords = []
        if p[0] > 0:
            coords.append((p[0] - 1, p[1]))
        if p[0] < t_height:
            coords.append((p[0] + 1, p[1]))
        if p[1] > 0:
            coords.append((p[0], p[1] - 1))
        if p[1] < t_width:
            coords.append((p[0], p[1] + 1))

        for i, j in coords:
            weight = cave_map[i % height][j % width]
            weight += i // height + j // width
            while weight > 9:
                weight -= 9
            yield ((i, j), weight)

    start = (0, 0)
    target = (t_height, t_width)
    return a_star(adj_func, start, target)


if __name__ == "__main__":
    start = timer()
    with open("input15.txt") as f:
        lines = f.readlines()

    cave_map = [[int(c) for c in line.strip()] for line in lines]

    risk = find_path(cave_map)
    print(risk)

    risk = find_path_wrapped(cave_map, 5)
    print(risk)

    print(f"Solution took {timer() - start:.3}s to complete.")
