import random
import pygame

RED = (255, 0, 0)
GREEN = (0,255,0)
BLACK = (0,0,0)

class Game():
    def __init__(self, grid_size = (30,30)):
        self.grid_size = grid_size
        #create list of size n*m with all tuples
        self.all_pos = [(x,y) for x in range(self.grid_size[0]) for y in range(self.grid_size[1])]
        self.generate_snake()
        self.generate_apple()
        self.dir = (1,0)
        self.new_dir = (1,0)
        self.AI = False
        self.stop = False

    #change direction if new_dir is not the opposite direction than self.dir
    def change_dir(self, new_dir):
        if self.dir != tuple([x * -1 for x in new_dir]):
            self.new_dir = new_dir

    def game_over(self):
        self.stop = True

    def update(self):
        self.dir = self.new_dir
        self.move()

    #move in direction in self.dir
    def move(self):
        self.snake.append((self.snake[-1][0] + self.dir[0], self.snake[-1][1] + self.dir[1]))

        #out of grid
        if self.snake[-1][0] < 0 or self.snake[-1][0] >= self.grid_size[0] or self.snake[-1][1] < 0 or self.snake[-1][1] >= self.grid_size[1]:
            self.game_over()
        #front of snake runs into self
        elif self.snake[-1] in self.snake[1:-1]:
            self.game_over()
        else:
            if self.snake[-1] == self.apple:
                self.generate_apple()
            else:
                del self.snake[0]

    def update_AI(self):
        pass

    def generate_snake(self):
        self.snake = [(0,0),(1,0),(2,0)]

    def generate_apple(self):
        all_possible_pos = [pos for pos in self.all_pos if pos not in self.snake]
        self.apple = random.choice(all_possible_pos)

    def draw(self, dim, screen):
        left, top, width, height = dim
        self.draw_grid(left, top, width, height, screen)
        self.draw_snake_and_apple(left, top, width, height, screen)

    def draw_grid(self, left, top, width, height, screen):
        for x in range(self.grid_size[0] + 1):
            x_pos = left + (x / self.grid_size[0] * width)
            pygame.draw.line(screen, BLACK, (x_pos, top), (x_pos, top + height - 1))

        for y in range(self.grid_size[1] + 1):
            y_pos = top + (y / self.grid_size[1] * height)
            pygame.draw.line(screen, BLACK, (left, y_pos), (left + width, y_pos))

    def draw_snake_and_apple(self, left, top, width, height, screen):
        x_grid_size = width / self.grid_size[0]
        y_grid_size = height / self.grid_size[1]

        #draw snake
        for pos in self.snake:
            x_pos = left + (pos[0] / self.grid_size[0] * width)
            y_pos = top + (pos[1] / self.grid_size[1] * height)

            pygame.draw.rect(screen, GREEN, (x_pos + 1, y_pos + 1, x_grid_size - 1, y_grid_size - 1))

        #draw apple
        x_pos = left + (self.apple[0] / self.grid_size[0] * width)
        y_pos = top + (self.apple[1] / self.grid_size[1] * height)
        pygame.draw.rect(screen, RED, (x_pos + 1, y_pos + 1, x_grid_size - 1, y_grid_size - 1))
