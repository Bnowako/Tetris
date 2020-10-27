import pygame
from logic import GameLogic
from gui import Game_Window, Piece


def main():
    game_window = Game_Window()
    display = game_window.initialize()
    game_logic = GameLogic(display)

    game_window.create_game_board()
    game_window.draw_grid()

    clock = pygame.time.Clock()
    time_elapsed = 0
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
                elif event.key == pygame.K_UP:
                    game_logic.rotate_piece()
                elif event.key == pygame.K_ESCAPE:
                    game_on = False
                    game_logic.restart_game()
                elif event.key == pygame.K_DOWN:
                    game_logic.handle_movement(event)
        time_elapsed += clock.get_rawtime()
        if game_on == True:
            game_logic.handle_game(game_window, time_elapsed)
        time_elapsed = 0
        clock.tick()


main()
