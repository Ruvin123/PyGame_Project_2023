# Импортируем модули
import sys
import pygame as pg
import os

# Основные настройки
pg.init()
FPS = 60
size = WIDTH, HEIGHT = 800, 500
# Экран
screen = pg.display.set_mode(size)
pg.display.set_caption('Demo Game')  # Название нужно будет поменять
# Время
clock = pg.time.Clock()


# Функция завершения программы
def terminate():
    pg.quit()
    sys.exit()


# Функция по загрузке спрайтов
def load_image(file_name, color_key=None):
    file_name = 'data/' + file_name
    if not os.path.isfile(file_name):
        print(f"Файл с изображением '{file_name}' не найден")
        sys.exit()
    image = pg.image.load(file_name)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# Функция загрузки уровня
def load_level(file_name):
    file_name = "data/" + file_name
    with open(file_name, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Класс анимированной кнопки
class ImageButton(object):
    def __init__(self, x, y, width, height, image_name, hover_image_path=None, sound_path=None):
        # Параметры кнопки
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Картинка кнопки
        self.image = pg.transform.scale(load_image(image_name), (width, height))
        self.hover_image = self.image

        # Картинка задействованной кнопки
        if hover_image_path:
            self.hover_image = pg.transform.scale(load_image(hover_image_path), (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Звук кнопки
        self.sound = None
        if sound_path:
            self.sound = pg.mixer.Sound(sound_path)

        self.is_hovered = False

    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            if self.sound:
                self.sound.play()
            pg.event.post(pg.event.Event(pg.USEREVENT, button=self))


# Кнопки главного меню
play_button = ImageButton(25, 150, 200, 125, 'Play.png', 'Play_hover.png')
score_button = ImageButton(25, 260, 150, 100, 'Score.png', 'Score_hover.png')
exit_button = ImageButton(25, 350, 150, 100, 'Exit.png', 'Exit_hover.png')


# Начальный экран
def home_screen():
    # Фон главного меню
    backround = pg.transform.scale(load_image('Back.png'), (WIDTH, HEIGHT))
    screen.blit(backround, (0, 0))


# Класс игрока
class Player(object):
    pass


# Класс врагов
class Enemy(object):
    pass


# Старт программы
if __name__ == '__main__':

    running = True

    # Запуск начального экрана
    home_screen()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                terminate()

            # Кнопка Exit
            if event.type == pg.USEREVENT and event.button == exit_button:
                running = False
                terminate()

            play_button.handle_event(event)
            score_button.handle_event(event)
            exit_button.handle_event(event)

        # Отрисовка кнопок на главном экране + Датчик пересечения курсора с кнопкой
        play_button.draw(screen)
        play_button.check_hover(pg.mouse.get_pos())
        score_button.draw(screen)
        score_button.check_hover(pg.mouse.get_pos())
        exit_button.draw(screen)
        exit_button.check_hover(pg.mouse.get_pos())
        # Отрисовка дисплея
        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
