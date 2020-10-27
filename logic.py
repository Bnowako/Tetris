from config import Config
from gui import Piece
import random


class GameLogic():
    def __init__(self, display):
        self.grid = [[0 for i in range(10)]for i in range(20)]
        self.grid_color = [[0 for i in range(10)]for i in range(20)]
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
        # self.pieces = ["I", "Z"]

        self.grid_column = ((self.piece_position_x -
                             ((self.window_x - self.game_board_width * self.square_size)//2))//self.square_size)
        self.grid_row = ((self.piece_position_y -
                          ((self.window_y - self.game_board_height*self.square_size)//2))//self.square_size)
        self.points = 0
        self.pieces_fallen = 0
        self.first_iteration = 0

        self.game_speed = 1000
        self.time_elapsed = 0

    def handle_game(self, game_window, time_elapsed):
        self.time_elapsed += time_elapsed
        game_window.display.fill((0, 0, 0))
        game_window.create_game_board()
        game_window.draw_grid()
        game_window.draw_fallen_pieces(self.grid, self.grid_color)
        game_window.draw_score(self.points)

        if self.time_elapsed > self.game_speed:
            if self.new_piece_needed:
                self.add_new_piece()
                self.first_iteration = 0
            if not self.track_piece_collisions():
                if self.first_iteration:
                    self.piece_position_y += self.square_size
            self.time_elapsed = 0

        self.piece.draw(1, self.piece_position_x, self.piece_position_y)
        self.first_iteration += 1

        self.check_for_game_over()

    def check_for_game_over(self):
        for square in self.grid[0]:
            if square == 1:
                self.restart_game()

    def handle_game_speed(self):
        # print(self.pieces_fallen)
        if self.game_speed == 100:
            return 0
        elif self.pieces_fallen % 10 == 0:
            self.game_speed -= 50

    def get_random_piece(self):
        return random.choice(self.pieces)

    def track_piece_collisions(self):
        self.update_grid_column_and_row()
        piece_height = len(self.piece.shape)

        if self.grid_row + piece_height == self.game_board_height:
            self.stop_current_piece(self.grid_row, self.grid_column)
            return True
        else:
            for i, row in enumerate(self.piece.shape):
                for j, square in enumerate(row):
                    if self.grid[self.grid_row+(i+1)][self.grid_column+j] and square:
                        self.stop_current_piece(
                            self.grid_row, self.grid_column)
                        return True
        return False

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
                    self.grid_color[grid_row +
                                    i][grid_column+j] = self.piece.color
        self.new_piece_needed = True
        self.check_if_scored()
        self.pieces_fallen += 1
        self.handle_game_speed()

    def handle_movement(self, event):
        right_arrow = 275
        left_arrow = 276
        down_arrow = 274
        key = event.__dict__['key']
        if not self.new_piece_needed:
            if key == left_arrow:
                if self.validate_movemenet("left"):
                    self.piece_position_x -= self.square_size
            elif key == right_arrow:
                if self.validate_movemenet("right"):
                    self.piece_position_x += self.square_size
            elif key == down_arrow:
                if self.validate_movemenet("down"):
                    self.piece_position_y += self.square_size

    def validate_movemenet(self, direction):
        self.update_grid_column_and_row()
        piece_width = len(self.piece.shape[0])
        piece_height = len(self.piece.shape)
        # valid = self.validate_movement_helper(direction)
        if direction == "right":
            if (self.grid_column + piece_width == self.game_board_width) or (not self.validate_movement_helper(direction)):
                return False
            else:
                return True
        elif direction == "left":
            if self.grid_column == 0 or not self.validate_movement_helper(direction):
                return False
            else:
                return True
        elif direction == "down":
            if self.grid_row + piece_height == self.game_board_height or not (self.validate_movement_helper(direction)):
                return False
            else:
                return True

    def validate_movement_helper(self, direction):
        if direction == "right" or direction == "left":

            grid_column_to_check = 1 if direction == "right" else -1
            for i, row in enumerate(self.piece.shape):
                for j, square in enumerate(row):
                    # if square and j == column_to_check:
                    if square and self.grid[self.grid_row + i][self.grid_column+grid_column_to_check + j]:
                        print(
                            "FALSE", i, j, self.grid[self.grid_row + i][self.grid_column+grid_column_to_check])
                        return False
            return True
        if direction == "down":
            if self.grid_row + len(self.piece.shape) == self.game_board_height:
                return False
            for i, square in enumerate(self.piece.shape[-1]):
                if square and self.grid[int(self.grid_row)+len(self.piece.shape)][self.grid_column + i]:

                    return False

            return True

    def update_grid_column_and_row(self):
        self.grid_column = ((self.piece_position_x -
                             ((self.window_x - self.game_board_width * self.square_size)//2))//self.square_size)
        self.grid_row = ((self.piece_position_y -
                          ((self.window_y - self.game_board_height*self.square_size)//2))//self.square_size)

    def rotate_piece(self):
        self.update_grid_column_and_row()

        rotated_shape = self.transverse_list(self.piece.shape)

        if len(self.piece.shape) + self.grid_column < self.game_board_width and len(self.piece.shape[0]) + self.grid_row < self.game_board_height and self.validate_rotation_collisions(rotated_shape):
            self.piece.shape = rotated_shape

    def validate_rotation_collisions(self, rotated_shape):
        for i, row in enumerate(rotated_shape):
            for j, square in enumerate(row):
                if square:
                    if self.grid[self.grid_row+i][self.grid_column+j]:
                        return False
        return True

    def transverse_list(self, list):
        temp_list = [[0 for i in range(len(self.piece.shape))]
                     for i in range(len(self.piece.shape[0]))]

        for i, row in enumerate(self.piece.shape):
            for j, square in enumerate(row):
                temp_list[j][-1*(i+1)] = square
        transversed_list = temp_list
        return transversed_list

    def check_if_scored(self):
        scored_points = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        points = 0
        for i, row in enumerate(self.grid):
            if row == scored_points:
                # self.grid[i] = blank.copy()
                self.move_rows_after_score(i)
                points += 1
        self.points += points

    def move_rows_after_score(self, scored_row_index):
        blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.grid.pop(scored_row_index)
        self.grid.insert(0, blank.copy())
        self.grid_color.pop(scored_row_index)
        self.grid_color.insert(0, blank.copy())

    def restart_game(self):
        self.grid = [[0 for i in range(10)]for i in range(20)]
        self.new_piece_needed = True
        self.points = 0
