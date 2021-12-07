from functools import lru_cache
from statistics import mean, median
from timeit import default_timer as timer


def part_1(start_positions):
    target = int(median(start_positions))
    fuel_used = sum(abs(x - target) for x in start_positions)
    print(f"Crabs move to {target} using {fuel_used} units of fuel.")

def triangular_fuel_used(position, target):
    diff = abs(target - position)
    return diff * (diff + 1) // 2

def trisect(a, b):
    return (2 * a + b) // 3, (a + 2 * b) // 3

def ternary_search(left_bound, right_bound, func):
    """Find the maximal point of a unimodal function between two bounds"""
    
    while right_bound - left_bound > 3:
        a, b = trisect(left_bound, right_bound)
        if func(a) > func(b):
            right_bound = b
        else:
            left_bound = a
    
    # down to 3 or fewer points - just check them
    best = max(range(left_bound, right_bound + 1), key = func)
    return best, func(best)


def part_2(start_positions):
    # I believe the negative fuel used function should be unimodal, so use ternary search across its range
    @lru_cache # Caching halves the execution time
    def negative_fuel_used(target):
        return -sum(triangular_fuel_used(p, target) for p in start_positions)

    best, negative_fuel = ternary_search(min(start_positions), max(start_positions), negative_fuel_used)

    print(f"Crabs move to {best} using {-negative_fuel} units of fuel.")

if __name__ == '__main__':
    start = timer()    
    with open("input7.txt") as f:
        start_positions = [int(s) for s in f.read().strip().split(',')]
    
    part_1(start_positions)
    part_2(start_positions)

    print(f"Solution took {timer() - start}s") # 0.009
