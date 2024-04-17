level_map = [
'X                                                              N   B                                                         N                N  X',
'X          E                                 N           XXXXXXXXXXXXXXXXXXX           XXXXXX                  N             X                X  X',
'X N     XXXXXXX           N      XXXXXXXXXXXXXXXXXXX                             X     X         E             X                    XXXX         X',
'XXXK                  XXXXXX                                                           X        XXXX                       X                     X',
'XXXX            N                                   C             N         X          X                  B          X              N      X     X',
'XXXXXB          XXX       XXXXXXX      N            X       XXXXXXXXXXX              N X                 XXXXX                      X            X',
'XXXXXXX                              XXXX                                        XXXXXXXXXX                                 XX                  BX',
'XXXXXXXX                                     XXXX                     XXX                                       XXX                       C     XX',
'X           XXXXXXXXXXXXXXXXXX                       XXXXXXXXXXX               XXXX            XXXXXXXXXXX              XXX  N           XXX     X',
'X      P                                B                                 N             XXXXXXXXX     NB          XXXXXXXXXXXXXX                 X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'] 
# zdefiniowanie wygladu mapki

tile_size = 64 #definiujemy rozmiar "kafelka/komorki/pola" mapy
screen_width= 1200 #ustawienie szerokosci okna
screen_height = len(level_map) * tile_size #dostosowanie rozmiaru okna mapki do ilosci pol