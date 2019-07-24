import pygame
import constants
from typing import Tuple, List
from assets_handler import SpriteSheet


class Bird(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, jump_speed: int,
                 starting_position: Tuple[int, int],
                 sfx_wing_path: str, sfx_point_path: str,
                 sfx_hit_path: str, sfx_die_path: str,
                 sprite_sheet_path: str, frames_coordinates: List) -> None:
        super().__init__()
        self.level = None

        self.width = width
        self.height = height
        self.jump_speed = jump_speed
        self.fall_speed = 0
        self.x, self.y = starting_position

        self.animation_frames = []
        sprite_sheet = SpriteSheet(sprite_sheet_path)
        for coord in frames_coordinates:
            frame = sprite_sheet.get_image(x=coord['x'], y=coord['y'],
                                           width=self.width,
                                           height=self.height)
            self.animation_frames.append(frame)

        self.sfx_wing = pygame.mixer.Sound(sfx_wing_path)
        self.sfx_point = pygame.mixer.Sound(sfx_point_path)
        self.sfx_hit = pygame.mixer.Sound(sfx_hit_path)
        self.sfx_die = pygame.mixer.Sound(sfx_die_path)

        self.is_obstacle_hit = False

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def jump(self) -> None:
        if not self.is_obstacle_hit:
            self.sfx_wing.play()
            self.fall_speed = self.jump_speed

    def update(self, delta_time: float) -> None:
        # Increase falling speed with time
        self.y -= self.fall_speed * delta_time
        self.fall_speed -= 50 * delta_time

        if self.rect.top < 0:
            self.rect.top = 0
            self.fall_speed = 10  # Bounce from top
            self.fall_speed -= 50 * delta_time

        if self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.fall_speed = 0
            self.rect.bottom = constants.SCREEN_HEIGHT

            self.sfx_hit.play()
            self.sfx_die.play()
            self.is_obstacle_hit = True
            return

        pipe_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_sprites, False)
        for pipe in pipe_hit_list:
            self.level.pipe_scroll = 0
            self.level.bkg_scroll = 0
            self.animation_frames = [self.animation_frames[1]] * 3

            self.sfx_hit.play()
            self.sfx_die.play()
            self.is_obstacle_hit = True
            return

    @property
    def animate(self):
        game_time = pygame.time.get_ticks()
        if game_time % 400 >= 200:
            return self.animation_frames[1]
        elif game_time % 400 >= 100:
            return self.animation_frames[2]
        else:
            return self.animation_frames[0]
