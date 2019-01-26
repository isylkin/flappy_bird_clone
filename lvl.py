"""
Module for creating and managing levels
"""
import os

import pygame
import constants
import assets_handler
import random


class Level:
    """ A generic super-class used to define a level.
    Create a child class for levels with their specific
    info. """

    def __init__(self, bird):
        """ Constructor. Pass a user (a bird). """

        # Level scrolling constants
        self.pipe_scroll = 2
        self.bkg_scroll = 0.5

        # Background image and its starting position
        self.background = None
        self.background_x = 0

        # Bird controlled by a player
        self.bird = bird

        # List of pipe sprites used in any levels
        self.pipe_list = pygame.sprite.Group()

        # Initial score and score sprites
        self.score = 0
        self.score_sprites = pygame.sprite.Group()
        self.numbers = assets_handler.Numbers(large=True)

        # Paths to sprite sheets
        self.pipe_path = os.path.join("assets", "pipe.png")


    # Update everything on this level
    def update(self):

        # Scroll level faster when the player hits 20 points
        if self.score != 0 and self.score == 20:
            self.pipe_scroll = 3

        # Scroll pipes
        for pipe in self.pipe_list:
            pipe.rect[0] -= self.pipe_scroll

        # Check if a bird passed any pipe and change the score
        for num, pipe in enumerate(self.pipe_list):
            if pipe.rect.x == self.bird.rect.left - constants.PIPE_WIDTH and num % 2 == 0:
                self.score += 1
                self.bird.sfx_point.play()

        # Fetch necessary score sprites
        self.score_sprites = self.numbers.generate_score(self.score_sprites, self.score)

    def draw(self, screen):
        """ Draw everything on the level. """

        # Scrolling Background Image
        # Create a rel_x value which stores a remainder of bkgd_x and bkgd_width
        rel_x = self.background_x % self.background.get_rect().width
        # Blit the image on the pos rel_x - bkgd_width
        screen.blit(self.background, (rel_x - self.background.get_rect().width, 0))
        # Blit the same image on the rel_x position to scroll bcgd smoothly
        if rel_x < constants.SCREEN_WIDTH:
            screen.blit(self.background, (rel_x, 0))
        self.background_x -= self.bkg_scroll

        # Draw all the sprite lists
        self.pipe_list.draw(screen)
        self.score_sprites.draw(screen)


class Level01(Level):

    def __init__(self, bird, background):
        # Call the parent constructor
        Level.__init__(self, bird)

        self.background = background

        # List with type of pipe and x, y location; initial pipes
        self.level = [[(0, 80, 100, 180), 900, 0],
                      [(100, 0, 100, 160), 900, 320],
                     ]

        # Constants for pipes
        self.max_height = 260
        self.pipe_width = 100
        self.pipes_break = 140

    def generate_level(self):
        # Generate a level with pipes of random heights
        for i in range(1, 200):
            # Calculate and store heights of top and bottom pipes
            top_height = random.randint(80, self.max_height)
            bot_height = constants.SCREEN_HEIGHT - self.pipes_break - top_height

            # Calculate and store x position of pipes
            pipes_x = self.level[len(self.level) - 1][1] + self.pipe_width * 3

            # Store the pipes and append them to the level
            top_pipe = [(0, abs(top_height - self.max_height), self.pipe_width, top_height),
                        pipes_x, 0]
            bottom_pipe = [(self.pipe_width, 0, self.pipe_width, bot_height),
                           pipes_x, abs(constants.SCREEN_HEIGHT - bot_height)]

            self.level.append(top_pipe)
            self.level.append(bottom_pipe)

        # Go through the list above and add pipes
        for pipe in self.level:
            p = assets_handler.Asset(pipe[0], self.pipe_path)
            p.rect.x = pipe[1]
            p.rect.y = pipe[2]
            self.pipe_list.add(p)
