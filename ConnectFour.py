import typing

from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis
import Colors

PLAYER_ONE = 1
PLAYER_TWO = 2
WHITE = 3

ROWS = 6
COLS = 7

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
        self.turn = PLAYER_ONE
        self.register_callbacks()
        print(self.is_board_full())

    def reset_game(self):
        #Empties the board
        self.game_state = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]

    def register_callbacks(self):
        #Register callbacks that will be run when buttons are pressed and released
        for x in range(8):
            self.board.set_callback(x, 0, self.handle_button_event) 
            self.board.activate_key(x, 0, Action.BUTTON_PRESSED)
  
    def handle_button_event(self, x:int, y: int, action: Action):
        #Logic for pressing buttons
        print(f"I'm handling a button ({x}, {y})")
        if x == 7 and y== 0:
            self.reset_game()
            self.update_board_colors()
        elif self.find_lowest_empty_row(x) == -1:
            self.board.play_sound("buzzer.mp3")
        else:
            self.place_piece(x)
        

        return x, y

    def find_lowest_empty_row(self, col: int):
        #Return the lowest empty row in the column.
        least = -1
        for row in self.game_state:
            if row[col] != 0:
                break
            least += 1
        return least

    def place_piece(self, col: int):
        #Finds the legal move in the column, and updates the game state to reflect the new piece, checking to see if a player has won with that new piece.
        row = self.find_lowest_empty_row(col)
        self.game_state[row][col] = self.turn
        self.board.play_sound("clack.mp3")

         
        self.update_board_colors()
        if self.check_win(row, col, self.turn):
            self.show_winner()
        self.switch_player()

    def update_board_colors(self):
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        for row in range(ROWS):
            for col in range(COLS):
                color = Colors.WHITE
                if self.game_state[row][col] == PLAYER_ONE:
                    color = Colors.RED
                elif self.game_state[row][col] == PLAYER_TWO:
                    color = Colors.BLUE
                self.board.set_cell_color(col, row+2, color)

        self.board.update_display()

    def switch_player(self):
        #TODO: Change which player is curently placing a piece. Keep track of this in some sort of variable
        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        elif self.turn == PLAYER_TWO:
            self.turn = PLAYER_ONE

    def show_current_player(self):
        #TODO: Function to indicate on the board which player is currently placing a piece
        pass
        

    def is_board_full(self):
        #TODO: Return whether or not the game state has no more legal moves
        j = 0
        for x in range(6):
            for y in range(7):
                if self.game_state[x][y] == 0:
                    return False
        return True 

    def get_player_color(self, player) -> tuple[int, int, int]:
        #TODO: Return the color for the given player 
        pass

    def is_column_full(self, col: int):
        for row in self.game_state:
            if row[col] == 0:
                return False

        return True
            
            

    def check_win(self, row, col, player):
        check_row = row
        check_col = col
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] #Includes horizantal, vertical, and both diagonals

        count = 1 #Tracks the amount of peices in a row
        for dr, dc in directions:
            check_row = row + dr
            check_col = col + dc
            while check_row < ROWS and check_row >= 0 and check_col < COLS and check_col >= 0:
                if self.game_state[check_row][check_col] == player:
                    count += 1
                    check_row += dr
                    check_col += dc
                else:
                    break

            check_row = row - dr
            check_col = col - dc
            while check_row < ROWS and check_row >= 0 and check_col < COLS and check_col >= 0:
                if self.game_state[check_row][check_col] == player:
                    count += 1
                    check_row -= dr
                    check_col -= dc
                else:
                    break

            if count >= 4:
                return True

        return False


            

    def show_winner(self):
        #TODO: Display on the board who won
        print("winner: " + str(self.turn))
        pass
        

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        if is_board_full:
            self.game_state = [
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3]
        ]
        pass


