__author__ = "Péter Kerekes"

import pygame, sys
from pygame.locals import * # no "pygame.locals" prefix is needed
import numpy as np # we can use aliases

from config import *
from vector2 import Vector2 # Vector2 class from vector2 module
import random

def main():
    init()
    while True:
        loop()

def init():
    pygame.init()
 
    # Setup display
    global display_surface # Create a global variable. If it already exists, then this is only required if we want to change its value.
    display_surface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Cloth simulation")

    # Points
    global Points
    Points = []

    rows, columns = 6, 11
    scale, offset = 2, 3

    for y in range(rows):
        for x in range(columns):
            if x % 2 == 0: # lock every second point
                Points.append(Point(offset + scale * x, offset + scale * y, True))
            else:
                #Points.append(Point())
                Points.append(Point(offset + scale * x, offset + scale * y))

    # Sticks
    global Sticks
    Sticks = []

    for i in range(len(Points) - 1):
        Sticks.append(Stick(Points[i], Points[i + 1], .01 + Vector2.distance(Points[i].pos, Points[i + 1].pos)))

    global clock
    clock = pygame.time.Clock()

def loop():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Physics
    for p in Points:
        p.move()
    
    for i in range(ITERATIONS):
        for s in Sticks:
            s.tether()

    # Graphics
    display_surface.fill(SCREEN_BACKGROUND) # Clear the screen first

    for p in Points:
        p.draw()
    
    for s in Sticks:
        s.draw()

    pygame.display.update()

    # Sleep
    clock.tick(1 / dT) # Limiting the framerate. Computes the time passed between two calls.

class Point():
    radius = 10
    max_x, max_y = SCREEN_SIZE[0] / SCREEN_SCALE, SCREEN_SIZE[1] / SCREEN_SCALE
    def __init__(self, x=None, y=None, locked=False):
        if x == None or y == None:
            self.pos = self.prev_pos = Vector2(x=random.random() * Point.max_x,
                                               y=random.random() * Point.max_y)
        else:
            self.pos = self.prev_pos = Vector2(x, y)
        self.locked = locked
    
    def move(self):
        if not self.locked:
            temp = self.pos
            self.pos += (self.pos - self.prev_pos) + Vector2.down() * g * dT * dT # velocity + gravity
            self.prev_pos = temp
    
    def draw(self):
        if not self.locked: color = WHITE
        else: color = RED
        
        center = pygame.Vector2((self.pos.x, self.pos.y))
        pygame.draw.circle(display_surface,
                           color,
                           SCREEN_SCALE * center,
                           Point.radius)

class Stick():
    width = 2
    def __init__(self, p1, p2, length):
        self.p1, self.p2 = p1, p2
        self.length = length
    
    def draw(self):
        start_pos = pygame.Vector2((self.p1.pos.x, self.p1.pos.y))
        end_pos = pygame.Vector2((self.p2.pos.x, self.p2.pos.y))
        pygame.draw.line(display_surface, WHITE, SCREEN_SCALE * start_pos, SCREEN_SCALE * end_pos, Stick.width)

    def tether(self):
        center = (self.p1.pos + self.p2.pos) * .5
        dir = Vector2.normalized(self.p1.pos - self.p2.pos)

        if Vector2.distance(self.p1.pos, self.p2.pos) > self.length:
            if not self.p1.locked:
                self.p1.pos = center + dir * self.length / 2
            if not self.p2.locked:
                self.p2.pos = center - dir * self.length / 2

class Player(pygame.sprite.Sprite): # We passed a class as an argument. The Player class will be derived from the Sprite class!
    # Class (~static) variables
    speed = 250
    colliderSize = (44, 96)

    def __init__(self):
        # Instance variables
        self.pos = Vector2(.5 * SCREEN_SIZE[0], .5 * SCREEN_SIZE[1]) # move to center

        super().__init__() # calls the init function in Sprite 
        self.image = pygame.image.load("Materials/Player.png")
        self.surf = pygame.Surface(Player.colliderSize) # create border
        self.rect = self.surf.get_rect()
 
    def input(self):
        # Read input
        pressed_keys = pygame.key.get_pressed()

        # Summarize input (+ boundaries)
        self.inputDir = Vector2.zero()
        
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.inputDir += Vector2.up()
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_SIZE[1]:
            self.inputDir += Vector2.down()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.inputDir += Vector2.left()
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_SIZE[0]:
            self.inputDir += Vector2.right()
        
        self.pos += self.inputDir.normalized() * Player.speed * dT

    def move(self):
        # Apply movement
        self.rect.move_ip(self.pos.x - self.rect.center[0], self.pos.y - self.rect.center[1])
        #self.rect.update(self.pos.x, self.pos.y, Player.colliderSize[0], Player.colliderSize[1])        
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     

def test_shapes():
    display_surface.fill(SCREEN_BACKGROUND)
    
    pygame.draw.line(display_surface, BLUE, (150,130), (130,170))
    pygame.draw.line(display_surface, BLUE, (150,130), (170,170))
    pygame.draw.line(display_surface, GREEN, (130,170), (170,170))
    pygame.draw.circle(display_surface, WHITE, (100,50), 30)
    pygame.draw.circle(display_surface, WHITE, (200,50), 30)
    pygame.draw.rect(display_surface, RED, (100, 200, 100, 50), 2)
    pygame.draw.rect(display_surface, WHITE, (110, 260, 80, 5))

    pygame.display.update()

def test_vector2():
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
    print()
    v7 = Vector2(-4.1, 3.2)
    v8 = Vector2(-4.1, 3.2)
    print('Distance between v7 and v8: ' + '{:.6f}'.format(Vector2.distance(v7, v8)))
    if v7 == v8:
        print('They are equal')
    else:
        print('They are different')
    print()
    print('v7 magnitude = ' + '{:.2f}'.format(v7.magnitude()))
    v8 = v7.normalized()
    v8.print('v8 = v7 normalized')
    v8 *= v7.magnitude()
    v8.print('v8 *= v7.magnitude')

if __name__ == "__main__": # If this section exists, this will be the entry point
    main()
