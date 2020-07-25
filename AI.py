import game
import random
import sys

#Just a random walk, really bad obviousily
class Random_walk(game.Game):
    def update(self):
        directions = [(-1,0),(0,-1),(1,0),(0,1)]
        possible_directions = [pos for pos in directions if pos != tuple([x * -1 for x in self.dir])]
        self.dir = random.choice(possible_directions)
        self.move()

#A_star will simply go to the fruit in a direct path, using the A_star algorithm
#It will generate a path every time a fruit is eaten.
#If no path is found, move randomely until a path is found
class A_star(game.Game):
    def custom_init(self):
        self.path = A_star.astar(self.snake, self.apple, self.all_pos)

    def update(self):
        if len(self.path) > 0:
            self.dir = game.Game.sub_tuple(self.path[-1], self.snake[-1])
            del self.path[-1]
            self.move()
        else:
            #if no path, move randomely, making sure to not run into the snake/wall if avoidable
            directions = [(-1,0),(0,-1),(1,0),(0,1)]
            possible_directions = [dir for dir in directions if dir != tuple([x * -1 for x in self.dir])]
            final_directions = []
            for dir in possible_directions:
                pos =  game.Game.add_tuple(self.snake[-1], dir)
                if pos in self.snake[1:]:
                    continue
                if not self.pos_in_grid(pos):
                    continue
                final_directions.append(dir)
            if (len(final_directions) == 0):
                self.move()
            else:
                self.dir = random.choice(final_directions)
                self.move()
                self.path = A_star.astar(self.snake, self.apple, self.all_pos)

    #helper function for astar()
    def lowest_pos(open):
        lowest = 99999
        curr = None
        for o in open:
            if o[4] < lowest:
                lowest = o[4]
                curr = o
        return curr

    def astar(snake, apple, all_pos):
        return_list = []
        #open list contains arrays of positions
        #each position has its own positions, it's parent position,
        #and a G (distance current to start), H (distance current to finish)
        #and F (G + H) value
        open = [[snake[-1], None, 0, distance(snake[-1], apple), distance(snake[-1], apple)]]
        all_pos = [pos for pos in all_pos if pos not in snake[1:]]
        closed = []

        while len(open) > 0:
            curr_pos = A_star.lowest_pos(open)

            open.remove(curr_pos)
            closed.append(curr_pos)

            directions = [(-1,0),(1,0),(0,1),(0,-1)]
            for dir in directions:
                pos = game.Game.add_tuple(curr_pos[0], dir)
                if pos in all_pos:
                    #check if position already visited
                    if pos in [c[0] for c in closed]:
                        continue
                    if pos in [o[0] for o in open]:
                        continue

                    #add position to open
                    g = curr_pos[2] + 1
                    h = distance(pos, apple)
                    f = g + h

                    open.append([pos, curr_pos[0], g, h, f])

                    #found the apple
                    if pos == apple:
                        return_list = [apple]
                        while curr_pos[1] is not None:
                            return_list.append(curr_pos[0])
                            next = [pos for pos in closed if pos[0] == curr_pos[1]]
                            if len(next) > 0:
                                curr_pos = next[0]
                            else:
                                break
                        return return_list
        return return_list

    def eat_apple(self):
        self.generate_apple()
        self.path = A_star.astar(self.snake, self.apple, self.all_pos)

    def draw(self, dim, screen):
        #self.draw_grid(dim, screen)
        line_width = 0.45
        color = (80,80,80)
        self.draw_line(screen, dim, line_width, color, self.path + [self.snake[-1]])
        self.draw_snake_and_apple(dim, screen)

#Generates a hamilton path, and will simply follow it until it is done
class Hamilton_simple(game.Game):
    def custom_init(self):
        self.path = []
        self.hamilton()

    def update(self):
        if len(self.path) > 0:
            self.path_index = (self.path_index + 1) % len(self.path)
            self.dir = game.Game.sub_tuple(self.path[self.path_index], self.snake[-1])
            self.move()

    #will generate a hamilton path, and store it in self.path
    #The path will start at the head of the snake, and stop at the tail.
    #Then it will add the snake to it, to generate a full cycle
    def hamilton(self):
        current_path = self.snake[-1]
        n = self.grid_size[0] * self.grid_size[1] - len(self.snake) + 2

        self.path = self.hamilton_rec([self.snake[-1]], self.snake[1:], self.snake[0]) + self.snake[1:-1]
        self.path_index = 0

    def hamilton_rec(self, path, wall, goal):
        n = self.grid_size[0] * self.grid_size[1] - len(self.snake) + 2
        directions = [(1,0),(0,1),(-1,0),(0,-1)]

        if len(path) == n:
            return path if path[-1] == goal else None
        else:
            for dir in directions:
                pos = game.Game.add_tuple(path[-1], dir)
                if pos in path:
                    continue
                elif pos in wall:
                    continue
                elif not self.pos_in_grid(pos):
                    continue
                else:
                    result = self.hamilton_rec(path + [pos], wall, goal)
                    if result == None:
                        continue
                    else:
                        return result
            return None

    def draw(self, dim, screen):
        #self.draw_grid(dim, screen)
        if len(self.path) > 0:
            line_width = 0.48
            color = (150,150,150)
            self.draw_line(screen, dim, line_width, color, self.path + [self.path[0]])
        self.draw_snake_and_apple(dim, screen)

class Hamilton_improved(Hamilton_simple):
    def custom_init(self):
        self.path = []
        self.astar_and_hamilton()

    def update(self):
        if len(self.path) > 0:
            self.dir = game.Game.sub_tuple(self.path[self.path_index], self.snake[-1])
            self.path_index = (self.path_index + 1) % len(self.path)
            self.move()

    #it will first find the astar path to the fruit, and test if a
    #hamilton path exist using that path.
    #else, just use the previous found hamilton path
    def astar_and_hamilton(self):
        a_star_path = A_star.astar(self.snake, self.apple, self.all_pos)

        path = [self.apple]
        snake_plus_path = self.snake + a_star_path[::-1]

        wall = snake_plus_path[-1 * len(self.snake):]

        found_path = self.hamilton_rec(path, wall[1:], wall[0])
        if found_path == None:
            self.hamilton()
        else:
            n = self.grid_size[0] * self.grid_size[1]
            self.path = snake_plus_path[len(self.snake):] + found_path[1:]
            self.path = self.path[:n]
            self.path_index = 0

    def hamilton(self):
        found_path = self.hamilton_rec([self.snake[-1]], self.snake[1:], self.snake[0]) + self.snake[1:-1]
        if len(found_path) > 0:
            self.path = found_path
            self.path_index = 0

def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] + pos2[1])
