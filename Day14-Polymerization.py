from collections import Counter
from timeit import default_timer as timer

def get_mapping(lines):
    """Gets a mapping representing the (ordered) pairs that each pair of elements will 
    evolve into after one step, if adjacent.
    """
    mapping = {}

    for line in lines:
        (a, b), c = line.strip().split(' -> ')
        mapping[a, b] = ((a, c), (c, b))

    return mapping

def polymerize_by_counts(seed, mapping, steps):
    """Gets the difference between the counts of the most and least common elements,
    following `steps` steps of polymerization on `seed` by `mapping`.
    """

    # Get initial pair counts
    counts = Counter(zip(seed, seed[1:]))

    # Evolve the pair counts
    for _ in range(steps):
        new_counts = Counter()
        for pair, count in counts.items():
            for successor in mapping[pair]:
                new_counts[successor] += count

        counts = new_counts
    
    # Get the element counts
    totals = Counter()
    for pair, count in counts.items():
        for element in pair:
            totals[element] += count
    
    # Everything but the first and last element will have been double-counted
    totals[seed[0]] += 1
    totals[seed[-1]] += 1

    return (max(totals.values()) - min(totals.values())) // 2

if __name__ == '__main__':
    start = timer()
    with open("input14.txt") as f:
        lines = f.readlines()

    seed = lines[0].strip()
    mapping = get_mapping(lines[2:])

    score = polymerize_by_counts(seed, mapping, 10)
    print("After 10 steps of polymerization, the score is", score)

    score = polymerize_by_counts(seed, mapping, 40)
    print("After 40 steps of polymerization, the score is", score)

    print(f"Solution took {timer() - start:.3}s to complete.") # 2.7ms
