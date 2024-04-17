import pygame
from os import getcwd
from os.path import join

class Note(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((45,45),pygame.SRCALPHA) #wymiary notatki
        note_img = pygame.image.load(join(getcwd(),'items', 'notatka.png')) #wgraj zdjęcie notatki
        self.image.blit(note_img, (0,0)) #ustaw wyglad notatki
        self.rect = self.image.get_rect(topleft = pos) 
    
    def update(self,x_shift): # x_shift-->world_shift szybkosc i kierunek przesuwania
        self.rect.x += x_shift

class Coffee(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((38,45),pygame.SRCALPHA) #wymiary kawy
        note_img = pygame.image.load(join(getcwd(),'items', 'kawa.png')) #wgraj zdjęcie notatki
        self.image.blit(note_img, (0,0)) #ustaw wyglad kawy
        self.rect = self.image.get_rect(topleft = pos) 

    def update(self,x_shift): # x_shift-->world_shift szybkosc i kierunek przesuwania
        self.rect.x += x_shift

class EnergyDrink(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((45,45),pygame.SRCALPHA) #wymiary 
        note_img = pygame.image.load(join(getcwd(),'items', 'monsterek.png')) #wgraj zdjęcie
        self.image.blit(note_img, (0,0)) #ustaw wyglad 
        self.rect = self.image.get_rect(topleft = pos) 

    def update(self,x_shift): # x_shift-->world_shift szybkosc i kierunek przesuwania
        self.rect.x += x_shift

class Beer(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((45,45),pygame.SRCALPHA) #wymiary 
        note_img = pygame.image.load(join(getcwd(),'items', 'piwo.png')) #wgraj zdjęcie 
        self.image.blit(note_img, (0,0)) #ustaw wyglad 
        self.rect = self.image.get_rect(topleft = pos) 

    def update(self,x_shift): # x_shift-->world_shift szybkosc i kierunek przesuwania
        self.rect.x += x_shift