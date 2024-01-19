# Импортируем модули
from os import walk
import pygame as pg

# Скелеты и базовые настроики уровней
level_map_1 = [
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                             ',
    '                                      XXXXXXX',
    '                  XXXXX                      ',
    '                              XXXXX          ',
    '  P       XXXXXX            XXXXXXXX         ',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]
tile_size = 18
WIDTH, HEIGHT = 800, 600


def add_folder(path):
    screen_list = []

    for _, _, image in walk(path):
        for img in image:
            full_path = path + '/' + img
            img_screen = pg.image.load(full_path)
            screen_list.append(img_screen)

    return screen_list
