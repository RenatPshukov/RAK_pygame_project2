# TODO Импортируем нужные библиотеки
import os
import sqlite3

import pygame
from random import randint, choice

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


# флаг цикла игры
running = True
# переменная времени (секунды)
time_str = 0


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
    # Подключение к БД
    con = sqlite3.connect("Insanity_balls.db")
    # Создание курсора
    cur = con.cursor()
    # Выполнение запроса
    cur.execute(f"INSERT INTO History (time) VALUES ('{time_str}');")
    # коммит
    con.commit()
    # Закрываем БД
    con.close()


# TODO класс шарика
class Ball(pygame.sprite.Sprite):
    # инициализация класса
    def __init__(self, group, radius, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        # импортируем спрайты шаров из папки data, устанавливая им размер radius
        red_ball = pygame.transform.scale(load_image("red_ball.png"), (radius, radius))
        blue_ball = pygame.transform.scale(load_image("blue_ball.png"), (radius, radius))
        dark_blue_ball = pygame.transform.scale(load_image("darkblue_ball.png"), (radius, radius))
        green_ball = pygame.transform.scale(load_image("green_ball.png"), (radius, radius))
        orange_ball = pygame.transform.scale(load_image("orange_ball.png"), (radius, radius))
        pink_ball = pygame.transform.scale(load_image("pink_ball.png"), (radius, radius))
        purple_ball = pygame.transform.scale(load_image("purple_ball.png"), (radius, radius))
        white_ball = pygame.transform.scale(load_image("white_ball.png"), (radius, radius))
        yellow_ball = pygame.transform.scale(load_image("yellow_ball.png"), (radius, radius))
        # список с спрайтами шаров
        sprite_list = [red_ball, blue_ball, dark_blue_ball, green_ball, orange_ball, pink_ball, purple_ball, white_ball,
                       yellow_ball]
        super().__init__(group)
        # выбираем один случайный спрайт из списка
        selected_sprite = choice(sprite_list)
        # и устанавливаем его на объект шара
        self.image = selected_sprite
        # создаём объект шара
        self.rect = pygame.Rect(x, y, radius, radius)
        # указываем случайное направления движения и скорость по осям
        self.vx = randint(-13, 13)
        self.vy = randint(-13, 13)
        # если выпало 0, то перезаписываем ещё раз, так же по осям
        while self.vx == 0:
            self.vx = randint(-13, 13)
        while self.vy == 0:
            self.vy = randint(-13, 13)

    # функция взаимодествия (столкновение и рикошет) шаров и границ
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        # если шар соприкоснулся с горизонтальной границей, то изменяем его направление на противоположное
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        # если шар соприкоснулся с вертикальной границей, то изменяем его направление на противоположное
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


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


# TODO функция проверки столкновения
def check_collision(balls):
    # перебираем все шары из группы спрайтов all_sprites
    for ball in balls:
        # если курсор соприкоснулся с центром окружности спрайта возвращаем True
        if cursor.rect.collidepoint(ball.rect.center):
            return True


# TODO функция запроса на повтор или выход из игры
def game_over():
    print('-')
    # флаг прекращение
    termination = True
    # цикл ...
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
        print('-')
        return True
    # если нажат escape то возвращаем False
    if keys[pygame.K_ESCAPE]:
        print('+')
        return False

    # обновляем экран
    pygame.display.update()
    # устанавливаем 15 fps
    clock.tick(15)


# группы спрайтов, содержащие горизонтальные и вертикальные границы
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()

# группа, содержащая спрайт игрока(курсора)
trigger = pygame.sprite.Group()

# создаём границы
Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

# создаём шары
for i in range(30):
    Ball(all_sprites, randint(30, 80), randint(100, 1300), randint(100, 800))

# создаём игрока(курсор)
cursor = Cursor(trigger)


# TODO основной цикл
def main_runner():
    global running
    # переменная времени (секунды)
    time_seconds = 0
    # пока running == True
    while running:
        # инициализация Pygame:
        pygame.init()

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
        bg = pygame.image.load('data\\bg3.png')
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
            running = False

        # FPS
        fps = clock.tick(30)

        # конвертируем время (время идёт пока игрок не коснулся шара)
        if running:
            time_seconds += fps / 1000

        # Обновляем экран после рисования объектов
        pygame.display.flip()

    # вызываем функцию записи времени в БД
    writing_to_the_database()
    # возвращаем функцию запроса на повтор или выход из игры
    return game_over()


# TODO главный цикл игры
while main_runner():
    pass

# выход
pygame.quit()
quit()
