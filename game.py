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
    IMAGE = "Dog"
    SOLID = True

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {}

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



class Dog_house(GameElement):
    SOLID = True
    IMAGE = "DogHouse"
    def interact(self, player):
        have_bones = False
        bones = 0
        poo_picked_up = False
        for item in player.inventory:
            if type(item) == Bone:
                bones += 1
        if bones == 3:        
            have_bones = True

        for item in player.inventory:
            if type(item) == Poop:
                poo_picked_up = True
        if have_bones:
            if poo_picked_up:
                GAME_BOARD.draw_msg("You have successfully stashed your dog bones in your dog house!")
                #add stars and hearts as a congratulations
                star_positions = [(5, 0), (6, 4), (1, 6)]
                for pos in star_positions:
                    star = Star()
                    GAME_BOARD.register(star)
                    GAME_BOARD.set_el(pos[0],pos[1], star)

            else:
                GAME_BOARD.draw_msg("Be a good doggie and clean up your poo before you stash your dog bones.")
        else:
            if poo_picked_up:
                GAME_BOARD.draw_msg("Go collect your dog bones to stash in your dog house.")
            else:
                GAME_BOARD.draw_msg("Be a good doggie and clean up your poo. Then go collect your dog bones to stash in your dog house.")


class Item(GameElement):
    SOLID = False

    def interact(self, player):
        player.inventory[self] = player.inventory.get(self, 0 + 1)
        GAME_BOARD.draw_msg("You just picked up a %s!"%self.name)
        GAME_BOARD.del_el(self.x, self.y)

class Bone(Item):
    IMAGE = "Bone"
    name = "bone"

class Star(Item):
    SOLID = True
    name = "star"
    IMAGE = "Star"

class Bag(Item):
    IMAGE = "Bag"
    name = "bag"

class Poop(Item):
    IMAGE = "Poo"
    name = "poo"
    SOLID = True

    def interact(self, player):
        have_bag = False
        for item in player.inventory:
            if type(item) == Bag:
                have_bag = True
        if have_bag:
            GAME_BOARD.draw_msg("You have used your poop bag to pick up this poo!")
            GAME_BOARD.del_el(self.x, self.y)
            player.inventory[Bag] = None
            player.inventory[self] = 1
        else:
            GAME_BOARD.draw_msg("You need a poop bag to pick up this poo.")



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
    GAME_BOARD.draw_msg("Collect the bones and put them in your dog house! Don't forget to clean up after yourself.")
    global doggie
    
    doghouse = Dog_house()
    GAME_BOARD.register(doghouse)
    GAME_BOARD.set_el(0,1,doghouse)

    doggie = Dog()
    GAME_BOARD.register(doggie)
    GAME_BOARD.set_el(2,2, doggie)

    bone_positions = [(5, 0), (6, 4), (1, 6)]
    for pos in bone_positions:
        bone = Bone()
        GAME_BOARD.register(bone)
        GAME_BOARD.set_el(pos[0],pos[1], bone)

    bag = Bag()
    GAME_BOARD.register(bag)
    GAME_BOARD.set_el(7,0, bag)

    poop = Poop()
    GAME_BOARD.register(poop)
    GAME_BOARD.set_el(7,6, poop)
