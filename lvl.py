import random
import pygame
import constants
from typing import Tuple, List
from assets_handler import Image, Numbers
from bird import Bird


class Level:
    def __init__(self, bird: Bird) -> None:
        self.bird = bird

        self.background_image = None
        self.background_scroll_speed = constants.BACKGROUND_SCROLL_SPEED
        self.background_x = constants.BACKGROUND_X

        self.pipe_sprites = pygame.sprite.Group()
        self.pipe_assets = constants.PIPE_ASSETS
        self.pipe_scroll_speed = constants.PIPE_SCROLL_SPEED
        self.increase_speed_milestone = constants.INCREASE_SPEED_MILESTONE

        self.score = 0
        self.score_sprites = pygame.sprite.Group()
        self.numbers = Numbers(large=True)

    def update(self) -> None:
        self._scroll_pipes()
        self._update_score()

    def _scroll_pipes(self) -> None:
        self._increase_pipe_scroll_speed(self.increase_speed_milestone)
        for pipe in self.pipe_sprites:
            pipe.rect[0] -= self.pipe_scroll_speed

    def _increase_pipe_scroll_speed(self, milestone: int) -> None:
        if self.score == milestone:
            self.pipe_scroll_speed = 3

    def _update_score(self) -> None:
        pipe_obstacles = self.pipe_sprites.sprites()[::2]  # One obstacle consists of two pipes
        for pipe in pipe_obstacles:
            if self._is_obstacle_passed(self.bird, obstacle=pipe):
                self.score += 1
                self.bird.sfx_point.play()
        self.score_sprites = self.numbers.generate_score(self.score_sprites,
                                                         self.score)

    def _is_obstacle_passed(self, bird: Bird,
                            obstacle: pygame.sprite.Sprite) -> bool:
        if obstacle.rect.x == bird.rect.left - constants.PIPE_WIDTH:
            return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        self._scroll_background_image(screen)
        self.pipe_sprites.draw(screen)
        self.score_sprites.draw(screen)

    def _scroll_background_image(self, screen: pygame.Surface) -> None:
        # Create a rel_x value which stores a remainder of bkgd_x and bkgd_width
        # Blit the image on the pos rel_x - bkgd_width
        # Blit the same image on the rel_x position to scroll bkgd smoothly
        rel_x = self.background_x % self.background_image.get_rect().width
        screen.blit(self.background_image,
                    (rel_x - self.background_image.get_rect().width, 0))
        if rel_x < constants.SCREEN_WIDTH:
            screen.blit(self.background_image, (rel_x, 0))
        self.background_x -= self.background_scroll_speed


class Level01(Level):
    def __init__(self, bird: Bird, background: pygame.Surface) -> None:
        super().__init__(bird)
        self.background_image = background

        # List with pipes and their locations
        self.level = []
        self.level.extend(constants.INITIAL_PIPES)
        self.max_obstacle_height = constants.MAX_OBSTACLE_HEIGHT
        self.pipe_width = constants.PIPE_WIDTH
        self.pipes_break = constants.PIPES_BREAK

    def create_level(self) -> None:
        self._create_obstacles()
        self._create_pipe_sprites()

    def _create_obstacles(self) -> None:
        for i in range(1, 200):
            top_pipe, bottom_pipe = self._generate_pipes_coordinates()
            self.level.append(top_pipe)
            self.level.append(bottom_pipe)

    def _generate_pipes_coordinates(self) -> Tuple[List, List]:
        top_pipe_height, bottom_pipe_height = self._calculate_pipe_heights()
        pipes_x = self._get_pipes_x()

        top_pipe = [(0, abs(top_pipe_height - self.max_obstacle_height),
                     self.pipe_width, top_pipe_height), pipes_x, 0]
        bottom_pipe = [(self.pipe_width, 0, self.pipe_width, bottom_pipe_height),
                       pipes_x, abs(constants.SCREEN_HEIGHT - bottom_pipe_height)]
        return top_pipe, bottom_pipe

    def _calculate_pipe_heights(self) -> Tuple[int, int]:
        top_height = random.randint(80, self.max_obstacle_height)
        bottom_height = constants.SCREEN_HEIGHT - self.pipes_break - top_height
        return top_height, bottom_height

    def _get_pipes_x(self) -> int:
        last_pipe_right_border = self.level[len(self.level) - 1][1]
        pipes_x = last_pipe_right_border + self.pipe_width * 3
        return pipes_x

    def _create_pipe_sprites(self) -> None:
        for pipe in self.level:
            p = Image(pipe[0], self.pipe_assets)
            p.rect.x = pipe[1]
            p.rect.y = pipe[2]
            self.pipe_sprites.add(p)
