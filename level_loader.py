# Импортирует модули и функции из других файлов
import pygame as pg
import sys
from settings import *
from level import Level


# Уровень №1
def level_1():
    # Основные настройки уровня
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    FPS = 60

    # Загрузка уровня на экран
    level = Level(level_map_1, screen)

    # Основной цикл игры
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        level.run()
        screen.fill('black')
        pg.display.update()
        clock.tick(FPS)


# Уровень 2
def level_2():
    pass


# Уровень 3
def level_3():
    pass
