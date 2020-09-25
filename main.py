import pygame
from config import Config


class Game_Window():
    def __init__(self):
        self.cfg = Config().get_config()
        self.window_x = self.cfg['window_x']
        self.window_y = self.cfg['window_y']
        self.square_size = self.cfg['square_size']
        self.game_board_width = self.cfg['game_board_width']
        self.game_board_height = self.cfg['game_board_height']
        self.fixed_x_value = (
            self.window_x - (self.square_size*self.game_board_width))/2
        self.fixed_y_value = (
            self.window_y - (self.square_size*self.game_board_height))/2

        self.display = 0

        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

    def initialize(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.window_x, self.window_y))
        return self.display

    def create_game_board(self):

        pygame.draw.lines(self.display, self.red, True,
                          [(self.fixed_x_value, self.fixed_y_value), (self.fixed_x_value+self.square_size*self.game_board_width, self.fixed_y_value), (self.fixed_x_value+self.square_size*self.game_board_width, self.fixed_y_value+self.square_size*self.game_board_height), (self.fixed_x_value, self.fixed_y_value+self.square_size*self.game_board_height)])

        pygame.display.update()

    def draw_grid(self):

        for i in range(self.game_board_width-1):
            pygame.draw.line(self.display, self.blue,
                             (self.fixed_x_value+self.square_size*(i+1), self.fixed_y_value), (self.fixed_x_value+self.square_size*(i+1), self.fixed_y_value+self.square_size*self.game_board_height))
        for i in range(self.game_board_height-1):
            pygame.draw.line(self.display, self.blue,
                             (self.fixed_x_value, self.fixed_y_value+self.square_size*(i+1)), (self.fixed_x_value+self.square_size*self.game_board_width, self.fixed_y_value+self.square_size*(i+1)))
        pygame.display.update()

    def draw_fallen_pieces(self, grid, color):

        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                if square:
                    pygame.draw.rect(self.display, (255, 0, 0), [
                        j*self.square_size + self.fixed_x_value, i *
                        self.square_size + self.fixed_y_value, self.square_size, self.square_size
                    ])


class Piece():
    def __init__(self, shape, rotation, position_x, position_y, display):
        self.cfg = Config().get_config()
        self.shape = shape
        self.rotation = rotation
        self.position_x = position_x
        self.position_y = position_y
        self.display = display
        self.square_size = self.cfg['square_size']

    def draw(self, rotation, position_x, position_y):
        # print(self.shape)
        # print(position_x, position_y)
        if self.rotation:
            print("ROTATE")
            self.rotation = False

        for i, row in enumerate(self.shape):
            for j, square in enumerate(row):
                if square == 1:
                    pygame.draw.rect(self.display, (255, 0, 0),
                                     [position_x+((j)*self.square_size), position_y+((i)*self.square_size),
                                      self.square_size, self.square_size]
                                     )
        pygame.display.update()
