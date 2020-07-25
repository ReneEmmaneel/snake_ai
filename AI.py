import game
import random

class Astar(game.Game):
    def update(self):
        directions = [(-1,0),(0,-1),(1,0),(0,1)]
        possible_directions = [pos for pos in directions if pos != tuple([x * -1 for x in self.dir])]
        self.dir = random.choice(possible_directions)
        self.move()
