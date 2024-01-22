# Импортируем модули
import pygame as pg
from settings import cut_graphics


# Класс частиц
class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        # Основные настройки
        self.frame_id = 0
        self.animation_speed = 0.25

        # Тип партикла (частиц)
        if type == 'explosion':
            self.frames = cut_graphics('sprites/enemies/smoke_sprites/smoke_sprite.png')

        # Добавляем точку партикла (частицы)
        self.image = self.frames[self.frame_id]
        self.rect = self.image.get_rect(center=pos)

    # Анимация партикла (частиц)
    def animate(self):
        self.frame_id += self.animation_speed
        if self.frame_id >= len(self.frames):
            self.kill()  # Убираем партикл (частицы), если был совершен круг
        else:
            self.image = self.frames[int(self.frame_id)]  # Иначе продолжаем воспроизводить

    # Обновление партикла (частиц) на экране
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
