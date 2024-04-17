import pygame, sys
from settings import *
from level import Level
from display_interactions import Interactions
from os import getcwd
from os.path import join

###5 PYGAME SETUP
pygame.init() # inicjalizacja pygame
pygame.display.set_caption('Session survival') #ustaw tytul okna
icon = pygame.image.load(join(getcwd(),'items', 'notatka.png')) #wgraj obraz do ikony
pygame.display.set_icon(icon) #ustaw obraz ikony
screen = pygame.display.set_mode((screen_width, screen_height)) #zdefiniowanie okienka
clock = pygame.time.Clock() #tworzy obiekt "zegar" do kontroli czasu w grze
level = Level(level_map, screen) #przekazuje do klasy argumenty 1-wyglad mapy(level data), 2-okno(surface)
bg_img = pygame.image.load(join(getcwd(),'interface', 'background.png')) #wgraj obraz tla
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)) #dostosuj rozmiar do wielkosci okna
interaction = Interactions(screen) # uruchomienie elementow interfejsow

while True: #petla "jesli zarejestruje zdarzenie zamknij --> wylacz pygame"
  for event in pygame.event.get(): #jesliz arejestruje zdarzenie
    if event.type == pygame.QUIT: #jesli wcisnieto wyjscie
      pygame.quit() #wyjdz z gry
      sys.exit() #zamknij okno
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Sprawdź, czy gracz kliknął przycisk "Play Again"
        if level.game_over == True:# Resetuj stan gry i rozpocznij grę od nowa
          level.game_over = False #cofnij "przegranie"
          screen.fill('black') # kolor tła
          level.setup_level(level_map)  # Dodaj metodę reset do klasy Player, aby zresetować położenie gracza


  screen.blit(bg_img, (0,0)) # otworzenie okna gry
  level.run() # uruchomienie glownych funkcji gry
  
  if level.game_over == True: # sprawdzenie czy gra sie skonczyla
    interaction.play_again() # odpalenie ekranu konca gry i restartu 

  pygame.display.update() # aktualizacja animacji na ekranie
  clock.tick(60) # kontrola ilości klatek/sek (FPS) w grze