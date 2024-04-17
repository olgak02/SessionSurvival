import pygame
from support import import_folder
from os.path import join
from os import getcwd

class Player(pygame.sprite.Sprite): # klasa gracz
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets() # pobiera wyglad (funkcja)
        self.frame_index = 0 # zaczynamy od ilości 0, gdy osiągnie 1 to zmieni się klatka animacji
        self.animation_speed = 0.15 # szybkość animacji, którą będziemy dodawać do frame index
        self.image = self.animations['idle'][self.frame_index] #wstawia obrazek 'idle' jako podstawowy
        self.rect = self.image.get_rect(topleft = pos) #wypozycjonowanie grafiki do powierzchni 
        self.health = 90 #nasze początkowe życie

        ###  PLAYER MOVEMENT
        self.direction = pygame.math.Vector2(0,0) #funkcja wektora (x,y) zmieniajacego pozycje gracza
        self.speed = 8 # predkosc ruchu postaci
        self.gravity = 0.8 # o 0.8 w dół
        self.jump_speed = -18 # o 16 w góre
       
        ## efekty itemow
        self.points = 0 # zmienna z punktami domyslnie na 0
        self.coffee = False # stan aktywacji domyslnie wylaczony zacznie dzialac po wejsciu w interakcjie z obiektem
        self.coffee_start = 0 # domyslny czas poczatkowy dzialania kawy, pozwala to na postawienie wielu kaw na mapie
        self.coffee_duration = 8000  # czas dzialania przedmiotu
        self.energy = False # tak samo jak wczesniej u reszty
        self.energy_start = 0 
        self.energy_duration = 5000
        self.beer = False
        self.beer_start = 0
        self.beer_duration = 5000
         
        #status gracza
        self.status = 'idle'
        self.facing_right = True # początkowo gracz skierowany jest w prawo
        self.on_ground = False #czy gracz jest na ziemi
        self.on_ceiling = False #czy dotyka sufitu
        self.on_left = False #
        self.on_right = False
        self.invincible = False #czy jest ranny
        self.invincibility_duration = 400 #okres niewrażliwości
        self.hurt_time = 0 #czas zranienia

    def import_character_assets(self): # wczytywanie animacji postaci z folderów i przechowywanie ich w liscie
        character_path = join(getcwd(), 'player') # nasza ścieżka do grafik
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'idle_hurt':[],'run_hurt':[],'jump_hurt':[],
                           'fall_hurt':[],'beer_idle':[],'beer_run':[],'beer_jump':[],'beer_fall':[],'beer_idle_hurt':[],
                           'beer_run_hurt':[],'beer_jump_hurt':[],'beer_fall_hurt':[],'coffe_idle_hurt':[],'coffe_run_hurt':[],
                           'coffe_jump_hurt':[],'coffe_fall_hurt':[],'coffe_idle':[],'coffe_run':[],'coffe_jump':[],'coffe_fall':[]} # słownik przechowujący animacje postaci
        for animation in self.animations.keys(): #importowanie plików według słownika
            full_path = join(character_path, animation)
            self.animations[animation] = import_folder(full_path)

    def animate(self): # animacja gracza w zależności od jej statusu, kierunku ruchu i efektów po zebraniu przedmiotów
        animation = self.animations[self.status] # uzależniamy animacje od statusu postaci

        self.frame_index += self.animation_speed # zwiększamy powoli frame index co spowoduje podmianę obrazku
        if self.frame_index >= len(animation): # if nam zapewnia, że frame index nie będzie rósł w nieskończoność
            self.frame_index = 0

        if self.facing_right:  # jeśli gracz patrzy w prawo
            self.image = animation[int(self.frame_index)] #oryginalny obrazek
        else: # jeśli patrzy w lewo, transformujemy obrazek (odbicie lustrzane)
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)

        # blok warunków, który w zależnośći od położenia postaci na ekranie aktualizuje protsokąt kolizji aby wypozycjonować postać na ekranie    
        if self.on_ground and self.on_right: # jeśli gracz jest na ziemi i dotyka czegoś po prawej
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left: # jest na ziemi i koliduje z czymś po lewej 
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground: # jeśli gracz jest na ziemi i nie dotyka niczego
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right: # jeśli gracz dotyka sufitu i czegoś z prawej
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left: # jeśli gracz dotyka sufitu i czegoś z lewej
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling: # jeśli dotyka sufitu
            self.rect = self.image.get_rect(midtop = self.rect.midtop)


    def get_input(self): #ruch gracza
        keys = pygame.key.get_pressed() # fukcja reagująca na nacisniecie przyciskow

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1 # jesli '->' to wektor o 1 w prawo
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1  #jesli '<-' to wektor o 1 w lewo
            self.facing_right = False #patrzymy w lewo, co wpływa nam na odwrócenie grafiki
        else:
            self.direction.x = 0 # jesli nic to wektor pozostaje )

        if keys[pygame.K_UP] and self.on_ground: #jesli nacisnieta spacja i gracz jest na ziemi lub ma podwójny skok
            self.jump() # skocz

    def get_status(self): # rozróżnienie statusu gracza w zależności od zmian wektora i nadajemu mu inną wartość zmiennej self.status
        # dodatkowo rozróżniono statusy gracza według efektu po spożyciu napojów i bycia rannym

        if self.direction.y < 0: # status, kiedy skczemy 'jump'
            if self.beer: # efekt piwa
                self.status = 'beer_jump'
                if self.beer and self.invincible:
                    self.status = 'beer_jump_hurt'
            elif self.coffee or self.energy: # efekt kawy lub energola
                self.status = 'coffe_jump'
                if (self.coffee or self.energy) and self.invincible: # efekt kawy + zraniony
                    self.status = 'coffe_jump_hurt'
            else:
                self.status = 'jump' #klasyczny obrazek
                if self.invincible:
                    self.status = 'jump_hurt'

        elif self.direction.y > 0: # kiedy upadamy 'fall'
            if self.beer: # efekt piwa
                self.status = 'beer_fall'
                if self.beer and self.invincible:
                    self.status = 'beer_fall_hurt'
            elif self.coffee or self.energy: # efekt kawy lub energola
                self.status = 'coffe_fall'
                if (self.coffee and self.invincible): # efekt kawy + zraniony
                    self.status = 'coffe_fall_hurt'
            else:
                self.status = 'fall' #wariant klasyczny
                if self.invincible:
                    self.status = 'fall_hurt'

        else: #run
            if self.direction.x != 0: # kiedy poruszamy się prawo/lewo
                if self.beer: # efekt piwa
                    self.status = 'beer_run'
                    if self.beer and self.invincible:
                        self.status = 'beer_run_hurt'
                elif self.coffee or self.energy: # efekt kawy lub energola
                    self.status = 'coffe_run'
                    if (self.coffee or self.energy) and self.invincible: # efekt kawy ;ub energola + zraniony
                        self.status = 'coffe_run_hurt'
                else: 
                    self.status = 'run' #wariant bez efektów
                    if self.invincible:
                        self.status = 'run_hurt'

            else: # idle
                if self.beer: # efekt piwa
                    self.status = 'beer_idle'
                    if self.beer and self.invincible:
                        self.status = 'beer_idle_hurt'
                elif self.coffee or self.energy: # efekt kawy lub energola
                    self.status = 'coffe_idle'
                    if (self.coffee or self.energy) and self.invincible: # efekt + zraniony
                        self.status = 'coffe_idle_hurt'
                else:
                    self.status = 'idle' #wariant bez efetków
                    if self.invincible:
                        self.status = 'idle_hurt' #zraniony

    def apply_gravity(self): # funkcja opisujaca dzialanie grawitacji
        self.direction.y += self.gravity # na wartosc y wektora pozycji sklada sie grawitacja
        self.rect.y += self.direction.y # pozycja gracza aktualizowana przez wartosc y wektora pozycji
    
    def jump(self): # funkcja skocz
        self.direction.y = self.jump_speed # wartosc y wektora pozycji rowna przemieszczeniu w gore

    def point_counter(self): # dodawanie punktow gdy gracz wejdzie w przedmiot aktywacyjny (notatka)
        self.points += 2 # dodanie punktu do puli
        print(self.points) # napisanie aktualnej liczby punktow

    def coffee_timer(self): # aktywacja efektu kawy
        if self.coffee:
            current_time = pygame.time.get_ticks() #jesli rozpoczeto zaczyna sie odliczanie dzialania
            if current_time - self.coffee_start >= self.coffee_duration: #jesli uplynie czas dzialania efekt zostanie wylaczony
                self.coffee = False   

    def energy_timer(self): # aktywacja efektu energetyka
        if self.energy:
            current_time = pygame.time.get_ticks()
            if current_time - self.energy_start >= self.energy_duration:
                self.energy = False    

    def beer_timer(self): # aktywacja efektu piwa
        if self.beer:
            current_time = pygame.time.get_ticks()
            if current_time - self.beer_start >= self.beer_duration:
                self.beer = False   

    def damage_counter(self): # otrzymanie obrazen
        if not self.invincible: # jesli nie ma niesmiertelnosci to funkcja zostanie spelniona
            self.health = self.health - 30 # po otrzymaniu obrazenia zostanie zabrane 30 pkt. zycia
            self.invincible = True # po otrzymaniu obrazenia gracz dostaje niesmiertelnosc 
            self.hurt_time = pygame.time.get_ticks() #

    def invincibility_timer(self): # otrzymanie niesmiertelnosci na kilka sekund po otrzymaniu obrazen 
        if self.invincible:
            current_time = pygame.time.get_ticks() #
            if current_time - self.hurt_time >= self.invincibility_duration: # sprawdzenie ile czasu jescze zostalo jesli sie skonczyl efekt zostaje cofniety 
                self.invincible = False
        
    

    def update(self): # funkcja aktualizujaca pozycje gracza
        self.get_input() # pobiera reakcje klawiatury
        self.animate() # animujemy ruch gracza (podstawiamy odpowiednie obrazki)
        self.get_status() # aktualizujemy na bieżąco status gracza
        self.invincibility_timer() # aktywujemy niesmiertelnosc
        self.coffee_timer() # sprawdzamy czy dziala efekt kawy
        self.energy_timer() # sprawdzamy czy dziala efekt kawy
        self.beer_timer() # sprawdzamy czy dziala efekt kawy