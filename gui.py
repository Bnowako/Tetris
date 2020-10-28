import pygame
from config import config
import typing


class GameWindow():
    def __init__(self):
        self.window_x = config['window_x']
        self.window_y = config['window_y']
        self.square_size = config['square_size']
        self.game_board_width = config['game_board_width']
        self.game_board_height = config['game_board_height']
        self.upper_left_board_corner_x = (
            self.window_x - (self.square_size*self.game_board_width))/2
        self.upper_left_board_corner_y = (
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

        upper_left_corner = (self.upper_left_board_corner_x,
                             self.upper_left_board_corner_y)
        upper_right_corner = (
            self.upper_left_board_corner_x+self.square_size*self.game_board_width, self.upper_left_board_corner_y)
        bottom_right_corner = (self.upper_left_board_corner_x+self.square_size*self.game_board_width,
                               self.upper_left_board_corner_y+self.square_size*self.game_board_height)
        bottom_left_corner = (
            self.upper_left_board_corner_x, self.upper_left_board_corner_y+self.square_size*self.game_board_height)

        board_coordinates = [
            upper_left_corner, upper_right_corner, bottom_right_corner, bottom_left_corner]

        pygame.draw.lines(self.display, self.red, True, board_coordinates)

        pygame.display.update()

    def draw_grid(self):
        for i in range(self.game_board_width-1):
            pygame.draw.line(self.display, self.blue,
                             (self.upper_left_board_corner_x+self.square_size*(i+1), self.upper_left_board_corner_y), (self.upper_left_board_corner_x+self.square_size*(i+1), self.upper_left_board_corner_y+self.square_size*self.game_board_height))
        for i in range(self.game_board_height-1):
            pygame.draw.line(self.display, self.blue,
                             (self.upper_left_board_corner_x, self.upper_left_board_corner_y+self.square_size*(i+1)), (self.upper_left_board_corner_x+self.square_size*self.game_board_width, self.upper_left_board_corner_y+self.square_size*(i+1)))
        pygame.display.update()

    def draw_fallen_pieces(self, grid: list, grid_color: list):
        # iterate through grid and list and draw fallen pieces
        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                if square:
                    pygame.draw.rect(self.display, grid_color[i][j], [
                        j*self.square_size + self.upper_left_board_corner_x, i *
                        self.square_size + self.upper_left_board_corner_y, self.square_size, self.square_size
                    ])

    def draw_score(self, score: int):
        textsurface = self.myfont.render(
            f'SCORE: {score}', False, (255, 255, 255))
        self.display.blit(textsurface, (10, 10))


class Piece():
    def __init__(self, shape: str,  position_x: int, position_y: int, display: pygame.Surface):
        self.shape = config[shape]
        self.position_x = position_x
        self.position_y = position_y
        self.display = display
        self.square_size = config['square_size']
        self.color = config[f'{shape}_color']

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
