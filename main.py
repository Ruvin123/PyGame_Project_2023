# Импортируем модули
import sys
import pygame as pg
import os
import level_loader
import sqlite3

# Основные настройки
pg.init()
FPS = 60
size = WIDTH, HEIGHT = 800, 500
# Экран
screen = pg.display.set_mode(size)
pg.display.set_caption('Fantastic Islands')

connection = sqlite3.connect('database/pg.db')

cur = connection.cursor()

font = pg.font.SysFont('comicsansms', 20)
record = cur.execute('''SELECT name, score FROM score''')

RED = (250, 0, 0)

records = {}

for name, score in record:
    records[name] = score


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
# Фон экрана смерти
gameoverscreen = pg.transform.scale(load_image('gameover.jpg'), (WIDTH, HEIGHT))
# Фон экрана рекордов
recordscreen = pg.transform.scale(load_image('records.jpg'), (WIDTH, HEIGHT))


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


# Экран проигрыша
def game_over_screen():
    running = True

    exit_button = ImageButton(20, 20, 150, 100, 'Exit_game_over.png', 'Exit_game_over.png', 'sounds/button.mp3')
    restart_button = ImageButton(780, 480, 150, 100, 'Reset.png', 'Reset_hover.png', 'sounds/button.mp3')
    main_menu_button = ImageButton(390, 240, 150, 100, 'Menu.png', 'Menu_hover.png', 'sounds/button.mp3')
    while running:
        screen.fill((0, 0, 0))
        screen.blit(gameoverscreen, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                terminate()

            if event.button == exit_button:
                running = False
                terminate()

            exit_button.handle_event(event)

            if event.button == restart_button:
                select_level_screen()

            if event.button == main_menu_button:
                home_screen()

        exit_button.draw(screen)
        exit_button.check_hover(pg.mouse.get_pos())
        # Отрисовка дисплея
        pg.display.flip()


# Экран рекордов
# Доработать
def score_screen():
    running = True

    record = cur.execute('''SELECT name, score FROM score''')

    records_ = {}

    for nam, scor in record:
        records_[nam] = scor

    records_ = sorted(records_.items(), key=lambda x: x[1], reverse=True)

    for nam, scor in records_:
        records[nam] = scor


    back_button = ImageButton(640, 400, 150, 100, 'Backrec.png', 'Backrec_hover.png', 'sounds/button.mp3')

    a = 50

    follow = None


    while running:
        # Фон главного меню
        screen.fill((0, 0, 0))
        screen.blit(recordscreen, (0, 0))

        for i in records.keys():
            follow = font.render(f'{i} {records[i]}', 1, "#ffffff")
            screen.blit(follow, (WIDTH / 2 - 90, a))
            a += 25
        a = 100

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
        pg.display.update()


def audio_screen():
    running = True

    click = pg.mixer.Sound('sounds/button.mp3')
    volume = 1
    play = True
    back_button = ImageButton(640, 400, 150, 100, 'Back.png', 'Back_hover.png', 'sounds/button.mp3')
    audio_pad = ImageButton(125, 20, 500, 400, 'Vol_pad.png')

    while running:
        # Фон
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

            # Стелочка влево -> понижение громкости музыки
            if event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_LEFT]:
                    volume -= 0.1
                    pg.mixer_music.set_volume(volume)
                    click.play()

            # Стрелочка вправо -> повышение громкости музыки
            if event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_RIGHT]:
                    volume += 0.1
                    pg.mixer_music.set_volume(volume)
                    click.play()

            # Стрелочка вниз -> Воспроизвести / Пауза
            if event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_DOWN]:
                    if play:
                        pg.mixer_music.pause()
                        play = False
                        click.play()
                    else:
                        pg.mixer_music.unpause()
                        play = True
                        click.play()

            # Кнопка back
            if event.type == pg.USEREVENT and event.button == back_button:
                running = False

            back_button.handle_event(event)
        back_button.check_hover(pg.mouse.get_pos())

        back_button.draw(screen)
        audio_pad.draw(screen)
        # Отрисовка дисплея
        pg.display.flip()


