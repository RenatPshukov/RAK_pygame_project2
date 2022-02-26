# TODO Импортируем нужные библиотеки
import os
import sqlite3

import pygame
from random import randint, choice
from datetime import datetime

# инициализируем pygame
pygame.init()

# устанавливаем название окну
pygame.display.set_caption('Insanity balls')  # название

# импортируем картинку логотипа из папки data
ICON = pygame.image.load('data\\logo_1.png')
# устанавливаем иконку (логотип)
pygame.display.set_icon(ICON)

# задаём ширину и высоту
SIZE = WIDTH, HEIGHT = 1400, 900
# устанавливаем размер окна
screen = pygame.display.set_mode(SIZE)

# Используется для управления fps
clock = pygame.time.Clock()


# TODO функция загрузки спрайтов
def load_image(name, color_key=None):
    # достаём картинку из папки data
    fullname = os.path.join('data', name)
    try:
        # создаём спрайт убирая задний фон
        image = pygame.image.load(fullname).convert_alpha()
    # в случае отсутствия картинки в папке data выводим ошибку
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    # если есть цветовой ключ то устанавливаем его
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    # иначе убираем задний фон спрайта
    else:
        image = image.convert_alpha()
    # возвращаем спрайт
    return image


RED_BALL, BLUE_BALL, DARKBLUE_BALL, GREEN_BALL, ORANGE_BALL, PINK_BALL, PURPLE_BALL, WHITE_BALL, YELLOW_BALL = \
    [], [], [], [], [], [], [], [], []
# импорт анимации
for num in range(24):
    RED_BALL.append(load_image(f"red_balls\\red{num}.png"))
    BLUE_BALL.append(load_image(f"blue_balls\\blue{num}.png"))
    DARKBLUE_BALL.append(load_image(f"darkblue_balls\\darkblue{num}.png"))
    GREEN_BALL.append(load_image(f"green_balls\\green{num}.png"))
    ORANGE_BALL.append(load_image(f"orange_balls\\orange{num}.png"))
    PINK_BALL.append(load_image(f"pink_balls\\pink{num}.png"))
    PURPLE_BALL.append(load_image(f"purple_balls\\purple{num}.png"))
    WHITE_BALL.append(load_image(f"white_balls\\white{num}.png"))
    YELLOW_BALL.append(load_image(f"yellow_balls\\yellow{num}.png"))
# список со спрайтами шаров
SPRITE_LIST = [RED_BALL, BLUE_BALL, DARKBLUE_BALL, GREEN_BALL, ORANGE_BALL, PINK_BALL, PURPLE_BALL, WHITE_BALL,
               YELLOW_BALL]


# TODO функция вывода текста на экран игры
def print_text(message, x, y, font_color, font_size):
    # устанавливаем шрифт
    font_type = pygame.font.Font('data\\lilita.otf', font_size)
    # создаём строку с текстом
    text = font_type.render(message, True, font_color)
    # отрисовываем текст на координатах x и y
    screen.blit(text, (x, y))


# TODO функция секундомера
def display_time(time_s):
    # импортируем переменные цикла игры и времени для их изменения
    global running
    global time_str
    # устанавливаем шрифт
    font = pygame.font.Font(None, 30)
    # временная строка с десятыми долями секунды
    time_str = str(int(time_s * 10) / 10)
    # строка секундомера
    label = font.render(f"Time : {time_str}", True, 'red')
    # отрисовываем на экране секундомер в координатах (20, 20)
    screen.blit(label, (20, 20))


