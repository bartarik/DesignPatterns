import pygame


class BoardSettings:
    WIDTH = 650
    HEIGHT = 650
    ROWS = 8
    COLS = 8
    CELLS = ROWS * COLS
    CELL_SIZE = WIDTH // COLS
    EMPTY_FIELD = 0


class PieceSettings:
    PADDING = 15
    OUTLINE = 2


class Colors:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)
    YELLOW = (255, 255, 0)
    BROWN = (237, 201, 175)
    GOLD = (255,215,0)


class Actions:
    REDO = 'redo'
    LOAD = 'load'
    SAVE = 'save'
    UNDO = 'undo'
    MOVE = 'move'


class Assets:
    CROWN = pygame.transform.scale(pygame.image.load('../assets/crown.png'), (45, 45))
    LOGO = pygame.image.load('../assets/dame.png')


class Settings:
    FPS = 60


class Direction:
    LEFT = 5
    RIGHT = 6
    POSITIVE_STEP = 1
    NEGATIVE_STEP = -1
