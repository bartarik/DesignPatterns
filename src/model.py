from constants import BoardSettings, Colors, Direction
import copy


class GameBoardMemento:
    def __init__(self, game_board):
        self._game_board_state = copy.deepcopy(game_board)

    def get_state(self):
        return self._game_board_state


class Caretaker:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def get_undo_stack(self):
        return self._undo_stack

    def get_redo_stack(self):
        return self._redo_stack

    def set_undo_stack(self, undo_stack):
        self._undo_stack = undo_stack

    def set_redo_stack(self, redo_stack):
        self._redo_stack = redo_stack

    def add_memento(self, memento):
        self._undo_stack.append(memento)
        self._redo_stack.clear()

    def remove_memento(self):
        self._undo_stack.pop()

    def get_undo_memento(self, current_game_board_memento):
        if len(self._undo_stack) > 1:
            self._redo_stack.append(copy.deepcopy(current_game_board_memento))
            undo_game_board_memento = self._undo_stack.pop()
            return undo_game_board_memento
        return None

    def get_redo_memento(self, current_game_board_memento):
        if self._redo_stack:
            redo_game_board_memento = self._redo_stack.pop()
            self._undo_stack.append(copy.deepcopy(current_game_board_memento))
            return redo_game_board_memento
        return None


class GameModel:

    def __init__(self):
        self.game_board = GameBoard()

    def save_to_memento(self):
        return GameBoardMemento(copy.deepcopy(self.game_board))

    def restore_from_memento(self, memento):
        self.game_board = memento.get_state()


