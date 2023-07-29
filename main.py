import pygame
import random
import sys

from pygame.math import Vector2

from settings import cell_number, cell_size

main_menu = True
icon = pygame.image.load("img/apple.png")
pygame.display.set_icon(icon)

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class Fruit:

    def __init__(self):
        self.x, self.y, self.pos = 0, 0, Vector2(0, 0)
        self.new_fruit()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(fruit, fruit_rect)

    def new_fruit(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10)]
        self.head = pygame.image.load('img/head_right.png').convert_alpha()
        self.direction = Vector2(1, 0)
        self.score = 0

        self.head_up = pygame.image.load('img/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('img/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('img/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('img/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('img/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('img/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('img/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('img/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('img/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('img/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('img/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('img/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('img/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('img/body_bl.png').convert_alpha()

    def add_block_to_snake(self):
        if len(self.body) >= 2:
            last_item = self.body[-1]
        else:
            last_item = self.body[:]
        self.body.append(Vector2(last_item.x, last_item.y))

    def draw_head(self):
        if self.direction == (1, 0):
            self.head = self.head_right
        if self.direction == (-1, 0):
            self.head = self.head_left
        if self.direction == (0, -1):
            self.head = self.head_up
        if self.direction == (0, 1):
            self.head = self.head_down

    def draw_snake(self):
        self.draw_head()

        for i, block in enumerate(self.body):
            snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)

            if i == 0:
                screen.blit(self.head, snake_rect)

            elif not 0 <= i or not i == len(self.body) - 1:
                if self.body[i].x < self.body[i - 1].x or self.body[i].x > self.body[i - 1].x:
                    screen.blit(self.body_horizontal, snake_rect)
                if self.body[i].y < self.body[i - 1].y or self.body[i].y > self.body[i - 1].y:
                    screen.blit(self.body_vertical, snake_rect)
            else:
                if i == len(self.body) - 1:
                    if self.body[i].x < self.body[i - 1].x:
                        screen.blit(self.tail_left, snake_rect)
                    if self.body[i].x > self.body[i - 1].x:
                        screen.blit(self.tail_right, snake_rect)
                    if self.body[i].y < self.body[i - 1].y:
                        screen.blit(self.tail_up, snake_rect)
                    if self.body[i].y > self.body[i - 1].y:
                        screen.blit(self.tail_down, snake_rect)
                else:
                    pygame.draw.rect(screen, (255, 0, 0), snake_rect)

    def move_snake(self):
        if len(self.body) >= 2:
            body_double = self.body[:-1]
        else:
            body_double = self.body[:]
        body_double.insert(0, body_double[0] + self.direction)
        self.body = body_double[:]


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.game_over = False
        self.counter = 0
        self.objects_eaten = 0

    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over = True
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over = True

    def draw_things(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def game_over(self):
        self.snake.score = 0
        self.game_over = True

    def snake_eats_fruit(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.score += 1
            self.objects_eaten += 1
            self.snake.add_block_to_snake()
            self.fruit.new_fruit()

    def update(self):
        self.snake.move_snake()
        self.check_game_over()
        self.snake_eats_fruit()


pygame.init()
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
fruit = pygame.image.load('img/apple.png').convert_alpha()

Game = Game()

SNAKE_IS_MOVING = pygame.USEREVENT
pygame.time.set_timer(SNAKE_IS_MOVING, 150)

restart_img = pygame.image.load('img/restart.png')
start_img = pygame.image.load('img/start.png')
end_img = pygame.image.load('img/end.png')

restart_button = Button(500, 350, restart_img)
img_size = restart_button.image.get_size()
new_restart = (img_size[0] * 5, img_size[1] * 5)
restart_img = pygame.transform.scale(restart_img, new_restart)
restart_button = Button(90, 350, restart_img)

new_end = (img_size[0] * 5, img_size[1] * 5)
end_img = pygame.transform.scale(end_img, new_end)
end_button = Button(450, 350, end_img)

new_start = (img_size[0] * 6, img_size[1] * 6)
start_img = pygame.transform.scale(start_img, new_start)
start_button = Button(250, 280, start_img)

pygame.display.set_caption("Game snake")


def game():
    game_over = False
    start_screen = True

    bg_img = pygame.image.load('img/Bg_snake.png')
    bg_img = pygame.transform.scale(bg_img, (cell_size * cell_number, cell_size * cell_number))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if start_screen:
            screen.blit(bg_img, (0, 0))
            if start_button.draw():
                start_screen = False
                game_over = False
                game_loop()

        elif game_over:
            screen.blit(bg_img, (0, 0))
            end_button.draw()
            font = pygame.font.Font(None, 36)
            text = font.render("Game over", True, (200, 18, 0))
            text_rect = text.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
            screen.blit(text, text_rect)
            if end_button.draw():
                pygame.quit()
                sys.exit()

        pygame.display.update()


bg_img = pygame.image.load('img/Bg_snake.png')
bg_img = pygame.transform.scale(bg_img, (screen.get_width(), screen.get_height()))


def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SNAKE_IS_MOVING and not Game.game_over:
                Game.update()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    if Game.snake.direction.y != 1:
                        Game.snake.direction = Vector2(0, -1)

                if event.key == pygame.K_DOWN:

                    if Game.snake.direction.y != -1:
                        Game.snake.direction = Vector2(0, 1)

                if event.key == pygame.K_LEFT:

                    if Game.snake.direction.x != 1:
                        Game.snake.direction = Vector2(-1, 0)

                if event.key == pygame.K_RIGHT:
                    if Game.snake.direction.x != -1:
                        Game.snake.direction = Vector2(1, 0)

        screen.fill((164, 221, 105))
        if not Game.game_over:
            Game.draw_things()

        else:

            screen.blit(bg_img, (0, 0))

            font = pygame.font.SysFont('Futura', 60)

            text = font.render("Game over!", True, (0, 0, 0))

            text_rect = text.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 - 190))

            screen.blit(text, text_rect)

            score_text = font.render("Result: {}".format(Game.objects_eaten), True, (0, 0, 0))

            score_rect = score_text.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 - 110))

            screen.blit(score_text, score_rect)

            restart_button.draw()

            end_button.draw()

            if restart_button.draw():
                Game.__init__()

            if end_button.draw():
                pygame.quit()

                sys.exit()
        pygame.display.update()


game()
