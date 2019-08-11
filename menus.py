import pygame
import constants
from bird import Bird
from assets_handler import Image, Numbers


class BaseMenu:
    def __init__(self, bird: Bird, background: pygame.Surface,
                 menu_assets_path: str) -> None:
        self.bird = bird
        self.background_image = background
        self.menu_assets = menu_assets_path
        self.background_x = constants.BACKGROUND_X
        self.background_scroll_speed = constants.BACKGROUND_SCROLL_SPEED
        self.sprite_list = pygame.sprite.Group()

    def _scroll_background_image(self, screen: pygame.Surface) -> None:
        rel_x = self.background_x % self.background_image.get_rect().width
        screen.blit(self.background_image,
                    (rel_x - self.background_image.get_rect().width, 0))
        if rel_x < constants.SCREEN_WIDTH:
            screen.blit(self.background_image, (rel_x, 0))
        self.background_x -= self.background_scroll_speed

    def draw(self, screen: pygame.Surface):
        self._scroll_background_image(screen)
        self.sprite_list.draw(screen)
        screen.blit(self.bird.animate, self.bird.rect)


class MainMenu(BaseMenu):
    def __init__(self, bird: Bird, background: pygame.Surface,
                 menu_assets_path: str) -> None:
        super().__init__(bird, background, menu_assets_path)
        self.start_button = Image(self.menu_assets,
                                  constants.START_BUTTON_SPRITE_COORDS,
                                  constants.START_BUTTON_POSITION,
                                  constants.START_BUTTON_COORDINATES)
        self.logo = Image(self.menu_assets,
                          constants.LOGO_SPRITE_COORDS,
                          constants.LOGO_POSITION)

        self.sprite_list.add(self.start_button)
        self.sprite_list.add(self.logo)

        self.is_hovered = False
        self.is_started = False

    def update(self):
        # Change hover status and cursor on hover over a start button
        if self.start_button.rect_object.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            self.is_hovered = True
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.is_hovered = False


class GetReadyMenu(BaseMenu):
    def __init__(self, bird: Bird, background: pygame.Surface,
                 menu_assets_path: str) -> None:
        super().__init__(bird, background, menu_assets_path)
        self.get_ready_button = Image(self.menu_assets,
                                      constants.GET_READY_BUTTON_SPRITE_COORDS,
                                      constants.GET_READY_BUTTON_POSITION)
        self.tap_tip = Image(self.menu_assets,
                             constants.TAP_TIP_SPRITE_COORDS,
                             constants.TAP_TIP_POSITION)

        self.sprite_list.add(self.get_ready_button)
        self.sprite_list.add(self.tap_tip)

        self.is_tapped = False


class GameOverScreen:
    def __init__(self) -> None:
        self.sprite_list = pygame.sprite.Group()
        self.menu_assets = constants.MENU_ASSETS
        self.game_over_image = Image(self.menu_assets,
                                     constants.GAME_OVER_SPRITE_COORDS,
                                     constants.GAME_OVER_POSITION)
        self.summary_banner = Image(self.menu_assets,
                                    constants.SUMMARY_SPRITE_COORD,
                                    constants.SUMMARY_POSITION)
        self.ok_button = Image(self.menu_assets,
                               constants.OK_BUTTON_SPRITE_COORDS,
                               constants.OK_BUTTON_POSITION,
                               constants.OK_BUTTON_COORDINATES)

        self.sprite_list.add(self.game_over_image)
        self.sprite_list.add(self.summary_banner)
        self.sprite_list.add(self.ok_button)

        self.is_hovered = False
        self.restart = False

        self.nums = Numbers(constants.NUMBERS_ASSETS,
                            constants.BIG_NUMS_SPRITE_COORDS,
                            constants.BIG_NUMS_POSITION,
                            constants.SMALL_NUMS_SPRITE_COORDS,
                            constants.SMALL_NUMS_POSITION)

    def draw(self, screen: pygame.Surface, score: int):
        self.sprite_list.draw(screen)
        score_sprites = self._generate_score_sprites(score)
        score_sprites.draw(screen)

    def _generate_score_sprites(self, score):
        score_sprites = self.nums.generate_score(score, is_big=False)
        return score_sprites

    def update(self):
        if self.ok_button.rect_object.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            self.is_hovered = True
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.is_hovered = False
