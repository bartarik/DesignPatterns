import pygame
from src.constants import *


# Consider making this as a separate clas entities.py
class GamePiece:
    PADDING = 10
    OUTLINE = 2
    """
    Represents a single game piece on the board.
    Each piece has a color and, potentially, other properties like whether it's a king.
    """
    def __init__(self, row, col, color):
        self.color = color
        self.is_king = False
        # Remove this later
        if self.color == RED:
            self.direction = -1
        else:
            self.direction = 1

        self.row = row
        self.col = col
        self.x = 0
        self.y = 0

    def cals_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.is_king = True

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def __repr__(self):
        return str(self.color)


class GameBoard:
    """
    Represents the game board TODO: write whole description
    """
    def __init__(self):
        self.rows = BOARD_ROWS
        self.columns = BOARD_COLS
        self.board = self.create_initial_board()
        # Remove this later, because we will move the logic of the game
        self.selected_piece = None
        self.red_kings = self.white_kings = 0
        self.red_left = self.white_left = 12


    def create_initial_board(self):
        """
        :return:
        """
        board = [[None for _ in range(self.columns)] for _ in range(self.rows)]

        # Initialize pieces in their correct starting positions.
        # This is just a simplified example; you'd set up the actual starting positions per the game's rules.
        #for row in range(self.rows):
        #    for column in range(self.columns):
        #        if (row < 3 or row > 4) and (row + column) % 2 == 1:
        #            piece_color = "black" if row < 3 else "white"
        #            board[row][column] = GamePiece(piece_color)
        #return board

    # Move this later
    def draw_cubes (self, win):
        win.fill(BLACK)
        for row in range(BOARD_ROWS):
            for col in range(row % 2, BOARD_ROWS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))








