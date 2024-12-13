import pygame
class entity_object:
    def __init__(self, pos, size):
        self.pos = list(pos)
        self.size = size
        self.flip = False
        self.collisions = {
            "up" : False,
            "right" : False,
            "left" : False,
            "down": False
            }
        self.vel = [0, 0]

    def update(self, tilemap, xmovement = 0):
        self.collisions = {
            "up" : False,
            "right" : False,
            "left" : False,
            "down": False
            }

        if xmovement > 0:
            self.flip = False
        elif xmovement < 0:
            self.flip = True
        self.vel[1] = min(5, self.vel[1]+0.1)
        
        last_xmovement = xmovement + self.vel[0]

        self.pos[0] += last_xmovement

        for tile in tilemap.physics_rects_around(self.pos):
            if self.rect().colliderect(tile):
                if last_xmovement > 0:
                    self.pos[0] = tile.x - self.size[0]
                    self.collisions["right"] = True
                if last_xmovement < 0:
                    self.pos[0] = tile.x + tile.width
                    self.collisions["left"] = True
                self.vel[0] = 0

        self.pos[1] += self.vel[1]

        for tile in tilemap.physics_rects_around(self.pos):
            if self.rect().colliderect(tile):
                if self.vel[1] > 0:
                    self.pos[1] = tile.y - self.size[1]
                    self.collisions["down"] = True
                if self.vel[1] < 0:
                    self.pos[1] = tile.y + tile.height
                    self.collisions["up"] = True

        if self.collisions["down"] or self.collisions["up"]:
            self.vel[1] = 0


    def render(self, surf, camdiff=(0,0)):
        e_rect= self.rect()
        e_rect.x -= camdiff[0]
        e_rect.y -= camdiff[1]
        pygame.draw.rect(surf, (255, 0, 0), e_rect)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
class Player(entity_object):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.can_jump = False
        
    
    def update(self, tilemap, movement):
        return super().update(tilemap, movement)
    
    def render(self, surf, camdiff=(0, 0)):
        return super().render(surf, camdiff)