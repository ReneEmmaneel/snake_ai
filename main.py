import pygame
import sys

import game
import AI

WHITE = (255,255,255)
GREEN = (0,255,0)
RED   = (255,0,0)
BLACK = (0,0,0)

def init():
    #Game = game.Game((30,30))
    grid_size = (30,30)
    Game = new_game(grid_size)

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600,600))

    render_frame_rate = 1
    steps = 0
    while True:
        steps += 1
        if Game.stop:
            Game = new_game(grid_size)
        #msElapsed = clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not Game.AI:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        Game.change_dir((-1,0))
                    elif event.key == pygame.K_RIGHT:
                        Game.change_dir((1,0))
                    elif event.key == pygame.K_UP:
                        Game.change_dir((0,-1))
                    elif event.key == pygame.K_DOWN:
                        Game.change_dir((0,1))
        Game.update()
        if steps % render_frame_rate == 0:
            screen.fill(WHITE)
            Game.draw((0, 0, 600, 600), screen)
        pygame.display.update()

args = ""
def new_game(grid_size):
    if args.lower() == 'random_walk':
        return AI.Random_walk(grid_size)
    elif args.lower() == 'a_star':
        return AI.A_star(grid_size)
    elif args.lower() == 'hamilton':
        return AI.Hamilton_simple(grid_size)
    else:
        return game.Game(grid_size)

if __name__ == '__main__':
    args = sys.argv[1] if len(sys.argv) > 1 else ''
    init()
