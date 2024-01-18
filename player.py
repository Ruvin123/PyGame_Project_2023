# Импортируем модули
import pygame as pg


# Класс игрока
class Player(pg.sprite.Sprite):
    # Основные настройки персонажа
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((24, 24))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # Движение игрока
        self.direction = pg.math.Vector2(0, 0)  # Вектор перемещения персонажа
        self.speed = 5  # Скорость
        self.gravity = 0.5  # Гравитация
        self.jump_speed = -8  # Скорость прыжка

    def player_assets(self):
        player_path = 'player_sprites/player'

        self.animations = {
            'idle': [],
            'run': [],
            'jump': [],
            'fall': []
        }

        for animation in self.animations.keys():
            files_path = player_path + animation
            self.animations[animation] = None  # import_folder(files_path)

    # Управление персонажем
    def get_keys(self):
        # Получение нажатой в данный момент кнопки
        keys = pg.key.get_pressed()

        # Перемещение
        if keys[pg.K_d]:
            self.direction.x = 1
        elif keys[pg.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # Прыжок
        if keys[pg.K_SPACE]:
            self.jump()

    # Функция гравитации
    def gravity_func(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # Функция прыжка
    def jump(self):
        self.direction.y = self.jump_speed

    # Обновление положения персонажа в пространстве
    def update(self):
        self.get_keys()
