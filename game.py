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
        self.waiting = True
        self.draw_steps = True

    def custom_init(self):
        pass

    #change direction if new_dir is not the opposite direction than self.dir
    def change_dir(self, new_dir):
        if self.dir != tuple([x * -1 for x in new_dir]):
            self.new_dir = new_dir

    def game_over(self):
        self.stop = True

    def update(self):
        self.dir = self.new_dir
        self.move()

    #returns true if pos is inside self.grid_size values
    def pos_in_grid(self, pos):
        return pos[0] >= 0 and pos[0] < self.grid_size[0] and pos[1] >= 0 and pos[1] < self.grid_size[1]

    def add_tuple(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def sub_tuple(a, b):
        return (a[0] - b[0], a[1] - b[1])

    #move in direction in self.dir
    def move(self):
        if (abs(self.dir[0] + self.dir[1]) != 1):
            print('illegal direction')
            self.game_over()

        self.snake.append(Game.add_tuple(self.snake[-1], self.dir))

        #out of grid
        if not self.pos_in_grid(self.snake[-1]):
            self.game_over()
        #front of snake runs into self
        elif self.snake[-1] in self.snake[1:-1]:
            self.game_over()
        else:
            if self.snake[-1] == self.apple:
                self.eat_apple()
            else:
                del self.snake[0]

    def update_AI(self):
        pass

    def generate_snake(self):
        self.snake = [(0,0),(1,0),(2,0)]

    def eat_apple(self):
        self.generate_apple()
        self.custom_eat_apple()

    def custom_eat_apple(self):
        pass

    def generate_apple(self):
        all_possible_pos = [pos for pos in self.all_pos if pos not in self.snake]
        if len(all_possible_pos) == 0:
            print('win!')
            self.game_over()
        else:
            self.apple = random.choice(all_possible_pos)

    def draw(self, dim, screen):
        #self.draw_grid(dim, screen)
        self.draw_snake_and_apple(dim, screen)

    def draw_grid(self, dim, screen):
        left, top, width, height = dim
        for x in range(self.grid_size[0] + 1):
            x_pos = left + (x / self.grid_size[0] * width)
            pygame.draw.line(screen, BLACK, (x_pos, top), (x_pos, top + height - 1))

        for y in range(self.grid_size[1] + 1):
            y_pos = top + (y / self.grid_size[1] * height)
            pygame.draw.line(screen, BLACK, (left, y_pos), (left + width, y_pos))

    def draw_snake_and_apple(self, dim, screen):
        left, top, width, height = dim

        line_width = 0.2
        color = GREEN
        self.draw_line(screen, dim, line_width, color, self.snake)

        #draw apple
        x_grid_size = width / self.grid_size[0]
        y_grid_size = height / self.grid_size[1]
        x_pos = left + (self.apple[0] / self.grid_size[0] * width)
        y_pos = top + (self.apple[1] / self.grid_size[1] * height)
        pygame.draw.ellipse(screen, RED, (x_pos + 1, y_pos + 1, x_grid_size - 1, y_grid_size - 1))

    def draw_line(self, screen, dim, line_width, color, line_list):

        if len(line_list) == 0 or len(line_list) == 1:
            return

        prev = line_list[0]
        curr = line_list[1]
        self.draw_line_part(screen, dim, line_width, color, None, prev, curr)
        for next in line_list[2:]:

            self.draw_line_part(screen, dim, line_width, color, prev, curr, next)

            prev = curr
            curr = next
        self.draw_line_part(screen, dim, line_width, color, prev, curr, None)

    def draw_line_part(self, screen, dim, line_width, color, prev, curr, next):
        left, top, width, height = dim

        x_grid_size = width / self.grid_size[0]
        y_grid_size = height / self.grid_size[1]

        snake_width = x_grid_size * line_width

        x_pos = left + (curr[0] / self.grid_size[0] * width)
        y_pos = top + (curr[1] / self.grid_size[1] * height)

        #look to each direction
        if Game.add_tuple(curr, (1,0)) in [prev, next]:
            pygame.draw.rect(screen, color, (x_pos + snake_width, y_pos + snake_width, x_grid_size - 1 * snake_width + 1, y_grid_size - 2 * snake_width + 1))
        if Game.add_tuple(curr, (0,1)) in [prev, next]:
            pygame.draw.rect(screen, color, (x_pos + snake_width, y_pos + snake_width, x_grid_size - 2 * snake_width + 1, y_grid_size - 1 * snake_width + 1))
        if Game.add_tuple(curr, (-1,0)) in [prev, next]:
            pygame.draw.rect(screen, color, (x_pos, y_pos + snake_width, x_grid_size - 1 * snake_width + 1, y_grid_size - 2 * snake_width + 1))
        if Game.add_tuple(curr, (0,-1)) in [prev, next]:
            pygame.draw.rect(screen, color, (x_pos + snake_width, y_pos, x_grid_size - 2 * snake_width + 1, y_grid_size - 1 * snake_width + 1))
