import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
doggie = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 7

class Dog(GameElement):
    IMAGE = "Heart"
    SOLID = True

    def next_pos(self, direction):
        if direction == "up":
            if self.y > 0:
                return (self.x, self.y-1)
            return (self.x, self.y)
        elif direction == "down":
            if self.y < GAME_HEIGHT - 1:
                return (self.x, self.y+1)
            return (self.x, self.y)
        elif direction == "left":
            if self.x > 0:
                return (self.x-1, self.y)
            return (self.x, self.y)
        elif direction == "right":
            if self.x < GAME_WIDTH - 1:
                return (self.x+1, self.y)
            return (self.x, self.y)
        return None

    def intereact(self, player):
        pass




####   End class definitions    ####
def keyboard_handler():
    global doggie
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
    elif KEYBOARD[key.DOWN]:
        direction = "down"
    elif KEYBOARD[key.LEFT]:
        direction = "left"
    elif KEYBOARD[key.RIGHT]:
        direction = "right"

    if direction:
        next_loc = doggie.next_pos(direction)
        next_x = next_loc[0]
        next_y = next_loc[1]

        existing_el = GAME_BOARD.get_el(next_x, next_y)
        
        if existing_el:
            existing_el.interact(doggie)
            if not existing_el.SOLID:
                GAME_BOARD.del_el(doggie.x, doggie.y)
                GAME_BOARD.set_el(next_x, next_y, doggie)
        elif existing_el == None or not existing_el.SOLID:
            GAME_BOARD.del_el(doggie.x, doggie.y)
            GAME_BOARD.set_el(next_x, next_y, doggie)

def initialize():
    global doggie
    doggie = Dog()
    GAME_BOARD.register(doggie)
    GAME_BOARD.set_el(2,2, doggie)

