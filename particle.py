import pygame as pg
from settings import cut_graphics


class ParticleEffect(pg.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_id = 0
        self.animation_speed = 0.25
        if type == 'explosion':
            self.frames = cut_graphics('sprites/enemies/smoke_sprites/smoke_sprite.png')
        self.image = self.frames[self.frame_id]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_id += self.animation_speed
        if self.frame_id >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_id)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
