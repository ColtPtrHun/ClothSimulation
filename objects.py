__author__ = "Péter Kerekes"

import pygame
import random
from pygame.locals import * # no "pygame.locals" prefix is needed

from config import *
from vector2 import Vector2 # Vector2 class from vector2 module

global Points
Points = []
global Sticks
Sticks = []

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

        # Add to list
        global Points
        Points.append(self)
    
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

    def draw(self, display_surface):
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

        # Add to list
        global Sticks
        Sticks.append(self)
    
    def destroy(self):
        # Remove from list
        global Sticks
        Sticks.remove(self)
    
    def draw(self, display_surface):
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