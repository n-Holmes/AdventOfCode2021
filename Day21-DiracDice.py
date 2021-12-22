from collections import defaultdict
from timeit import default_timer as timer

class IncrementingDie:
    def __init__(self, faces:int) -> None:
        self.rolls = 0
        self.faces = faces
    
    def roll(self) -> int:
        self.rolls += 1
        outcome = self.rolls % self.faces
        return outcome if outcome else self.faces # 0 is actually 100

class IncrementingGame:
    def __init__(self, p1_start, p2_start, faces, spaces, target):
        # Game
        self._die = IncrementingDie(faces)
        self.winning_score = target
        self.spaces = spaces
        
        # Players
        self.positions = [p1_start - 1, p2_start - 1]
        self.scores = [0, 0]
        self.active_player = 0

    def play_turn(self):
        p = self.active_player # for legibility
        move = sum(self._die.roll() for _ in range(3))
        self.positions[p] += move
        self.positions[p] %= self.spaces
        self.scores[p] += self.positions[p] + 1

        self.active_player = 1 - p

    def play_game(self):
        while max(self.scores) < self.winning_score:
            self.play_turn()
        
    def part1_score(self):
        """Get the number of die rolls, multiplied by the losing score"""
        return min(self.scores) * self._die.rolls

class DiracDie:
    def __init__(self, faces:int) -> None:
        self.faces = faces
        self._outcomes = None
    
    def roll3(self):
        """Roll the dirac dice three times.
        Returns a list containing the possible outcomes and the number
        of ways each can occur.
        """
        if self._outcomes:
            return self._outcomes

        outcomes = {0:1}
        for _ in range(3):
            new_outcomes = defaultdict(int)
            for score, chances in outcomes.items():
                for roll in range(1, self.faces + 1):
                    new_outcomes[score + roll] += chances
            outcomes = new_outcomes

        self._outcomes = outcomes.items()
        return self._outcomes

class DiracGame:
    def __init__(self, p1_start, p2_start, faces, spaces, target):
        # Game setup:
        self.spaces = spaces
        self._die = DiracDie(faces)
        self.winning_score = target
        
        # Indices are: player, position on board, score
        # Value is the number of timelines ending in that situation
        self.position_scores = [
            {i:{} for i in range(spaces + 1)}
            for _ in range(2)
        ]
        self.position_scores[0][p1_start - 1][0] = 1
        self.position_scores[1][p2_start - 1][0] = 1
        # Number of timelines active for each player
        self.total_counts = [1, 1]
        # Number of timelines each player has won
        self.games_won = [0, 0]
        self.active_player = 0


    def play_turn(self):
        p = self.active_player

        new_positions = {
            i:defaultdict(int) for i in range(self.spaces + 1)
        }
        new_total = 0

        for roll, roll_count in self._die.roll3():
            for pre_pos in range(self.spaces):
                new_pos = (pre_pos + roll) % self.spaces
                for pre_score, pre_count in self.position_scores[p][pre_pos].items():
                    new_score = pre_score + new_pos + 1
                    new_count = pre_count * roll_count # * self.total_counts[1 - p]

                    if new_score >= self.winning_score:
                        self.games_won[p] += new_count * self.total_counts[1 - p]
                    else:
                        new_total += new_count

                        new_positions[new_pos][new_score] += new_count

        self.position_scores[p] = new_positions
        self.total_counts[p] = new_total
        self.active_player = 1 - p
    
    def play_all(self):
        """Keep going until one player has won in all of their timelines."""
        while all(self.total_counts):
            self.play_turn()

        return self.games_won


if __name__ == '__main__':
    start = timer()
    with open("input21.txt") as f:
        positions = [int(line.split()[-1]) for line in f.readlines()]

    print(f"Starting positions:", positions)

    game = IncrementingGame(*positions, faces=100, spaces=10, target=1000)

    game.play_game()
    print(f"The score for the deterministic game is {game.part1_score()}.")

    d_game = DiracGame(*positions, faces=3, spaces=10, target=21)
    wins = d_game.play_all()
    print(f"Using a d3, player 1 wins in {wins[0]} scenarios.")
    print(f"Player 2 wins in {wins[1]} scenarios.")
    print(f"Player {(wins[0] < wins[1]) + 1} wins overall.")

    print(f"Solution took {timer() - start:.3}s to complete.")
