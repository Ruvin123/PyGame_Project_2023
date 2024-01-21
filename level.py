import pygame as pg
from settings import *
from tiles import Tile, StaticTile, AnimatedTile, Coin, Enemy
from player import Player


class Level(object):
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0

        player_layout = csv_layout(level_data['player'])
        self.player = pg.sprite.GroupSingle()
        self.end = pg.sprite.GroupSingle()
        self.player_setup(player_layout)

        grass_decor_layout = csv_layout(level_data['grass_decor'])
        self.grass_decor_sprites = self.create_tile_group(grass_decor_layout, 'grass_decor')

        scores_layout = csv_layout(level_data['scores'])
        self.score_sprites = self.create_tile_group(scores_layout, 'scores')

        trees_layout = csv_layout(level_data['trees'])
        self.trees_sprites = self.create_tile_group(trees_layout, 'trees')

        trees_top_layout = csv_layout(level_data['trees_top'])
        self.trees_top_sprites = self.create_tile_group(trees_top_layout, 'trees_top')

        enemies_layout = csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        constraints_layout = csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

        block_layout = csv_layout(level_data['blocks'])
        self.block_sprites = self.create_tile_group(block_layout, 'blocks')

        self.water = Water(HEIGHT - 18)

    def create_tile_group(self, layout, type):
        sprite_group = pg.sprite.Group()

        for row_id, row in enumerate(layout):
            for col_id, val in enumerate(row):
                if val != '-1':
                    x, y = col_id * tile_size, row_id * tile_size

                    if type == 'blocks':
                        blocks_tile_list = cut_graphics('levels/level_data/blocks/tilemap_packed.png')
                        tile_surface = blocks_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass_decor':
                        grass_decor_tile_list = cut_graphics('levels/level_data/blocks/tilemap_packed.png')
                        tile_surface = grass_decor_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'scores':
                        sprite = Coin(tile_size, x, y,
                                      'sprites/score')

                    if type == 'trees':
                        trees_tile_list = cut_graphics('levels/level_data/blocks/tilemap_packed.png')
                        tile_surface = trees_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'trees_top':
                        trees_top_tile_list = cut_graphics('levels/level_data/blocks/tilemap_packed.png')
                        tile_surface = trees_top_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'enemies':
                        sprite = Enemy(enemy_size, x, y,
                                       'sprites/enemies')

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_reverse(self):
        for enemy in self.enemies_sprites.sprites():
            if pg.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()

    def player_setup(self, layout):
        for row_id, row in enumerate(layout):
            for col_id, val in enumerate(row):
                x, y = col_id * tile_size, row_id * tile_size
                if val == '0':
                    sprite = Player((x, y))
                    self.player.add(sprite)

                if val == '1':
                    door_surface = pg.image.load('sprites/exit/door.png')
                    sprite = StaticTile(tile_size, x + 1, y, door_surface)
                    self.end.add(sprite)

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.block_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_collision(self):
        player = self.player.sprite
        player.gravity_func()

        for sprite in self.block_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceil = True

            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False

            if player.on_ceil and player.direction.y > 0:
                player.on_ceil = False

    def run(self):
        # Отрисовка объектов на карте
        self.grass_decor_sprites.draw(self.display_surface)
        self.score_sprites.draw(self.display_surface)
        self.enemies_sprites.draw(self.display_surface)
        self.trees_sprites.draw(self.display_surface)
        self.trees_top_sprites.draw(self.display_surface)
        self.block_sprites.draw(self.display_surface)

        # Обновление объектов на карте
        self.grass_decor_sprites.update(self.world_shift)
        self.block_sprites.update(self.world_shift)
        self.score_sprites.update(self.world_shift)
        self.trees_sprites.update(self.world_shift)
        self.trees_top_sprites.update(self.world_shift)
        self.enemies_sprites.update(self.world_shift)

        # Границы врагов
        self.constraints_sprites.update(self.world_shift)
        # Поворот врагов, когда они дошлли границы
        self.enemy_reverse()

        # Место появления игрока и место его выхода с уровня
        self.end.update(self.world_shift)
        self.end.draw(self.display_surface)

        # Отрисовка воды на экране
        self.water.draw(self.display_surface, self.world_shift)

        # Отображение игрока
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_collision()
        self.vertical_collision()


class Water(object):
    def __init__(self, top):
        water_start = -WIDTH // 2
        water_tile_width = 18
        tile_x_amount = int(((number_tile_x * 18) + WIDTH) / water_tile_width)
        self.water_sprites = pg.sprite.Group()

        for tile in range(tile_x_amount):
            x, y = tile * water_tile_width + water_start, top
            sprite = AnimatedTile(18, x, y, 'sprites/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)
