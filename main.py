import pygame
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
background = constants.BACKGROUND.convert()

pygame.display.set_caption('Flappy Bird')


def main():
    bird = Bird(constants.BIRD_WIDTH, constants.BIRD_HEIGHT,
                constants.BIRD_JUMP_SPEED, constants.BIRD_STARTING_POSITION,
                constants.SFX_WING_PATH, constants.SFX_POINT_PATH,
                constants.SFX_HIT_PATH, constants.SFX_DIE_PATH,
                constants.BIRD_SPRITE_SHEET_PATH, constants.BIRD_FRAMES_COORDINATES)

    level_list = list()
    level_list.append(Level01(bird, background))

    current_level_no = 0
    current_level = level_list[current_level_no]
    current_level.create_level()
    bird.level = current_level
    go = menus.GameOverScreen()

    # Create and handle main menu
    m = menus.MainMenu(bird, background, constants.MENU_ASSETS)
    while not m.is_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit('QUIT')
            elif event.type == pygame.MOUSEBUTTONUP and m.is_hovered:
                m.is_started = True
        m.update()
        m.draw(screen)
        pygame.display.flip()

    # Create pre game screen
    pgs = menus.GetReadyMenu(bird, background, constants.MENU_ASSETS)

    # Main game loop
    while True:

        # Handle pre game screen inside the main loop
        while not pgs.is_tapped:
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
                    pgs.is_tapped = True
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

        current_level.update()
        current_level.draw(screen)

        screen.blit(bird.animate, bird.rect)
        bird.update(delta_time / 100)

        if bird.is_obstacle_hit:
            go.update()
            go.draw(screen, current_level.score)
            while not go.restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        raise SystemExit('QUIT')
                    elif event.type == pygame.MOUSEBUTTONUP and go.is_hovered:
                        main()
                pygame.display.flip()

        clock.tick(65)
        pygame.display.flip()


if __name__ == '__main__':
    main()
