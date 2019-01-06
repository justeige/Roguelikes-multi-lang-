import libtcodpy as libtcod

class Tile:
    def __init__(self, is_walkable):
        self.is_walkable = is_walkable
        self.is_known = False

class World:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height

    def create_map(self):
        new_map = [[ Tile(True) for y in range(0, self.map_width)] for x in range(0, self.map_height)]
        new_map[10][10].is_walkable = False
        new_map[10][15].is_walkable = False

        # create a border around a screen
        for x in range(self.map_height):
            new_map[x][0].is_walkable = False
            new_map[x][self.map_width - 1].is_walkable = False

        for y in range(self.map_width):
            new_map[0][y].is_walkable = False
            new_map[self.map_height - 1][y].is_walkable = False

        fov = self.create_fov(new_map)
        return (new_map, fov)

    def create_fov(self, game_map):
        fov = libtcod.map_new(self.map_height, self.map_width)
        
        for y in range(self.map_width):
            for x in range(self.map_height):

                is_transparent = game_map[x][y].is_walkable == True # TODO everything that is walkable counts as transparent for now
                is_walkable = game_map[x][y].is_walkable

                libtcod.map_set_properties(fov, x, y, is_transparent, is_walkable)

        return fov