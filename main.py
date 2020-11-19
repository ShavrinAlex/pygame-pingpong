import sys
import random
import time
import pygame as pg



class Ball():
    """Класс мячика"""
    def __init__(self, window, board_top, board_bottom):
        """Инициализаця первичных настроек"""
        self.window = window
        self.board_top = board_top
        self.board_bottom = board_bottom
        self.pos_x = pg.display.get_window_size()[0] // 2
        self.pos_y = pg.display.get_window_size()[1] // 2
        self.radius = 15
        self.color = (200, 30, 30)
        self.speed_x = random.choice([-8, 8])
        self.speed_y = random.choice([-7, -6, -5, 5, 6, 7])
        

    def draw(self):
        """
        Отрисовывает шарик в на поверхности window цветом self.color
        в позициях self.pos_x self.pos_y с радиусом self.radius
        """

        pg.draw.circle(self.window, self.color, (self.pos_x, self.pos_y), self.radius)


    def check_collision_wall(self):
        """Проверка на столкновение шарика со стенкой"""

        if self.pos_x + self.radius > pg.display.get_window_size()[0] or\
            self.pos_x - self.radius < 0:
                self.speed_x = -self.speed_x
        elif self.pos_y + self.radius > pg.display.get_window_size()[1]:
            self.board_top.score += 1
            restart()
        elif self.pos_y - self.radius < 0:
            self.board_bottom.score += 1
            restart()


    def check_collision_board(self, board_top, board_bottom):
        if self.pos_x + self.radius >= board_top.pos_x and self.pos_x - self.radius <= board_top.pos_x + board_top.width and\
            self.pos_y - self.radius <= board_top.pos_y + board_top.height:
                self.speed_y = -self.speed_y
        if self.pos_x + self.radius >= board_bottom.pos_x and self.pos_x - self.radius <= board_bottom.pos_x + board_bottom.width and\
            self.pos_y + self.radius >= board_bottom.pos_y:
                self.speed_y = -self.speed_y


    def move(self):
        """Изменяет координаты self.pos_x, self.pos_y с шагом self.speed_x и self.speed_y"""
        
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y


class Board():
    """Класс платформы"""
    def __init__(self, window, pos_y: int, height: int):
        """Инициализация первичных настроек"""

        self.window = window
        self.width = 100
        self.height = height
        self.color = (20, 20, 250)
        self.pos_x = pg.display.get_window_size()[0] // 2 - self.width // 2
        self.pos_y = pos_y
        self.speed = 10
        self.score = 0


    def draw(self):
        """
        Отрисовывает платформу на поверхности window цветом self.color
        в позиции self.pos_x, self.pos_y и размером self.width и self.height
        """

        pg.draw.rect(self.window, self.color, (self.pos_x, self.pos_y, self.width, self.height))

    def check_collision_wall(self):
        if self.pos_x < 0:
            self.pos_x = 0
        elif self.pos_x + self.width > pg.display.get_window_size()[0]:
            self.pos_x = pg.display.get_window_size()[0] - self.width

    def move_right(self):
        """платформу"""
        self.pos_x += self.speed

    
    def move_left(self):
        self.pos_x -= self.speed
        

def check_events():
    global board_top, board_bottom

    [sys.exit() for e in pg.event.get() if e.type == pg.QUIT]
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        sys.exit()
    if keys[pg.K_d]:
        board_top.move_right()
    elif keys[pg.K_a]:
        board_top.move_left()
    if keys[pg.K_RIGHT]:
        board_bottom.move_right()
    elif keys[pg.K_LEFT]:
        board_bottom.move_left()


def restart():
    """Возвращение начального положения всех объектов"""
    font_render = font.render(f'{board_top.score} : {board_bottom.score}', True, (250, 250, 250))
    window.blit(font_render, (window_width // 2 - 35, window_height // 2 - 100))
    ball.pos_x = pg.display.get_window_size()[0] // 2
    ball.pos_y = pg.display.get_window_size()[1] // 2
    ball.speed_x = random.choice([-8, 8])
    ball.speed_y = random.choice([-7, -6, -5, 5, 6, 7])
    ball.draw()
    board_top.pos_x = pg.display.get_window_size()[0] // 2 - board_top.width // 2
    board_bottom.pos_x = pg.display.get_window_size()[0] // 2 - board_bottom.width // 2
    board_top.draw()
    board_bottom.draw()
    pg.display.update()
    time.sleep(2)


clock = pg.time.Clock()

window_width = 600
window_height = 600
window_fps = 30
window = pg.display.set_mode((window_width, window_height))
board_top = Board(window, 15, 10)
board_bottom = Board(window, window_height - 25, 10)
ball = Ball(window, board_top, board_bottom)
font_size = 42
font = pg.font.SysFont(None, font_size, bold=True, italic=True)

#Инициализация библиотеки
pg.init()

while True:
    check_events()

    window.fill((0, 0, 0))
    ball.check_collision_wall()
    ball.check_collision_board(board_top, board_bottom) 
    ball.move()
    ball.draw()
    board_top.check_collision_wall()
    board_top.draw()
    board_bottom.check_collision_wall()
    board_bottom.draw()

    pg.display.update()
    clock.tick(window_fps)

