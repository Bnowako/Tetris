import pygame
from config import Config
import typing


class GameWindow():
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

    def initialize(self) -> pygame.Surface:
        # initialize pygame, font, display
        # return Surface on which all elements will be drawn
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        self.display = pygame.display.set_mode((self.window_x, self.window_y))
        return self.display

    def create_game_board(self):
        # draw boundaries for grid
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

    def draw_fallen_pieces(self, grid: list, grid_color: list):
        # iterate through grid and list and draw fallen pieces
        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                if square:
                    pygame.draw.rect(self.display, grid_color[i][j], [
                        j*self.square_size + self.fixed_x_value, i *
                        self.square_size + self.fixed_y_value, self.square_size, self.square_size
                    ])

    def draw_score(self, score: int):
        textsurface = self.myfont.render(
            f'SCORE: {score}', False, (255, 255, 255))
        self.display.blit(textsurface, (10, 10))


class Piece():
    def __init__(self, shape: list,  position_x: int, position_y: int, display: pygame.Surface):
        self.cfg = Config().get_config()
        self.shape = shape
        self.position_x = position_x
        self.position_y = position_y
        self.display = display
        self.square_size = self.cfg['square_size']
        self.color = (255, 0, 0)
        self.assign_piece_color()

    def draw(self, position_x: int, position_y: int):
        # draw piece in specified position
        for i, row in enumerate(self.shape):
            for j, square in enumerate(row):
                if square == 1:
                    pygame.draw.rect(self.display, self.color,
                                     [position_x+((j)*self.square_size), position_y+((i)*self.square_size),
                                      self.square_size, self.square_size]
                                     )
        pygame.display.update()

    def assign_piece_color(self):
        if self.shape == self.cfg['T']:
            self.color = (255, 0, 255)
        elif self.shape == self.cfg['I']:
            self.color = (0, 191, 255)
        elif self.shape == self.cfg['O']:
            self.color = (255, 255, 0)
        elif self.shape == self.cfg['J']:
            self.color = (0, 0, 255)
        elif self.shape == self.cfg['L']:
            self.color = (255, 165, 0)
        elif self.shape == self.cfg['S']:
            self.color = (0, 255, 0)
        elif self.shape == self.cfg['Z']:
            self.color = (255, 0, 0)
