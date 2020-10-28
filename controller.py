import pygame
from logic import GameLogic
from gui import GameWindow, Piece


def main():
    # create game_window object from GameWindow() class from gui.py
    game_window = GameWindow()

    # get Surface object and initialize pygame
    display = game_window.initialize()

    # create game_logic object from GameLogic
    game_logic = GameLogic(display)

    # create clock object
    clock = pygame.time.Clock()

    # create time_elapsed variable to store elapsed time of each tick
    time_elapsed = 0

    # create run variable to handle breaking while loop
    run = True

    # create game_on variable to start/stop game
    game_on = False

    # core loop of the program that:
    # - listens for event from keyboard
    # - calls handle_game every tick if game_on is True

    while run:
        for event in pygame.event.get():
            # if user click quit button it quits the program
            if event.type == pygame.QUIT:
                run = False
            # handling all events for controling the game
            movement_keys = [pygame.K_RIGHT,
                             pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_on = not game_on
                elif event.key == pygame.K_ESCAPE:
                    game_logic.restart_game()
                elif event.key in movement_keys:
                    game_logic.handle_movement(event)

        # update elapsed time before calling handle_game func to pass it as an argument
        time_elapsed += clock.get_rawtime()
        # if game is on call handle_game
        if game_on == True:
            game_logic.handle_game(game_window, time_elapsed)
        # set elapsed time to 0
        # this allows to get elapsed time of each iteration
        time_elapsed = 0
        clock.tick()


main()
