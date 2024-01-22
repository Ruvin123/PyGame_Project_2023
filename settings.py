# Импортируем модули
from os import walk
import pygame as pg
from csv import reader

# Скелеты и базовые настроики уровней
# Карта уровня 1
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
level_map_2 = {
    'blocks': 'levels/level_2/level_2_blocks.csv',
    'constraints': 'levels/level_2/level_2_constraints.csv',
    'enemies': 'levels/level_2/level_2_enemies.csv',
    'grass_decor': 'levels/level_2/level_2_grass_decor.csv',
    'player': 'levels/level_2/level_2_player.csv',
    'scores': 'levels/level_2/level_2_scores.csv',
    'trees': 'levels/level_2/level_2_trees.csv',
    'trees_top': 'levels/level_2/level_2_trees_top.csv'
}
level_map_3 = {
    'blocks': 'levels/level_3/level_3_blocks.csv',
    'constraints': 'levels/level_3/level_3_constraints.csv',
    'enemies': 'levels/level_3/level_3_enemies.csv',
    'grass_decor': 'levels/level_3/level_3_grass_decor.csv',
    'player': 'levels/level_3/level_3_player.csv',
    'scores': 'levels/level_3/level_3_scores.csv',
    'trees': 'levels/level_3/level_3_trees.csv',
    'trees_top': 'levels/level_3/level_3_trees_top.csv'
}
# Основные настройки уровня
number_tile_y, number_tile_x = 27, 79
tile_size = 18
enemy_size = 24
WIDTH, HEIGHT = 800, number_tile_y * tile_size


# Функция, которая фозвращает картинки из заданной папки
def add_folder(path):
    screen_list = []

    for _, _, image in walk(path):
        for img in image:
            full_path = path + '/' + img
            img_screen = pg.image.load(full_path)
            screen_list.append(img_screen)

    return screen_list


# Загрузчик уровней
# Читает CSV формат и возвращает его построчно в формате списка
def csv_layout(path):
    level_map = []

    with open(path, 'r', encoding='utf-8') as map:
        level = reader(map, delimiter=',')
        for row in level:
            level_map.append(list(row))

    return level_map


# Вырезка тайлов
def cut_graphics(path):
    # Загружаем тайлсет
    surface = pg.image.load(path)
    # Находим по Ох и по Оу сколько тайлов располагается
    tile_num_x, tile_num_y = int(surface.get_size()[0] / tile_size), int(surface.get_size()[1] / tile_size)

    # Список вырезанных тайлов
    cut_tiles = []
    # Цикл, который вырезает и добавляет тайлы в список
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x, y = col * tile_size, row * tile_size
            new_surf = pg.Surface((tile_size, tile_size), flags=pg.SRCALPHA)
            new_surf.blit(surface, (0, 0), pg.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles
