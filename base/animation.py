import pygame
import time

from config import animation_frame

class Animation():
    def __init__(self) -> None:
        self.start = 0
        self.end = 0 
        self.current = 0
        self.dt = 10
        self.count_dt = 0
        self.master_img = pygame.image.load("assets/animation.png")
        rect = self.master_img.get_rect()
        w = rect.width
        h = rect.height
        self.frame_w = w // 5
        self.frame_h = h // 3
        

    def set_state(self,state):
        if state not in animation_frame.keys():
            return 
        
        self.start = animation_frame[state][0]
        self.end = animation_frame[state][1]
        self.current = self.start

    def update(self):
        self.count_dt += 1
        if(self.count_dt == self.dt):
            self.count_dt = 0
            self.next_frame() 

    def next_frame(self):
        if self.current == self.end:
            self.current = self.start
        else:
            self.current = self.current + 1

    def get_sprite(self):
        row = self.current // 5
        col = int(int(self.current) % 5)
        surface = self.master_img.subsurface(col*self.frame_w,row*self.frame_h,self.frame_h,self.frame_h)
        surface = pygame.transform.scale(surface, (100,100))
        # surface = pygame.transform.flip(surface,xbool=True)
        return surface