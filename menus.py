"""
Module with all the game's menus
"""
import os

import pygame
import constants
from bird import Bird
import assets_handler


class MainMenu:
    def __init__(self, background):
        # Background variables
        self.background = background
        self.background_x = 0
        self.bkg_scroll = 0.2

        # Objects to be displayed in main menu
        self.bird = Bird(395, 235)
        self.assets_path = os.path.join("assets", "menu.png")
        self.start = assets_handler.Asset((345, 763, 144, 52), self.assets_path)
        self.start.rect = (345, 320)
        self.start_rect_object = pygame.Rect(345, 320, 144, 52)
        self.logo = assets_handler.Asset((0, 955, 500, 144), self.assets_path)
        self.logo.rect = (177, 50)

        # Disclaimer variables
        self.font_17 = pygame.font.SysFont('Comic Sans MS', 17)
        self.disclaimer = self.font_17.render('Non-commercial Flappy Bird clone', False, (0, 0, 255))
        self.font_20 = pygame.font.SysFont('Comic Sans MS', 20)
        self.author = self.font_17.render('made by Ivan', False, (0, 0, 255))
        self.email = self.font_17.render('ivan.sylkin.k@gmail.com', False, (0, 0, 255))

        self.sprite_list = pygame.sprite.Group()
        self.sprite_list.add(self.start)
        self.sprite_list.add(self.logo)

        self.hover = False
        self.started = False

    def draw(self, screen):
        rel_x = self.background_x % self.background.get_rect().width
        # Blit the image on the pos rel_x - bkgd_width
        screen.blit(self.background, (rel_x - self.background.get_rect().width, 0))
        # Blit the same image on the rel_x position to scroll bcgd smoothly
        if rel_x < constants.SCREEN_WIDTH:
            screen.blit(self.background, (rel_x, 0))
        self.background_x -= self.bkg_scroll

        self.sprite_list.draw(screen)
        screen.blit(self.bird.animate, self.bird.rect)
        screen.blit(self.disclaimer, (280, 400))
        screen.blit(self.author, (365, 425))
        screen.blit(self.email, (325, 445))

    def update(self):
        # Change hover status and cursor on hover over a start button
        if self.start_rect_object.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            self.hover = True
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.hover = False


class PreGameMenu:
    def __init__(self, background, bird):
        self.background = background
        self.background_x = 0
        self.bkg_scroll = 0.2

        self.bird = bird

        self.sprite_list = pygame.sprite.Group()
        self.assets_path = os.path.join("assets", "menu.png")
        self.get_ready = assets_handler.Asset((0, 792, 312, 85), self.assets_path)
        self.get_ready.rect = (275, 40)
        self.sprite_list.add(self.get_ready)
        self.tap = assets_handler.Asset((102, 430, 145, 184), self.assets_path)
        self.tap.rect = (460, 153)
        self.sprite_list.add(self.tap)

        self.tapped = False

    def draw(self, screen):
        rel_x = self.background_x % self.background.get_rect().width
        # Blit the image on the pos rel_x - bkgd_width
        screen.blit(self.background, (rel_x - self.background.get_rect().width, 0))
        # Blit the same image on the rel_x position to scroll bcgd smoothly
        if rel_x < constants.SCREEN_WIDTH:
            screen.blit(self.background, (rel_x, 0))
        self.background_x -= self.bkg_scroll

        self.sprite_list.draw(screen)
        screen.blit(self.bird.animate, self.bird.rect)


class GameOver:
    def __init__(self, score):
        self.score = score

        self.sprite_list = pygame.sprite.Group()
        self.assets_path = os.path.join("assets", "menu.png")
        self.game_over = assets_handler.Asset((0, 710, 340, 75), self.assets_path)
        self.game_over.rect = (270, 8)
        self.sprite_list.add(self.game_over)

        self.summary = assets_handler.Asset((0, 202, 411, 215), self.assets_path)
        self.summary.rect = (230, 140)
        self.sprite_list.add(self.summary)

        self.ok_button = assets_handler.Asset((357, 477, 150, 54), self.assets_path)
        self.ok_button.rect = (357, 390)
        self.ok_button_rect_object = pygame.Rect(357, 390, 150, 54)
        self.sprite_list.add(self.ok_button)

        self.hover = False
        self.restart = False

        self.nums = assets_handler.Numbers(large=False)
        self.score_sprites = pygame.sprite.Group()
        self.score_sprites.empty()

        self.score_sprites = self.nums.generate_score(self.score_sprites, self.score)

    def draw(self, screen):
        self.sprite_list.draw(screen)
        self.score_sprites.draw(screen)

    def update(self):
        if self.ok_button_rect_object.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
            self.hover = True
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            self.hover = False
