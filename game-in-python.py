__author__ = "Péter Kerekes"

import pygame, sys
from pygame.locals import * # no "pygame.locals" prefix is needed
import numpy as np
import random

from config import *
import vector2 as Vector2

DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE)

def main():
    # Initialize program
    pygame.init()
 
    # Setup display
    DISPLAYSURF.fill(SCREEN_BACKGROUND)
    pygame.display.set_caption("Game In Python")

    # Test
    #draw_shapes()

    P1 = Player()

    # Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Physics
        P1.input()
        P1.move()

        # Draw
        DISPLAYSURF.fill(SCREEN_BACKGROUND) # Clear the screen first
        P1.draw(DISPLAYSURF)

        # Update screen and wait
        pygame.display.update()
        pygame.time.Clock().tick(1 / dT)

class Player(pygame.sprite.Sprite): # We passed a class as an argument. The Player class will be derived from the Sprite class!
    speed = 4 # class (~static) variable
    colliderSize = (44, 96)

    def __init__(self):
        self.moveDirection = np.array([0, 0]) # instance variable

        super().__init__() 
        self.image = pygame.image.load("Materials/Player.png")
        self.surf = pygame.Surface(Player.colliderSize) # create border
        self.rect = self.surf.get_rect()

        self.rect.move_ip(.5 * SCREEN_SIZE[1] + Player.colliderSize[0],
                          .5 * SCREEN_SIZE[1] - .5 * Player.colliderSize[1]) # move to center
 
    def input(self):
        # Read input
        pressed_keys = pygame.key.get_pressed()

        # Summarize input (+ boundaries)
        self.moveDirection = np.array([0, 0])
        
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.moveDirection += np.array([0, -1])
    
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_SIZE[1]:
            self.moveDirection += np.array([0, 1])
        
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.moveDirection += np.array([-1, 0])

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_SIZE[0]:
            self.moveDirection += np.array([1, 0])

    def move(self):
        # Apply movement
        self.rect.move_ip(Vector2.normalized(self.moveDirection) * Player.speed)
        
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     

def draw_shapes():
    # Creating Lines and Shapes
    pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (130,170))
    pygame.draw.line(DISPLAYSURF, BLUE, (150,130), (170,170))
    pygame.draw.line(DISPLAYSURF, GREEN, (130,170), (170,170))
    pygame.draw.circle(DISPLAYSURF, WHITE, (100,50), 30)
    pygame.draw.circle(DISPLAYSURF, WHITE, (200,50), 30)
    pygame.draw.rect(DISPLAYSURF, RED, (100, 200, 100, 50), 2)
    pygame.draw.rect(DISPLAYSURF, WHITE, (110, 260, 80, 5))

if __name__ == "__main__": # If this section exists, this will be the entry point
    main()