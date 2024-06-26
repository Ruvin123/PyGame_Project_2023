# Импортирование модули
import pygame as pg
import csv
from main import cur, connection


# Класс интерфейса уровня
class UI(object):
    def __init__(self, surface):
        # экран
        self.display = surface

        # здоровье
        self.health_bar = pg.image.load('sprites/health/health_3.png')

        # коины
        self.coin = pg.image.load('sprites/coin/coin.png')
        self.coin_rect = self.coin.get_rect(topleft=(20, 28))

        # текст
        self.font = pg.font.SysFont('comicsansms', 18)

    # Отображение и подсчет здоровья на экране
    def show_health(self, current, full):
        self.display.blit(self.health_bar, (20, 10))
        if current == 2:
            self.health_bar = pg.image.load('sprites/health/health_2.png')
            self.display.blit(self.health_bar, (20, 10))
        elif current == 1:
            self.health_bar = pg.image.load('sprites/health/health_1.png')
            self.display.blit(self.health_bar, (20, 10))

    # Отображение монет на экране
    def show_coins(self, amount):
        self.display.blit(self.coin, self.coin_rect)
        coin_amount = self.font.render(str(amount), False, '#ffffff')
        coin_amount_rect = coin_amount.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display.blit(coin_amount, coin_amount_rect)
        self.amount = amount

        with open('database/base.txt', 'a', encoding='utf-8') as r_file:
            file_writer = csv.writer(r_file)
            file_writer.writerow(str(self.amount))




