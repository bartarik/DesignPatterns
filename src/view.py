import pygame
from constants import BoardSettings, Colors, Assets, PieceSettings, Settings


class GameView:
    def __init__(self, controller):
        self.game_controller = controller
        self.initialize()
        self.create_buttons()

    def initialize(self):
        pygame.init()
        self.window = pygame.display.set_mode((BoardSettings.WIDTH - 3, BoardSettings.HEIGHT + 75))
        self.clock = pygame.time.Clock()
        self.name = pygame.display.set_caption('Dame')
        pygame.display.set_icon(Assets.LOGO)
        self.window.fill(Colors.GREY)

    def tick(self):
        self.clock.tick(Settings.FPS)

    def update(self):
        # Update the board
        self.draw_board(self.window, self.game_controller.game_model.game_board)

        # Update valid moves
        self.draw_valid_moves(self.game_controller.game_model.game_board.get_valid_moves())

        # Update buttons
        for button in self.buttons.values():
            button.draw(self.window)

        # Update current player
        self.draw_player_turn()

        # Update the display
        pygame.display.update()

    def create_buttons(self):
        self.buttons = {
            'load': Button(Colors.GREY, 20, BoardSettings.HEIGHT + 20, 100, 40, 'Load'),
            'save': Button(Colors.GREY, 120 + 20, BoardSettings.HEIGHT + 20, 100, 40, 'Save'),
            'undo': Button(Colors.GREY, 240 + 20, BoardSettings.HEIGHT + 20, 100, 40, 'Undo'),
            'redo': Button(Colors.GREY, 360 + 20, BoardSettings.HEIGHT + 20, 100, 40, 'Redo'),
            'player': Button(Colors.RED, 480 + 10, BoardSettings.HEIGHT + 20, 145, 40, 'Player')
        }

    def draw_piece(self, window, piece):
        if piece is None:
            return
        radius = BoardSettings.CELL_SIZE // 2 - PieceSettings.PADDING
        pygame.draw.circle(window, Colors.GREY, (piece.x, piece.y), radius + PieceSettings.OUTLINE)
        pygame.draw.circle(window, piece.color, (piece.x, piece.y), radius)
        if piece.is_king():
            window.blit(Assets.CROWN, (piece.x - Assets.CROWN.get_width() // 2, piece.y - Assets.CROWN.get_height() // 2))

    def draw_board(self, window, game_board):
        self.draw_fields(window)
        for row in range(BoardSettings.ROWS):
            for col in range(BoardSettings.COLS):
                piece = game_board.get_field(row, col)
                if piece != 0:
                    self.draw_piece(window, piece)

    def draw_fields(self, window):
        for row in range(BoardSettings.ROWS):
            for col in range(BoardSettings.COLS):
                color = Colors.BROWN if (row + col) % 2 == 0 else Colors.BLACK
                pygame.draw.rect(window, color, (col * BoardSettings.CELL_SIZE, row * BoardSettings.CELL_SIZE, BoardSettings.CELL_SIZE, BoardSettings.CELL_SIZE))

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, Colors.GREEN,
                               (col * BoardSettings.CELL_SIZE + BoardSettings.CELL_SIZE // 2, row * BoardSettings.CELL_SIZE + BoardSettings.CELL_SIZE // 2), 20, 4)

    def draw_player_turn(self):
        self.buttons['player'].color = self.game_controller.game_model.game_board.get_turn()

    def display_winner(self):
        winner = self.game_controller.game_model.game_board.winner()
        winner = 'RED' if winner == Colors.RED else 'WHITE'
        font = pygame.font.SysFont('comicsans', 60)
        message = f"{winner} WINS!" if winner else "Draw!"
        text = font.render(message, True, Colors.GOLD)
        self.window.blit(text, (
            BoardSettings.WIDTH // 2 - text.get_width() // 2,
            BoardSettings.HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=1):

        if outline:
            pygame.draw.rect(window, Colors.BLACK, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, True, (0, 0, 0))
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, position):
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True
        return False