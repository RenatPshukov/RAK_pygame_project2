# TODO Импортируем нужные библиотеки
import os
import pygame
from random import randint, choice

pygame.display.set_caption('Insanity balls')  # название
# устанавливаем размер окна
size = width, height = 1400, 900
screen = pygame.display.set_mode(size)
# Используется для управления fps
clock = pygame.time.Clock()


# TODO функция загрузки спрайтов
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# устанавливаем иконку (логотип)
# icon = load_image('red_ball.png')
# pygame.display.set_icon(icon)


# TODO класс шарика
class Ball(pygame.sprite.Sprite):

    def __init__(self, group, radius, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        red_ball = pygame.transform.scale(load_image("red_ball.png"), (radius, radius))
        blue_ball = pygame.transform.scale(load_image("blue_ball.png"), (radius, radius))
        darkblue_ball = pygame.transform.scale(load_image("darkblue_ball.png"), (radius, radius))
        green_ball = pygame.transform.scale(load_image("green_ball.png"), (radius, radius))
        orange_ball = pygame.transform.scale(load_image("orange_ball.png"), (radius, radius))
        pink_ball = pygame.transform.scale(load_image("pink_ball.png"), (radius, radius))
        purple_ball = pygame.transform.scale(load_image("purple_ball.png"), (radius, radius))
        white_ball = pygame.transform.scale(load_image("white_ball.png"), (radius, radius))
        yellow_ball = pygame.transform.scale(load_image("yellow_ball.png"), (radius, radius))
        s = [red_ball, blue_ball, darkblue_ball, green_ball, orange_ball, pink_ball, purple_ball, white_ball,
             yellow_ball]
        super().__init__(group)
        ds = choice(s)
        self.image = ds
        # self.image = pygame.Surface((2 * radius, 2 * radius),
        # pygame.SRCALPHA, 32)
        # pygame.draw.circle(self.image, pygame.Color((randint(0, 255), randint(0, 255), randint(0, 255))),
        # (radius, radius), radius)
        self.rect = pygame.Rect(x, y, radius, radius)
        self.vx = randint(-13, 13)
        self.vy = randint(-13, 13)
        while self.vx == 0:
            self.vx = randint(-13, 13)
        while self.vy == 0:
            self.vy = randint(-13, 13)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


# TODO класс границ
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
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


# группа, содержащая все спрайты
all_sprites = pygame.sprite.Group()

# создаём границы
Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

# создаём шары
for i in range(50):
    Ball(all_sprites, randint(30, 70), randint(100, 1300), randint(100, 800))
print(all_sprites)

running = True
# TODO основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # задаём задний фон
    # screen.fill(pygame.Color('white'))
    bg = pygame.image.load('data\\bg3.png')
    screen.blit(bg, (0, 0))
    # Обновляем спрайты
    all_sprites.update()
    # Рисуем объекты на окне
    all_sprites.draw(screen)
    # Обновляем экран после рисования объектов
    pygame.display.flip()
    # FPS
    clock.tick(30)

# выход
pygame.quit()
