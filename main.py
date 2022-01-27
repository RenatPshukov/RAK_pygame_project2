# Импортируем нужные библиотеки
import pygame
from random import randint

# Запуск
if __name__ == '__main__':
    pygame.init()
    NEXT_COORDINATES = pygame.USEREVENT + 1  # событие для пересчета новых координат
    pygame.time.set_timer(NEXT_COORDINATES, 10)  # раз в 10 миллисекунд считать новые коорд
    pygame.display.set_caption('Insanity balls')  # название
    size = width, height = 1400, 900  # размеры окна
    screen = pygame.display.set_mode(size)
    pos = None
    running = True
    R = 25  # размер шаров
    v = randint(1, 5)  # скорость шаров
    clock = pygame.time.Clock()
    # создание шаров
    list_of_circles = []
    for i in range(20):
        x = randint(0, 1390)
        y = randint(0, 890)
        pos = (x, y)
        # pos = event.pos
        print(pos)
        list_of_circles.append([*pos, randint(1, 4)])  # координаты шарика и его направление
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # математика

            if event.type == NEXT_COORDINATES:
                for circle in list_of_circles:
                    # перемещение
                    if circle[2] == 1:
                        circle[0] += v
                        circle[1] -= v
                    if circle[2] == 2:
                        circle[0] -= v
                        circle[1] -= v
                    if circle[2] == 3:
                        circle[0] -= v
                        circle[1] += v
                    if circle[2] == 4:
                        circle[0] += v
                        circle[1] += v
                    # отскок
                    if not (10 < circle[0] < 1390):
                        if circle[2] == 1:
                            circle[2] = 2
                        elif circle[2] == 2:
                            circle[2] = 1
                        elif circle[2] == 3:
                            circle[2] = 4
                        elif circle[2] == 4:
                            circle[2] = 3
                    elif not (10 < circle[1] < 890):
                        if circle[2] == 1:
                            circle[2] = 4
                        elif circle[2] == 2:
                            circle[2] = 3
                        elif circle[2] == 3:
                            circle[2] = 2
                        elif circle[2] == 4:
                            circle[2] = 1
        # графика
        # задаём задний фон
        screen.fill(pygame.Color('black'))
        for circle in list_of_circles:
            # рисуем шарики
            pygame.draw.circle(screen, pygame.Color("white"), (circle[0], circle[1]), R)
        # FPS
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
