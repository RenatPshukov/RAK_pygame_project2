# TODO Импортируем нужные библиотеки
import os
import pygame
from random import randint, randrange

pygame.display.set_caption('Insanity balls')  # название
size = width, height = 1400, 900  # размеры окна
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# TODO загрузка спрайта
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


# TODO класс шарика
class Ball(pygame.sprite.Sprite):
    def __init__(self, group, radius, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        super().__init__(group)
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color((randint(0, 255), randint(0, 255), randint(0, 255))),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = randint(-3, 6)
        self.vy = randrange(-3, 6)

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
    Ball(all_sprites, randint(15, 30), randint(20, 1380), randint(20, 880))

running = True
# TODO основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # задаём задний фон
    screen.fill(pygame.Color("white"))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    # FPS
    clock.tick(100)

# выход
pygame.quit()
