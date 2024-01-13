import pygame as pg

WIDTH, HEIGHT = 800, 500


# Класс игрока
class Hero(pg.sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(player_image), (x, y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = False
        self.right = False
        self.count = 0
        self.health = 3


class Player(Hero):
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.left = True
            self.right = False
        elif keys[pg.K_a] and self.rect.x < WIDTH - 5:
            self.rect.x += self.speed
            self.left = False
            self.right = True
        else:
            self.left = False
            self.right = False
            self.count = 0

    def animation(self):
        pass

