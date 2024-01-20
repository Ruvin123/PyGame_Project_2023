# Импортируем модули
import pygame as pg
from settings import *


# Класс блоков (Тайлов)
class Tile(pg.sprite.Sprite):
    # Основные настройки блоков
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pg.Surface((size, size))

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder('\sprites\score')

        def animate(self):
            self.frame_index += 0.15
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.imag = self.frames[int(self.frame_index)]

        def update(self, shift):
            self.animate()
            self.rect.x += shift


class Coin(AnimatedTile):
    def __init__(self, size, x, y, path='\sprites\score'):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
