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
    # Input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            global Points
            pos = pygame.mouse.get_pos()

            if event.button == 1: # Left mouse button
                Points.append(Point(pos[0] / SCREEN_SCALE, pos[1] / SCREEN_SCALE, False))
                print('New floating point at (', pos[0], ', ', pos[1], ')')
            elif event.button == 3: # Right mouse button
                Points[5].destroy()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Physics
    for p in Points:
        p.move()
    
    for i in range(ITERATIONS):
        for s in Sticks:
            s.tether()
    
    i = 0
    while i < len(Points):
        if Points[i].is_out_of_bounds():
            Points[i].destroy()
            i = 0
        else:
            i += 1

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
    radius = 10 # Class variable (~static)
    max_x, max_y = SCREEN_SIZE[0] / SCREEN_SCALE, SCREEN_SIZE[1] / SCREEN_SCALE
    def __init__(self, x=None, y=None, locked=False):
        # Instance variables
        if x == None or y == None:
            self.pos = self.prev_pos = Vector2(x=random.random() * Point.max_x,
                                               y=random.random() * Point.max_y)
        else:
            self.pos = self.prev_pos = Vector2(x, y)
        self.locked = locked
    
    def destroy(self):
        # Destroy every attached stick
        i = 0
        while i < len(Sticks):
            if Sticks[i].p1 == self or Sticks[i].p2 == self:
                Sticks[i].destroy()
                i = 0
            else:
                i += 1

        # Remove from list
        print('Point destroyed at (', self.pos.x, ', ', self.pos.y, ')')
        global Points
        Points.remove(self)
    
    def move(self):
        if not self.locked:
            temp = self.pos
            self.pos += (self.pos - self.prev_pos) + Vector2.down() * g * dT * dT # velocity + gravity
            self.prev_pos = temp
    
    def is_out_of_bounds(self):
        if self.pos.x < 0 or self.pos.x > Point.max_x or self.pos.y < 0 or self.pos.y > Point.max_y:
            return True
        else:
            return False

    def draw(self):
        if not self.locked: color = WHITE
        else: color = RED
        
        pygame.draw.circle(display_surface,
                           color,
                           SCREEN_SCALE * pygame.Vector2((self.pos.x, self.pos.y)),
                           Point.radius)

class Stick():
    width = 2
    def __init__(self, p1, p2, length):
        self.p1, self.p2 = p1, p2
        self.length = length
    
    def destroy(self):
        # Remove from list
        global Sticks
        Sticks.remove(self)
    
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

if __name__ == "__main__": # If this section exists, this will be the entry point
    main()
