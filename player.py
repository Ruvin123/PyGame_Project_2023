# Импортируем модули
import pygame as pg
from settings import add_folder
from math import sin


# Класс игрока
class Player(pg.sprite.Sprite):
    # Основные настройки персонажа
    def __init__(self, pos, change_health):
        super().__init__()
        # Настройки анимации спрайтов
        self.player_assets()
        self.frame_id = 0
        self.animation_speed = 0.1

        # Начальная картинка игрока на уровне
        self.image = self.animations['idle'][self.frame_id]
        self.rect = self.image.get_rect(topleft=pos)

        # Движение игрока
        self.direction = pg.math.Vector2(0, 0)  # Вектор перемещения персонажа
        self.speed = 3  # Скорость
        self.gravity = 0.3  # Гравитация
        self.jump_speed = -5  # Скорость прыжка

        # Статус игрока
        self.status = 'idle'
        self.left = True
        self.on_ground = True
        self.on_ceil = False

        # Изменение здоровья
        self.change_health = change_health

        # Маркер неуязвимости
        self.invincible = False

        # Время неуязвимости
        self.invincibility_duration = 2300

        # Время удара (По умолчанию 0)
        self.hurt_time = 0

    # Спрайты игрока
    def player_assets(self):
        # Путь до папки со спрайтами игрока
        player_path = 'sprites/player/'

        # Словарь анимации
        self.animations = {
            'idle': [],
            'run': [],
            'jump': [],
            'fall': []
        }

        # Добавление названий спрайта в словарь анимации
        for animation in self.animations.keys():
            files_path = player_path + animation
            self.animations[animation] = add_folder(files_path)

    # Функция анимации спрайтов
    def animate(self):
        animation = self.animations[self.status]

        # Цикл кадров
        self.frame_id += self.animation_speed
        if self.frame_id >= len(animation):
            self.frame_id = 0

        # Отделый кадр из словаря фреймов
        image = animation[int(self.frame_id)]

        # Смена взгляда игрока (Вправо, Влево)
        if self.left:
            self.image = image
        else:
            mirror_image = pg.transform.flip(image, True, False)
            self.image = mirror_image

        # Анимация нанесения урона
        if self.invincible:
            alpha = self.sin_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

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

    # Статус игрока (Покой, Бег, Прыжок, Падение)
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
    # Происходит смещение по направлению вектора по Оу (self.direction.y)
    def gravity_func(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # Функция прыжка
    # Проверка находитьсяли игрок на земле и смещение по вектору по Оу (self.direction.y)
    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_speed
        else:
            self.on_ground = True

    # Подсчет полученного урона (Из текущего здоровья при получении урона вычитаем 1 и активируется защита)
    def get_damage(self):
        if not self.invincible:
            damage = pg.mixer.Sound('sounds/damage_sound.mp3')
            damage.play()
            self.change_health(-1)
            self.invincible = True
            self.hurt_time = pg.time.get_ticks()

    # Отсчет таймера неуязвимости
    def invincibility_timer(self):
        if self.invincible:
            # Текущее время
            current_time = pg.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False  # Защита выключается по истечению времени

    # Видимость и невидимость игрока после удара (Она движется по синусоиду)
    def sin_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255  # Альфа канал в спрайте
        else:
            return 0  # Альфа канал в спрайте

    # Обновление положения персонажа в пространстве
    def update(self):
        self.get_keys()  # Клавиши
        self.get_status()  # Статус игрока
        self.animate()  # Анимация игрока
        self.invincibility_timer()  # Неуязвимость игрока
