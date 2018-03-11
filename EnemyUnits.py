import pygame

from math import sqrt
from operator import pos

from Map import *


class EnemyUnit(pygame.sprite.Sprite):
    
    """ Vihollista kuvaava luokka """
 
    def __init__(self, starting_point, enemy_class, map, current_path_part_index, next_path_part_index):
        
        # Kutsuu parent-luokan (Sprite) konstruktoria
        super().__init__()
        
        # ALoituspiste
        self.starting_point = starting_point
        
        # Vihollisen kulkema matka
        self.move_distance = 0
        
        self.enemy_class = enemy_class
        self.map = map
        self.current_path_part_index = current_path_part_index
        self.next_path_part_index = next_path_part_index
        
        #Lataa vihollisen spriten 
        if self.enemy_class == "ball_1":
            self.image = pygame.image.load("ball_1.png")
        elif self.enemy_class == "ball_2":
            self.image = pygame.image.load("ball_2.png")
        elif self.enemy_class == "ball_3":
            self.image = pygame.image.load("ball_3.png")
        
        #Luo suorakulmaisen objektin jolla on ladatun spriten mitat. Sen paikkaa voi siirtaa 
        #maarittamalla koordinaatit rect.centerx ja rect.centery ja pygame piirtaa spriten tahan sijaintiin.
        self.rect = self.image.get_rect()
        self.rect.center = self.starting_point
        
        # Vihollisen vauhti
        self.speed = 1
         
        # Vihollisen nopeuden suunnan komponentit
        self.velocity_x = 0
        self.velocity_y = 0
        
        self.direction = None
        
        
    def enemy_unit_direction(self,current_path_part, next_path_part):
        """ Vihollisen suunta """
        
        self.current_path_part = current_path_part
        self.next_path_part = next_path_part
        
        
        if self.current_path_part[0] - self.next_path_part[0] == 0:
            if self.current_path_part[1] - self.next_path_part[1] > 0:
                self.direction = "up"
            else:
                self.direction = "down"
        
                
        elif self.current_path_part[1] - self.next_path_part[1] == 0:
            if self.current_path_part[0] - self.next_path_part[0] > 0:
                self.direction = "left"
            else:
                self.direction = "right"
                
        return self.direction
    
        
    def move_enemy_unit(self):
        """ Liikuttaa vihollista """
        
        # Liikkumissuunta
        if self.next_path_part_index < len(self.map.path):
            self.direction = self.enemy_unit_direction(self.map.path[self.current_path_part_index], self.map.path[self.next_path_part_index])
        
            self.path_part_indexes = self.get_path_part_index(self.map.path,self.map.path[self.current_path_part_index], self.map.path[self.next_path_part_index],self.direction)
        
            self.current_path_part_index = self.path_part_indexes[0]
            self.next_path_part_index = self.path_part_indexes[1]
        
        # Nopeusvektorit eri suuntiin
        if self.direction == "up":
            self.velocity_x = 0
            self.velocity_y = -self.speed
            
            if self.rect.centery <= self.next_path_part[1]+self.speed and self.rect.centery > self.next_path_part[1]:
                self.rect.centery = self.next_path_part[1]
                self.current_path_part_index += 1
                self.next_path_part_index += 1
            else:
                # Liikutetaan vihollista nopeusvektorin mukaisesti
                self.rect.centerx += self.velocity_x
                self.rect.centery += self.velocity_y
                
        if self.direction == "down":
            self.velocity_x = 0
            self.velocity_y = self.speed
            
            if self.rect.centery >= self.next_path_part[1]-self.speed and self.rect.centery < self.next_path_part[1]:
                self.rect.centery = self.next_path_part[1]
                self.current_path_part_index += 1
                self.next_path_part_index += 1
            else:
                self.rect.centerx += self.velocity_x
                self.rect.centery += self.velocity_y
            
        if self.direction == "left":
            self.velocity_x = -self.speed
            self.velocity_y = 0
            
            if self.rect.centerx <= self.next_path_part[0]-self.speed and self.rect.centerx > self.next_path_part[0]:
                self.rect.centerx = self.next_path_part[0]
                self.current_path_part_index += 1
                self.next_path_part_index += 1
            else:
                self.rect.centerx += self.velocity_x
                self.rect.centery += self.velocity_y
                
        if self.direction == "right":
            self.velocity_x = self.speed
            self.velocity_y = 0
            
            if self.rect.centerx >= self.next_path_part[0]-self.speed and self.rect.centerx < self.next_path_part[0]:
                self.rect.centerx = self.next_path_part[0]
                self.current_path_part_index += 1
                self.next_path_part_index += 1
            else:
                self.rect.centerx += self.velocity_x
                self.rect.centery += self.velocity_y
        
        # Kasvatetaan vihollisen kulkemaa matkaa
        self.move_distance += self.speed
        
        
    def get_path_part_index(self, path, current_path_part, next_path_part, direction):
        """ Haetaan polun koordinaattien listan indeksit """
        
        self.path = path
        self.current_path_part = current_path_part
        self.next_path_part = next_path_part
        self.direction = direction
        
        if self.direction == "up":
            if self.rect.centery <= self.next_path_part[1]:
                self.current_path_part_index = self.next_path_part_index
            
                if len(self.path) > self.next_path_part_index + 1:
                    self.next_path_part_index = self.next_path_part_index + 1
                    
                return [self.current_path_part_index,self.next_path_part_index]
            
            return [self.current_path_part_index,self.next_path_part_index]
        
        elif self.direction == "down":
            if self.rect.centery >= self.next_path_part[1]:
                self.current_path_part_index = self.next_path_part_index
            
                if len(self.path) > self.next_path_part_index + 1:
                    self.next_path_part_index = self.next_path_part_index + 1
                    
                return [self.current_path_part_index,self.next_path_part_index]
            
            return [self.current_path_part_index,self.next_path_part_index]
        
        elif self.direction == "left":
            if self.rect.centerx <= self.next_path_part[0]:
                self.current_path_part_index = self.next_path_part_index
            
                if len(self.path) > self.next_path_part_index + 1:
                    self.next_path_part_index = self.next_path_part_index + 1
                    
                return [self.current_path_part_index,self.next_path_part_index]
            
            return [self.current_path_part_index,self.next_path_part_index]
        
        elif self.direction == "right":
            if self.rect.centerx >= self.next_path_part[0]:
                self.current_path_part_index = self.next_path_part_index
            
                if len(self.path) > self.next_path_part_index + 1:
                    self.next_path_part_index = self.next_path_part_index + 1
                    
                return [self.current_path_part_index,self.next_path_part_index]
            
            return [self.current_path_part_index,self.next_path_part_index]
        
        else:
            return [self.current_path_part_index,self.next_path_part_index]
        
    def get_move_distance(self):
        """ Hakee vihollisen kulkeman matkan """
        return self.move_distance

