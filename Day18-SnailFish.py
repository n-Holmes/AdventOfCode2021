from copy import deepcopy
from itertools import permutations
from timeit import default_timer as timer


class SFNum:
    def __init__(self, in_s):
        self.contents = eval(in_s)

        self._last_locs = None

    def get_node_locs(self):
        if self._last_locs:
            return self._last_locs

        confirmed = []
        check = [[0], [1]]
        for pos in check:
            val = self.at(pos)
            if isinstance(val, int):
                confirmed.append(pos)
            else:
                check.extend((pos + [0], pos + [1]))
        
        # cache it
        self._last_locs = sorted(confirmed)
        return self._last_locs

    def at(self, pos):
        loc = self.contents
        for i in pos:
            loc = loc[i]
        return loc
    
    def set_at(self, pos, val):
        loc = self.contents
        for i in pos[:-1]:
            loc = loc[i]
        loc[pos[-1]] = val

        # Clear the cache
        self._last_locs = None
    
    def explode(self):
        """Tries to explode the first pair contained in 4 other pairs.
        Returns True if an explosion happened.
        """
        for i, pos in enumerate(self.get_node_locs()):
            if len(pos) == 5:
                # pos is the left hand element of the exploding pair
                parent = pos[:-1]
                left = self.at(pos)
                right = self.at(parent + [1])
                self.set_at(parent, 0)

                new_locs = self.get_node_locs()
                if not all(p == 0 for p in pos):
                    left_loc = new_locs[i - 1]
                    left_val = self.at(left_loc) + left
                    self.set_at(left_loc, left_val)
                if not all(p == 1 for p in parent):
                    right_loc = new_locs[i + 1]
                    right_val = self.at(right_loc) + right
                    self.set_at(right_loc, right_val)
                
                # print(f"Explosion of [{left},{right} at {parent}")
                return True # Only do the leftmost explosion
        
        return False
    
    def split(self):
        """Tries to split the first value that is 10 or more. Returns True if split."""
        for i, pos in enumerate(self.get_node_locs()):
            val = self.at(pos)
            if val >= 10:
                new_pair = [val // 2, (val + 1) // 2]
                self.set_at(pos, new_pair)
                # print(f"Splitting {val} to {new_pair} at {pos}")
                return True
        
        return False

    def reduce(self):
        """Explode and split until no more operations are valid"""
        either = True
        while either:
            either = self.explode()
            if either:
                continue
            either = self.split()
        
    def __add__(self, other):
        new = SFNum("None")
        new.contents = [deepcopy(self.contents), deepcopy(other.contents)]
        new.reduce()
        return new
        
    def magnitude(self, target=None):
        if target is None:
            target = self.contents
        
        if isinstance(target, int):
            return target
        else:
            return 3 * self.magnitude(target[0]) + 2 * self.magnitude(target[1])


if __name__ == '__main__':
    start = timer()
    with open("input18.txt") as f:
        lines = f.read().splitlines()
    
    snailfish = [SFNum(line) for line in lines]

    result = snailfish[0]
    for sf in snailfish[1:]:
        sf.reduce()
        result += sf

    print(f"The sum of all SnailFish is {result.contents},")
    print("with magnitude", result.magnitude())

    max_mag = 0
    for (a, b) in permutations(snailfish, r=2):
        s = a + b
        max_mag = max(max_mag, s.magnitude())
    
    print("The highest pair-sum magnitude is", max_mag)

    print(f"Solution took {timer() - start:.3}s to complete.")
