# Импортирует модули и функции из других файлов
import pygame as pg
import sys
from settings import *
from level import Level
from UI import UI

coin = 0


# Класс игры
class Game(object):
    def __init__(self, current_level, surface, level_id):
        global coin
        # Начальные настройки уровня (Здооровье, монеты и статус уровня(идет игра или нет))
        self.health = 3
        self.current_health = 3
        self.coin = 0
        self.status = True

        # Создание Уровня
        self.level = Level(current_level, surface, self.change_coin, self.change_health, self.get_status, level_id)

        # Интерфейс уровня
        self.ui = UI(surface)

    # Изменения счетчика монет
    def change_coin(self, amount):
        self.coin += amount

    # Изменения счетчика здоровья
    def change_health(self, amount):
        self.current_health += amount

    # При 0 здоровья у игрока игра заканчивается
    def get_status(self):
        if self.current_health == 0:
            self.current_health = 3
            self.coin = 0
            self.status = False
        return self.status

    # Отображение уровня и интерфейса на экран
    def run(self):
        self.level.run()
        self.ui.show_health(self.current_health, self.health)
        self.ui.show_coins(self.coin)
        # Функция нужна для отслеживания здоровья
        self.get_status()


# Уровень №1
def level_1():
    # Основные настройки уровня
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    FPS = 60

    # Загрузка уровня на экран
    game = Game(level_map_1, screen, 1)

    # Основной цикл игры
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill('black')
        game.run()
        pg.display.update()
        clock.tick(FPS)


# Уровень 2
def level_2():
    # Основные настройки уровня
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    FPS = 60

    # Загрузка уровня на экран
    game = Game(level_map_2, screen, 2)

    # Основной цикл игры
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill('black')
        game.run()
        pg.display.update()
        clock.tick(FPS)


# Уровень 3
def level_3():
    # Основные настройки уровня
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    FPS = 60

    # Загрузка уровня на экран
    game = Game(level_map_3, screen, 3)

    # Основной цикл игры
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill('black')
        game.run()
        pg.display.update()
        clock.tick(FPS)
