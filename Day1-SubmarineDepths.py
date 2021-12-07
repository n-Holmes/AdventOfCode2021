def count_increases(depths):
    increases = sum(1 for (a, b) in zip(depths, depths[1:]) if a < b)
    return increases

def count_window_increases(depths):
    new_depths = [sum(depths[:3])]
    for add, sub in zip(depths[3:], depths):
        new_depths.append(
            new_depths[-1] + add - sub
        )
    return count_increases(new_depths)



if __name__ == '__main__':
    with open("input1.txt") as f:
        depths = list(map(int, f.read().strip().split()))

    print(count_increases(depths))
    print(count_window_increases(depths))
