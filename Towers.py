import pygame

from math import sqrt
from operator import pos

class Tower(pygame.sprite.Sprite):
    
    """ Tornia kuvaava luokka """

    def __init__(self, location, tower_class):
 
        # Kutsuu parent-luokan (Sprite) konstruktoria
        super().__init__()
        self.tower_class = tower_class
        self.tower_class_stats = TowerClassStats(self.tower_class)
        
        if self.tower_class == "basic tower":
            #Lataa tornin spriten
            self.image = self.tower_class_stats.get_tower_class_image()
            self.reload_time = self.tower_class_stats.get_tower_class_reload_time()
            self.range = self.tower_class_stats.get_tower_class_range()
            self.price = self.tower_class_stats.get_tower_class_price()
            self.upgrade_price = self.tower_class_stats.get_tower_class_upgrade_price()
            self.bullet_type = self.tower_class_stats.get_tower_class_bullet_type()
            self.tower_info = self.tower_class_stats.get_tower_class_info()
            
        elif self.tower_class == "piercing tower":
            #Lataa tornin spriten
            self.image = self.tower_class_stats.get_tower_class_image()
            self.reload_time = self.tower_class_stats.get_tower_class_reload_time()
            self.range = self.tower_class_stats.get_tower_class_range()
            self.price = self.tower_class_stats.get_tower_class_price()
            self.upgrade_price = self.tower_class_stats.get_tower_class_upgrade_price()
            self.bullet_type = self.tower_class_stats.get_tower_class_bullet_type()
            self.tower_info = self.tower_class_stats.get_tower_class_info()
        
        self.location = location
        self.reload = 0
        self.distance_to_enemy = None
        self.level = 1
        #Luo suorakulmaisen objektin jolla on ladatun spriten mitat. Sen paikkaa voi siirtaa 
        #maarittamalla koordinaatit rect.centerx ja rect.centery ja pygame piirtaa spriten tahan sijaintiin.
        self.rect = self.image.get_rect()
        
        # Asettaa tornin aloitussijainnin
        self.rect.centerx = self.location[0]
        self.rect.centery = self.location[1]
            
        self.bullet_list = []
        
    def fire(self, target):
        """ Ampuminen """
        
        self.target = target
        self.bullet = Bullet([self.rect.centerx, self.rect.centery] , self.target, self.bullet_type)
        self.bullet_list.append(self.bullet)
        self.reload = self.reload_time
    
    def get_target(self, enemy_list, tower):
        """ Haetaan kohde """
        
        self.enemy_list = enemy_list
        self.tower = tower
        self.enemies_in_range_list = []
        self.target = None
        
        for enemy in self.enemy_list:
            self.distance_to_enemy = sqrt((self.tower.rect.centerx-enemy.rect.centerx)**2+(self.tower.rect.centery-enemy.rect.centery)**2)
            if self.distance_to_enemy <= self.range:
                self.enemies_in_range_list.append(enemy)
        if len(self.enemies_in_range_list) > 0:
            self.target = self.enemies_in_range_list[0]
        
        for enemy in self.enemies_in_range_list:
            self.distance_to_enemy = sqrt((self.tower.rect.centerx-enemy.rect.centerx)**2+(self.tower.rect.centery-enemy.rect.centery)**2)
            if enemy.move_distance > self.target.move_distance:
                self.target = enemy
        
        return self.target
        
    def upgrade(self, player):
        """ Tornin kehitys """
        
        self.level += 1
        self.reload_time -= 40
        player.gold -= self.upgrade_price

    def sell_tower(self, player):
        """ Myynti """
        
        self.kill()
        player.gold += self.price
    

class TowerClassStats():
    
    """ Tornityyppien tiedot """

    def __init__(self, tower_class):
        
        self.tower_class = tower_class
        
        if self.tower_class == "basic tower":
            self.image = pygame.image.load("ball_3.png")
            self.range = 150
            self.reload_time = 180
            self.price = 10
            self.upgrade_price = 10
            self.bullet_type = "basic"
            self.tower_info = "Basic tower"
        elif self.tower_class == "piercing tower":
            self.image = pygame.image.load("piercing_tower.png")
            self.range = 200
            self.reload_time = 240
            self.price = 25
            self.upgrade_price = 25
            self.bullet_type = "piercing"
            self.tower_info = "Piercing tower"
            
    def get_tower_class_image(self):
        return self.image
    
    def get_tower_class_range(self):
        return self.range
    
    def get_tower_class_reload_time(self):
        return self.reload_time
    
    def get_tower_class_bullet_type(self):
        return self.bullet_type
    
    def get_tower_class_price(self):
        return self.price
    
    def get_tower_class_upgrade_price(self):
        return self.upgrade_price
    
    def get_tower_class_info(self):
        return self.tower_info
        

