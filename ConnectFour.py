import typing
import time
from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis
import Colors
import time

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
        self.game_over = False
        self.start_screen = True
        print(self.is_board_full())

        self.win_flash = []

        self.show_start()

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
        self.turn = PLAYER_ONE
        self.game_over = False
        self.win_flash = []

        self.update_board_colors()

    def register_callbacks(self):
        #Register callbacks that will be run when buttons are pressed and released
        for x in range(8):
            self.board.set_callback(x, 0, self.handle_button_event) 
            self.board.activate_key(x, 0, Action.BUTTON_PRESSED)
  
    def handle_button_event(self, x:int, y: int, action: Action):
        #Logic for pressing buttons
        print(f"I'm handling a button ({x}, {y})")

        if self.start_screen:
            self.reset_game()
            self.start_screen = False
            return

        if x == 7 and y== 0:
            self.board.play_sound("reset.mp3")
            self.reset_game()
            self.update_board_colors()
        elif self.find_lowest_empty_row(x) == -1:
            if self.game_over:
                return
            self.board.play_sound("better_buzzer.mp3")
        else:
            if self.game_over:
                return
            self.board.play_sound("piece_in.mp3")
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
        for i in range(row):
            self.game_state[i][col] = self.turn
            self.update_board_colors()
            time.sleep(0.1)
            self.game_state[i][col] = 0
            self.update_board_colors()
        self.game_state[row][col] = self.turn
        self.board.play_sound("clack.mp3")

        if self.check_win(row, col, self.turn):
            self.game_over = True
            self.show_winner()
        elif self.is_board_full():
            self.game_over = True
            self.show_tie_game()
        else:
            self.switch_player()
        self.update_board_colors()

    def update_board_colors(self):
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        for row in range(ROWS):
            for col in range(COLS):
                color = self.get_player_color(self.game_state[row][col])
                self.board.set_cell_color(col, row+2, color)

        for x in range(7):
            self.board.set_cell_color(x, 0, self.get_player_color(self.turn))

        
        if self.game_over:
            self.board.set_cell_color(7, 0, Colors.GREEN)
        else:
            self.board.set_cell_color(7, 0, Colors.YELLOW)

        self.board.update_display()

    def switch_player(self):
        #Change which player is curently placing a piece. Kept track of this in some sort of variable
        if self.turn == PLAYER_ONE:
            self.turn = PLAYER_TWO
        elif self.turn == PLAYER_TWO:
            self.turn = PLAYER_ONE

        self.win_flash = []

    def show_current_player(self):
        #Function to indicate on the board which player is currently placing a piece
        pass
        

    def is_board_full(self):
        #Returns whether or not the game state has no more legal moves
        j = 0
        for x in range(6):
            for y in range(7):
                if self.game_state[x][y] == 0:
                    return False
        return True

    def get_player_color(self, player) -> tuple[int, int, int]:
        #Returns the color for the given player 
        if player == PLAYER_ONE:
            return Colors.RED
        elif player == PLAYER_TWO:
            return Colors.BLUE
        elif player == 3:
            return Colors.PURPLE
        elif player == 4:
            return Colors.YELLOW
        else:
            return Colors.WHITE

    def is_column_full(self, col: int):#Checks whether the column is full
        for row in self.game_state:
            if row[col] == 0:
                return False

        return True
            
            

    def check_win(self, row, col, player):#win check
        check_row = row
        check_col = col
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)] # Includes horizantal, vertical, and both diagonals

        self.win_flash.append((row, col))

        for dr, dc in directions:
            count = 1 # Tracks the amount of peices in a row
            check_row = row + dr
            check_col = col + dc
            while check_row < ROWS and check_row >= 0 and check_col < COLS and check_col >= 0:
                if self.game_state[check_row][check_col] == player:
                    count += 1
                    self.win_flash.append((check_row, check_col))
                    print(self.win_flash)
                    check_row += dr
                    check_col += dc
                else:
                    break

            check_row = row - dr
            check_col = col - dc
            while check_row < ROWS and check_row >= 0 and check_col < COLS and check_col >= 0:
                if self.game_state[check_row][check_col] == player:
                    count += 1
                    self.win_flash.append((check_row, check_col))
                    check_row -= dr
                    check_col -= dc
                else:
                    break

            if count >= 4:
                return True

        return False



    def show_winner(self):
        #Displays on the board who won
        print("winner: " + str(self.turn))
        self.board.play_sound("cheer.mp3")

        for _ in range(5):
            for r, c in self.win_flash:
                self.board.set_cell_color(c, r+2, Colors.WHITE)
            self.board.update_display()

            time.sleep(.2)

            self.update_board_colors()

            time.sleep(.2)
        

    def show_tie_game(self):
        #Displays on the board that there was a draw
        self.board.play_sound("draw_sound.mp3")
        for _ in range(5):
            for r in range(ROWS):
                for c in range(COLS):
                    self.board.set_cell_color(c, r+2, Colors.WHITE)
            self.board.update_display()

            time.sleep(.2)

            self.update_board_colors()

            time.sleep(.2)
        print("TIE")

    def show_start(self):#Start screen
        self.game_state = [
            [1, 1, 2, 2, 1, 1, 1],
            [1, 0, 2, 2, 1, 0, 1],
            [1, 1, 2, 2, 1, 0, 1],
            [0, 0, 4, 0, 4, 0, 0],
            [0, 0, 4, 4, 4, 0, 0],
            [0, 0, 0, 0, 4, 0, 0]
        ]

        self.update_board_colors()


