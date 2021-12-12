from collections import defaultdict
from timeit import default_timer as timer


def get_adj_map(lines):
    """Gets the adjacency map from a list of edges.
    All edges are two-way, apart from those touching "start" or "end".
    """
    adj = defaultdict(list)

    for line in lines:
        a, b = line.strip().split("-")
        if b != "start" and a != "end":
            adj[a].append(b)
        if a != "start" and b != "end":
            adj[b].append(a)

    return adj


def count_paths(adj_map, start, end, repeats_allowed=0):
    """Counts the paths through a maze of tunnels.
    Paths must begin at start and terminate at end.
    Paths may visit nodes with uppercase lables multiple times.
    Paths may only visit lowercase nodes once each, with repeats_allowed exceptions.
    """
    big_caves = {
        x for x in adj_map if x.isupper()
    }  # slightly faster than repeated str.isupper calls

    # Paths stored as (head of the path, small caves visited, small cave repeats)
    # We lose information about the history of the path this way, but don't care
    paths = [(start, [], 0)]
    path_count = 0

    # Depth-first search.  Backtracking might be slightly faster, but a lot more complicated.
    while paths:
        head, smalls, repeats = paths.pop()
        for target in adj_map[head]:
            if target == end:
                path_count += 1  # found a path to the end!
            elif target in big_caves:
                # Shouldn't have to worry about adjacent pairs of big caves causing
                # infinite loops - it would make the question invalid
                paths.append((target, smalls, repeats))
            elif target not in smalls:
                paths.append((target, smalls + [target], repeats))
            elif repeats < repeats_allowed:
                paths.append((target, smalls, repeats + 1))

    return path_count


if __name__ == "__main__":
    start = timer()

    with open("input12.txt") as f:
        lines = f.readlines()

    adj_map = get_adj_map(lines)
    path_count = count_paths(adj_map, "start", "end")
    print(
        f"There are {path_count} paths through the caves without revisiting small caves."
    )

    path_count = count_paths(adj_map, "start", "end", 1)
    print(
        f"There are {path_count} paths through the caves revisiting at most one small cave."
    )

    print(f"Solution took {timer() - start:.3}s to complete")  # 0.15s