# TODO функция записи в Базу данных
def writing_to_the_database():
    # импортируем флаг уровней
    global mode
    # Подключение к БД
    con = sqlite3.connect("Insanity balls.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса по условию какой уровень запущен
    if mode == '1':
        cur.execute(f"INSERT INTO History (easy_time) VALUES ('{time_str}');")
    elif mode == '2':
        cur.execute(f"INSERT INTO History (normal_time) VALUES ('{time_str}');")
    elif mode == '3':
        cur.execute(f"INSERT INTO History (hard_time) VALUES ('{time_str}');")
    # коммит
    con.commit()
    # Закрываем БД
    con.close()


# TODO класс шарика
class Ball(pygame.sprite.Sprite):
    # инициализация класса
    def __init__(self, group, radius, x, y):
        # импортируем переменную для подсчёта числа кадров в анимации
        global img_counter
        self.x = x
        self.y = y
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        # импортируем спрайты шаров из папки data, устанавливая им размер radius

        super().__init__(group)
        # выбираем один случайный спрайт из списка
        self.selected_sprite = [pygame.transform.scale(sprite, (radius, radius)) for sprite in choice(SPRITE_LIST)]
        # указываем случайное направления движения и скорость по осям
        self.vx = randint(-13, 13)
        self.vy = randint(-13, 13)
        # если выпало 0, то перезаписываем ещё раз, так же по осям
        while self.vx == 0:
            self.vx = randint(-13, 13)
        while self.vy == 0:
            self.vy = randint(-13, 13)
        # создаём объект шара
        self.rect = pygame.Rect(self.x, self.y, radius, radius)

    # функция взаимодествия (столкновение и рикошет) шаров и границ
    def update(self):
        global img_counter
        # проверка, были ли использованы все спрайты
        if img_counter == 1150:
            img_counter = 0
        # создаём объект шара
        self.image = self.selected_sprite[img_counter // 50]
        # и устанавливаем его на объект шара
        # указываем случайное направления движения и скорость по осям
        self.rect = self.rect.move(self.vx, self.vy)
        # если шар соприкоснулся с горизонтальной границей, то изменяем его направление на противоположное
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        # если шар соприкоснулся с вертикальной границей, то изменяем его направление на противоположное
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        # на один шаг ближе к новому спрайту
        img_counter += 1


# TODO класс игрока(курсора)
class Cursor(pygame.sprite.Sprite):
    # инициализация класса
    def __init__(self, group):
        super().__init__(group)
        # импортируем спрайт курсора из папки data
        self.image = load_image("arrow.png")  # это будет будущий спрайт
        self.rect = self.image.get_rect()
        # скрываем системный курсор
        pygame.mouse.set_visible(False)


# TODO функция показа системного курсора
def mouse_visible():
    pygame.mouse.set_visible(True)


# TODO класс границ
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    # инициализация класса
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        # вертикальная стенка
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        # горизонтальная стенка
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# TODO класс кнопка
class Button:
    def __init__(self, width, height, font):
        # высота
        self.width = width
        # ширина
        self.height = height
        # шрифт
        self.font = font
        # неактивный цвет
        self.inactive_color = (234, 160, 154)
        # активный цвет
        self.active_color = (247, 178, 149)

    # функция отрисовки кнопки
    def draw(self, x, y, message, action=None):
        # переменная с позицией мышки
        mouse = pygame.mouse.get_pos()
        # переменная для проверки было ли нажатие
        click = pygame.mouse.get_pressed()

        # если курсор наведён на кнопку, то устанавливаем активный цвет
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
            ''' если кнопка нажата и действие не None, то проверяем является ли действие выходу из игры
                если да, то выходим из игры, иначе выполняем другое действие. '''
            if click[0] == 1 and action is not None:
                if action == quit:
                    pygame.quit()
                    quit()
                else:
                    action()
        # иначе устанавливаем неактивный цвет
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        # отрисовываем надпись на кнопке
        print_text(message=message, x=x + 10, y=y + 10, font_color=(128, 128, 128), font_size=30)


# TODO функция проверки столкновения
def check_collision(balls):
    # перебираем все шары из группы спрайтов all_sprites
    for ball in balls:
        # если курсор соприкоснулся с центром окружности спрайта возвращаем True
        if cursor.rect.collidepoint(ball.rect.center):
            return True


# TODO функция запроса на повтор, выход в меню или выход из игры
def end_of_game_requests():
    # флаг прекращение
    termination = True
    # цикл, в период которого игрок решает, играть ему снова, выйти в меню или же закрыть игру
    while termination:
        # ожидание закрытия окна:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # нажата клавиша
        keys = pygame.key.get_pressed()
        # если нажат enter, то возвращаем True
        if keys[pygame.K_RETURN]:
            return True
        # если нажат escape то возвращаем False
        if keys[pygame.K_ESCAPE]:
            return False

    # обновляем экран
    pygame.display.update()
    # устанавливаем 15 fps
    clock.tick(15)


# TODO функция меню игры
def show_menu(menu_background):
    # устанавливаем задний фон меню

    # создаём экземпляры кнопок
    lvl1_btn = Button(283, 60, 'data\\lilita.otf')
    lvl2_btn = Button(222, 60, 'data\\lilita.otf')
    lvl3_btn = Button(283, 60, 'data\\lilita.otf')
    quit_btn = Button(95, 60, 'data\\lilita.otf')

    # флаг показа меню
    show = True

    # цикл показа меню, пока show == True
    while show:
        # ожидание закрытия окна:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # отрисовываем задний фон
        screen.blit(menu_background, (0, 0))
        logo_menu = pygame.transform.scale(load_image('menu_logo.png'), (460, 390))
        screen.blit(logo_menu, (450, 50))
        # отрисовываем надпись выбора уровня сложности
        print_text('Choose the difficulty level:', 400, 480, (128, 128, 128), 50)
        # отрисовываем все кнопки
        lvl1_btn.draw(100, 590, 'BALLS TO THE WALL', level1)
        lvl2_btn.draw(575, 590, 'BALLS OF STEEL', level2)
        lvl3_btn.draw(1000, 590, 'KICK IN THE BALLS', level3)
        quit_btn.draw(640, 750, 'QUIT', quit)
        # обновляем экран
        pygame.display.update()
        # вызываем функцию показа системного курсора после завершения игры
        mouse_visible()
        # устанавливаем 60 fps
        clock.tick(60)


# TODO функция финального окна
def game_over(game_over_background):
    # устанавливаем задний фон конца игры

    # флаг показа меню
    global record
    show = True

    # Подключение к БД
    con = sqlite3.connect("Insanity balls.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса
    if mode == '1':
        record_b = cur.execute(f"SELECT MAX(easy_time) FROM History").fetchall()
    elif mode == '2':
        record_b = cur.execute(f"SELECT MAX(normal_time) FROM History").fetchall()
    elif mode == '3':
        record_b = cur.execute(f"SELECT MAX(hard_time) FROM History").fetchall()
    else:
        record_b = ''
    for elem in record_b:
        record = elem
    # коммит
    con.commit()
    # Закрываем БД
    con.close()

    # цикл показа меню, пока show == True
    while show:
        # ожидание закрытия окна:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # нажата клавиша
        keys = pygame.key.get_pressed()
        # если нажат enter, то возвращаем True
        if keys[pygame.K_RETURN]:
            return True
        # если нажат escape то возвращаем False
        if keys[pygame.K_ESCAPE]:
            return False

        # отрисовываем задний фон
        screen.blit(game_over_background, (0, 0))
        # отрисовываем надпись конца игры и результат с рекордом
        print_text('GAME OVER', 430, 100, (0, 0, 0), 100)
        print_text(f'Your result: {time_str}', 500, 300, (0, 0, 0), 60)
        print_text(f'Your record: {record[0]}', 505, 400, (0, 0, 0), 55)
        print_text('Press Enter to restart', 450, 550, (0, 0, 0), 55)
        print_text('Press Escape to return to the menu', 320, 650, (0, 0, 0), 55)
        # обновляем экран
        pygame.display.update()
        # вызываем функцию показа системного курсора после завершения игры
        mouse_visible()
        # устанавливаем 60 fps
        clock.tick(60)


# TODO отсчёт перед началом боя
def time_report(bg):
    # задаём задний фон

    counter, text = 3, '3'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    run = True
    # цикл показа меню, пока run == True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1
                if counter > 0:
                    text = str(counter).rjust(3)
                else:
                    run = False
            # ожидание закрытия окна:
            if event.type == pygame.QUIT:
                run = False

        # отрисовываем задний фон
        screen.blit(bg, (0, 0))
        # отрисовываем отчёт времени
        print_text(text, 500, 250, (0, 0, 0), 300)
        # обновляем экран
        pygame.display.flip()
        # вызываем функцию показа системного курсора после завершения игры
        mouse_visible()
        # устанавливаем 60 fps
        clock.tick(60)


# TODO основная функция игры
def main_runner(bg):
    global running
    # переменная времени (секунды)
    time_seconds = 0
    # пока running == True
    while running:
        # инициализация Pygame:
        pygame.init()

        # отключаем показ системного курсора
        pygame.mouse.set_visible(False)

        # ожидание закрытия окна:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # проверка события передвижения мыши
            if event.type == pygame.MOUSEMOTION:
                # изменяем положение спрайта-стрелки
                cursor.rect.topleft = event.pos

        # задаём задний фон
        screen.blit(bg, (0, 0))

        # отрисовываем секундомер
        display_time(time_seconds)

        # Обновляем спрайты
        all_sprites.update()
        trigger.update()

        # Рисуем объекты на окне
        all_sprites.draw(screen)
        trigger.draw(screen)

        # Проверка на столкновение курсора с шарами
        if check_collision(all_sprites):
            # вызываем функцию записи времени в БД после завершения игры
            writing_to_the_database()
            # вызываем функцию показа финального окна
            game_over(game_over_background)
            running = False

        # FPS
        fps = clock.tick(30)

        # конвертируем время (время идёт пока игрок не коснулся шара)
        if running:
            time_seconds += fps / 1000

        # Обновляем экран после рисования объектов
        pygame.display.flip()

    # вызываем функцию показа системного курсора после завершения игры
    mouse_visible()
    # возвращаем функцию запроса на повтор или выход из игры
    return end_of_game_requests()


# TODO первый уровень
def level1():
    # импортируем нужные переменные
    global mode
    global running
    global time_str
    global img_counter
    global all_sprites
    global trigger
    global cursor
    global horizontal_borders
    global vertical_borders

    while True:
        # флаг уровней
        mode = '1'

        # флаг цикла игры
        running = True

        # переменная времени (секунды)
        time_str = 0

        # переменная для подсчёта числа кадров в анимации
        img_counter = 0

        # группа, содержащая все спрайты
        all_sprites = pygame.sprite.Group()

        # группа, содержащая спрайт игрока(курсора)
        trigger = pygame.sprite.Group()

        # создаём шары
        for _ in range(25):
            Ball(all_sprites, randint(30, 80), randint(100, 1300), randint(100, 800))

        # создаём игрока(курсор)
        cursor = Cursor(trigger)

        # группы спрайтов, содержащие горизонтальные и вертикальные границы
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()

        # создаём границы
        Border(5, 5, WIDTH - 5, 5)
        Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
        Border(5, 5, 5, HEIGHT - 5)
        Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

        # Создал отсчёт времени перед запуском боя
        time_report(bg)

        if not main_runner(bg):
            show_menu(menu_background)


# TODO второй уровень
def level2():
    # импортируем нужные переменные
    global mode
    global running
    global time_str
    global img_counter
    global all_sprites
    global trigger
    global cursor
    global horizontal_borders
    global vertical_borders

    while True:
        # обозначение lvl
        mode = '2'
        # флаг цикла игры
        running = True
        # переменная времени (секунды)
        time_str = 0
        # переменная для подсчёта числа кадров в анимации
        img_counter = 0
        # группа, содержащая все спрайты
        all_sprites = pygame.sprite.Group()

        # группа, содержащая спрайт игрока(курсора)
        trigger = pygame.sprite.Group()

        # создаём шары
        for _ in range(35):
            Ball(all_sprites, randint(30, 80), randint(100, 1300), randint(100, 800))

        # создаём игрока(курсор)
        cursor = Cursor(trigger)

        # группы спрайтов, содержащие горизонтальные и вертикальные границы
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()

        # создаём границы
        Border(5, 5, WIDTH - 5, 5)
        Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
        Border(5, 5, 5, HEIGHT - 5)
        Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

        # Создал отсчёт времени перед запуском боя
        time_report(bg)

        if not main_runner(bg):
            show_menu(menu_background)


# TODO третий уровень
def level3():
    # импортируем нужные переменные
    global mode
    global running
    global time_str
    global img_counter
    global all_sprites
    global trigger
    global cursor
    global horizontal_borders
    global vertical_borders

    while True:
        # обозначение lvl
        mode = '3'

        # флаг цикла игры
        running = True
        # переменная времени (секунды)
        time_str = 0
        # переменная для подсчёта числа кадров в анимации
        img_counter = 0
        # группа, содержащая все спрайты
        all_sprites = pygame.sprite.Group()

        # группа, содержащая спрайт игрока(курсора)
        trigger = pygame.sprite.Group()

        # создаём шары
        for _ in range(45):
            Ball(all_sprites, randint(30, 80), randint(100, 1300), randint(100, 800))

        # создаём игрока(курсор)
        cursor = Cursor(trigger)

        # группы спрайтов, содержащие горизонтальные и вертикальные границы
        horizontal_borders = pygame.sprite.Group()
        vertical_borders = pygame.sprite.Group()

        # создаём границы
        Border(5, 5, WIDTH - 5, 5)
        Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
        Border(5, 5, 5, HEIGHT - 5)
        Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

        # Создал отсчёт времени перед запуском боя
        time_report(bg)

        if not main_runner(bg):
            show_menu(menu_background)


data = datetime.now()
if data.replace(hour=7, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=12, minute=0, second=0, microsecond=0):
    game_over_background = pygame.image.load('data\\menu_back\\morning.png')
elif data.replace(hour=12, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=17, minute=0, second=0, microsecond=0):
    game_over_background = pygame.image.load('data\\menu_back\\day.png')
elif data.replace(hour=17, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=21, minute=0, second=0, microsecond=0):
    game_over_background = pygame.image.load('data\\menu_back\\evening.png')
elif data.replace(hour=21, minute=0, second=0, microsecond=0) <= data or \
        data < data.replace(hour=7, minute=0, second=0, microsecond=0):
    game_over_background = pygame.image.load('data\\menu_back\\night.png')
else:
    game_over_background = 'ну даёт этот python, без этого else не работает'
if data.replace(hour=7, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=12, minute=0, second=0, microsecond=0):
    menu_background = pygame.image.load('data\\menu_back\\morning.png')
elif data.replace(hour=12, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=17, minute=0, second=0, microsecond=0):
    menu_background = pygame.image.load('data\\menu_back\\day.png')
elif data.replace(hour=17, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=21, minute=0, second=0, microsecond=0):
    menu_background = pygame.image.load('data\\menu_back\\evening.png')
elif data.replace(hour=21, minute=0, second=0, microsecond=0) <= data or \
        data < data.replace(hour=7, minute=0, second=0, microsecond=0):
    menu_background = pygame.image.load('data\\menu_back\\night.png')
else:
    menu_background = 'ну даёт этот python, без этого else не работает'
if data.replace(hour=7, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=12, minute=0, second=0, microsecond=0):
    bg = pygame.image.load('data\\menu_back\\morning.png')
elif data.replace(hour=12, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=17, minute=0, second=0, microsecond=0):
    bg = pygame.image.load('data\\menu_back\\day.png')
elif data.replace(hour=17, minute=0, second=0, microsecond=0) <= data < \
        data.replace(hour=21, minute=0, second=0, microsecond=0):
    bg = pygame.image.load('data\\menu_back\\evening.png')
elif data.replace(hour=21, minute=0, second=0, microsecond=0) <= data or \
        data < data.replace(hour=7, minute=0, second=0, microsecond=0):
    bg = pygame.image.load('data\\menu_back\\night.png')
else:
    bg = 'ну даёт этот python, без этого else не работает'

# обозначение lvl
mode = '1'

# флаг цикла игры
running = True

# переменная времени (секунды)
time_str = 0

# переменная для подсчёта числа кадров в анимации
img_counter = 0

# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()

# группа, содержащая спрайт игрока(курсора)
trigger = pygame.sprite.Group()

# создаём шары
for i in range(30):
    Ball(all_sprites, randint(30, 80), randint(100, 1300), randint(100, 800))

# создаём игрока(курсор)
cursor = Cursor(trigger)

# группы спрайтов, содержащие горизонтальные и вертикальные границы
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

# создаём границы
Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

# вызываем функцию показа меню
show_menu(menu_background)
