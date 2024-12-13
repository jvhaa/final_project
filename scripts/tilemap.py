import pygame
import json
physics_rects = "colliables"

class Tilemap:
    def __init__(self, game, playersize):
        # initializes tilemap
       self.game = game
       self.tilesize = 8
       self.neighbours = [(x, y) for x in range(-1, 4) for y in range(-1, 4)] 
       self.tilemap = {}
       self.offgrid = {}

    def tiles_around(self, pos):
        # returns the map objects that are close to this position
        tiles = []
        tile_loc = (int(pos[0]//self.tilesize), int(pos[1]//self.tilesize))
        for offset in self.neighbours:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1]) 
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
            if check_loc in self.offgrid:
                tiles.append(self.offgrid[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        # returns close map objects that be collisded with
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] == "colliables":
                x, y, width, height = tile["rects"]
                rects.append(pygame.Rect(x, y, width, height))
        return rects

    def render(self, surf, camdiff=(0,0)):
        #only renders those that are within view of the player
        for y in range(camdiff[1]//self.tilesize, (camdiff[1] + surf.height)//self.tilesize+1):
            for x in range(camdiff[0]//self.tilesize, (camdiff[0] + surf.width)//self.tilesize+1):
                loc = str(x) + ";" + str(y)
                if loc in self.offgrid:
                    tile = self.offgrid[loc]
                    surf.blit(pygame.transform.rotate(self.game.assets[tile["type"]][tile["variant"]], tile["degrees"]), (tile["pos"][0]-camdiff[0], tile["pos"][1]-camdiff[1]))
        for y in range(camdiff[1]//self.tilesize, (camdiff[1] + surf.height)//self.tilesize+1):
            for x in range(camdiff[0]//self.tilesize, (camdiff[0] + surf.width)//self.tilesize+1):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(pygame.transform.rotate(self.game.assets[tile["type"]][tile["variant"]], tile["degrees"]), (tile["pos"][0]*self.tilesize-camdiff[0], tile["pos"][1]*self.tilesize-camdiff[1]))

    def load(self, level):
        file = open("maps/" + str(level) + ".json", "r")
        world = json.load(file)
        file.close()
        self.tilemap = world["tilemap"]
        self.offgrid = world["offgrid"]

    def save(self, level):
        file = open("maps/" + str(level) + ".json", "w")
        json.dump({"tilemap" : self.tilemap, "offgrid" : self.offgrid}, file)
        file.close()