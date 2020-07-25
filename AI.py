import game
import random

#Just a random walk, really bad obviousily
class Random_walk(game.Game):
    def update(self):
        directions = [(-1,0),(0,-1),(1,0),(0,1)]
        possible_directions = [pos for pos in directions if pos != tuple([x * -1 for x in self.dir])]
        self.dir = random.choice(possible_directions)
        self.move()

#A_star will simply go to the fruit in a direct path, using the A_star algorithm
class A_star(game.Game):
    def custom_init(self):
        self.path = []
        self.astar()

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
                self.astar()

    #helper function for astar()
    def lowest_pos(open):
        lowest = 99999
        curr = None
        for o in open:
            if o[4] < lowest:
                lowest = o[4]
                curr = o
        return curr

    def astar(self):
        #open list contains arrays of positions
        #each position has its own positions, it's parent position,
        #and a G (distance current to start), H (distance current to finish)
        #and F (G + H) value
        open = [[self.snake[-1], None, 0, distance(self.snake[-1], self.apple), distance(self.snake[-1], self.apple)]]
        all_pos = [pos for pos in self.all_pos if pos not in self.snake[1:]]
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
                    h = distance(pos, self.apple)
                    f = g + h

                    open.append([pos, curr_pos[0], g, h, f])

                    #found the apple
                    if pos == self.apple:
                        self.path = [self.apple]
                        while curr_pos[1] is not None:
                            self.path.append(curr_pos[0])
                            next = [pos for pos in closed if pos[0] == curr_pos[1]]
                            if len(next) > 0:
                                curr_pos = next[0]
                            else:
                                break
                        return

    def eat_apple(self):
        self.generate_apple()
        self.astar()

def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] + pos2[1])
