import pygame
from constants import BoardSettings, Actions
from view import GameView
from model import GameModel, Caretaker
import tkinter as tk
from tkinter import filedialog
import pickle
import copy
import os


class GameCommand:
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def execute(self):
        raise NotImplementedError("Execute method must be implemented")


class SaveCommand(GameCommand):
    def execute(self):
        print("Execute Save Command")
        save_file(self.game_controller)


class LoadCommand(GameCommand):
    def execute(self):
        print("Execute Load Command")
        load_file(self.game_controller)


class UndoCommand(GameCommand):
    def execute(self):
        print("Execute Undo Command")
        current_game_board_memento = self.game_controller.game_model.save_to_memento()
        undo_game_board_memento = self.game_controller.caretaker.get_undo_memento(current_game_board_memento)
        if undo_game_board_memento:
            self.game_controller.game_model.restore_from_memento(undo_game_board_memento)
            self.game_controller.game_model.game_board.reset_valid_moves()
            self.game_controller.game_view.update()
            print("Undo successful!")
        print("Nothing to undo!")


class RedoCommand(GameCommand):
    def execute(self):
        print("Execute Redo Command")
        current_game_board_memento = self.game_controller.game_model.save_to_memento()
        redo_game_board_memento = self.game_controller.caretaker.get_redo_memento(current_game_board_memento)
        if redo_game_board_memento:
            self.game_controller.game_model.restore_from_memento(redo_game_board_memento)
            print("Redo successful!")
        print("Nothing to redo!")


class MoveCommand(GameCommand):
    def execute(self):
        row, col = self.game_controller.mouse_position
        self.game_controller.save_state()
        success = self.game_controller.game_model.game_board.select(row, col)
        if success:
            print("Execute Move Command")
        else:
            self.game_controller.caretaker.remove_memento()


class GameController:
    def __init__(self):
        self.game_model = GameModel()
        self.game_view = GameView(self)
        self.mouse_position = (0, 0)
        self.run = True

        self.caretaker = Caretaker()

        self.save_state()

        self.commands = {
            Actions.SAVE: SaveCommand(self),
            Actions.UNDO: UndoCommand(self),
            Actions.REDO: RedoCommand(self),
            Actions.LOAD: LoadCommand(self),
            Actions.MOVE: MoveCommand(self)
        }

    def save_state(self):
        game_board_memento = self.game_model.save_to_memento()
        self.caretaker.add_memento(game_board_memento)

    def end_game(self):
        self.run = False

    def run_game(self):

        while self.run:

            self.game_view.tick()

            if self.game_model.game_board.winner():
                self.game_view.display_winner()
                self.end_game()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_position = pygame.mouse.get_pos()
                    click_type, self.mouse_position = self.get_click(mouse_position)

                    if click_type in self.commands:
                        command = self.commands[click_type]
                        command.execute()

            self.game_view.update()

        pygame.quit()

    def get_click(self, position):
        x, y = position

        # Check if click is on the board
        if 0 <= x < BoardSettings.WIDTH and 0 <= y < BoardSettings.HEIGHT:
            col = x // BoardSettings.CELL_SIZE
            row = y // BoardSettings.CELL_SIZE
            return Actions.MOVE, (row, col)

        # Check if click is on any button
        for button_name, button in self.game_view.buttons.items():
            if button.is_over(position):
                return button_name, (0, 0)

        # Undefined
        return 'none', (None, None)


def save_file(game_controller):
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.asksaveasfilename(
        defaultextension=".pkl",
        filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
        title="Save Game"
    )

    if filename:
        with open(filename, "wb") as file:
            saved_state = {
                "game_board": copy.deepcopy(game_controller.game_model.game_board),
                "undo_stack": copy.deepcopy(game_controller.caretaker.get_undo_stack()),
                "redo_stack": copy.deepcopy(game_controller.caretaker.get_redo_stack())
            }
            pickle.dump(saved_state, file)
        print("Game saved to", filename)
    else:
        print("Save operation cancelled.")


def load_file(game_controller):
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename(
        defaultextension=".pkl",
        filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
        title="Load Game"
    )

    if filename:
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                loaded_state = pickle.load(file)
                game_controller.game_model.game_board = loaded_state["game_board"]
                game_controller.caretaker.set_undo_stack(loaded_state["undo_stack"])
                game_controller.caretaker.set_redo_stack(loaded_state["redo_stack"])
            print("Game loaded from", filename)
            game_controller.game_view.update()
        else:
            print("No saved game found.")
    else:
        print("Load operation cancelled.")