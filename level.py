# Импортирует модули и функции из других файлов
import pygame as pg
from Tiles import Tile
from settings import *
from player import Player


class Level(object):
    # Настройки уровня
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.level_loader(level_data)
        self.world_shift = 0  # Смещение экрана (Камера)

    # Функция, которая переделывает текстовую заготовку уровня в картинку
    def level_loader(self, layout):
        self.tiles = pg.sprite.Group()
        self.player = pg.sprite.GroupSingle()

        # Перерисовка символов в блоки (Картинки) на экран
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                # Координаты определенного элемента
                x, y = col_index * tile_size, row_index * tile_size

                # X -> tile
                # P -> player
                # continue...
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    # Функция передвижения камеры по оси Ox
    def camera_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # Установили диапазон при котором камеру будет оставать статичной по оси Ox (установлены скорость и смещение)
        if player_x < 200 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > 600 and direction_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    # Функция столкновения модельки персонажа  объектами по оси Ox
    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # Проверка на пересечение спрайта блока со спрайтом игрока по оси Ох
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_collision(self):
        player = self.player.sprite
        player.gravity_func()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def run(self):
        # Блоки уровня
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.camera_x()
        # Игрок
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_collision()
        self.vertical_collision()
