import pygame
import os
from scripts.loadfile import get_file

baselink = "assets/"

#loads a image given the address
def load_image(path):
    return pygame.image.load(get_file(baselink +path)).convert_alpha()

# loads multiple images given a folder
def load_images(path):
    images = []
    arr = os.listdir(get_file(baselink +path))
    arr = sorted(arr, key= lambda x: int(x.split(".")[0]))
    for img in arr:
        images.append(load_image(path + "/" + img))
    return images

# creates an aniamtion based on given images 
class Animation:
    def __init__(self, images, img_dur = 5, loop = True):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frames = 0

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)
    
    def update(self):
        if self.loop:
            self.frames = (self.frames+1) % (self.img_dur*len(self.images))
        else:
            self.frames = min(self.frames+1 , self.img_dur * len(self.images)-1)
            if self.frames >= self.img_dur * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frames/ self.img_dur)]