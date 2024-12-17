import pygame, sys
import json
from scripts.utils import load_images
from scripts.tilemap import Tilemap
RENDER_SCALE = 2.0

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300))
        self.clock = pygame.time.Clock()
        self.move = [False, False, False, False]

        self.assets = {
            "colliables" : load_images("colliables"),
            "flag" : load_images("flag"),
            "spawner" : load_images("spawner")
        }

        self.Tilemap = Tilemap(self, (0,0))
        self.tilelist = list(self.assets)
        self.tilegroup = 0
        self.tilevariant = 0

        self.size = [8,8]
        
        self.scroll = [0, 0]

        self.click = False
        self.rightclick = False
        self.shift = False
        self.ongrid = True
        self.ml = 0
        self.degrees = 0

        try:
            self.Tilemap.load(str(self.ml))
        except FileNotFoundError:
            print('nuh uh')
    
    def run(self):
        while True:
            self.display.fill((125, 125, 255))
            if self.tilelist[self.tilegroup] == "spawner":
                self.ongrid = False
            self.scroll[0] += (self.move[1] - self.move[0]) *2
            self.scroll[1] += (self.move[3] - self.move[2]) *2 
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            current_tile = pygame.transform.rotate(self.assets[self.tilelist[self.tilegroup]][self.tilevariant].copy(), self.degrees)
            current_tile.set_alpha(100)
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] /RENDER_SCALE, mpos[1]/RENDER_SCALE)
            tile_pos = int((mpos[0]+self.scroll[0])//self.Tilemap.tilesize), int((mpos[1]+self.scroll[1])//self.Tilemap.tilesize)
            if self.click and self.ongrid:
                self.Tilemap.tilemap[str(tile_pos[0]) +";" + str(tile_pos[1])] = {"degrees" : self.degrees, "type": self.tilelist[self.tilegroup], 'variant': self.tilevariant, "pos": tile_pos, "rects" : (tile_pos[0]*self.Tilemap.tilesize, tile_pos[1]*self.Tilemap.tilesize, self.size[0], self.size[1])}
            if self.rightclick:
                tile_loc = str(tile_pos[0]) + ";" + str(tile_pos[1])
                if tile_loc in self.Tilemap.tilemap:
                    del self.Tilemap.tilemap[tile_loc]
                for pos, tile in self.Tilemap.offgrid.copy().items():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.Tilemap.offgrid.pop(pos)
            self.Tilemap.render(self.display, render_scroll)
            if self.ongrid:
                self.display.blit(current_tile, (tile_pos[0]*self.Tilemap.tilesize-self.scroll[0], tile_pos[1]*self.Tilemap.tilesize-self.scroll[1]))
            else:
                self.display.blit(current_tile, mpos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                        if not self.ongrid:
                            self.Tilemap.offgrid[str(tile_pos[0])+";"+str(tile_pos[1])] = {"degrees": self.degrees, "type": self.tilelist[self.tilegroup], 'variant': self.tilevariant, "pos": (mpos[0]+self.scroll[0], mpos[1]+self.scroll[1]), "rects" : (mpos[0]+self.scroll[0], mpos[1]+self.scroll[1], self.size[0], self.size[1])}
                    if event.button == 3:
                        self.rightclick = True
                    if not self.shift:
                        if event.button == 4:
                            self.tilevariant = (self.tilevariant+1) % len(self.assets[self.tilelist[self.tilegroup]])
                        if event.button == 5:
                            self.tilevariant = (self.tilevariant-1) % len(self.assets[self.tilelist[self.tilegroup]])
                    else:
                        if event.button == 4:
                            self.tilevariant = 0
                            self.tilegroup = (self.tilegroup+1) % len(self.tilelist)
                        if event.button == 5:
                            self.tilevariant = 0
                            self.tilegroup = (self.tilegroup-1) % len(self.tilelist)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click = False
                    if event.button == 3:
                        self.rightclick = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.move[0] = True
                    if event.key == pygame.K_d:
                        self.move[1] = True
                    if event.key == pygame.K_w:
                        self.move[2] = True
                    if event.key == pygame.K_s:
                        self.move[3] = True
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.shift = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:
                        self.Tilemap.save(str(self.ml))
                    if event.key == pygame.K_q:
                        self.degrees = (self.degrees+90) % 360
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.move[0] = False
                    if event.key == pygame.K_d:
                        self.move[1] = False
                    if event.key == pygame.K_w:
                        self.move[2] = False
                    if event.key == pygame.K_s:
                        self.move[3] = False
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.shift = False
                    if event.key == pygame.K_LEFT:
                        self.ml = max(0, self.ml-1)
                        try:
                            self.Tilemap.load(self.ml)
                        except FileNotFoundError:
                            self.Tilemap.tilemap = {}
                            self.Tilemap.offgrid = {}
                    if event.key == pygame.K_RIGHT:
                        self.ml += 1
                        try:
                            self.Tilemap.load(str(self.ml))
                        except FileNotFoundError:
                            self.Tilemap.tilemap = {}
                            self.Tilemap.offgrid = {}
            pygame.display.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)

Game().run()