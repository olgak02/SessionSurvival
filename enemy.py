import pygame
from support import import_folder
from os.path import join
from os import getcwd
from settings import screen_height, screen_width

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets() # pobiera wyglad (funkcja)
        self.frame_index = 0 # zaczynamy od ilości 0
        self.animation_speed = 0.15 # szybkość animacji, którą będziemy dodawać do frame index
        self.image = self.animations['idle'][self.frame_index] #wstawia obrazek 'idle' jako podstawowy
        self.rect = self.image.get_rect(topleft = pos) #parametr pozycji = lewy górny róg ikony wroga
        self.speed = 2  # Adjust the speed of the enemy as needed

        #status
        self.status = 'idle' 
        self.facing_right = True #twarz wroga w prawo (domyślnie tak)

    def import_character_assets(self): #wczytywanie animacji postaci z folderów i przechowywanie ich w liscie
        character_path = join(getcwd(), 'proffesor') #nasza ścieżka do grafik
        self.animations = {'idle':[]} #słownik przechowujący animacje postaci

        for animation in self.animations.keys(): # iterowanie przez dostepne elementy animacji
            full_path = join(character_path, animation) # sciezka do plikow
            self.animations[animation] = import_folder(full_path) # zaimportowanie plikow do funkcji animujacej

    def animate(self): 
        animation = self.animations[self.status] # wybor animacji na bazie aktualnego jej statusu postoj lub ruch 

        self.frame_index += self.animation_speed # zapetlenie klatek i nadanie im odpowiedniej predkosci zmiany
        if self.frame_index >= len(animation): # zapetlenie sie klatek postaci
            self.frame_index = 0 # predkosc zmiany klatek

        if self.facing_right: # wybor kierunku "patrzenia sie" postaci 
            self.image = animation[int(self.frame_index)] # jak idzie w prawo nic sie nie zmienia
        else: 
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False) # jak idzie w lewo spirte'y zostaja odwrocone w lewo

    def update_up_down(self, player_rect): # funkcja aktualizacji pozycji wroga w pionie
        if self.rect.y < player_rect.y and self.rect.y > 0: #jeśli wrog wyżej od gracza i nie wyszedl poza ekran
            self.rect.y += self.speed #obniż wroga
        elif self.rect.y <= 0: #jesli wróg wyszedł poza ekran
            self.rect.y = 1 #zatrzymaj wroga przy gornej krawedzi
        elif self.rect.y > player_rect.y and self.rect.y < screen_height-127: #jesli wrog nizej od gracza i nie wyszedl poza ekran 
            self.rect.y -= self.speed #podnies wroga
        elif self.rect.y >= screen_height-127: # jesli wrog wychodzi poza ekran
            self.rect.y = screen_height-128 #zatrzymaj przy dolnej krawedzi

    def update(self, player_rect, player_direction, world_shift): #funkcja aktualizacji pozycji gracza w poziomie
        self.animate() # uruchomienie funkcji animacji postaci
        if self.rect.x < player_rect.x and (player_direction > 0 and world_shift <0): #jesli wrog po lewej a gracz idzie w prawo (z przesunieciem swiata)
        
            if self.rect.x>0: #jesli nie przy lewej krawedzi
                self.rect.x -= abs(world_shift)-2  # wrog oddala sie
                self.facing_right = True # obrocenie modelu profesora w prawo
            else:
                self.rect.x = 0 #jesli przy lewej krawedzi to sie zatrzymuje i nie wychodzi poza ekran

            self.update_up_down(player_rect) #aktywuj sprawdzenie w pionie
        
        elif self.rect.x < player_rect.x and player_direction > 0: #jesli wrog po lewej a gracz idzie w prawo
            self.rect.x += self.speed # przesuniecie przeciwnika w prawo
            self.facing_right = True # obrocenie modelu profesora w prawo

            self.update_up_down(player_rect) #aktywuj sprawdzenie w pionie
        
        elif self.rect.x <= player_rect.x and (player_direction <0 and world_shift >0):#jesli wrog po lewej a gracz idzie w lewo (z przesunieciem swiata)
            self.rect.x += abs(world_shift)-2 # przesuniecie przeciwnika w prawo
            self.facing_right = True # obrocenie modelu profesora w prawo

            self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie
            
        elif self.rect.x < player_rect.x and player_direction <0: #jesli wrog po lewej a gracz idzie w lewo
            self.rect.x += self.speed # przesuniecie przeciwnika w prawo
            self.facing_right = True # obrocenie modelu profesora w prawo

            self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie
            
        elif self.rect.x > player_rect.x and (player_direction <0 or world_shift >0): #jesli wrog po prawej a gracz idzie w lewo (z przesunieciem swiata)
            if self.rect.x<screen_width-40: #jeśli nie jest przy prawej krawędzi
                self.rect.x += abs(world_shift)-2  # przesuniecie przeciwnika w prawo
                self.facing_right = False # obrocenie modelu profesora w lewo
            else:
                self.rect.x = screen_width-40 #jesli przy prawej krawedzi to tam zatrzymaj

            self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie

        elif self.rect.x > player_rect.x and player_direction < 0: #jesli wrog po prawej a gracz idzie w lewo
            self.rect.x -= self.speed # przesuniecie przeciwnika w lewo
            self.facing_right = False # obrocenie modelu profesora w lewo

            self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie
           
        elif self.rect.x >= player_rect.x and (player_direction >0 and world_shift <0): #jesli wrog po prawej a gracz idzie w prawo (z przesunięciem świata)
            self.rect.x -= abs(world_shift)-2  # przesuniecie przeciwnika w lewo
            self.facing_right = False # obrocenie modelu profesora w lewo
         
            self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie

        elif self.rect.x >= player_rect.x and player_direction >0: #jesli wrog po prawej a gracz idzie w prawo
            self.rect.x -= self.speed   # przesuniecie przeciwnika w lewo
            self.facing_right = False # obrocenie modelu profesora w lewo

            self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie

        else: #jeśli gracz nie zmienia pozycji w poziomie
            if self.rect.x > player_rect.x: # jeśli wróg po prawo
                self.rect.x -= self.speed # przesuniecie przeciwnika w lewo
                self.facing_right = False # obrocenie modelu profesora w lewo

                self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie
               
            elif self.rect.x < player_rect.x: # jesli wróg po lewo
                self.rect.x += self.speed # przesuniecie przeciwnika w prawo
                self.facing_right = True # obrocenie modelu profesora w prawo

                self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie

            else: #jesli jest równo z przeicwnikiem
                self.update_up_down(player_rect)#aktywuj sprawdzenie w pionie