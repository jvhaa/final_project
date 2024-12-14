# imports
import pygame
import sys
import time
import json

# imports from other files i created
from scripts.utils import load_image, load_images, Animation
from scripts.player import Player, Clone
from scripts.tilemap import Tilemap


# making game a class
class game:
    def __init__(self):
        #initializing all thing that are needed, music, audio, maps, screen, and time
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((self.screen.width/2, self.screen.height/2))
        self.clock = pygame.time.Clock()
        self.player = Player((0,0), (10, 20))
        self.camerapos = [0, 0]
        self.tilemap = Tilemap(self, self.player.size)
        self.gamestate = "game"
        self.tilemap.load(0)
        self.assets = {
            "colliables" : load_images("colliables")
        }
        self.movement = [False, False]
        self.starttime = time.time()
        self.lastmoved = time.time()
        self.moves = {}
        self.level = 0
        file = open("ais_moves/" + str(self.level)  + ".json")
        self.clone = Clone((0,0), (10, 20), json.load(file))
        file.close()

    # changes what game loop you are in : main menu, end screen, game, pause screen, etc
    def change_state(self):
        pass

    def Time(self):
        return time.time() - self.starttime

    #main loop that runs everything and handles what should be ran and what shouldn't
    def game_handler(self):
        #mouse position
        self.mousepos = pygame.mouse.get_pos()
        while True:
            self.click = False
            self.rightclick = False
            for event in pygame.event.get():
                # quits the game if you press the x mark
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if playing main games then look for movement controls
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.click = True

                if self.gamestate == "game":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.movement[0] = True # if pressing a move left
                            self.moves[self.Time()] = {"action" : "left", "passed": False}
                        if event.key == pygame.K_d:
                            self.movement[1] = True # if pressing d move right
                            self.moves[self.Time()] = {"action" : "right", "passed": False}
                        if event.key == pygame.K_w:
                            self.player.jump() # if pressing w jump
                            self.moves[self.Time()] = {"action" : "jump", "passed": False}
                        if event.key == pygame.K_q:
                            self.player.dash() # dashes if the player presses q
                            self.moves[self.Time()] = {"action" : "dash", "passed": False}
                        if event.key == pygame.K_e:
                            file = open("ais_moves/0.json", "w")
                            json.dump(self.moves, file)
                            file.close()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            self.movement[0] = False # if you let go of a stop moving left
                            self.moves[self.Time()] = {"action" : "right", "passed": False}
                        if event.key == pygame.K_d:
                            self.movement[1] = False # if you let go of d stop moving right
                            self.moves[self.Time()] = {"action" : "left", "passed": False}
            if self.gamestate == "game":
                self.game()


            self.screen.blit(pygame.transform.scale(self.display, self.screen.size), (0,0))
            pygame.display.flip()
            self.clock.tick(60)

    # the main game loop
    def game(self):
        self.display.fill((0,0,0))
        self.camerapos[0] += int((self.player.pos[0] - self.camerapos[0] - self.display.width//2)//20)
        self.camerapos[1] += int((self.player.pos[1] - self.camerapos[1] - self.display.height//2)//20)
        self.player.update(self.tilemap, ((self.movement[1] - self.movement[0])*2))
        self.player.render(self.display,self.camerapos)
        self.clone.update(self.tilemap, time.time()-self.starttime)
        self.clone.render(self.display, self.camerapos)
        self.tilemap.render(self.display, self.camerapos)

game().game_handler()