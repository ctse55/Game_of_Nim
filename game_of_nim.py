from games import Game, alpha_beta_player, query_player
from collections import namedtuple

class GameOfNim(Game):
    """Game of Nim class, extending the base Game class."""

    def __init__(self, board=[3, 1]):
        """Initialize the game with a given board setup (list of heaps/rows)."""
        self.State = namedtuple('State', 'to_move, utility, board, moves')
        moves = self.get_moves(board)
        self.initial = self.State(to_move='MAX', utility=0, board=board, moves=moves)

    def get_moves(self, board):
        """Generate all possible moves from the current board."""
        moves = []
        for row in range(len(board)):
            for count in range(1, board[row] + 1):
                moves.append((row, count))  # (row, number of objects to remove)
        return moves

    def actions(self, state):
        """Return the list of valid actions (moves) in the given state."""
        return state.moves

    def result(self, state, move):
        """Return the new state after a move is applied."""
        board = state.board[:]  # Make a copy of the current board
        row, count = move
        board[row] -= count  # Remove the selected objects from the selected row
        moves = self.get_moves(board)
        return self.State(
            to_move='MIN' if state.to_move == 'MAX' else 'MAX',  # Alternate turns
            utility=0,  # Utility is not evaluated until the end
            board=board,
            moves=moves
        )

    def utility(self, state, player):
        """Return 1 if MAX wins, -1 if MIN wins, 0 otherwise."""
        if self.terminal_test(state):
            return -1 if player == 'MAX' else 1  # Losing player gets -1
        return 0

    def terminal_test(self, state):
        """Return True if the game is over (all objects have been removed)."""
        return all(x == 0 for x in state.board)

    def display(self, state):
        """Display the current board configuration."""
        print("board: ", state.board)

if __name__ == "__main__":
    # Example of playing the Game of Nim between a human and AI
    nim = GameOfNim(board=[7, 5, 3, 1])  # Initial board setup
    nim.display(nim.initial)
    print(nim.initial.moves)  # Display initial moves available

    # Play the game using Alpha-Beta player (AI) vs human player (query_player)
    utility = nim.play_game(alpha_beta_player, query_player)  # Computer moves first
    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
