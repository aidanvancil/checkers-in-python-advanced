import pygame

from .piece import Piece # only used for 'isinstance'
from .board import Board
from .constants import BOX_SIZE, red, OUTLINE, GRAY, ROWS, COLS, volatility
import logging
import random

# INTIALIZING & UPDATES
#####################################################################################

class Game():
    def __init__(self, win) -> None:
        self.window = win
        self.selected_piece = None
        self.board = Board(win)
        self.player = red
        self.available_moves = {}
        self.turn_count = 0
        self.turn_gamemode = False

    def reset(self, win) -> None:
        self.__init__(win)
        self.gamemode(self.selection)

    def gamemode(self, selection) -> None:
        self.selection = selection
        if selection == 1: # Regular
            return None
        elif selection == 2: # Only Kings
            self.board.red_kings = 12
            self.board.gray_kings = 12
            for row in range(ROWS):
                for col in range(COLS):
                    p = self.board.flat[row][col]
                    if isinstance(p, Piece):
                        p.make_king(selection)
            return None
        elif selection == 3: # RNG Kings
            red_count, gray_count = 0, 0
            SCALE = 24
            rng = random.randint(0, SCALE)
            for row in range(ROWS):
                for col in range(COLS):
                    p = self.board.flat[row][col]
                    if isinstance(p, Piece):
                        choice = random.choice([True, False])
                        if choice:
                            rng -= 1
                            if rng > 0:  
                                if p.color == GRAY:
                                    gray_count += 1
                                else:
                                    red_count += 1
                                p.make_king(selection)
            self.board.red_kings = red_count
            self.board.gray_kings = gray_count


            return None
        elif selection == 4: # Two moves every turn
            self.turn_gamemode = True
            return None     
        return None

    def update(self) -> None:
        self.board.draw_setup()
        if self.player == GRAY:
            tie_game = self.random_movement()
            if tie_game:
                print("No Game Winner! Tie Game")
                self.reset(self.window)
        self.draw_available_moves(self.available_moves)
        

# DRAWING NODES
#####################################################################################

    def draw_available_moves(self, moves) -> None:
        for selection in moves:
            row, col = selection
            pygame.draw.circle(self.window, OUTLINE, (col * BOX_SIZE + BOX_SIZE//2, row * BOX_SIZE + BOX_SIZE//2), 15)

# SELECTION & MOVEMENT TO (ROW, COL)
#####################################################################################
    def random_movement(self) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                if random.choice(volatility):
                    p = self.board.flat[row][col]
                    if isinstance(p, Piece) and p.color == GRAY and (self.board.get_available_moves(p) != {}):
                        self.selected(row, col)
                        first_coords = self.board.get_available_moves(p)
                        first_value = list(first_coords.items())[0][0]
                        self.if_moved(first_value[0], first_value[1])
                        return None
        result = self.check_tie()
        return result

    def check_tie(self) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                p = self.board.flat[row][col]
                if isinstance(p, Piece) and p.color == GRAY and (self.board.get_available_moves(p) != {}):
                    return False
        return True


    def selected(self, row, col) -> bool:
        if self.selected_piece:
            result = self.if_moved(row, col)
            if not result:
                self.selected_piece = None 
                self.selected(row, col)

        piece = self.board.flat[row][col]
        if piece != 0 and piece.color == self.player:
            self.selected_piece = piece
            count = 0
            for row in range(ROWS):
                for col in range(COLS):
                    p = self.board.flat[row][col]
                    if isinstance(p, Piece):
                        if p.selected:
                            count += 1
                        if count > 0:
                            self.board.flat[row][col].selected = False
            piece.selected = True
            self.available_moves = self.board.get_available_moves(piece)
            return True
        if isinstance(piece, Piece):
            piece.selected = False
        return False

    def if_moved(self, row, col) -> bool:
        logging.info("Moved {}".format(self.player)) 
        piece = self.board.flat[row][col]
        if self.selected_piece and piece == 0 and (row, col) in self.available_moves:
            self.board.move_piece(self.selected_piece, row, col)
            skipped = self.available_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.turns()
        else:
            return False

        return True

# RULESETS & FETCHING
#####################################################################################

    def turns(self) -> None:
        self.available_moves = {}   # Reset Available Moves
        self.turn_count += 1
        if self.turn_gamemode:
            if self.player == red and (self.turn_count == 2):
                self.turn_count = 0
                self.player = GRAY
            elif self.player == GRAY and (self.turn_count == 2):
                self.player = red
                self.turn_count = 0
        else:
            if self.player == red:
                self.player = GRAY
            else:
                self.player = red

    def win_condition(self) -> None:
        # W.I.P. tied games
        if self.board.gray_pieces <= 0:
            print("Game Winner: RED")
            return -1
        elif self.board.red_pieces <= 0:
            print("Game Winner: GRAY")
            return -1
        return None 

    def get_rows_cols(self, x, y) -> tuple:
        return y // BOX_SIZE, x // BOX_SIZE

        