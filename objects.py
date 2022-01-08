__author__ = "Péter Kerekes"

import random
import numpy as np
import pygame
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
    
    def is_on_position(self, screen_pos):
        dist = Vector2.distance(self.pos, Vector2(screen_pos[0] / SCREEN_SCALE,
                                                  screen_pos[1] / SCREEN_SCALE))
        if dist < Point.radius / SCREEN_SCALE: return True
        else: return False
    
    @staticmethod
    def select_point(screen_pos):
        for p in Points:
            if p.is_on_position(screen_pos):
                return p
        return False

class Stick():
    width = 2
    def __init__(self, p1, p2, length=None):
        # Ordering. Instances can be compared more easily.
        if p2.pos.x < p1.pos.x: self.p1, self.p2 = p2, p1
        else: self.p1, self.p2 = p1, p2

        if length == None:
            self.length = Vector2.distance(self.p1.pos, self.p2.pos)
        else:
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
    
    def is_on_position(self, screen_pos):
        screen_pos /= SCREEN_SCALE

        # Is it in the rectangle of the stick?
        p1 = Vector2(min(self.p1.pos.x, self.p2.pos.x) - STICK_SELECT_TOLERANCE,
                     min(self.p1.pos.y, self.p2.pos.y) - STICK_SELECT_TOLERANCE)
        
        p2 = Vector2(max(self.p1.pos.x, self.p2.pos.x) + STICK_SELECT_TOLERANCE,
                     max(self.p1.pos.y, self.p2.pos.y) + STICK_SELECT_TOLERANCE)

        if screen_pos.x < p1.x or screen_pos.x > p2.x or screen_pos.y < p1.y or screen_pos.y > p2.y:
            return False
        
        # Is it on the stick?
        dist = (abs((self.p2.pos.x - self.p1.pos.x) * (self.p1.pos.y - screen_pos.y)
                    - (self.p1.pos.x - screen_pos.x) * (self.p2.pos.y - self.p1.pos.y))
                / np.sqrt(np.square(self.p2.pos.x - self.p1.pos.x) + np.square(self.p2.pos.y - self.p1.pos.y)))
        
        if dist < STICK_SELECT_THRESHOLD:
            return True

        return False
    
    @staticmethod
    def compare(p1, p2):
        if p2.pos.x < p1.pos.x: p1, p2 = p2, p1 # Ordering

        # Is there already a stick between the two points?
        for s in Sticks:
            if p1.pos == s.p1.pos and p2.pos == s.p2.pos:
                return True
        return False

    @staticmethod
    def cut_stick(screen_pos):
        i = 0
        while i < len(Sticks):
            if Sticks[i].is_on_position(screen_pos):
                Sticks[i].destroy()
                i = 0
            else:
                i += 1
