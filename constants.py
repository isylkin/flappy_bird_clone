"""
Global constants
"""
import os

import pygame

FPS = 60

# Colors
BLACK = (0, 0, 0)
VIOLET = (128, 0, 128)
PIPE_COLOR = '#004400'

# Pipes dimensions
PIPE_WIDTH = 100
PIPE_HEIGHT = 20

# Screen dimensions
SCREEN_WIDTH = 854
SCREEN_HEIGHT = 480

# Bird dimensions
BIRD_WIDTH = 57
BIRD_HEIGHT = 40
BIRD_JUMP_SPEED = -70

# Background asset path
BKGD = pygame.image.load(os.path.join("assets", "bg.png"))

