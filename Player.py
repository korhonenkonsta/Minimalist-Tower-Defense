import pygame

class Player():
    
    """ Pelaajaa kuvaava luokka, sisaltaa tarvittavat tietodot rahasta ym. """
    
    def __init__(self):
        
        self.gold = 100
        self.starting_gold = self.gold
        self.hp = 10
        self.starting_hp = self.hp