__author__ = "Péter Kerekes"

import pygame, sys
from pygame.locals import * # no "pygame.locals" prefix is needed

from config import *
from vector2 import Vector2
from objects import Point, Stick, Points, Sticks

States = {
  0: "PAUSE",
  1: "PLAY"
}

global creatingStick # The first point of the stick being created.
creatingStick = False

def main():
    init()
    while True:
        loop()

def init():
    pygame.init()
 
    # Setup display
    global display_surface # Create a global variable. If it already exists, then this is only required if we want to change its value.
    display_surface = pygame.display.set_mode(SCREEN_SIZE)

    # Texts
    pygame.display.set_caption("Cloth simulation")
    global font
    font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
    #print(pygame.font.get_fonts())
    #font = pygame.font.Font(print(pygame.font.match_font('couriernew')), FONT_SIZE)

    global state
    state = PAUSE

    global clock
    clock = pygame.time.Clock()

def loop():
    input()

    if state == PLAY:
        physics()
    
    graphics()

    # Sleep
    clock.tick(1 / dT) # Limiting the framerate. Computes the time passed between two calls.

def input():
    global state, Points, Sticks, creatingStick
    mousePos = pygame.mouse.get_pos()

    if state == PLAY and pygame.mouse.get_pressed()[0]:
        # Left Mouse Button is being held down.
        Stick.cut_stick(Vector2(mousePos[0], mousePos[1]))

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                global SCREEN_BACKGROUND
                if state == PAUSE:
                    state = PLAY
                    SCREEN_BACKGROUND = DARK_BLUE
                    print('Play!')
                else:
                    state = PAUSE
                    SCREEN_BACKGROUND = DEEP_BLUE
                    print('Pause!')
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_BUTTON and state == PAUSE:
            creatingStick = Point.select_point(mousePos)

        elif event.type == pygame.MOUSEBUTTONUP and state == PAUSE:
            if event.button == LEFT_MOUSE_BUTTON:
                if creatingStick:
                    point = Point.select_point(mousePos)

                    if point and point != creatingStick: # We found a second point!
                        if Stick.compare(creatingStick, point):
                            print('Stick already present. Cancelling.')
                            return
                        
                        Stick(creatingStick, point)
                        print('New stick!')
                    else:
                        print('Cancel stick creation.')

                    creatingStick = False
                else:
                    Point(mousePos[0] / SCREEN_SCALE, mousePos[1] / SCREEN_SCALE, False)
                    print('New floating point at (', mousePos[0], ', ', mousePos[1], ')')
            elif event.button == RIGHT_MOUSE_BUTTON:
                Point(mousePos[0] / SCREEN_SCALE, mousePos[1] / SCREEN_SCALE, True)
                print('New locked point at (', mousePos[0], ', ', mousePos[1], ')')

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

def physics():
    # Velocity, gravity
    for p in Points:
        p.move()
    
    # Tethering
    for i in range(TETHERING_ITERATIONS):
        for s in Sticks:
            s.tether()
    
    # Check boundaries
    i = 0
    while i < len(Points):
        if Points[i].is_out_of_bounds():
            Points[i].destroy()
            i = 0
        else:
            i += 1

def graphics():
    # Clear the screen first
    display_surface.fill(SCREEN_BACKGROUND)

    # Draw objects
    for p in Points:
        p.draw(display_surface)
    
    for s in Sticks:
        s.draw(display_surface)
    
    draw_instructions(display_surface)

    pygame.display.update()

def draw_instructions(display_surface):
    global line
    line = 0

    draw_text(display_surface, States[state])
    if state == PAUSE:
        draw_text(display_surface, 'Place floating points using the \'Left Mouse Button\'.')
        draw_text(display_surface, 'Place locked points using the \'Right Mouse Button\'.')
        draw_text(display_surface, 'Hold and drag the \'Left Mouse Button\' from point A to point B to create a stick.')
        draw_text(display_surface, 'Press \'Space\' to play!')
    else: # Play
        draw_text(display_surface, 'Hold and drag the \'Left Mouse Button\' to cut sticks.')
        draw_text(display_surface, 'Press \'Space\' to pause.')

def draw_text(display_surface, string):
    global line
    text = font.render(string, True, WHITE) # Text surface object
    textRect = text.get_rect() # Rectangle
    textRect.topleft = (FONT_OFFSET, FONT_OFFSET + line * FONT_SIZE)
    display_surface.blit(text, textRect)
    line += 1

if __name__ == "__main__": # If this section exists, this will be the entry point
    main()
