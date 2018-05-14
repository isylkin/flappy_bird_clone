"""
Main function of the game
"""

import os, sys, pygame
import constants
from lvl import Level01
import time
from bird import Bird
import menus

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

pygame.init()
pygame.font.init()

# Define display and screen variables
DISPLAY = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
screen = pygame.display.set_mode(DISPLAY)
screen_rect = screen.get_rect()
background = constants.BKGD.convert()

pygame.display.set_caption('Flappy Bird')


def main():
    bird = Bird(388, 231)

    level_list = list()
    level_list.append(Level01(bird, background))

    current_level_no = 0
    current_level = level_list[current_level_no]
    current_level.generate_level()
    bird.level = current_level

    active_sprite_list = pygame.sprite.Group()

    # Create and handle main menu
    m = menus.MainMenu(background)
    while not m.started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit('QUIT')
            elif event.type == pygame.MOUSEBUTTONUP and m.hover:
                m.started = True
        m.update()
        m.draw(screen)
        pygame.display.flip()

    # Create pre game screen
    pgs = menus.PreGameMenu(background, bird)

    # Main game loop
    while True:

        # Handle pre game screen inside the main loop
        while not pgs.tapped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit('QUIT')
                elif event.type == pygame.KEYUP and event.key in (pygame.K_PAUSE, pygame.K_p):
                    paused = not paused
                elif event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and
                                                            event.key in (pygame.K_UP,
                                                            pygame.K_RETURN, pygame.K_SPACE)):
                    bird.jump
                    start_time = time.time() - 4
                    clock = pygame.time.Clock()
                    pgs.tapped = True
            pgs.draw(screen)
            pygame.display.flip()

        # Start of main game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit('QUIT')
            elif event.type == pygame.KEYUP and event.key in (pygame.K_PAUSE, pygame.K_p):
                paused = not paused
            elif event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and
                                                        event.key in (pygame.K_UP, pygame.K_RETURN, pygame.K_SPACE)):
                bird.jump
                start_time = time.time() - 4

        delta_time = start_time - time.time()

        active_sprite_list.update()
        current_level.update()

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        bird.update(delta_time / 100)
        screen.blit(bird.animate, bird.rect)

        if bird.hit:

            # Create and handle Game Over screen, if a bird hit any pipe or ground
            go = menus.GameOver(current_level.score)
            while not go.restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise SystemExit('QUIT')
                    elif event.type == pygame.MOUSEBUTTONUP and go.hover:
                        main()

                go.update()
                go.draw(screen)
                pygame.display.flip()

        clock.tick(65)
        pygame.display.flip()


if __name__ == '__main__':
    main()
