import pygame
from os import getcwd
from os.path import join

class Interactions: #klasa Interakcje
    def __init__(self,surface): #inicjalizacja 
        #setup
        self.display_surface = surface #przyjmuję powierzchnię ekranu jako atrybut obiektu, wyświetlanie stałych, nieruszających się elementów w naszej grze
        # health
        self.health3 = pygame.image.load(join(getcwd(),'interface', 'health3.png')) # zaladowanie grafik z poziomami zycia
        self.health2 = pygame.image.load(join(getcwd(),'interface', 'health2.png'))
        self.health1 = pygame.image.load(join(getcwd(),'interface', 'health1.png'))
        #notes
        self.note = pygame.image.load(join(getcwd(),'items', 'notatka.png')) # zaladowanie grafik z notatkami
        self.note_rect = self.note.get_rect(topleft = (100,0)) #ustawienie notatki w rogu ekranu
        self.font = pygame.font.Font(join(getcwd(),'interface', 'KGShakeitOff.ttf'), 24) # zaladowanie fontu tekstu do ilości notatek i napisu dead, gdy umrzemy, rozmiar czcionki 24 
        #health and notes background
        self.h_n_background = pygame.image.load(join(getcwd(),'interface', 'h_n_background.png')) # zaladowanie grafik tla interfejsu (indeks)
        #end game
        self.font2 = pygame.font.Font(join(getcwd(),'interface', 'KGShakeitOff.ttf'), 120) # zaladowanie fontu tekstów na koniec gry z folderu interface (font w pliku ttf) 120 - rozmiar czcionki
        self.background = pygame.image.load(join(getcwd(),'interface', 'final_background.png')) # załadowanie tła na koniec gry
        
 
    def show_health(self, health): # aktualizacja grafik z zyciami w zaleznosci od ich poziomu
        if health == 90: # dla 90 pkt zycia 3 serduszka dla 60 2 serduszka itd
            self.display_surface.blit(self.health3,(10,0))
        elif health == 60:
            self.display_surface.blit(self.health2,(10,0))
        elif health == 30:
            self.display_surface.blit(self.health1,(10,0))
        else:
            death = self.font.render("Dead",False,'red') # ustawienie napisu 'dead' w miejscu serduszek po smierci gracza 
            self.display_surface.blit(death,(10,0))
            
    def show_notes(self, points): # wyswietlanie notatek w rogu ekranu
        self.display_surface.blit(self.h_n_background, (5,0)) # miejsce wyświetlania notatki na tle indeksu
        self.display_surface.blit(self.note,self.note_rect) # self.note - obraz reprezentujący notatkę, self.display_surface.blit - powierzchnia, na której rysujemy self.note_rect - prostokąt okalający obraz notatki
        show_points = self.font.render(str(points),False,"black") # wyświetlanie liczby punktów w kolorze czarnym 
        show_points_rect = show_points.get_rect(midleft = (self.note_rect.right+5,self.note_rect.centery)) #obszar, w którym pokazuje się nam notatka 
        self.display_surface.blit(show_points, show_points_rect) # aktualizowanie punktow na menu

    def show_game_over(self): # wyswietlanie grafiki ekranu koncowego (negatywny)
        self.display_surface.blit(self.background, (30,90)) # pozycja grafiki na ekranie
        text1 = self.font2.render("YOU FAILED",False,(46,0,1)) # tekst na grafice i kolor czcionki, rozmiar czcionki 2
        self.display_surface.blit(text1, (230,100)) # wyswietlenie napisu 1 (pozycja)
        text2 = self.font2.render("SESJA killed you",False,(46,0,1)) # tekst na grafice i kolor czcionki, rozmiar czcionki 2
        self.display_surface.blit(text2, (35, 240)) # wyswietlenie napisu 2 (pozycja)

    def show_winner(self): # wyswietlanie grafiki ekranu koncowego (pozytywny)
        self.display_surface.blit(self.background, (30,90)) # pozycja grafiki na ekranie
        text1 = self.font2.render("YOU PASS",False,(46,0,1)) # tekst na grafice i kolor czcionki, rozmiar czcionki 2 
        self.display_surface.blit(text1, (300,100)) # wyswietlenie napisu 1 (pozycja)
        text2 = self.font2.render("MARVELOUS!",False,(46,0,1)) # tekst na grafice i kolor czcionki, rozmiar czcionki 2 
        self.display_surface.blit(text2, (220, 240)) # wyswietlenie napisu 2 (pozycja)
 
    def play_again(self): # wyswietlanie tekstu zacznij ponownie
        text1 = self.font.render("PRESS SPACE", True, (255, 255, 255)) # tekst na grafice i kolor czcionki
        text2 = self.font.render("TO PLAY AGAIN", True, (255, 255, 255)) # tekst na grafice i kolor czcionki
        self.display_surface.blit(text1, (520,450)) # wyswietlenie napisu (pozycja)
        self.display_surface.blit(text2, (500,500)) # wyswietlenie napisu (pozycja)