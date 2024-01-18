# Импортируем модули
import pygame as pg


# Класс блоков (Тайлов)
class Tile(pg.sprite.Sprite):
    # Основные настройки блоков
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    # Обновление положения блоков на экране
    def update(self, x_shift):
        self.rect.x += x_shift
