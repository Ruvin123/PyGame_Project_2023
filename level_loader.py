# Импортирует модули и функции из других файлов
import pygame as pg
import sys
from settings import *
from level import Level
from UI import UI


class Game(object):
    def __init__(self, current_level, surface):
        self.health = 3
        self.cur_health = 3
        self.coin = 0

        self.level = Level(current_level, surface, self.change_coin)

        self.ui = UI(surface)

    def change_coin(self, amount):
        self.coin += amount

    def run(self):
        self.level.run()
        self.ui.show_health(self.cur_health, self.health)
        self.ui.show_coins(self.coin)


# Уровень №1
def level_1():
    # Основные настройки уровня
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    FPS = 60

    # Загрузка уровня на экран
    game = Game(level_map_1, screen)

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
    pass


# Уровень 3
def level_3():
    pass
