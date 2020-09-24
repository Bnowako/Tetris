import pygame

I = [[1, 1, 1, 1]]

O = [[1, 1],
     [1, 1]]

T = [[1, 1, 1],
     [0, 1, 0]]

J = [[1, 0, 0],
     [1, 1, 1]]

L = [[0, 0, 1],
     [1, 1, 1]]

S = [[0, 1, 1],
     [1, 1, 0]]

Z = [[1, 1, 0],
     [0, 1, 1]]


class Game_Window():
    def __init__(self):
        self.window_x = 500
        self.window_y = 500
        self.display = 0
        self.square_size = 20
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

    def initialize(self):
        pygame.init()
        self.display = pygame.display.set_mode((self.window_x, self.window_y))
        return self.display

    def create_game_board(self):
        fixed_x_value = (self.window_x - (self.square_size*10))/2
        fixed_y_value = (self.window_y - (self.square_size*20))/2

        pygame.draw.lines(self.display, self.red, True,
                          [(fixed_x_value, fixed_y_value), (fixed_x_value+self.square_size*10, fixed_y_value), (fixed_x_value+self.square_size*10, fixed_y_value+self.square_size*20), (fixed_x_value, fixed_y_value+self.square_size*20)])
        pygame.display.update()

    def draw_grid(self):
        fixed_x_value = (self.window_x - (self.square_size*10))/2
        fixed_y_value = (self.window_y - (self.square_size*20))/2

        for i in range(9):
            pygame.draw.line(self.display, self.blue,
                             (fixed_x_value+self.square_size*(i+1), fixed_y_value), (fixed_x_value+self.square_size*(i+1), fixed_y_value+self.square_size*20))
        for i in range(19):
            pygame.draw.line(self.display, self.blue,
                             (fixed_x_value, fixed_y_value+self.square_size*(i+1)), (fixed_x_value+self.square_size*10, fixed_y_value+self.square_size*(i+1)))
        pygame.display.update()


class Piece():
    def __init__(self, shape, rotation, position_x, position_y, display):
        self.shape = shape
        self.rotation = rotation
        self.position_x = position_x
        self.position_y = position_y
        self.display = display
        self.square_size = 20

    def draw(self):
        for i, row in enumerate(self.shape):
            for j, square in enumerate(row):
                if square == 1:
                    pygame.draw.rect(self.display, (255, 0, 0),
                                     [self.position_x+((j+1)*self.square_size), self.position_y+((i+1)*self.square_size),
                                      self.square_size, self.square_size]
                                     )
                    print("DRAWING", [self.position_x+((j+1)*self.square_size), self.position_y+((i+1)*self.square_size),
                                      self.square_size, self.square_size])
        pygame.display.update()


def main():
    game_window = Game_Window()
    display = game_window.initialize()
    game_window.create_game_board()
    game_window.draw_grid()
    piece = Piece(T, 0, 190, 30, display)
    piece.draw()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
