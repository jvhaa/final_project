# imports
import pygame
import sys

# imports from other files i created
from scripts.utils import load_image, load_images, Animation
from scripts.player import Player
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
        self.tilemap.load(1)
        self.assets = {
            "colliables" : load_images("colliables")
        }
        self.movement = [False, False]

    # changes what game loop you are in : main menu, end screen, game, pause screen, etc
    def change_state(self):
        pass

    #main loop that runs everything and handles what should be ran and what shouldn't
    def game_handler(self):
        #mouse position
        self.mousepos = pygame.mouse.get_pos()
        while True:
            for event in pygame.event.get():
                # quits the game if you press the x mark
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if playing main games then look for movement controls
                if self.gamestate == "game":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.movement[0] = True
                        if event.key == pygame.K_d:
                            self.movement[1] = True
                        if event.key == pygame.K_w:
                            self.player.vel[1] = -4
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            self.movement[0] = False
                        if event.key == pygame.K_d:
                            self.movement[1] = False
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
        self.tilemap.render(self.display, self.camerapos)

game().game_handler()