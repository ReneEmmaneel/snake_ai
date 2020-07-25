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
    Game = AI.Astar((30,30))

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((600,600))
    while True:
        if Game.stop:
            Game = AI.Astar((30,30))
        msElapsed = clock.tick(10)
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
        screen.fill(WHITE)
        Game.update()
        Game.draw((0, 0, 600, 600), screen)
        pygame.display.update()

if __name__ == '__main__':
    init()
