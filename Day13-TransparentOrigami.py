from timeit import default_timer as timer

def fold(points, instruction):
    eq_i = instruction.index('=')
    axis = instruction[eq_i - 1]
    line = int(instruction[eq_i + 1:])

    new_points = set()
    for point in points:
        if axis == 'x' and point[0] > line:
            new_points.add((2 * line - point[0], point[1]))
        elif axis == 'y' and point[1] > line:
            new_points.add((point[0], 2 * line - point[1]))
        else:
            new_points.add(point)
    
    return new_points

def print_points(points):
    width = max(x for x, y in points) + 1
    height = max(y for x, y in points) + 1

    grid = [[' '] * width for _ in range(height)]
    for x, y in points:
        grid[y][x] = '█'

    print('-' * width)
    for row in grid:
        print(''.join(row))
    print('-' * width)

if __name__ == '__main__':
    start = timer()

    with open("input13.txt") as f:
        a, b = f.read().split("\n\n")

    points = []
    for line in a.splitlines():
        x, y = line.split(',')
        points.append((int(x), int(y)))
    instructions = b.splitlines()
    print(f"Points: {len(points)}, Instructions: {len(instructions)}")

    points = fold(points, instructions[0])
    print(f"After {instructions[0]}, there are {len(points)} points remaining.")

    for instruction in instructions[1:]:
        points = fold(points, instruction)
    
    print(f"After performing all folds, there are {len(points)} points remaining.")
    print("This is the grid:")
    print_points(points)

    print(f"Solution took {timer() - start:.3}s to complete.") # 3ms
