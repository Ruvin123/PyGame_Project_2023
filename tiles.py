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
        self.frames = import_folder('levels')
