import pygame

class Flag:
    def __init__(self, pos):
        self.pos = pos
        self.state = 0
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], 29, 29)

    def render(self, game, surf, camdiff):
        surf.blit(game.assets["flag"][self.state], (self.pos[0] - camdiff[0], self.pos[1] - camdiff[1]))
        if game.player.rect().colliderect(self.rect()) and self.state == 0:
            self.state = 1
        elif game.clone.rect().colliderect(self.rect()) and self.state == 0:
            self.state = 2