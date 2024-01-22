# Импортируем модули
import pygame as pg
from settings import add_folder


# Класс игрока
class Player(pg.sprite.Sprite):
    # Основные настройки персонажа
    def __init__(self, pos):
        super().__init__()
        self.player_assets()
        self.frame_id = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_id]
        self.rect = self.image.get_rect(topleft=pos)

        # Движение игрока
        self.direction = pg.math.Vector2(0, 0)  # Вектор перемещения персонажа
        self.speed = 3  # Скорость
        self.gravity = 0.3  # Гравитация
        self.jump_speed = -5 # Скорость прыжка

        self.status = 'idle'
        self.left = True
        self.on_ground = True
        self.on_ceil = False

    def player_assets(self):
        player_path = 'sprites/player/'

        self.animations = {
            'idle': [],
            'run': [],
            'jump': [],
            'fall': []
        }

        for animation in self.animations.keys():
            files_path = player_path + animation
            self.animations[animation] = add_folder(files_path)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_id += self.animation_speed
        if self.frame_id >= len(animation):
            self.frame_id = 0

        image = animation[int(self.frame_id)]

        if self.left:
            self.image = image
        else:
            mirror_image = pg.transform.flip(image, True, False)
            self.image = mirror_image

    # Управление персонажем
    def get_keys(self):
        # Получение нажатой в данный момент кнопки
        keys = pg.key.get_pressed()

        # Перемещение
        if keys[pg.K_d]:
            self.direction.x = 1
            self.left = False
        elif keys[pg.K_a]:
            self.direction.x = -1
            self.left = True
        else:
            self.direction.x = 0

        # Прыжок
        if keys[pg.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # Функция гравитации
    def gravity_func(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # Функция прыжка
    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_speed
        else:
            self.on_ground = True


    # Обновление положения персонажа в пространстве
    def update(self):
        self.get_keys()
        self.get_status()
        self.animate()
