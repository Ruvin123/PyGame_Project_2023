# Импортируем модули
from os import walk
import pygame as pg
from csv import reader

# Скелеты и базовые настроики уровней
level_map_1 = {
    'blocks': 'levels/level_1/level_1_blocks.csv',
    'constraints': 'levels/level_1/level_1_constraints.csv',
    'enemies': 'levels/level_1/level_1_enemies.csv',
    'grass_decor': 'levels/level_1/level_1_grass_decor.csv',
    'player': 'levels/level_1/level_1_player.csv',
    'scores': 'levels/level_1/level_1_scores.csv',
    'trees': 'levels/level_1/level_1_trees.csv',
    'trees_top': 'levels/level_1/level_1_trees_top.csv'
}
number_tile_y, number_tile_x = 19, 79
tile_size = 18
enemy_size = 24
WIDTH, HEIGHT = 800, number_tile_y * tile_size

def add_folder(path):
    screen_list = []

    for _, _, image in walk(path):
        for img in image:
            full_path = path + '/' + img
            img_screen = pg.image.load(full_path)
            screen_list.append(img_screen)

    return screen_list


def csv_layout(path):
    level_map = []

    with open(path, 'r', encoding='utf-8') as map:
        level = reader(map, delimiter=',')
        for row in level:
            level_map.append(list(row))

    return level_map


def cut_graphics(path):
    surface = pg.image.load(path)
    tile_num_x, tile_num_y = int(surface.get_size()[0] / tile_size), int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x, y = col * tile_size, row * tile_size
            new_surf = pg.Surface((tile_size, tile_size))
            new_surf.blit(surface, (0, 0), pg.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles


def import_folder(path='sprites/score'):
    surface_list = []

    for _, __, image_files in walk('sprites/score'):
        for image_ in image_files:
            full_path = path + '/' + image_
            image_surf = pg.image.load('sprites/score/sprite_score.png').convert_alpha()
            surface_list.append(image_surf)