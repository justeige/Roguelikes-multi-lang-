import libtcodpy as libtcod
import pygame

import color


CELL_W = 32
CELL_H = 32



class Tile:
    def __init__(self, is_walkable):
        self.is_walkable = is_walkable

def create_map():
    new_map = [[ Tile(True) for y in range(0, 20)] for x in range(0, 20)]
    new_map[10][10].is_walkable = False
    new_map[10][15].is_walkable = False

    return new_map



class Actor:
    def __init__(self, x, y, sprite, surface, current_map):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.surface = surface
        self.current_map = current_map

    def draw(self):
        self.surface.blit(self.sprite, (self.x * CELL_W, self.y * CELL_H))

    def move(self, dx, dy):
        if self.current_map[self.x + dx][self.y + dy].is_walkable == True:
            self.x += dx
            self.y += dy
    

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

        # create entities
        self.player = Actor(0, 0, self.PLAYER_S, self.surface, self.current_map)

        pygame.init()

    def draw(self):

        self.surface.fill(color.DEFAULT_BG)
   
        for x in range(0, 20):
            for y in range(0, 20):
                if self.current_map[x][y].is_walkable == True:
                    self.surface.blit(self.FLOOR_S, (x * CELL_W, y * CELL_H))                    
                else:
                    self.surface.blit(self.WALL_S, (x * CELL_W, y * CELL_H))
    
        self.player.draw()
    
        pygame.display.flip() # update pygame's display


    def main_loop(self):

        while self.is_running:

            # fetch input
            events = pygame.event.get()

            # process input
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:

                    # alternative way of shutdown
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        continue

                    if event.key == pygame.K_UP:
                        self.player.move(0, -1)
                    if event.key == pygame.K_DOWN:
                        self.player.move(0, 1)
                    if event.key == pygame.K_LEFT:
                        self.player.move(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.player.move(1, 0)

            # draw game
            self.draw()
    
        pygame.quit()
        exit()


