# Импортируем модули
import pygame as pg
from settings import *
from random import randint


# Класс блоков (Тайлов)
class Tile(pg.sprite.Sprite):
    # Основные настройки блоков
    def init(self, size, x, y):
        super().__init__()
        self.image = pg.Surface((size, size))

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift


class StaticTile(Tile):
    def init(self, size, x, y, surface):
        super().init(size, x, y)
        self.image = surface


class AnimatedTile(Tile):
    def init(self, size, x, y, path):
        super().init(size, x, y)
        self.frames = add_folder(path)
        self.frame_id = 0

    def animate(self):
        self.frame_id += 0.15
        if self.frame_id >= len(self.frames):
            self.frame_id = 0
        self.image = self.frames[int(self.frame_id)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTile):
    def init(self, size, x, y, path):
        super().init(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Enemy(AnimatedTile):
    def init(self, size, x, y, path):
        super().init(size, x, y, path)
        x, y = x, y - 6
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = randint(1, 2)
        self.left = True

    def move(self):
        self.rect.x += self.speed

    def revers_sprite(self):
        if self.speed > 0:
            self.image = pg.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.move()
        self.animate()
        self.revers_sprite()
        self.rect.x += shift
