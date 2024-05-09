import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Основные переменные
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
snake_speed = 15

# Цвета
dark_gray = (50, 50, 50)  # Цвет клеточек
red = (200, 0, 0)
green = (0, 200, 0)
gray = (100, 100, 100)  # Цвет сетки

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

game_over_image = pygame.image.load('game_over.png')
game_over_image = pygame.transform.scale(game_over_image, (width, height))
game_over = False


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = green
        self.speed = snake_speed
        self.last_boost_time = 0
        self.boost_duration = 1  # продолжительность ускорения в секундах

    def check_for_boost(self, current_time):
        if current_time - self.last_boost_time < 0.3:  # 0.3 секунды - максимальное время между нажатиями для активации турбо
            self.speed = snake_speed * 2  # увеличиваем скорость в 2 раза
            self.last_boost_time = current_time + self.boost_duration  # обновляем время последнего ускорения
        else:
            self.last_boost_time = current_time

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*10)) % width), (cur[1] + (y*10)) % height)
        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((width // 2), (height // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        global game_over
        game_over = True

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, pygame.Rect(p[0], p[1], 10, 10))


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = red
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (width - 10) // 10) * 10, random.randint(0, (height - 10) // 10) * 10)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], 10, 10))


def drawGrid(surface):
    for y in range(0, int(height/10)):
        for x in range(0, int(width/10)):
            rect = pygame.Rect(x*10, y*10, 10, 10)
            pygame.draw.rect(surface, dark_gray, rect, 1)


def main():
    snake = Snake()
    food = Food()
    global game_over

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        screen.fill(dark_gray)
        drawGrid(screen)
        snake.draw(screen)
        food.draw(screen)

        if game_over:
            screen.blit(game_over_image, (0, 0))

        pygame.display.update()
        clock.tick(snake_speed)
        if game_over:
            time.sleep(3)
            break


if __name__ == "__main__":
    main()
