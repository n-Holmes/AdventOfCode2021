from timeit import default_timer as timer
from re import findall

INF = float("inf")


def max_height(v_y):
    return v_y * (v_y + 1) // 2 if v_y > 0 else 0


def get_x_velocities(x_bounds):
    # Assume x bounds are non-negative
    # Get a dict of the valid x_velocities, along with step range to hit the target
    valid_x = {}
    for init_v_x in range(int(x_bounds[0] ** 0.5), x_bounds[1] + 1):
        x, v_x = 0, init_v_x
        steps = 0
        min_steps = None
        max_steps = INF
        while v_x > 0 and x <= x_bounds[1]:
            if x_bounds[0] <= x:
                if min_steps is None:
                    min_steps = steps

            x += v_x
            v_x -= 1
            steps += 1

        if x > x_bounds[1]:
            # We went out of bounds rather than coming to a stop.
            max_steps = steps - 1

        if min_steps is not None:
            valid_x[init_v_x] = (min_steps, max_steps)

    return valid_x


def is_valid_y(v_y, y_bounds, min_steps, max_steps):
    """Will the y position fall in the bounds within the given step range?"""

    steps = 0
    if v_y > 0:
        if max_steps < 4:
            return False  # Won't even have time to get below 0
        # We know how long it will take to get back to 0
        steps = 2 * v_y + 1
        v_y = -v_y - 1

    y = 0
    while steps < min_steps or (y > y_bounds[1] and steps <= max_steps):
        y += v_y
        v_y -= 1
        steps += 1

    return y >= y_bounds[0] and steps <= max_steps


def get_trajectories(x_bounds, y_bounds):
    # Assume x bounds are non-negative and y bounds are negative
    # y bounds including 0 would generally make the question ill-formed
    # positive y_bounds would be possible, but isn't seen in the example or input.

    valid_x_steps = get_x_velocities(x_bounds)

    for v_x, (min_steps, max_steps) in valid_x_steps.items():
        if max_steps == 1:
            # If we only have one step (a lot of the time), the answer is clear
            for v_y in range(y_bounds[0], y_bounds[1] + 1):
                yield v_x, v_y
        
        elif max_steps != INF:
            # Conservative bounds - we have to be back down in time
            for v_y in range(max_steps // 2, y_bounds[0] // min_steps - 1, -1):
                if is_valid_y(v_y, y_bounds, min_steps, max_steps):
                    yield (v_x, v_y), max_height(v_y)
        
        else:
            # Broad range of options
            for v_y in range(-y_bounds[0] - 1, y_bounds[0] - 1, -1):
                if is_valid_y(v_y, y_bounds, min_steps, max_steps):
                    yield (v_x, v_y), max_height(v_y)




if __name__ == "__main__":
    start = timer()
    with open("input17.txt") as f:
        lines = f.read().splitlines()

    for line in lines:
        bounds = findall(r"=(-?\d+)\.\.(-?\d+)", line)
        x_bounds = list(map(int, bounds[0]))
        y_bounds = list(map(int, bounds[1]))

        trajectories = list(get_trajectories(x_bounds, y_bounds))
        traj, height = max(trajectories, key=lambda x: x[1])
        print(f"{len(trajectories)} valid trajectories found.")
        print(f"The best height is {height}, which is achieved with trajectory {traj}.")

    print(f"Solution took {timer() - start:.3}s to complete.")  # 5ms
