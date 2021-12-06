from timeit import default_timer as timer
from typing import final

import numpy as np

class Swarm:
    def __init__(self, ages):
        self.ages = [0] * 9
        for i in map(int, ages.split(',')):
            self.ages[i] += 1
    
    def step(self):
        self.ages = self.ages[1:] + [self.ages[0]]
        self.ages[6] += self.ages[8]

    def progress(self, n):
        for _ in range(n):
            self.step()

    @property
    def size(self):
        return sum(self.ages)

### Closed form solution below

DECOMPOSITION = None # cache the TX matrix, no point getting it twice
def get_decomposed_transform():
    """Get the diagonalization of the linear transformation"""
    global DECOMPOSITION
    if DECOMPOSITION is not None:
        return DECOMPOSITION

    # Define the primary transformation - the matrix moving one step to the next
    TX = np.zeros((9, 9))
    for i in range(9):
        TX[i, (i+1)%9] = 1
    TX[6, 0] = 1

    # P @ diag(e_vals) @ P_inv == TX (roughly, @ is matrix multiply)
    e_vals, P = np.linalg.eig(TX)
    P_inv = np.linalg.inv(P)
    
    DECOMPOSITION = P, e_vals, P_inv
    return DECOMPOSITION
get_decomposed_transform() # Cache the value - we could just write these matrices out, if we were competing fully

def get_progression_transform(steps):
    """Use the diagonalization to get the transformation for the whole process"""
    P, e_vals, P_inv = get_decomposed_transform()
    D = np.diag(np.power(e_vals, steps))
    return P @ D @ P_inv

def get_population(initial_pops, steps):
    """Get the population after a given number of steps"""
    M = get_progression_transform(steps)
    final_pops = M @ initial_pops
    return int(sum(final_pops.round(decimals = 0).real))


### Solution functions, for comparison

def solve_iterative(inputs, target_steps):
    swarm = Swarm(inputs)
    start = timer()

    current_steps = 0
    for s in target_steps:
        swarm.progress(s - current_steps)
        current_steps = s
        print(swarm.size)
    
    print(f"Iterative solution for {target_steps[-1]} steps took {timer() - start}s")


def solve_closed(inputs, target_steps):
    swarm = Swarm(inputs)
    start = timer()

    initials = np.array(swarm.ages)
    for steps in target_steps:
        print(get_population(initials, steps))
    
    print(f"Closed form solution for {target_steps[-1]} steps took {timer() - start}s")

    

if __name__ == '__main__':
    with open("input6.txt") as f:
        inputs = f.read().strip()

    solve_iterative(inputs, (80, 256))
    solve_closed(inputs, (80, 256))

    # Closed form with standard accuracy fails at a certain point, due to float rounding
    solve_iterative(inputs, [1000])
    solve_closed(inputs, [1000])
