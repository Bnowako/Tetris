from config import Config
from main import Piece
import random


class GameLogic():
    def __init__(self, display):
        self.grid = [[0 for i in range(10)]for i in range(20)]
        self.color_grid = [[0 for i in range(10)]for i in range(20)]
        self.new_piece_needed = True

        self.square_size = 20

        self.display = display
        self.piece_position_x = 250
        self.piece_position_y = 50
        self.piece = Piece("I", 1, self.piece_position_x,
                           self.piece_position_y, self.display)

        self.pieces = ["T", "I", "O", "J", "L", "Z", "S"]
        self.shapes = Config().get_config()

    def piece_falldown(self):
        pass

    def handle_game(self, game_window):
        game_window.display.fill((0, 0, 0))
        game_window.create_game_board()
        game_window.draw_grid()

        if self.new_piece_needed:
            piece_name = self.get_random_piece()
            self.piece = Piece(self.shapes[piece_name], 1, self.piece_position_x,
                               self.piece_position_y, self.display)
            self.new_piece_needed = False
        self.piece_position_y += self.square_size

        self.piece.draw(1, self.piece_position_x, self.piece_position_y)

    def get_random_piece(self):
        return random.choice(self.pieces)
