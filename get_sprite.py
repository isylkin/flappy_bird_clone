"""
Module for pulling sprites from sprite sheets
of required width and height.
"""

import pygame
import constants


class SpriteSheet(object):
    def __init__(self, file_name):

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height]).convert()

        # Copy the sprite from large img to the smaller one
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Black as the transparent color
        image.set_colorkey(constants.VIOLET)

        return image
