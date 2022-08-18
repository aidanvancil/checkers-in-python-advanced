from .constants import BOX_SIZE, OUTLINE, CROWN, KING_WAV, IS_SELECTED, red
import pygame

# INTIALIZING & ATTRIBUTES
#####################################################################################

class Piece():
    def __init__(self, row, col, color) -> None:
        self.x = 0
        self.y = 0
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.PADDING = 12
        self.selected = False
        self.new_coords()

    def new_coords(self) -> None:
        self.x = BOX_SIZE * self.col + BOX_SIZE // 2
        self.y = BOX_SIZE * self.row + BOX_SIZE // 2

    def make_king(self, selection) -> bool:
        if selection == None:
            KING_WAV.play()
        self.king = True

# BOOLEAN ATTRIBUTE METHODS
#####################################################################################

    def is_empty(self, flat) -> bool:
        return flat[self.row][self.col] == 0

    def is_king(self) -> bool:
        return self.king

    def is_red(self, flat) -> bool:
        return flat[self.row][self.col].color == red

    def is_gray(self, flat) -> bool:
        return flat[self.row][self.col].color == GRAY

    def get_coords(self) -> tuple:
        return self.x, self.y

# PIECE (MEN) MOVEMENT & DRAWING
#####################################################################################

    def move(self, row, col) -> None:
        self.row = row
        self.col = col
        self.new_coords()

    def draw_pieces(self, window) -> None:
        radius = BOX_SIZE//2 - self.PADDING
        pygame.draw.circle(window, OUTLINE, (self.x, self.y), radius + 3)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        
        if self.selected and self.king:
            window.blit(CROWN, (self.x - CROWN.get_size()[0]//2, self.y - CROWN.get_size()[1]//2))
            window.blit(IS_SELECTED, (self.x - IS_SELECTED.get_size()[0]//2, self.y - IS_SELECTED.get_size()[1]//2))
        elif self.king:
            window.blit(CROWN, (self.x - CROWN.get_size()[0]//2, self.y - CROWN.get_size()[1]//2))
        elif self.selected:
            window.blit(IS_SELECTED, (self.x - IS_SELECTED.get_size()[0]//2, self.y - IS_SELECTED.get_size()[1]//2))
