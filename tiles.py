import pygame 
from os import getcwd 
from os.path import join

class Tile(pygame.sprite.Sprite): # pola mapy
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size)) #rozmiary x,y kafelka(prostokat)
        tile_img = pygame.image.load(join(getcwd(),'interface', 'cegla.png')) #wgraj zdjęcie cegly
        tile_img = pygame.transform.scale(tile_img, (size, size)) #dostosuj rozmiar do wielkosci okna
        self.image.blit(tile_img, (0,0)) #wyswietl obraz cegly
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,x_shift): # x_shift-->world_shift szybkosc i kierunek przesuwania
        self.rect.x += x_shift