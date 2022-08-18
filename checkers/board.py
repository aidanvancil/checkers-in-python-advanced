from .constants import BOX_SIZE, ROWS, COLS, BLACK, red, WHITE, GRAY, MOVE_WAV
from .piece import Piece
import pygame
#import logging

# WAV Imports

# INTIALIZING & SETUP
#####################################################################################

class Board():
    def __init__(self, win) -> None:
        self.row = 0
        self.col = 0
        self.window = win
        self.flat = []
        self.red_pieces, self.gray_pieces = 12, 12
        self.red_kings = self.gray_kings = 0
        self.setup_board()

    def setup_board(self) -> None:
        for row in range(ROWS):
            self.flat.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.flat[row].append(Piece(row, col, GRAY))
                    elif row > 4:
                        self.flat[row].append(Piece(row, col, red))
                    else:
                        self.flat[row].append(0)
                else:
                    self.flat[row].append(0)

# DRAWING
#####################################################################################

    def draw_flat(self) -> None:
        self.window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.window, WHITE, (row*BOX_SIZE, col *BOX_SIZE, BOX_SIZE, BOX_SIZE))

    def draw_setup(self) -> None:
        self.draw_flat()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.flat[row][col]
                if piece != 0:
                    piece.draw_pieces(self.window)  

# ATTRIBUTE MOVEMENT
##################################################################################### 

    def move_piece(self, piece, row, col) -> None:
        self.flat[piece.row][piece.col], self.flat[row][col] = self.flat[row][col], self.flat[piece.row][piece.col]
        piece.move(row, col)

        if (row == 7 or row == 0) and piece.king == False:
            piece.make_king(selection=None)
            if piece.color == WHITE:
                self.gray_kings += 1
            else:
                self.red_kings += 1 

    def remove(self, pieces) -> None:
        for piece in pieces:
            self.flat[piece.row][piece.col] = 0
            MOVE_WAV.play()
            if piece != 0:
                MOVE_WAV.play()
                if piece.color == red:
                    if piece.is_king():
                        self.red_kings  -= 1
                    self.red_pieces -= 1
                else:
                    if piece.is_king():
                        self.gray_kings -= 1
                    self.gray_pieces -= 1

# FETCHING & PHYSICAL MOVEMENT
##################################################################################### 

    def get_available_moves(self, piece) -> dict:
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == red or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == GRAY or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]) -> dict:
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.flat[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]) -> dict:
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.flat[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves