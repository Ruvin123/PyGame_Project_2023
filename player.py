import pygame as pg

WIDTH, HEIGHT = 800, 500
JUMP_POWER = 5
GRAVITY = 0.5

move_right = []
move_left = []


# Класс игрока
class Hero(pg.sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(player_image), (x, y))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
        self.left = False
        self.right = False
        self.count = 0
        self.health = 3
        self.on_ground = False
        self.x_vel = 0
        self.y_vel = 0


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
        elif keys[pg.K_SPACE] and self.rect.y < HEIGHT - 5:
            pass
        else:
            self.left = False
            self.right = False
            self.count = 0

    def animation(self):
        pass

