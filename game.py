from enum import Enum
import libtcodpy as libtcod
import pygame

import console
import color
import world


CELL_W = 32
CELL_H = 32
MAP_X = 30
MAP_Y = 30

def random_move(step = 1):
    return (libtcod.random_get_int(0, -step, step), libtcod.random_get_int(0, -step, step))







class Strategy:
    '''
    This is an ememies strategy/AI for walking, attacking etc.
    '''
    def take_turn(self, entities):
        x, y = random_move()
        self.owner.move(x, y, entities)
        #pass

cmd = console.Console(color.BLACK)

class Actor:
    def __init__(self, x, y, sprite, current_map, current_fov, strategy = None, creature = None):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.current_map = current_map
        self.current_fov = current_fov
        self.strategy = strategy
        self.creature = creature

        if strategy:
            strategy.owner = self


    def draw(self, surface):
        is_visible = libtcod.map_is_in_fov(self.current_fov, self.x, self.y)
        if is_visible:
            surface.blit(self.sprite, (self.x * CELL_W, self.y * CELL_H))

    def move(self, dx, dy, objects):
        new_x = self.x + dx
        new_y = self.y + dy

        is_floor = (self.current_map[new_x][new_y].is_walkable == True)

        target = None

        for obj in objects:
            if obj is not self and obj.x == new_x and obj.y == new_y:
                target = obj
                break
        
        if target:
            cmd.message(self.creature.name + " hit " + target.creature.name)
            target.creature.take_dmg(5)

        if is_floor and target is None:
            self.x = new_x
            self.y = new_y
    



class Creature:
    def __init__(self, name, hp = 10, death_handler = None):
        self.name = name 
        self.hp = hp # current hp
        self.max_hp = hp # max available hp
        self.death_handler = death_handler # how is the death of the creature handled?

    def take_dmg(self, damage):
        self.hp -= damage
        cmd.message(self.name + " took " + str(damage) + " damage (" + str(self.hp) + "/" + str(self.max_hp) + ")")

        if self.hp <= 0:
            if self.death_handler is not None:
                self.death_handler(self)

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
        self.world = world.World(MAP_X, MAP_Y)
        self.current_map, self.current_fov = self.world.create_map()
        self.new_fov = True
        self.messages = []

        # load sprites
        self.PLAYER_S = pygame.image.load("player.png")
        self.WALL_S = pygame.image.load("wall.png")
        self.FLOOR_S = pygame.image.load("floor.png")
        self.ENEMY_S = pygame.image.load("enemy.png")
        self.WALL_SHADOW_S = pygame.image.load("wall_shadow.png")
        self.FLOOR_SHADOW_S = pygame.image.load("floor_shadow.png")

        # create entities
        strat_test = Strategy()
        devil = Creature("Small devil", 10, self.default_death)
        human = Creature("Player", 200, self.default_death)

        self.player = Actor(1, 1, self.PLAYER_S, self.current_map, self.current_fov, None, human)
        self.enemy = Actor(5, 10, self.ENEMY_S, self.current_map, self.current_fov, strat_test, devil)

        # create a list of all entities
        self.actors = [self.player, self.enemy]

        # create a test message # TODO change!!
        cmd.message('hello world!')

        pygame.init()

    def default_death(self, entity):
        cmd.message(entity.name + " died!")
        self.actors.remove(self.enemy) # TODO remove hack!
    
    def calculate_new_fov(self):
        if self.new_fov:
            self.new_fov = False
            x, y = self.player.x, self.player.y
            torch_radius = 10
            libtcod.map_compute_fov(self.current_fov, x, y, torch_radius, True, libtcod.FOV_BASIC)


    def draw(self):

        self.surface.fill(color.DEFAULT_BG)
   
        self.draw_map()
    
        for a in self.actors:
            a.draw(self.surface)
    
        cmd.draw_messages(self.heigth, self.surface)

        pygame.display.flip() # update pygame's display


    def draw_map(self):
        for x in range(0, MAP_X):
            for y in range(0, MAP_Y):

                is_visible = libtcod.map_is_in_fov(self.current_fov, x, y)
                is_known = self.current_map[x][y].is_known # tile was explored once

                if is_visible:

                    self.current_map[x][y].is_known = True

                    if self.current_map[x][y].is_walkable == True:
                        self.surface.blit(self.FLOOR_S, (x * CELL_W, y * CELL_H))                    
                    else:
                        self.surface.blit(self.WALL_S, (x * CELL_W, y * CELL_H))

                else:
                    if is_known:
                        if self.current_map[x][y].is_walkable == True:
                            self.surface.blit(self.FLOOR_SHADOW_S, (x * CELL_W, y * CELL_H))                    
                        else:
                            self.surface.blit(self.WALL_SHADOW_S, (x * CELL_W, y * CELL_H))


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
                    self.player.move(0, -1, self.actors)
                    return PlayerAction.Move

                if event.key == pygame.K_DOWN:
                    self.player.move(0, 1, self.actors)
                    return PlayerAction.Move

                if event.key == pygame.K_LEFT:
                    self.player.move(-1, 0, self.actors)
                    return PlayerAction.Move

                if event.key == pygame.K_RIGHT:
                    self.player.move(1, 0, self.actors)
                    return PlayerAction.Move
            
        # no specific key was struck - do nothing
        return PlayerAction.Idle


    def main_loop(self):

        self.calculate_new_fov()

        while self.is_running:

            player_action = self.process_input()

            self.new_fov = (player_action == PlayerAction.Move)
            self.calculate_new_fov()
           
            if player_action == PlayerAction.Quit:
                self.is_running = False

            if player_action != PlayerAction.Idle:
                for a in self.actors:
                    if a.strategy:
                        a.strategy.take_turn(self.actors)

            self.draw()
    
        pygame.quit()
        exit()


