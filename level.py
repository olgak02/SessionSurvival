import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player
from items import Note, Coffee, EnergyDrink, Beer 
from display_interactions import Interactions 
from enemy import Enemy

class Level:
    def __init__(self, level_data, surface):
        ### LEVEL SETUP
        self.display_surface = surface #przestrzeń poruszania się postaci -> okno
        self.setup_level(level_data) #inicjuje wyswietlenie stanu poczatkowego gry
        self.world_shift = 0 #predkosc przesuwania swiata
        self.interaction = Interactions(surface)
        self.game_over = False #zmienna okreslajace przegranie (zakonczenie) gry

    def setup_level(self,layout): # layout->level data-> pobrany wyglad mapy
        self.tiles = pygame.sprite.Group() #zbior wchodzacych w interakcje elementow w oknie (nie tło)
        self.player = pygame.sprite.GroupSingle()
        self.notes = pygame.sprite.Group()
        self.coffee = pygame.sprite.Group()
        self.energy_drink = pygame.sprite.Group()
        self.beer = pygame.sprite.Group()
        self.enemy = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row): #iterujemy po kolejnych polach mapy
                x = column_index * tile_size ## -...-
                y = row_index * tile_size    ## dopasowanie koordynatów do wielkosci mapy  
                if cell == 'X': #jesli komorka to platforma
                    tile = Tile((x,y),tile_size) #pozycja platform na mapie
                    self.tiles.add(tile) #dodawanie pola do zbioru
                elif cell == 'P': # 'P' to nasz gracz
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                elif cell == 'N': # 'N' to notatka do zbierania
                    note = Note((x,y))
                    self.notes.add(note)
                elif cell == 'C': # 'C' to kawa
                    coffee_sprite = Coffee((x,y))
                    self.coffee.add(coffee_sprite)
                elif cell == 'E': # 'E' to energetyk
                    energy = EnergyDrink((x,y))
                    self.energy_drink.add(energy)
                elif cell == 'B': # 'B' to piwo
                    beer_sprite = Beer((x,y))
                    self.beer.add(beer_sprite)
                elif cell == 'K': # 'K' to wróg scigajacy gracza
                    enemy_sprite = Enemy((x,y))
                    self.enemy.add(enemy_sprite)

    def scroll_x(self): #funkcja przesuwajaca nieruchome elementy na ekranie
        player = self.player.sprite
        player_x = player.rect.centerx #aktualne polozenie gracza
        direction_x = player.direction.x #aktualny wektor ruchu gracza
        enemy = self.enemy.sprite

        if player.coffee == True: #jesli gracz wypije kawe

            if player.health <= 0 or player.points == 30: #jesli gracz niezyje lub ukonczyl gre odbieramy mu mozliwosc ruchu
                
                self.world_shift = 0
                player.speed = 0
                enemy.speed = 0
                player.jump_speed = 0
            
            elif player_x < screen_width/4 and direction_x < 0: #jesli pozycja gracza przed 1/4 okna i wcisniete <--
                self.world_shift = 12 #przesuwanie swiata predkosc 12 w prawo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            
            elif player_x > screen_width*(3/4) and direction_x > 0: #jesli pozycja gracza po 3/4 okna i wcisniete -->
                self.world_shift = -12 #przesuwanie swiata predkosc 12 w lewo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            else: #w pozostałych przyapdkach normalnie, rusza się tylko gracz
                self.world_shift = 0
                player.speed = 12
                enemy.speed = 2

        elif player.energy == True: #jesli gracz wypije energetyka

            if player.health <= 0 or player.points == 30: #jesli gracz niezyje lub ukonczyl gre odbieramy mu mozliwosc ruchu
                
                self.world_shift = 0
                player.speed = 0
                enemy.speed = 0
                player.jump_speed = 0
            
            elif player_x < screen_width/4 and direction_x < 0: #jesli pozycja gracza przed 1/4 okna i wcisniete <--
                self.world_shift = 16 #przesuwanie swiata predkosc 16 w prawo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            
            elif player_x > screen_width*(3/4) and direction_x > 0: #jesli pozycja gracza po 3/4 okna i wcisniete -->
                self.world_shift = -16 #przesuwanie swiata predkosc 16 w lewo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            else: #w pozostałych przyapdkach normalnie, rusza się tylko gracz
                self.world_shift = 0
                player.speed = 16
                enemy.speed = 2

        elif player.beer == True: #jesli gracz wypije piwo

            if player.health <= 0 or player.points == 30: #jesli gracz niezyje lub ukonczyl gre odbieramy mu mozliwosc ruchu
                
                self.world_shift = 0
                player.speed = 0
                enemy.speed = 0
                player.jump_speed = 0
            
            elif player_x < screen_width/4 and direction_x < 0: #jesli pozycja gracza przed 1/4 okna i wcisniete <--
                self.world_shift = 4 #przesuwanie swiata predkosc 4 w prawo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            
            elif player_x > screen_width*(3/4) and direction_x > 0: #jesli pozycja gracza po 3/4 okna i wcisniete -->
                self.world_shift = -4 #przesuwanie swiata predkosc 4 w lewo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            else: #w pozostałych przyapdkach normalnie, rusza się tylko gracz
                self.world_shift = 0
                player.speed = 4
                enemy.speed = 2

        
        else: # poruszanie bez efektow specjalnych
            if player.health <= 0 or player.points == 30: #jesli gracz niezyje lub ukonczyl gre odbieramy mu mozliwosc ruchu
                            
                self.world_shift = 0
                player.speed = 0
                enemy.speed = 0
                player.jump_speed = 0

            elif player_x < screen_width/4 and direction_x < 0: #jesli pozycja gracza przed 1/4 okna i wcisniete <--
                self.world_shift = 8 #przesuwanie swiata predkosc 8 w prawo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            
            elif player_x > screen_width*(3/4) and direction_x > 0: #jesli pozycja gracza po 3/4 okna i wcisniete -->
                self.world_shift = -8 #przesuwanie swiata predkosc 8 w lewo
                player.speed = 0 #ale zatrzymaj przesuwanie gracza (zostanie w tym samym miejscu, zmieni sie tlo)
                enemy.speed = 2
            else: #w pozostałych przyapdkach normalnie, rusza się tylko gracz
                self.world_shift = 0
                player.speed = 8
                enemy.speed = 2

    def horizontal_movement_collision(self): #funkcja wyszukujaca kolizje w poziomie
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed #wykonuje zmiane koordynatow gracza (ruch) w poziomie

        for sprite in self.tiles.sprites(): #sprawdzanie dla każdej komórki z kafelkiem
            if sprite.rect.colliderect(player.rect): #jesli koliduje to
                if player.direction.x < 0: #jesli był ruch w lewo
                    player.rect.left = sprite.rect.right #to jego lewa pozycja zatrzymuje sie na prawej pozycji przeszkody
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0: #jesli był ruch w lewo
                    player.rect.right = sprite.rect.left #to jego lewa pozycja zatrzymuje sie na prawej pozycji przeszkody
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
  
    def vertical_movement_collision(self): #funkcja wyszukujaca kolizje w pionie
        player = self.player.sprite
        player.apply_gravity() #wykonuje zmiane pozycji w dół na skutek grawitacji

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect): #kolizja góru i dołu postaci z obiektami

                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top #kolizja góry postaci
                    player.direction.y = 0
                    player.on_ground = True 

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom #kolizja dołu postaci
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    
    def get_note(self): #funkcja zbierania notatek i liczenia punktów
        player = self.player.sprite 
        for sprite in self.notes.sprites(): #sprawdzanie dla każdej komórki z kafelkiem
            if sprite.rect.colliderect(player.rect): #jesli koliduje to
                player.point_counter() #dodaj punkt
                sprite.kill() #skasuj
                
    def get_coffee(self): #zbieranie kawy
        player = self.player.sprite 
        for sprite in self.coffee.sprites(): #sprawdzanie dla każdej komórki z kafelkiem
            if sprite.rect.colliderect(player.rect): #jesli koliduje to
                self.player.sprite.beer = False
                self.player.sprite.energy = False
                sprite.kill()
                player.coffee_start = pygame.time.get_ticks()
                player.coffee = True

    def get_energy(self): #zbieranie energetykow
        player = self.player.sprite 
        for sprite in self.energy_drink.sprites(): #sprawdzanie dla każdej komórki z kafelkiem
            if sprite.rect.colliderect(player.rect): #jesli koliduje to
                self.player.sprite.coffee = False
                self.player.sprite.beer = False
                sprite.kill()
                player.energy_start = pygame.time.get_ticks()
                player.energy = True

    def get_beer(self): #zbieranie piwa
        player = self.player.sprite 
        for sprite in self.beer.sprites(): #sprawdzanie dla każdej komórki z kafelkiem
            if sprite.rect.colliderect(player.rect): #jesli koliduje to
                self.player.sprite.coffee = False
                self.player.sprite.energy = False
                sprite.kill()
                player.beer_start = pygame.time.get_ticks()
                player.beer = True

    def damage(self): #funkcja dodawania obrazen i odbierania zdrowia
        player = self.player.sprite 
        enemy = self.enemy.sprite 
        if enemy.rect.colliderect(player.rect): #jesli koliduje to
            player.damage_counter() # odbierz punkty zycia

    def end(self, health, notes, under_level): #funkcja konczoca gre
        
        if health <= 0 or under_level>700: #jesli gracz bez zycia lub wypadl z ekranu
            self.interaction.show_game_over()
            self.game_over = True

        elif notes == 30: #jesli gracz zebrał wszystkie notatki
            self.interaction.show_winner()
            self.game_over = True

    def run(self): #odpala poziom w okienku
        #kafelki w poziomie, świat
        self.tiles.update(self.world_shift) #przesuwanie mapy(odswieza) +(w lewo) -(w prawo), numer -> szybkość
        self.tiles.draw(self.display_surface) #wyswietla kafelki ze zbioru
        self.scroll_x()
        #gracz
        self.player.update() # nie wymaga argumentów
        self.horizontal_movement_collision() # kolizje w poziomie
        self.vertical_movement_collision() # kolizje w pionie
        self.player.draw(self.display_surface) #rysowanie gracza na mapie
        self.damage() # przyjmowanie obrazen
        #wrog
        self.enemy.update(self.player.sprite.rect, self.player.sprite.direction.x, self.world_shift) # aktualizacja polozenia wroga
        self.enemy.draw(self.display_surface) # rysowanie wroga na mapie
        #notatki
        self.notes.draw(self.display_surface) # rysowanie na mapie notatek
        self.notes.update(self.world_shift) # aktualizacja ktore notatki istnieja 
        self.get_note() # zbieranie notatek
        self.interaction.show_notes(self.player.sprite.points) # dodawanie punktow za zbieranie notatek i znikanie zebranych
        #kawa
        self.coffee.draw(self.display_surface) # rysowanie kawy
        self.coffee.update(self.world_shift) # aktualizacja ktore kawy istnieja 
        self.get_coffee() # zbieranie kawy
        #energetyk
        self.energy_drink.draw(self.display_surface) # rysowanie energetyka
        self.energy_drink.update(self.world_shift) # aktualizacja ktore energetyki istnieja 
        self.get_energy() # zbieranie energetyka
        #piwo
        self.beer.draw(self.display_surface) # rysowanie piwa
        self.beer.update(self.world_shift) # aktualizacja ktore piwa istnieja 
        self.get_beer() # zbieranie piwa
        #zdrowie
        self.interaction.show_health(self.player.sprite.health) # aktualiacja poziomu zycia
        #koniec gry
        self.end(self.player.sprite.health, self.player.sprite.points, self.player.sprite.rect.y) # ekran koncowy 