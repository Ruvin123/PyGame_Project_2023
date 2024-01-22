# Импортируем модули и файлы
import pygame as pg
from settings import *
from tiles import Tile, StaticTile, AnimatedTile, Coin, Enemy
from player import Player
from main import game_over_screen, home_screen, Check, names, cur
from particle import ParticleEffect


# Класс уровня игры
class Level(object):
    def __init__(self, level_data, surface, change_coin, change_health, get_status, index):
        # Основные настройки
        self.display_surface = surface
        self.world_shift = 0
        self.level_id = index
        self.status = get_status

        # Настройки игрока
        player_layout = csv_layout(level_data['player'])
        self.player = pg.sprite.GroupSingle()
        self.end = pg.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # Изменение счетчика монет
        self.change_coin = change_coin

        # Партикл исчезновения врагов
        self.explosion = pg.sprite.Group()

        # Газон
        grass_decor_layout = csv_layout(level_data['grass_decor'])
        self.grass_decor_sprites = self.create_tile_group(grass_decor_layout, 'grass_decor')

        # Монеты
        scores_layout = csv_layout(level_data['scores'])
        self.score_sprites = self.create_tile_group(scores_layout, 'scores')

        # Деревья
        trees_layout = csv_layout(level_data['trees'])
        self.trees_sprites = self.create_tile_group(trees_layout, 'trees')

        # Верхний слой деревьев
        trees_top_layout = csv_layout(level_data['trees_top'])
        self.trees_top_sprites = self.create_tile_group(trees_top_layout, 'trees_top')

        # Враги
        enemies_layout = csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        # Невидимое ограничение врагов на уровне
        constraints_layout = csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # Блоки
        block_layout = csv_layout(level_data['blocks'])
        self.block_sprites = self.create_tile_group(block_layout, 'blocks')

        # Вода
        self.water = Water(HEIGHT - 18)
        # Задний фон
        if self.level_id == 1:
            self.background = Background()
        elif self.level_id == 2:
            self.background = Background_1()
        elif self.level_id == 3:
            self.background = Background_2()

    # Функция, которая создает группы тайлов по указанным выше значением из карты уровня
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
                                       'sprites/enemies/enemy_sprites')

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    # Переворот врагов, если они долши до конца их области передвижения
    def enemy_reverse(self):
        for enemy in self.enemies_sprites.sprites():
            if pg.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()

    # Настройки игрока (Место появления и место выхода)
    def player_setup(self, layout, change_health):
        for row_id, row in enumerate(layout):
            for col_id, val in enumerate(row):
                x, y = col_id * tile_size, row_id * tile_size
                if val == '0':
                    sprite = Player((x, y), change_health)
                    self.player.add(sprite)

                if val == '1':
                    door_surface = pg.image.load('sprites/exit/door.png')
                    sprite = StaticTile(tile_size, x, y, door_surface)
                    self.end.add(sprite)

    # Камера, которая следует за игроком на уровне
    def camera_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 3
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:
            self.world_shift = -3
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3

    # Столкновение с блоками по оси Ох
    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.block_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    # Столкновение с блоками по оси Оу
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

    # Столкновение с врагами
    def check_enemy_collisions(self):
        enemy_collisions = pg.sprite.spritecollide(self.player.sprite, self.enemies_sprites, 0)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -5
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion.add(explosion_sprite)
                    enemy_beat = pg.mixer.Sound('sounds/enemy_destroy.mp3')
                    enemy_beat.play()
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    # Если игрок выйграл, то он переходит на экран выбора другого уровня
    def win(self):
        if pg.sprite.spritecollide(self.player.sprite, self.end, 0):
            win = pg.mixer.Sound('sounds/end.mp3')
            win.play()
            home_screen()

    # Если игрок проиграл (Упал в воду или потратил все здоровье)
    # он может переиграть уровень, выйти в меню или закрыть игру
    def death(self):
        if self.player.sprite.rect.top > HEIGHT or not self.status():
            death = pg.mixer.Sound('sounds/death.mp3')
            death.play()
            game_over_screen(self.level_id)


    # Подбор монет на уровне
    def collide_coin(self):
        collided_coins = pg.sprite.spritecollide(self.player.sprite, self.score_sprites, 1)
        if collided_coins:
            for coin in collided_coins:
                coin_grab = pg.mixer.Sound('sounds/coin_grab.mp3')
                coin_grab.play()
                self.change_coin(1)

        if Check:
            cur.execute(f"""INSERT INTO score (name, score) VALUES ('{names}', {coin});""")

    # Отображение всех спрайтов на экране
    def run(self):
        self.background.draw(self.display_surface)
        # Отрисовка объектов на карте
        self.grass_decor_sprites.draw(self.display_surface)
        self.score_sprites.draw(self.display_surface)
        self.trees_sprites.draw(self.display_surface)
        self.trees_top_sprites.draw(self.display_surface)
        self.block_sprites.draw(self.display_surface)
        self.enemies_sprites.draw(self.display_surface)

        # Обновление объектов на карте
        self.grass_decor_sprites.update(self.world_shift)
        self.block_sprites.update(self.world_shift)
        self.score_sprites.update(self.world_shift)
        self.trees_sprites.update(self.world_shift)
        self.trees_top_sprites.update(self.world_shift)
        self.enemies_sprites.update(self.world_shift)

        # Границы врагов
        self.constraints_sprites.update(self.world_shift)
        self.explosion.update(self.world_shift)
        self.explosion.draw(self.display_surface)

        # Поворот врагов, когда они дошли границы
        self.enemy_reverse()

        # Уничтожение врага
        self.check_enemy_collisions()

        # Место появления игрока и место его выхода с уровня
        self.end.update(self.world_shift)
        self.end.draw(self.display_surface)

        # Сбор монет
        self.collide_coin()

        # Выйгрыш или проигрыщ
        self.win()
        self.death()

        # Отрисовка воды на экране
        self.water.draw(self.display_surface, self.world_shift)

        # Отображение игрока
        self.player.update()
        self.player.draw(self.display_surface)
        self.camera_x()
        self.horizontal_collision()
        self.vertical_collision()


# Класс заднего фона на уровне
class Background(object):
    def __init__(self):
        self.background = pg.image.load('levels/level_data/backgrounds/background_level_1.png').convert()

        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))

    # Отрисовка заднего фона на экран
    def draw(self, surface):
        surface.blit(self.background, (0, 0))


class Background_1(object):
    def __init__(self):
        self.background = pg.image.load('levels/level_data/backgrounds/background_level_2.png').convert()

        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))

    # Отрисовка заднего фона на экран
    def draw(self, surface):
        surface.blit(self.background, (0, 0))


class Background_2(object):
    def __init__(self):
        self.background = pg.image.load('levels/level_data/backgrounds/background_level_3.png').convert()

        self.background = pg.transform.scale(self.background, (WIDTH, HEIGHT))

    # Отрисовка заднего фона на экран
    def draw(self, surface):
        surface.blit(self.background, (0, 0))


# Класс воды на уровне
class Water(object):
    def __init__(self, top):
        # Основные насторйки
        water_start = -WIDTH // 2
        water_tile_width = 18
        tile_x_amount = int(((number_tile_x * 18) + WIDTH) / water_tile_width)
        self.water_sprites = pg.sprite.Group()

        for tile in range(tile_x_amount):
            x, y = tile * water_tile_width + water_start, top
            sprite = AnimatedTile(18, x, y, 'sprites/water')
            self.water_sprites.add(sprite)

    # Отрисовка воды на экран
    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)
