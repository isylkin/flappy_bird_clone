import time
import pygame
import menus
import constants
from lvl import Level01
from bird import Bird


def main_menu_stage(main_menu: menus.MainMenu,
                    screen: pygame.Surface) -> None:
    while not main_menu.is_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit('QUIT')
            elif event.type == pygame.MOUSEBUTTONUP and main_menu.is_hovered:
                main_menu.is_started = True
        main_menu.update()
        main_menu.draw(screen)
        pygame.display.flip()


def get_ready_stage(get_ready_menu: menus.GetReadyMenu,
                    screen: pygame.Surface, bird: Bird) -> None:
    while not get_ready_menu.is_tapped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit('QUIT')
            elif event.type == pygame.KEYUP and event.key in (pygame.K_PAUSE, pygame.K_p):
                paused = not paused
            elif event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and
                                                        event.key in (pygame.K_UP,
                                                        pygame.K_RETURN, pygame.K_SPACE)):
                bird.jump
                get_ready_menu.is_tapped = True
        get_ready_menu.draw(screen)
        pygame.display.flip()


def game_over_stage(game_over_screen: menus.GameOverScreen,
                    screen: pygame.Surface, current_level: Level01) -> None:
    while not game_over_screen.restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit('QUIT')
            elif event.type == pygame.MOUSEBUTTONUP and game_over_screen.is_hovered:
                game_over_screen.restart = True
        game_over_screen.update()
        game_over_screen.draw(screen, current_level.score)
        pygame.display.flip()


def main() -> None:
    pygame.init()
    pygame.font.init()
    DISPLAY = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    screen = pygame.display.set_mode(DISPLAY)
    background = constants.BACKGROUND.convert()
    bird = Bird(constants.BIRD_WIDTH, constants.BIRD_HEIGHT,
                constants.BIRD_JUMP_SPEED,
                constants.BIRD_STARTING_POSITION,
                constants.SFX_WING_PATH, constants.SFX_POINT_PATH,
                constants.SFX_HIT_PATH, constants.SFX_DIE_PATH,
                constants.BIRD_SPRITE_SHEET_PATH,
                constants.BIRD_FRAMES_COORDINATES)

    level_list = list()
    level_list.append(Level01(bird, background))
    current_level_no = 0
    current_level = level_list[current_level_no]
    current_level.create_level()
    bird.level = current_level

    clock = pygame.time.Clock()
    main_menu = menus.MainMenu(bird, background, constants.MENU_ASSETS)
    get_ready_menu = menus.GetReadyMenu(bird, background, constants.MENU_ASSETS)
    game_over_screen = menus.GameOverScreen()

    # Game start
    main_menu_stage(main_menu, screen)
    while True:
        get_ready_stage(get_ready_menu, screen, bird)
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
            game_over_stage(game_over_screen, screen, current_level)
            break

        clock.tick(65)
        pygame.display.flip()


if __name__ == '__main__':
    while True:
        main()
