import pygame
from logic import GameLogic
from main import Game_Window, Piece


def main():
    game_window = Game_Window()
    display = game_window.initialize()
    game_logic = GameLogic(display)

    game_window.create_game_board()
    game_window.draw_grid()

    clock = pygame.time.Clock()

    run = True
    game_on = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_on = not game_on
                elif event.key == pygame.K_RIGHT:
                    game_logic.handle_movement(event)
                elif event.key == pygame.K_LEFT:
                    game_logic.handle_movement(event)

        if game_on == True:
            game_logic.handle_game(game_window)

        clock.tick(5)


main()