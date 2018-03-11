import pygame

from math import sqrt
from operator import pos

# Vareja
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

class Map():
    """ Kenttaa kuvaava luokka """
    
    def __init__(self):
        
        self.hud = pygame.image.load("hud.png")
        self.screen_width = 1024
        self.screen_height = 576
        self.screen_marginal = 30
        # Reitti
        self.path = [[100,-self.screen_marginal],[100,0],[100,150],[400,150],[400,350],[500,350],[500,150],[600,150],[600,500],[0,500],[-self.screen_marginal,500]]
        # Vaihtoehtoisia reitteja
        #self.path = [[100,-self.screen_marginal],[100,0],[100,150],[400,150],[400,350],[500,350],[500,150],[600,150],[600,self.screen_height],[600,self.screen_height+self.screen_marginal]]
        #self.path = [[100,-self.screen_marginal],[100,0],[100,150],[400,150],[400,350],[500,350],[500,150],[700,150],[700,80],[600,80],[600,0],[600,-self.screen_marginal]]
    
    def draw_path(self):
        """ Piirtaa polun """
        
        self.path_width = 50
        self.inner_path_width = 46
        self.path_index = 0
        self.path_hitbox_list = []
        
        # Piirretaan polun musta osuus (reunat)
        while self.path_index <= len(self.path) - 2:
            x1 = self.path[self.path_index][0]
            y1 = self.path[self.path_index][1]
            x2 = self.path[self.path_index + 1][0]
            y2 = self.path[self.path_index + 1][1]
            
            if x2 > x1:
                self.path_rect = pygame.Rect(x1,y1,(x2-x1),self.path_width)
                self.path_rect.midleft = [x1,y1]
            elif y2 > y1:
                self.path_rect = pygame.Rect(x1,y1,self.path_width,(y2-y1))
                self.path_rect.midtop = [x1,y1]
            elif x2 < x1:
                self.path_rect = pygame.Rect(x1,y1,(x1-x2),self.path_width)
                self.path_rect.midright = [x1,y1]
            elif y2 < y1:
                self.path_rect = pygame.Rect(x1,y1,self.path_width,(y1-y2))
                self.path_rect.midbottom = [x1,y1]
            
            self.path_hitbox_list.append(self.path_rect)
            self.hud.fill(BLACK,self.path_rect)
            
            # Taytetaan reitin kulmat
            self.corner_rect = pygame.Rect(x1,y1,self.path_width,self.path_width)
            self.corner_rect.center = (x1,y1)
            self.hud.fill(BLACK,self.corner_rect)
            self.path_hitbox_list.append(self.corner_rect)
            self.path_index += 1
            
        self.path_index = 0
        
        # Piirretaan polun valkoinen osuus
        while self.path_index <= len(self.path) - 2:
            x1 = self.path[self.path_index][0]
            y1 = self.path[self.path_index][1]
            x2 = self.path[self.path_index + 1][0]
            y2 = self.path[self.path_index + 1][1]
            
            if x2 > x1:
                self.path_rect = pygame.Rect(x1,y1,(x2-x1),self.inner_path_width)
                self.path_rect.midleft = [x1,y1]
            elif y2 > y1:
                self.path_rect = pygame.Rect(x1,y1,self.inner_path_width,(y2-y1))
                self.path_rect.midtop = [x1,y1]
            elif x2 < x1:
                self.path_rect = pygame.Rect(x1,y1,(x1-x2),self.inner_path_width)
                self.path_rect.midright = [x1,y1]
            elif y2 < y1:
                self.path_rect = pygame.Rect(x1,y1,self.inner_path_width,(y1-y2))
                self.path_rect.midbottom = [x1,y1]
            
            self.hud.fill(WHITE,self.path_rect)
            
            # Taytetaan reitin kulmat
            self.corner_rect = pygame.Rect(x1,y1,self.inner_path_width,self.inner_path_width)
            self.corner_rect.center = (x1,y1)
            self.hud.fill(WHITE,self.corner_rect)
            self.path_index += 1
        
        