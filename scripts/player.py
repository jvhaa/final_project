import pygame
class entity_object:
    def __init__(self, pos, size):
        self.pos = list(pos)
        self.size = size
        self.flip = False
        self.last_movement = (0,0)
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
        if self.vel[0] > 0:
            self.vel[0] = max(0, self.vel[0]-0.1)
        if self.vel[0] < 0:
            self.vel[0] = min(0, self.vel[0]+0.1)
        
        last_xmovement = xmovement + self.vel[0]
        
        self.last_movement = (last_xmovement, self.vel[1])

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
            self.air_time = 0


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
        self.dashing = 0
        self.dashcharge = 50
        self.dashtime = 10
        self.can_jump = True
        self.air_time = 0
    
    def update(self, tilemap, movement):
        super().update(tilemap, movement)
        if self.collisions["down"]:
            self.can_jump = True
            self.air_time = 0
        if self.collisions["right"] and self.last_movement[0] > 0 and self.air_time>0:
            self.vel[1] = min(1, self.vel[1])
        if self.collisions["left"] and self.last_movement[0] < 0 and self.air_time>0:
            self.vel[1] = min(1, self.vel[1])
        if self.dashing > 0:
            self.dashing = max(0, self.dashing-1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing+1)
        if abs(self.dashing) > self.dashcharge:
            self.vel[0] = (self.dashing // abs(self.dashing))*8
            if abs(self.dashing) == self.dashcharge+1:
                self.vel[0] //= 16

    
    def render(self, surf, camdiff=(0, 0)):
        return super().render(surf, camdiff)
    
    def jump(self):
        if self.collisions["right"] and self.last_movement[0] >0 and self.air_time >0:
            self.vel = [-5, -3]
            self.can_jump = False
        elif self.collisions["left"] and self.last_movement[0] < 0 and self.air_time > 0:
            self.vel = [5, -3]
            self.can_jump = False
        elif self.can_jump:
            self.vel[1] = -4
            self.can_jump = False
            self.air_time = 1
    
    def dash(self):
        if self.dashing == 0:
            self.dashing = (self.dashcharge + self.dashtime) * (-1 if self.flip else 1)
            print(self.dashing)

class Clone(Player):
    def __init__(self, pos, size, moves):
        super().__init__(pos, size)
        self.moves = moves
        self.movement = 0

    def update(self, tilemap, time):
        for move in self.moves:
            timelim = float(move)
            if timelim <= time+0.1 and self.moves[move]["passed"] == False:
                self.moves[move]["passed"] = True
                action = self.moves[move]["action"]
                if action == "dash":
                    self.dash()
                elif action == "jump":
                    self.jump()
                elif action == "left":
                    self.movement -= 2
                elif action == "right":
                    self.movement += 2

        return super().update(tilemap, self.movement)


    def render(self, surf, camdiff=(0, 0)):
        return super().render(surf, camdiff)