from enum import Enum
import libtcodpy as libtcod
import pygame

import color


CELL_W = 32
CELL_H = 32
MAP_X = 30
MAP_Y = 30

def random_move(step = 1):
    return (libtcod.random_get_int(0, -step, step), libtcod.random_get_int(0, -step, step))


class Tile:
    def __init__(self, is_walkable):
        self.is_walkable = is_walkable

def create_map():
    new_map = [[ Tile(True) for y in range(0, MAP_Y)] for x in range(0, MAP_X)]
    new_map[10][10].is_walkable = False
    new_map[10][15].is_walkable = False

    # create a border around a screen
    for x in range(MAP_X):
        new_map[x][0].is_walkable = False
        new_map[x][MAP_Y - 1].is_walkable = False

    for y in range(MAP_Y):
        new_map[0][y].is_walkable = False
        new_map[MAP_X - 1][y].is_walkable = False

    return new_map

class Strategy:
    '''
    This is an ememies strategy/AI for walking, attacking etc.
    '''
    def take_turn(self):
        #x, y = random_move()
        #self.owner.move(x, y)
        pass

class Actor:
    def __init__(self, x, y, sprite, surface, current_map, strategy = None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.surface = surface
        self.current_map = current_map
        self.strategy = strategy

        if strategy:
            strategy.owner = self

    def draw(self):
        self.surface.blit(self.sprite, (self.x * CELL_W, self.y * CELL_H))

    def move(self, dx, dy, objects):
        new_x = self.x + dx
        new_y = self.y + dy

        is_floor = (self.current_map[new_x][new_y].is_walkable == True)

        target = None

        for obj in objects:
            if obj is not self and obj.x == new_x and obj.y == new_y:
                target = obj
                break

        if is_floor and target is None:
            self.x = new_x
            self.y = new_y
    

class Creature:
    def __init__(self, name, hp = 10):
        self.name = name 
        self.hp = hp


class PlayerAction(Enum):
    Idle = 0
    Quit = 1
    Move = 2

class Game:
    def __init__(self, w, h):
        # variables
        self.is_running = True
        self.width = w
        self.heigth = h
        self.surface = pygame.display.set_mode((self.width, self.heigth))
        self.current_map = create_map()        

        # load sprites
        self.PLAYER_S = pygame.image.load("player.png")
        self.WALL_S = pygame.image.load("wall.png")
        self.FLOOR_S = pygame.image.load("floor.png")
        self.ENEMY_S = pygame.image.load("enemy.png")

        # create entities
        strat_test = Strategy()

        self.player = Actor(1, 1, self.PLAYER_S, self.surface, self.current_map)
        self.enemy = Actor(5, 10, self.ENEMY_S, self.surface, self.current_map, strat_test)

        # create a list of all entities
        self.entities = [self.player, self.enemy]

        pygame.init()

   
    
    def draw(self):

        self.surface.fill(color.DEFAULT_BG)
   
        self.draw_map()
    
        for e in self.entities:
            e.draw()
    
        pygame.display.flip() # update pygame's display


    def draw_map(self):
        for x in range(0, MAP_X):
            for y in range(0, MAP_Y):
                if self.current_map[x][y].is_walkable == True:
                    self.surface.blit(self.FLOOR_S, (x * CELL_W, y * CELL_H))                    
                else:
                    self.surface.blit(self.WALL_S, (x * CELL_W, y * CELL_H))
   

    def process_input(self):

        events = pygame.event.get()

        for event in events:

            # quit by pressing x on the window
            if event.type == pygame.QUIT:
                return PlayerAction.Quit

            if event.type == pygame.KEYDOWN:

                # alternative way of shutdown
                if event.key == pygame.K_ESCAPE:
                    return PlayerAction.Quit

                # movement
                if event.key == pygame.K_UP:
                    self.player.move(0, -1, self.entities)
                    return PlayerAction.Move

                if event.key == pygame.K_DOWN:
                    self.player.move(0, 1, self.entities)
                    return PlayerAction.Move

                if event.key == pygame.K_LEFT:
                    self.player.move(-1, 0, self.entities)
                    return PlayerAction.Move

                if event.key == pygame.K_RIGHT:
                    self.player.move(1, 0, self.entities)
                    return PlayerAction.Move
            
        # no specific key was struck - do nothing
        return PlayerAction.Idle



    def main_loop(self):

        while self.is_running:

            player_action = self.process_input()
           
            if player_action == PlayerAction.Quit:
                self.is_running = False

            if player_action != PlayerAction.Idle:
                for e in self.entities:
                    if e.strategy:
                        e.strategy.take_turn()

            self.draw()
    
        pygame.quit()
        exit()


