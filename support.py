from os import walk
import pygame

def import_folder(path): #funkcja do wczytywania obrazów z określonego folderu
    surface_list = [] #pusta lista do przechowywania powierzchni obrazu

    for _,__, img_files in walk(path): #pętla przechodzi przez liki w danym folderze (path)
        for image in img_files: #pętla przechodzi przez obrazy w folderze
            full_path = path + '/' + image #tworzenie pełnej ścieżki do obrazka
            image_surf = pygame.image.load(full_path).convert_alpha() #wczytuje obraz z pełnej ścieżki, convert.alpha zapewnia nam transparentność tła 
            image_surf = pygame.transform.scale(image_surf,(42,64)) #wczytujemy obraz o podanych w pikselach wymiarach (skaluje nam obraz do podanego wymiaru)
            surface_list.append(image_surf) #dodaje powierzchnię obrazu (obrazek) do listy
            
    return surface_list #zwraca listę obrazów wczytanych na naszej określonej powierchni