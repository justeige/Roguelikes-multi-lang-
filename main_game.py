import libtcodpy as libtcod
import pygame

PLAYER_S = pygame.image.load("player.png")
WALL_S = pygame.image.load("wall.png")
FLOOR_S = pygame.image.load("floor.png")
CELL_W = 32
CELL_H = 32



class Tile:
    def __init__(self, block_path):
        self.block_path = block_path

def create_map():
    new_map = [[ Tile(False) for y in range(0, 20)] for x in range(0, 20)]
    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map

GAME_MAP = create_map()

class Actor:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self):
        MAIN_SURFACE.blit(self.sprite, (self.x * CELL_W, self.y * CELL_H))

    def move(self, dx, dy):
        if GAME_MAP[self.x + dx][self.y + dy].block_path == False:
            self.x += dx
            self.y += dy
    



def init():
    pygame.init()

    global MAIN_SURFACE, GAME_MAP, PLAYER
    GAME_W = 800
    GAME_H = 600

    MAIN_SURFACE = pygame.display.set_mode((GAME_W, GAME_H))
    PLAYER = Actor(0, 0, PLAYER_S)

def draw():
    global MAIN_SURFACE
    COLOR_BLACK = (0,     0,   0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GREY  = (100, 100, 100)

    COLOR_DEFAULT_BG = COLOR_GREY

    MAIN_SURFACE.fill(COLOR_DEFAULT_BG)
   

    for x in range(0, 20):
        for y in range(0, 20):
            if GAME_MAP[x][y].block_path == True:
                MAIN_SURFACE.blit(WALL_S, (x * CELL_W, y * CELL_H))
            else:
                MAIN_SURFACE.blit(FLOOR_S, (x * CELL_W, y * CELL_H))
    
    PLAYER.draw()
    
    pygame.display.flip()


def main_loop():

    is_running = True

    while is_running:

        # fetch input
        events = pygame.event.get()

        # process input
        for event in events:
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0, -1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0, 1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1, 0)

        # draw game
        draw()
    
    pygame.quit()
    exit()



if __name__ == '__main__':
    init()
    main_loop()