__author__ = "Péter Kerekes"

import pygame, sys
from pygame.locals import * # no "pygame.locals" prefix is needed
import numpy as np # we can use aliases

from config import *
from vector2 import Vector2 # Vector2 class from vector2 module

def start():
    pygame.init()
 
    # Setup display
    global display_surface # Create a global variable. If it already exists, then this is only required if we want to change its value.
    display_surface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Game In Python")

    # Test
    #draw_shapes()
    #vector_operations()

    global P1
    P1 = Player()

def update():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Physics
        P1.input()
        P1.move()

        # Graphics
        display_surface.fill(SCREEN_BACKGROUND) # Clear the screen first
        P1.draw(display_surface)
        pygame.display.update()

        # Sleep
        clock.tick(1 / dT) # Limiting the framerate. Computes the time passed between two calls.


class Player(pygame.sprite.Sprite): # We passed a class as an argument. The Player class will be derived from the Sprite class!
    # Class (~static) variables
    speed = 250
    colliderSize = (44, 96)

    def __init__(self):
        # Instance variables
        self.pos = Vector2(.5 * SCREEN_SIZE[0], .5 * SCREEN_SIZE[1]) # move to center

        super().__init__() 
        self.image = pygame.image.load("Materials/Player.png")
        self.surf = pygame.Surface(Player.colliderSize) # create border
        self.rect = self.surf.get_rect()
 
    def input(self):
        # Read input
        pressed_keys = pygame.key.get_pressed()

        # Summarize input (+ boundaries)
        self.inputDir = Vector2.zeros()
        
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.inputDir -= Vector2(0, 1)
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_SIZE[1]:
            self.inputDir += Vector2(0, 1)
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.inputDir -= Vector2(1, 0)
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_SIZE[0]:
            self.inputDir += Vector2(1, 0)
        
        self.pos += self.inputDir.normalized() * Player.speed * dT

    def move(self):
        # Apply movement
        self.rect.move_ip(self.pos.x - self.rect.center[0], self.pos.y - self.rect.center[1])
        #self.rect.update(self.pos.x, self.pos.y, Player.colliderSize[0], Player.colliderSize[1])        
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     

def draw_shapes():
    display_surface.fill(SCREEN_BACKGROUND)
    
    pygame.draw.line(display_surface, BLUE, (150,130), (130,170))
    pygame.draw.line(display_surface, BLUE, (150,130), (170,170))
    pygame.draw.line(display_surface, GREEN, (130,170), (170,170))
    pygame.draw.circle(display_surface, WHITE, (100,50), 30)
    pygame.draw.circle(display_surface, WHITE, (200,50), 30)
    pygame.draw.rect(display_surface, RED, (100, 200, 100, 50), 2)
    pygame.draw.rect(display_surface, WHITE, (110, 260, 80, 5))

    pygame.display.update()

def vector_operations():
    v1 = Vector2(2, 1)
    v1.print('v1')
    v2 = Vector2()
    v2.print('v2')
    v2.x, v2.y = 3, 3
    v2.print('v2')
    print()
    print('v3 = v1 + v2')
    v3 = v1 + v2
    v3.print('v3')
    print()
    print('v3 -= (10, 10)')
    v3 -= Vector2(10, 10)
    v3.print('v3')
    print()
    print('v3 /= 2')
    v3 /= 2
    v3.print('v3')
    print('v4 = v3 / 2')
    v4 = v3 / 2
    v4.print('v4')
    print()
    print('v5 = v4 * (-2)')
    v5 = v4 * (-2)
    v5.print()
    print('v4 *= (-2)')
    v4 *= (-2)
    v4.print()

if __name__ == "__main__": # If this section exists, this will be the entry point
    start()
    update()
