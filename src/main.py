import pygame

from src.constants import *
from src.gameboard import *

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Draughts')


def main():
    # TODO: Later
    # Initialize the main components of the game
    # game_board = GameBoard()
    # game_view = GameView()
    # game_controller = GameController(game_board, game_view)
    # game_controller.run_game_loop()
    # This code will be moved somewhere else

    run = True
    clock = pygame.time.Clock()
    game_board = GameBoard()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        game_board.draw_cubes(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
