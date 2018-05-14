"""
This module holds the Bird class, which represents
the controlled sprite on the screen.
"""

import pygame
from get_sprite import SpriteSheet
import constants

pygame.mixer.init()


class Bird(pygame.sprite.Sprite):
    """ The class represents the bird
    controlled by the player """

    WIDTH = constants.BIRD_WIDTH
    HEIGHT = constants.BIRD_HEIGHT
    JUMP_SPEED = constants.BIRD_JUMP_SPEED

    def __init__(self, x, y):

        # Call the parent's constructor
        super(Bird, self).__init__()
        # --- Attributes
        self.x, self.y = x, y
        self.fall_speed = 0

        self.score = 0

        self.hit = False

        # All the images for bird's animation
        self.flying_frames = []

        # List of sprites we can bump against
        self.level = None

        sprite_sheet = SpriteSheet('assets\\bird.png')
        # Load all the images into a list
        image = sprite_sheet.get_image(0, 0, 57, 39)
        self.flying_frames.append(image)
        image = sprite_sheet.get_image(97, 0, 57, 39)
        self.flying_frames.append(image)
        image = sprite_sheet.get_image(193, 0, 57, 39)
        self.flying_frames.append(image)

        # Set the image the player starts with
        self.image = self.flying_frames[0]

        # Sounds
        self.sfx_wing = pygame.mixer.Sound('assets\sfx\sfx_wing.wav')
        self.sfx_point = pygame.mixer.Sound('assets\sfx\sfx_point.wav')
        self.sfx_hit = pygame.mixer.Sound('assets\sfx\sfx_hit.wav')
        self.sfx_die = pygame.mixer.Sound('assets\sfx\sfx_die.wav')

        self.pipe_hit_list = None

    @property
    def jump(self):
        if not self.pipe_hit_list:
            self.sfx_wing.play()
            self.fall_speed = Bird.JUMP_SPEED

    def update(self, delta_time):
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
            self.hit = True

        # See if we hit a pipe
        pipe_hit_list = pygame.sprite.spritecollide(self, self.level.pipe_list, False)
        for pipe in pipe_hit_list:
            self.pipe_hit_list = pipe_hit_list
            self.level.pipe_scroll = 0
            self.level.bkg_scroll = 0
            self.flying_frames = [self.flying_frames[1]] * 3

            self.sfx_hit.play()
            self.hit = True
            self.sfx_die.play()

    @property
    def animate(self):
        """ Animate a bird's image """
        game_time = pygame.time.get_ticks()
        if game_time % 400 >= 200:
            return self.flying_frames[1]
        elif game_time % 400 >= 100:
            return self.flying_frames[2]
        else:
            return self.flying_frames[0]

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)
