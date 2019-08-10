import os
import pygame

FPS = 60
SCREEN_WIDTH = 854
SCREEN_HEIGHT = 480

# COLORS
BLACK = (0, 0, 0)
VIOLET = (128, 0, 128)

# PIPES
MAX_OBSTACLE_HEIGHT = 260
PIPE_WIDTH = 100
PIPES_BREAK = 140
PIPE_SCROLL_SPEED = 2
INCREASE_SPEED_MILESTONE = 20
PIPE_COLOR = '#004400'
PIPE_ASSETS = os.path.join("assets", "pipe.png")
INITIAL_PIPES = [[(0, 80, 100, 180), 900, 0],
                [(100, 0, 100, 160), 900, 320],]

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

# BACKGROUND
BACKGROUND = pygame.image.load(os.path.join("assets", "bg.png"))
BACKGROUND_SCROLL_SPEED = 0.5
BACKGROUND_X = 0

# MENUS
MENU_ASSETS = os.path.join("assets", "menu.png")
START_BUTTON_SPRITE_COORDS = (345, 763, 144, 52)
START_BUTTON_POSITION = (345, 345)
START_BUTTON_COORDINATES = pygame.Rect(345, 345, 144, 52)

LOGO_SPRITE_COORDS = (0, 955, 500, 144)
LOGO_POSITION = (177, 50)

GET_READY_BUTTON_SPRITE_COORDS = (0, 792, 312, 85)
GET_READY_BUTTON_POSITION = (275, 40)

TAP_TIP_SPRITE_COORDS = (102, 430, 145, 184)
TAP_TIP_POSITION = (460, 153)

GAME_OVER_SPRITE_COORDS = (0, 710, 340, 75)
GAME_OVER_POSITION = (270, 8)

SUMMARY_SPRITE_COORD = (0, 202, 411, 215)
SUMMARY_POSITION = (230, 140)

OK_BUTTON_SPRITE_COORDS = (357, 477, 150, 54)
OK_BUTTON_POSITION = (357, 390)
OK_BUTTON_COORDINATES = pygame.Rect(357, 390, 150, 54)