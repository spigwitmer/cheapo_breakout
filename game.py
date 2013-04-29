#!/usr/bin/env python
from breakout.gamestate import GameState
import pygame

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    windowsurface = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pygame shiz")
    gs = GameState(
            canvas=windowsurface,
            clock=clock,
            pygame_obj=pygame
            )
    gs.startgame()