# Экран новой игры
def select_level_screen():
    running = True

    back_button = ImageButton(640, 400, 150, 100, 'Back.png', 'Back_hover.png', 'sounds/button.mp3')
    level_1_button = ImageButton(10, 80, 300, 300, 'Level_1.png', 'Level_1_hover.png',
                                 'sounds/button_play.mp3')
    level_2_button = ImageButton(250, 80, 300, 300, 'Level_2.png', 'Level_2_hover.png',
                                 'sounds/button_play.mp3')
    level_3_button = ImageButton(500, 80, 300, 300, 'Level_3.png', 'Level_3_hover.png',
                                 'sounds/button_play.mp3')

    while running:
        # Фон главного меню
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                terminate()

            # Кнопка back
            if event.type == pg.USEREVENT and event.button == back_button:
                running = False

            # Первый уровень
            if event.type == pg.USEREVENT and event.button == level_1_button:
                pg.mixer.music.stop()
                level_loader.level_1()

            # Второй уровень
            if event.type == pg.USEREVENT and event.button == level_2_button:
                pg.mixer.music.stop()

            # Третий уровень
            if event.type == pg.USEREVENT and event.button == level_3_button:
                pg.mixer.music.stop()

            back_button.handle_event(event)
            level_1_button.handle_event(event)
            level_2_button.handle_event(event)
            level_3_button.handle_event(event)

        back_button.draw(screen)
        back_button.check_hover(pg.mouse.get_pos())
        level_1_button.draw(screen)
        level_1_button.check_hover(pg.mouse.get_pos())
        level_2_button.draw(screen)
        level_2_button.check_hover(pg.mouse.get_pos())
        level_3_button.draw(screen)
        level_3_button.check_hover(pg.mouse.get_pos())
        # Отрисовка дисплея
        pg.display.flip()


# Регистрация
# Доработать
def register():
    running = True

    register_button = ImageButton(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 32, 'registr.png', 'registr_hover.png',
                                  'sounds/button.mp3')
    back_button = ImageButton(640, 400, 150, 100, 'Back.png', 'Back_hover.png', 'sounds/button.mp3')

    base_font = pg.font.Font(None, 32)
    user_text = ''
    input_rect = pg.Rect(WIDTH // 2 - 50, HEIGHT // 2, 300, 32)

    color_active = pg.Color('lightskyblue3')
    color_passive = pg.Color(250, 50, 162, 100)
    color = color_passive

    active = False

    while running:
        # Фон
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_ESCAPE]:
                    running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

            # Кнопка back
            if event.type == pg.USEREVENT and event.button == back_button:
                running = False

            # Кнопка registr
            if event.type == pg.USEREVENT and event.button == register_button:
                cur.execute(f"""INSERT INTO score (name, score) VALUES ('{user_text}', 0);""")
                connection.commit()

            if active:
                color = color_active
            else:
                color = color_passive
            register_button.handle_event(event)
            back_button.handle_event(event)

        back_button.check_hover(pg.mouse.get_pos())
        back_button.draw(screen)
        register_button.draw(screen)
        register_button.check_hover(pg.mouse.get_pos())

        pg.draw.rect(screen, color, input_rect, 3)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        pg.display.flip()


# Начальный экран
def home_screen():
    # Кнопки главного меню
    play_button = ImageButton(25, 150, 200, 125, 'Play.png', 'Play_hover.png', 'sounds/button.mp3')
    score_button = ImageButton(25, 260, 150, 100, 'Score.png', 'Score_hover.png', 'sounds/button.mp3')
    exit_button = ImageButton(25, 350, 150, 100, 'Exit.png', 'Exit_hover.png', 'sounds/button.mp3')
    audio_button = ImageButton(690, 450, 100, 50, 'Audio.png', 'Audio_hover.png', 'sounds/button.mp3')
    register_button = ImageButton(700, 200, 100, 50, 'registr.png', 'registr.png', 'sounds/button.mp3')

    running = True

    # Музыка игры
    pg.mixer.music.load('sounds/main_menu.mp3')
    pg.mixer_music.play()

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

            # Кнопка Score
            if event.type == pg.USEREVENT and event.button == score_button:
                score_screen()

            # Кнопка Audio
            if event.type == pg.USEREVENT and event.button == audio_button:
                audio_screen()

            # Кнопка PLay
            if event.type == pg.USEREVENT and event.button == play_button:
                select_level_screen()

            # Кнопка Register
            if event.type == pg.USEREVENT and event.button == register_button:
                register()

            play_button.handle_event(event)
            audio_button.handle_event(event)
            score_button.handle_event(event)
            exit_button.handle_event(event)
            register_button.handle_event(event)

        # Отрисовка кнопок на главном экране + Датчик пересечения курсора с кнопкой
        play_button.draw(screen)
        play_button.check_hover(pg.mouse.get_pos())
        register_button.draw(screen)
        register_button.check_hover(pg.mouse.get_pos())
        audio_button.draw(screen)
        audio_button.check_hover(pg.mouse.get_pos())
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
