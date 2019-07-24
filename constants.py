import os
import pygame

FPS = 60

# Colors
BLACK = (0, 0, 0)
VIOLET = (128, 0, 128)

# Pipes dimensions
MAX_OBSTACLE_HEIGHT = 260
PIPE_WIDTH = 100
PIPES_BREAK = 140
PIPE_SCROLL_SPEED = 2
INCREASE_SPEED_MILESTONE = 20
PIPE_COLOR = '#004400'
PIPE_ASSETS = os.path.join("assets", "pipe.png")
INITIAL_PIPES = [[(0, 80, 100, 180), 900, 0],
                [(100, 0, 100, 160), 900, 320],]

# Screen dimensions
SCREEN_WIDTH = 854
SCREEN_HEIGHT = 480

# BIRD
MAIN_MENU_POSITION = (395, 235)
BIRD_STARTING_POSITION = (388, 231)
BIRD_WIDTH = 57
BIRD_HEIGHT = 39
BIRD_JUMP_SPEED = -70
SFX_WING_PATH = os.path.join("assets", "sfx", "sfx_wing.wav")
SFX_POINT_PATH = os.path.join("assets", "sfx", "sfx_point.wav")
SFX_HIT_PATH = os.path.join("assets", "sfx", "sfx_hit.wav")
SFX_DIE_PATH = os.path.join("assets", "sfx", "sfx_die.wav")
BIRD_SPRITE_SHEET_PATH = os.path.join("assets", "bird.png")
BIRD_FRAMES_COORDINATES = [{'x': 0, 'y': 0},
                           {'x': 97, 'y': 0},
                           {'x': 193, 'y': 0},]

# Background asset path
BACKGROUND = pygame.image.load(os.path.join("assets", "bg.png"))
BACKGROUND_SCROLL_SPEED = 0.5
BACKGROUND_X = 0
