import typing

from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis

PLAYER_ONE = 1
PLAYER_TWO = 2

class ConnectFour:
    def __init__(self, board: typing.Optional[AbstractNeoTrellisGame] = None):
        self.board = board if board is not None else NeoTrellisGame()
        super().__init__()
        self.game_state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        self.register_callbacks()

    def reset_game(self):
        #TODO reset the game state to its original empty state
        pass

    def register_callbacks(self):
        #TODO: Register callbacks that will be run when buttons are pressed and released
        for x in range(8):
            self.board.set_callback(x, 0, self.handle_button_event) 
            self.board.activate_key(x, 0, Action.BUTTON_PRESSED)
        

        pass
  
    def handle_button_event(self, x:int, y: int, action: Action):
        """
        This is an example of how a callback function will look. It takes an x value, y value, and action, which will indicate what button activated the callback and what action the user did to run it.
        See NeoTrellisGame.set_callback() for info about callbacks.
        """
        #TODO: Implement what will happen when the button at position x,y is pressed or released
        print(f"I'm handling a button ({x}, {y})")
        return x, y

    def find_lowest_empty_row(self, col: int):
        #TODO: Return the lowest empty row in the column.
        pass

    def place_piece(self, col: int):
        #TODO: Finds the legal move in the column, and updates the game state to reflect the new piece, checking to see if a player has won with that new piece. Don't forget to play a sound!
        pass

    def update_board_colors(self):
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        pass

    def switch_player(self):
        #TODO: Change which player is curently placing a piece. Keep track of this in some sort of variable
        pass

    def show_current_player(self):
        #TODO: Function to indicate on the board which player is currently placing a piece
        pass

    def is_board_full(self):
        #TODO: Return whether or not the game state has no more legal moves
        pass  

    def get_player_color(self, player) -> tuple[int, int, int]:
        #TODO: Return the color for the given player 
        pass

    def is_column_full(self, col: int):
        for row in self.game_state:
            if row[col] == 0:
                return False

        return True
            
            

    def check_win(self):
        #TODO: Check the game state to see if any player has won or if there is a draw
        pass

    def show_winner(self):
        #TODO: Display on the board who won
        pass

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        pass


