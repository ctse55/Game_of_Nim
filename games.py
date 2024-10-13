import random
from collections import namedtuple

class Game:
    """A base class for two-player, zero-sum games."""

    GameState = namedtuple('GameState', 'to_move, utility, board, moves')

    def __init__(self):
        self.initial = None  # Placeholder for initial state; to be set in the specific game class

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print("Board: ", state.board)

    def play_game(self, *players):
        """Play a two-player, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                self.display(state)
                move = player(self, state)
                print(f"Player {state.to_move} chooses move {move}")
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    print(f"Player {self.to_move(state)} wins the game!")
                    return self.utility(state, self.to_move(self.initial))

# ______________________________________________________________________________
# Players for Games

def query_player(game, state):
    """Make a move by querying standard input."""
    print("Available moves: {}".format(game.actions(state)))
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('No legal moves: passing turn to next player.')
    return move

def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state))

def alpha_beta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning."""

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -float('inf')
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = float('inf')
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -float('inf')
    beta = float('inf')
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)

# ______________________________________________________________________________
# Example Main Function

if __name__ == "__main__":
    # Create a GameOfNim instance and play a game
    from game_of_nim import GameOfNim  # Assuming game_of_nim.py is in the same directory

    nim = GameOfNim(board=[7, 5, 3, 1])  # Set up the initial board
    nim.play_game(alpha_beta_player, query_player)  # Alpha-beta vs. human player
