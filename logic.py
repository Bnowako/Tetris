from config import Config
from main import Piece
import random


class GameLogic():
    def __init__(self, display):
        self.grid = [[0 for i in range(10)]for i in range(20)]
        self.color_grid = [[0 for i in range(10)]for i in range(20)]
        self.new_piece_needed = True
        self.cfg = Config().get_config()

        self.square_size = self.cfg['square_size']

        self.window_x = self.cfg['window_x']
        self.window_y = self.cfg['window_y']
        self.game_board_width = self.cfg['game_board_width']
        self.game_board_height = self.cfg['game_board_height']

        self.display = display
        self.current_piece_name = "I"
        self.piece_position_x = (self.window_x // 2) - self.square_size
        self.piece_position_y = (
            self.window_y - (self.game_board_height*self.square_size))//2

        self.piece = Piece("I", False, self.piece_position_x,
                           self.piece_position_y, self.display)

        self.pieces = ["I", "O", "J", "L", "Z", "S", "T"]
        # self.pieces = ["I"]

        self.grid_column = ((self.piece_position_x -
                             ((self.window_x - self.game_board_width * self.square_size)//2))//self.square_size)
        self.grid_row = ((self.piece_position_y -
                          ((self.window_y - self.game_board_height*self.square_size)//2))//self.square_size)
        self.points = 0
        self.pieces_fallen = 0

    def handle_game(self, game_window):

        game_window.display.fill((0, 0, 0))
        game_window.create_game_board()
        game_window.draw_grid()
        game_window.draw_fallen_pieces(self.grid, 1)
        game_window.draw_score(self.points)
        if self.new_piece_needed:
            self.add_new_piece()

        self.track_grid_collisions()

        self.piece.draw(1, self.piece_position_x, self.piece_position_y)
        self.piece_position_y += self.square_size

    def get_random_piece(self):
        return random.choice(self.pieces)

    def track_grid_collisions(self):
        self.update_grid_column_and_row()
        piece_height = len(self.piece.shape)

        if self.grid_row + piece_height == self.game_board_height:
            self.stop_current_piece(self.grid_row, self.grid_column)
        else:
            for i, row in enumerate(self.piece.shape):
                for j, square in enumerate(row):
                    if self.grid[self.grid_row+(i+1)][self.grid_column+j] and square:
                        self.stop_current_piece(
                            self.grid_row, self.grid_column)

    def add_new_piece(self):
        self.piece_position_x = (self.window_x // 2) - self.square_size
        self.piece_position_y = (
            self.window_y - (self.game_board_height*self.square_size))//2

        self.current_piece_name = self.get_random_piece()
        self.piece = Piece(self.cfg[self.current_piece_name], False, self.piece_position_x,
                           self.piece_position_y, self.display)
        self.new_piece_needed = False

    def stop_current_piece(self, grid_row, grid_column):
        for i, row in enumerate(self.piece.shape):
            for j, square in enumerate(row):
                if square:
                    self.grid[grid_row+i][grid_column+j] = 1
        self.new_piece_needed = True
        self.check_if_scored()
        self.pieces_fallen += 1

        # print(self.grid)

    def handle_movement(self, event):
        right_arrow = 275
        left_arrow = 276

        key = event.__dict__['key']

        if key == left_arrow:
            if self.validate_movemenet("left"):
                self.piece_position_x -= self.square_size
                self.update_grid_column_and_row()
        elif key == right_arrow:
            if self.validate_movemenet("right"):
                self.piece_position_x += self.square_size
                self.update_grid_column_and_row()

    def validate_movemenet(self, direction):
        piece_width = len(self.piece.shape[0])

        if direction == "right":
            if self.grid_column + piece_width == self.game_board_width:
                return False
            else:
                return True
        elif direction == "left":
            if self.grid_column == 0:
                return False
            else:
                return True

    def update_grid_column_and_row(self):
        self.grid_column = ((self.piece_position_x -
                             ((self.window_x - self.game_board_width * self.square_size)//2))//self.square_size)
        self.grid_row = ((self.piece_position_y -
                          ((self.window_y - self.game_board_height*self.square_size)//2))//self.square_size)

    def rotate_piece(self):
        temp_list = [[0 for i in range(len(self.piece.shape))]
                     for i in range(len(self.piece.shape[0]))]

        for i, row in enumerate(self.piece.shape):
            for j, square in enumerate(row):
                temp_list[j][-1*(i+1)] = square

        self.piece.shape = temp_list

    def check_if_scored(self):
        scored_points = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        points = 0
        for i, row in enumerate(self.grid):
            if row == scored_points:
                self.grid[i] = blank.copy()
                points += 1
        self.points += points