class Builder(pygame.sprite.Sprite): 
    
    """ Tornin valinta ja rakentaminen tiettyy sijaintiin """
    
    def __init__(self, location, tower_class): 
        
        super().__init__()
        
        self.location = location
        self.tower_class = tower_class
        self.tower_class_stats = TowerClassStats(self.tower_class)
        
        if self.tower_class == "basic tower":
            self.image = self.tower_class_stats.get_tower_class_image()
            self.level = 1
            self.range = self.tower_class_stats.get_tower_class_range()
            self.price = self.tower_class_stats.get_tower_class_price()
            self.upgrade_price = self.tower_class_stats.get_tower_class_upgrade_price()
            self.reload_time = self.tower_class_stats.get_tower_class_reload_time()
            self.tower_info = self.tower_class_stats.get_tower_class_info()
        elif self.tower_class == "piercing tower":
            self.image = self.tower_class_stats.get_tower_class_image()
            self.level = 1
            self.range = self.tower_class_stats.get_tower_class_range()
            self.price = self.tower_class_stats.get_tower_class_price()
            self.upgrade_price = self.tower_class_stats.get_tower_class_upgrade_price()
            self.reload_time = self.tower_class_stats.get_tower_class_reload_time()
            self.tower_info = self.tower_class_stats.get_tower_class_info()
            
        self.rect = self.image.get_rect()
        self.rect.center = location

    def move(self, location):
        
        self.location = location
        self.rect.center = self.location


class Bullet(pygame.sprite.Sprite):
    
    """ Ammusta kuvaava luokka  """
    
    def __init__(self, location, target, bullet_type):
        
        self.bullet_type = bullet_type
        if self.bullet_type == "basic":
            
            # Lataa ammuksen spriten
            self.image = pygame.image.load("basic_bullet.png")
            
        elif self.bullet_type == "piercing":
            
            # Lataa ammuksen spriten
            self.image = pygame.image.load("piercing_bullet.png")
        
        # Luo suorakulmaisen objektin jolla on ladatun spriten mitat. Sen paikkaa voi siirtaa 
        # maarittamalla koordinaatit rect.centerx ja rect.centery ja pygame piirtaa spriten tahan sijaintiin.
        self.rect = self.image.get_rect()
        # Sijainti
        self.location = location
        self.rect.centerx = self.location[0]
        self.rect.centery = self.location[1]
        
        self.target = target
        self.target_is_destroyed = True
        
        self.previous_direction = [0,0]
        
        # Kutsuu parent-luokan (Sprite) konstruktoria
        super().__init__()
        
        # Ammuksen vauhti
        self.speed = 2
        # Ammuksen nopeuden suunnan komponentit
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Ammuksen kulkema matka
        self.move_distance = 0
        # Ammuksen elossaoloaika
        self.lifetime = 0
        
 
    def bullet_direction(self):
        """ Ammuksen suunta """
        
        # Nopeusvektorin paatepisteet
        velocity_vector_a = pygame.math.Vector2(self.rect.centerx,self.rect.centery)
        velocity_vector_b = pygame.math.Vector2(self.target.rect.centerx,self.target.rect.centery)
        # Pisteiden a ja b (tornin ja kohteen) valinen nopeusvektori
        velocity_vector_a_b = velocity_vector_b - velocity_vector_a
        # Laskee nopeusvektori velocity_vector_a_b:n suuntaisen yksikkovektorin
        n_velocity_vector_a_b = pygame.math.Vector2.normalize(velocity_vector_a_b)
        # Palauttaa ammuksesta kohteesen osoittavan yksikkovektorin eli suunnan ammukselle
        return n_velocity_vector_a_b
    
    
    def get_bullet_direction(self, target, enemy_units):
        """ Hakee ammuksen suunnan """
        
        # Kohde, jota ammutaan
        self.target = target
        # Lista kentalla olevista vihollisista
        self.enemy_units = enemy_units
        
        # Jos kohde on olemassa 
        if self.target in self.enemy_units:
            # Asettaa suunnan
            self.direction = self.bullet_direction()
            self.previous_direction = self.direction
            self.target_is_destroyed = False
            return self.direction
        elif self.target_is_destroyed == True: # Jos kohde ei enaa ole olemassa
            return self.target_is_destroyed
        else:
            return self.previous_direction
        
    
    def move_bullet(self, n_vector):
        """ Liikuttaa ammusta """
        
        # Saa parametrina suunnan eli ammuksesta kohteesen osoittavan yksikkovektorin
        self.n_vector = n_vector
        
        # Suunnan x-suuntainen komponentti kerrotaan ammuksen vauhdilla
        self.velocity_x += (self.n_vector[0] * self.speed)
        # Suunnan y-suuntainen komponentti kerrotaan ammuksen vauhdilla
        self.velocity_y += (self.n_vector[1] * self.speed)
        
        # Liikutetaan ammusta nopeusvektorin mukaisesti
        self.rect.centerx += self.velocity_x
        self.rect.centery += self.velocity_y
        
        # Paivitetaan ammuksen kulkema matka ja aika
        self.move_distance += self.speed
        self.lifetime += 1

