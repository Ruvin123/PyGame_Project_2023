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


# Фон главного меню
background = pg.transform.scale(load_image('Background.png'), (WIDTH, HEIGHT))


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


# Класс игрока
# Доработать
class Player(object):
    pass


# Класс врагов
# Доработать
class Enemy(object):
    pass


# Экран проигрыша
# добавить кнопки restart, main_menu, exit
def game_over_screen():
    pass


# Экран рекордов
# Добавить кнопки back
# Добавить возможность выхода нажатием кнопки escape
def score_screen():
    pass


# Экран настроек
# Добавить кнопки video
def settings_screen():
    running = True

    back_button = ImageButton(640, 400, 150, 100, 'Back.png', 'Back_hover.png')

    while running:
        # Фон главного меню
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                terminate()

            # Escape
            if event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_ESCAPE]:
                    running = False

            # Кнопка back
            if event.type == pg.USEREVENT and event.button == back_button:
                running = False

            back_button.handle_event(event)

        back_button.draw(screen)
        back_button.check_hover(pg.mouse.get_pos())
        # Отрисовка дисплея
        pg.display.flip()


# Экран новой игры
def new_game_screen():
    pass


# Начальный экран
def home_screen():
    # Кнопки главного меню
    play_button = ImageButton(25, 150, 200, 125, 'Play.png', 'Play_hover.png')
    score_button = ImageButton(25, 260, 150, 100, 'Score.png', 'Score_hover.png')
    exit_button = ImageButton(25, 350, 150, 100, 'Exit.png', 'Exit_hover.png')

    running = True

    while running:
        # Фон главного меню
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                terminate()

            # Кнопка Exit
            if event.type == pg.USEREVENT and event.button == exit_button:
                running = False
                terminate()

            if event.type == pg.USEREVENT and event.button == score_button:
                settings_screen()

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


# Старт программы
if __name__ == '__main__':
    # Запуск начального экрана
    home_screen()
    pg.quit()