class GameBoard:
    def __init__(self):
        self._board = []
        self._turn = Colors.RED
        self._red_left, self._white_left = 12, 12
        self._selected = None
        self._valid_moves = {}
        self.create_board()

    def create_board(self):
        for row in range(BoardSettings.ROWS):
            self._board.append([])
            for col in range(BoardSettings.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self._board[row].append(Piece(row, col, Colors.WHITE, NormalMoveStrategy()))
                    elif row > 4:
                        self._board[row].append(Piece(row, col, Colors.RED, NormalMoveStrategy()))
                    else:
                        self._board[row].append(BoardSettings.EMPTY_FIELD)
                else:
                    self._board[row].append(BoardSettings.EMPTY_FIELD)

    def select(self, row, col):
        piece = self.get_piece_or_empty_field(row, col)
        if piece == BoardSettings.EMPTY_FIELD:
            return self.move_to(row, col)
        else:
            return self.select_piece(piece)

    def move_to(self, row, col):
        successful = True
        if (row, col) in self._valid_moves:
            self.move_piece(self._selected, row, col)
            if self._valid_moves[(row, col)]:
                self.remove_pieces(self._valid_moves[(row, col)])
            self.change_turn()
        else:
            successful = False

        self._selected = None
        self._valid_moves = {}
        return successful

    def select_piece(self, piece):
        if piece.color == self._turn:
            self._valid_moves = piece.get_valid_moves(self._board)
            self._selected = None if not self._valid_moves else piece
        return False

    def move_piece(self, piece, row, col):
        self._board[piece.row][piece.col], self._board[row][col] = self._board[row][col], self._board[piece.row][piece.col]
        piece.calc_pos(row, col)
        self.update_king_status(piece, row)

    def update_king_status(self, piece, row):
        if row in [0, BoardSettings.ROWS - 1] and not piece.is_king():
            piece.make_king()

    def get_piece_or_empty_field(self, row, col):
        return self._board[row][col]

    def remove_pieces(self, pieces):
        for piece in pieces:
            self._board[piece.row][piece.col] = BoardSettings.EMPTY_FIELD
            if piece != 0:
                if piece.color == Colors.RED:
                    self._red_left -= 1
                else:
                    self._white_left -= 1

    def change_turn(self):
        self._valid_moves = {}
        self._turn = Colors.WHITE if self._turn == Colors.RED else Colors.RED

    def winner(self):
        return Colors.WHITE if self._red_left <= 0 else Colors.RED if self._white_left <= 0 else None

    def get_field(self, row, col):
        return self._board[row][col]

    def get_turn(self):
        return self._turn

    def get_valid_moves(self):
        return self._valid_moves

    def reset_valid_moves(self):
        self._valid_moves = {}


class Piece:
    def __init__(self, row, col, color, move_strategy):
        self.x, self.y = 0, 0
        self.row, self.col = row, col
        self.color = color
        self.calc_pos(row, col)
        self.move_strategy = move_strategy
        self._king = False

    def calc_pos(self, row, col):
        self.row = row
        self.col = col
        self.x = BoardSettings.CELL_SIZE * self.col + BoardSettings.CELL_SIZE // 2
        self.y = BoardSettings.CELL_SIZE * self.row + BoardSettings.CELL_SIZE // 2

    def make_king(self):
        self._king = True
        self.move_strategy = KingMoveStrategy()

    def is_king(self):
        return self._king

    def get_valid_moves(self, board):
        return self.move_strategy.get_valid_moves(self, board)


class MoveStrategy:
    def get_valid_moves(self, piece, board):
        raise NotImplementedError

    def explore_direction(self, begin, end, step, color, direction_step, direction_type, board, skipped=[]):
        found_moves = {}
        last_moves = []
        for i_row in range(begin, end, step):
            if direction_type == Direction.LEFT:
                if direction_step < 0:
                    break
            else:
                if direction_step >= BoardSettings.COLS:
                    break

            field = board[i_row][direction_step]

            if field == BoardSettings.EMPTY_FIELD:
                if skipped and not last_moves:
                    break
                elif skipped:
                    found_moves[(i_row, direction_step)] = last_moves + skipped
                else:
                    found_moves[(i_row, direction_step)] = last_moves
                if last_moves:
                    if step == Direction.NEGATIVE_STEP:
                        row = max(i_row - 3, 0)
                    else:
                        row = min(i_row + 3, BoardSettings.ROWS)
                    found_moves.update(self.explore_direction(i_row + step, row, step, color, direction_step - 1, Direction.LEFT, board, skipped=last_moves))
                    found_moves.update(self.explore_direction(i_row + step, row, step, color, direction_step + 1, Direction.RIGHT, board, skipped=last_moves))
                break
            elif field.color == color:
                break
            else:
                last_moves = [field]

            if direction_type == Direction.LEFT:
                direction_step -= 1
            else:
                direction_step += 1

        return found_moves


class NormalMoveStrategy(MoveStrategy):
    def get_valid_moves(self, piece, board):
        valid_moves = {}
        if piece.color == Colors.RED:
            begin = piece.row - 1
            end = max(piece.row - 3, -1)
            step = Direction.NEGATIVE_STEP
        else:
            begin = piece.row + 1
            end = min(piece.row + 3, BoardSettings.ROWS)
            step = Direction.POSITIVE_STEP

        valid_moves.update(self.explore_direction(begin, end, step, piece.color, piece.col - 1, Direction.LEFT, board))
        valid_moves.update(self.explore_direction(begin, end, step, piece.color, piece.col + 1, Direction.RIGHT, board))

        return valid_moves


class KingMoveStrategy(MoveStrategy):
    def get_valid_moves(self, piece, board):
        valid_moves = {}
        valid_moves.update(self.explore_direction(piece.row - 1, max(piece.row - 3, -1), Direction.NEGATIVE_STEP, piece.color, piece.col - 1, Direction.LEFT, board))
        valid_moves.update(self.explore_direction(piece.row - 1, max(piece.row - 3, -1), Direction.NEGATIVE_STEP, piece.color, piece.col + 1, Direction.RIGHT, board))
        valid_moves.update(self.explore_direction(piece.row + 1, min(piece.row + 3, BoardSettings.ROWS), Direction.POSITIVE_STEP, piece.color, piece.col - 1, Direction.LEFT, board))
        valid_moves.update(self.explore_direction(piece.row + 1, min(piece.row + 3, BoardSettings.ROWS), Direction.POSITIVE_STEP, piece.color, piece.col + 1, Direction.RIGHT, board))
        return valid_moves
