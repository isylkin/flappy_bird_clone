import pygame
import constants
from typing import Tuple, Dict, List


class SpriteSheet:
    def __init__(self, file_name: str) -> None:
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        image = pygame.Surface([width, height]).convert()
        image.blit(source=self.sprite_sheet,
                   dest=(0, 0), area=(x, y, width, height))
        image.set_colorkey(constants.VIOLET)  # Violet as the transparent color
        return image


class Image(pygame.sprite.Sprite):
    def __init__(self, assets_path: str,
                 sprite_coords: Tuple[int, int, int, int],
                 rect: Tuple[int, int],
                 rect_object: pygame.Rect = None) -> None:
        super().__init__()
        sprite_sheet = SpriteSheet(assets_path)
        self.image = sprite_sheet.get_image(sprite_coords[0],
                                            sprite_coords[1],
                                            sprite_coords[2],
                                            sprite_coords[3],)
        self._rect = self.image.get_rect()
        self._rect.x = rect[0]
        self._rect.y = rect[1]

        self._rect_object = rect_object

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = self.image.get_rect()
        self._rect.x = value[0]
        self._rect.y = value[1]

    @property
    def rect_object(self):
        return self._rect_object

    @rect_object.setter
    def rect_object(self, value):
        self._rect_object = value


class Numbers:
    def __init__(self, nums_assets_path: str,
                 big_nums_coords: List, big_nums_position: Tuple [int, int],
                 small_nums_coords: List, small_nums_position: Tuple[int, int]) -> None:
        self.nums_assets = nums_assets_path
        self.big_nums_coords = big_nums_coords  # Live score
        self.big_nums_position = big_nums_position
        self.small_nums_coords = small_nums_coords  # Summary
        self.small_nums_position = small_nums_position
        self.big_nums_images = {}
        self.small_nums_images = {}

        for num in range(len(self.big_nums_coords)):
            self.big_nums_images[f'{num}'] = Image(self.nums_assets,
                                                   self.big_nums_coords[num],
                                                   self.big_nums_position)
            self.small_nums_images[f'{num}'] = Image(self.nums_assets,
                                                     self.small_nums_coords[num],
                                                     self.small_nums_position)

    def generate_score(self, score: int, is_big: bool) -> pygame.sprite.Group:
        score_sprites = pygame.sprite.Group()
        str_score = str(score)
        nums_images, nums_coords, nums_position = self._get_nums_data(is_big)

        first_number = nums_images[str_score[0]]
        pos_x = first_number.rect[0]
        score_sprites.add(first_number)

        self._add_extra_numbers(pos_x, str_score, nums_images,
                                nums_coords, nums_position, score_sprites)

        return score_sprites

    def _get_nums_data(self, is_big: bool) -> Tuple:
        if is_big:
            nums_images = self.big_nums_images
            nums_coords = self.big_nums_coords
            nums_position = self.big_nums_position
        else:
            nums_images = self.small_nums_images
            nums_coords = self.small_nums_coords
            nums_position = self.small_nums_position
        return nums_images, nums_coords, nums_position

    def _add_extra_numbers(self, pos_x: int, score: str, nums_images: Dict,
                           nums_coords: List, nums_position: Tuple,
                           score_sprites: pygame.sprite.Group) -> None:
        if len(score) > 1:
            for i in range(1, len(score)):
                if score[i] == score[0] or score[i] == score[i - 1]:
                    extra_number = Image(self.nums_assets,
                                         nums_coords[i],
                                         nums_position)
                else:
                    extra_number = nums_images[score[i]]
                pos_x += extra_number.rect.width + 2
                extra_number.rect = (pos_x, nums_position[1])
                score_sprites.add(extra_number)