class Effect(pygame.sprite.Sprite):
    """ Efektia kuvaava luokka """
    
    def __init__(self, location):
        
        # Kutsuu parent-luokan (Sprite) konstruktoria
        super().__init__()
        
        # Sijainti
        self.location = location
        # Sprite
        self.image = pygame.image.load("explosion.png")
        #Luo suorakulmaisen objektin jolla on ladatun spriten mitat. Sen paikkaa voi siirtaa 
        #maarittamalla koordinaatit rect.centerx ja rect.centery ja pygame piirtaa spriten tahan sijaintiin.
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        
        self.effect_duration = 12
        
        
class EnemyWave():
    """ Vihollisaaltoja kuvaava luokka """
    
    def __init__(self):
        
        self.wave_1 = [["ball_1",10]]
        self.wave_2 = [["ball_1",15]]
        self.wave_3 = [["ball_1",20]]
        self.wave_4 = [["ball_1",10],["ball_2",10]]
        self.wave_5 = [["ball_2",20]]
        self.wave_6 = [["ball_2",25],["ball_3",10]]
        self.wave_7 = [["ball_2",20],["ball_3",20]]
        self.wave_8 = [["ball_1",50],["ball_2",50]]
        self.wave_9 = [["ball_3",50]]
        self.wave_10 = [["ball_1",50],["ball_2",50],["ball_3",50]]
        
        self.wave_list = [self.wave_1,self.wave_2,self.wave_3,self.wave_4,self.wave_5,self.wave_6,self.wave_7,self.wave_8,self.wave_9,self.wave_10]
        self.wave_number = 0
        self.starting_wave_number = self.wave_number
        self.visible_wave_number = self.wave_number + 1
        self.starting_visible_wave_number = self.visible_wave_number
        self.wave_count = len(self.wave_list)
        self.spawn_interval = 20
        
    def get_wave(self, wave_number):
        """ Hakee vihollisaallon """
        return self.wave_list[self.wave_number]
    