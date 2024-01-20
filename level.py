import pygame as pg
from settings import *
from tiles import Tile, StaticTile, AnimatedTile


class Level(object):
    def __init__(self, level_data, surface):
        self.display_surface = surface

        block_layout = csv_layout(level_data['blocks'])
        self.block_sprites = self.create_tile_group(block_layout, 'blocks')

        grass_decor_layout = csv_layout(level_data['grass_decor'])
        self.grass_decor_sprites = self.create_tile_group(grass_decor_layout, 'grass_decor')

        scores_layout = csv_layout(level_data['scores'])
        self.score_sprites = self.create_tile_group(scores_layout, 'scores')

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
                        sprite = AnimatedTile(tile_size, x, y, 'sprites/score/sprite_score.png') # Добавить спрайты монет

                    sprite_group.add(sprite)

        return sprite_group

    def run(self):
        self.block_sprites.draw(self.display_surface)
        self.grass_decor_sprites.draw(self.display_surface)
        self.score_sprites.draw(self.display_surface)

        self.grass_decor_sprites.update(-1)
        self.block_sprites.update(-1)
        self.score_sprites.update(-1)

