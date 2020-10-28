from config import config
import gui
import random
import typing
import pygame


class GameLogic():
    def __init__(self, display: pygame.Surface):
        self.grid = [[0 for i in range(10)]for i in range(20)]
        self.grid_color = [[0 for i in range(10)]for i in range(20)]
        self.new_piece_needed = True

        self.square_size = config['square_size']

        self.window_x = config['window_x']
        self.window_y = config['window_y']
        self.game_board_width = config['game_board_width']
        self.game_board_height = config['game_board_height']

        self.display = display
        self.current_piece_name = "I"
        self.piece_position_x = (self.window_x // 2) - self.square_size
        self.piece_position_y = (
            self.window_y - (self.game_board_height*self.square_size))//2

        self.piece = gui.Piece("I", self.piece_position_x,
                               self.piece_position_y, self.display)

        self.pieces = ["I", "O", "J", "L", "Z", "S", "T"]

        self.grid_column = ((self.piece_position_x -
                             ((self.window_x - self.game_board_width * self.square_size)//2))//self.square_size)
        self.grid_row = ((self.piece_position_y -
                          ((self.window_y - self.game_board_height*self.square_size)//2))//self.square_size)
        self.points = 0
        self.pieces_fallen = 0
        self.first_iteration = 0

        self.game_speed = 500
        self.time_elapsed = 0

    def handle_game(self, game_window: gui.GameWindow, time_elapsed: int):
        # update elapsed time
        self.time_elapsed += time_elapsed
        # draw grid,scoreboard,fallen pieces
        self.draw_game_setup(game_window)
        # if new_piece_needed add new piece and set self.first_iteration to 0
        if self.new_piece_needed:
            self.add_new_piece()
            self.first_iteration = 0
        # handle_game function is triggered every pygame clock tick
        # game_speed is slower than frequency of pygame clock tick
        # game_speed is time interval in wich piece will be falling
        # so if self.time_elapsed is greater than self.game_speed
        # move piece one unit down
        if self.time_elapsed > self.game_speed:
            if not self.track_piece_collisions() and self.first_iteration:
                self.piece_position_y += self.square_size
            # reset time_elapsed so we can measure each interval
            self.time_elapsed = 0
        # draw piece each time handle_game is triggerd
        # this allows to move piece independently from game_speed
        self.piece.draw(self.piece_position_x, self.piece_position_y)

        # this variable allows piece to appear on the top and fall after interval
        # without it piece will fall immediately one unit
        self.first_iteration += 1

        # each iteration check if game is over
        self.check_for_game_over()

    def draw_game_setup(self, game_window: gui.GameWindow):
        # draw all background elements needed and all fallen pieces

        game_window.display.fill((0, 0, 0))
        game_window.create_game_board()
        game_window.draw_grid()
        game_window.draw_fallen_pieces(self.grid, self.grid_color)
        game_window.draw_score(self.points)

    def check_for_game_over(self):
        # if any of top squares are occupied restart game
        # it differs from original game but it doesnt make crucial difference for gameplay
        for square in self.grid[0]:
            if square == 1:
                self.restart_game()

    def handle_game_speed(self):
        # increase speed by 50 ms after each 10 fallen pieces
        # if speed reaches 50ms that is 2s per piece to fall down - stop increasing speed
        if self.game_speed == 50:
            return 0
        elif self.pieces_fallen % 10 == 0:
            self.game_speed -= 50

    def get_random_piece(self) -> str:
        # return random piece name
        return random.choice(self.pieces)

    def track_piece_collisions(self) -> bool:
        # tracking if fallen pieces or pieces that stack on top of another piece

        self.update_grid_column_and_row()
        piece_height = len(self.piece.shape)

        # if piece fall down - stop it
        if self.grid_row + piece_height == self.game_board_height:
            self.stop_current_piece(self.grid_row, self.grid_column)
            return True
        else:
            # if piece will fall on top of another piece - stop it
            for i, row in enumerate(self.piece.shape):
                for j, square in enumerate(row):
                    if self.grid[self.grid_row+(i+1)][self.grid_column+j] and square:
                        self.stop_current_piece(
                            self.grid_row, self.grid_column)
                        return True
        return False

    def add_new_piece(self):
        # reseting position of piece
        self.piece_position_x = (self.window_x // 2) - self.square_size
        self.piece_position_y = (
            self.window_y - (self.game_board_height*self.square_size))//2
        # get new random piece name
        self.current_piece_name = self.get_random_piece()
        # make new piece object from Piece class
        self.piece = gui.Piece(self.current_piece_name, self.piece_position_x,
                               self.piece_position_y, self.display)
        # change new_piece_needed to false - we already made new piece
        self.new_piece_needed = False

    def stop_current_piece(self, grid_row: int, grid_column: int):
        # if any of the collisions occur:
        # - stop current piece
        # - add it to grid that will be drawn
        # - add its color to list

        for i, row in enumerate(self.piece.shape):
            for j, square in enumerate(row):
                if square:
                    self.grid[grid_row+i][grid_column+j] = 1
                    self.grid_color[grid_row +
                                    i][grid_column+j] = self.piece.color
        self.new_piece_needed = True
        # after each fall of the piece check if any of the rows was scored
        self.check_if_scored()
        # update pieces_fallen counter
        self.pieces_fallen += 1
        # check if game_speed needs to be increased
        self.handle_game_speed()

    def handle_movement(self, event: pygame.event):
        # handler for:
        # - movement left,right,down
        # - rotation
        right_arrow = 275
        left_arrow = 276
        down_arrow = 274
        up_arrow = 273
        # get key value from event object
        key = event.__dict__['key']
        # distinguish each event
        if not self.new_piece_needed:
            if key == left_arrow:
                if self.is_move_valid("left"):
                    # if movement is possible move piece 1 unit to the left
                    self.piece_position_x -= self.square_size
            elif key == right_arrow:
                if self.is_move_valid("right"):
                    # if movement is possible move piece 1 unit to the right
                    self.piece_position_x += self.square_size
            elif key == down_arrow:
                if self.is_move_valid("down"):
                    # if movement is possible move piece 1 unit down
                    self.piece_position_y += self.square_size
            elif key == up_arrow:
                # rotate piece validation inside function
                self.rotate_piece()

    def is_move_valid(self, direction: str) -> bool:
        # validate movment left,right,down
        self.update_grid_column_and_row()
        piece_width = len(self.piece.shape[0])
        piece_height = len(self.piece.shape)

        if direction == "right":
            if (self.grid_column + piece_width == self.game_board_width) or (not self.is_move_valid_helper(direction)):
                return False
            else:
                return True
        elif direction == "left":
            if self.grid_column == 0 or not self.is_move_valid_helper(direction):
                return False
            else:
                return True
        elif direction == "down":
            if self.grid_row + piece_height == self.game_board_height or not (self.is_move_valid_helper(direction)):
                return False
            else:
                return True

    def is_move_valid_helper(self, direction: str) -> bool:
        # validate movment left,right,down
        # iterate through piece shape list and:
        # - if square under any piece square is unavailable return False
        # - if square under every piece square is available return True

        if direction == "right" or direction == "left":

            grid_column_to_check = 1 if direction == "right" else -1
            for i, row in enumerate(self.piece.shape):
                for j, square in enumerate(row):
                    if square and self.grid[self.grid_row + i][self.grid_column+grid_column_to_check + j]:
                        return False
            return True
        if direction == "down":
            if self.grid_row + len(self.piece.shape) == self.game_board_height:
                return False
            for i, row in enumerate(self.piece.shape):
                for j, square in enumerate(row):
                    if square and self.grid[self.grid_row+i+1][self.grid_column + j]:
                        return False

            return True

    def update_grid_column_and_row(self):
        # update piece position variables
        self.grid_column = ((self.piece_position_x -
                             ((self.window_x - self.game_board_width * self.square_size)//2))//self.square_size)
        self.grid_row = ((self.piece_position_y -
                          ((self.window_y - self.game_board_height*self.square_size)//2))//self.square_size)

    def rotate_piece(self):
        # due to piece_shape format - list with 1 representing piece suqares
        # piece rotation is implemented by transversing list

        self.update_grid_column_and_row()

        rotated_shape = self.transverse_list(self.piece.shape)
        # validate rotation
        if self.is_rotation_valid(rotated_shape):
            self.piece.shape = rotated_shape

    def is_rotation_valid(self, rotated_shape: list) -> bool:
        # check if there is space for rotation on the board
        enough_space_horizontal = len(
            rotated_shape[0]) + self.grid_column - 1 < self.game_board_width
        enough_space_vertical = len(
            rotated_shape) + self.grid_row - 1 < self.game_board_height

        if not enough_space_horizontal or not enough_space_vertical:
            return False

        # iterate through rotated shape and check if it will collide with any fallen pieces

        for i, row in enumerate(rotated_shape):
            for j, square in enumerate(row):
                if square:
                    if self.grid[self.grid_row + i][self.grid_column+j]:
                        return False

        return True

    def transverse_list(self, list: list) -> list:
        temp_list = [[0 for i in range(len(self.piece.shape))]
                     for i in range(len(self.piece.shape[0]))]

        for i, row in enumerate(self.piece.shape):
            for j, square in enumerate(row):
                temp_list[j][-1*(i+1)] = square
        transversed_list = temp_list
        return transversed_list

    def check_if_scored(self):
        # check if any of the rows are scored
        # if True move rows after score and add points
        scored_points = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        points = 0
        for i, row in enumerate(self.grid):
            if row == scored_points:
                self.move_rows_after_score(i)
                points += 1
        self.points += points

    def move_rows_after_score(self, scored_row_index: int):
        # in tetris after score all rows fall 1 row
        blank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.grid.pop(scored_row_index)
        self.grid.insert(0, blank.copy())
        self.grid_color.pop(scored_row_index)
        self.grid_color.insert(0, blank.copy())

    def restart_game(self):
        # if game over or if escape pressed
        self.grid = [[0 for i in range(10)]for i in range(20)]
        self.new_piece_needed = True
        self.points = 0
