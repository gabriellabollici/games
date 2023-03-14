import pygame
import random
import json
import os
from config import Config
from pygame import mixer
from spritesheet import SpriteSheet
from Enemigo import Enemy
from Player import Player
from Plataforma import Plataforma


#inicializamos pygame
mixer.init()
pygame.init()

#definir fuente
fuente_pequenya = pygame.font.SysFont('Gorilla Milkshake', Config.instance().constantes["fuente_pequenya"])
fuente_mediana = pygame.font.SysFont('Gorilla Milkshake', Config.instance().constantes["fuente_mediana"])
fuente_grande = pygame.font.SysFont('Gorilla Milkshake', Config.instance().constantes["fuente_grande"])

#creamos la ventana
screen = pygame.display.set_mode((Config.instance().constantes["SCREEN_WIDTH"], Config.instance().constantes["SCREEN_HEIGHT"]))
pygame.display.set_caption('Saltitos')

#frecuencia de los frames
clock = pygame.time.Clock()

#cargamos la musica
pygame.mixer.music.load('assets/cancion.mp3')
#controlamos el volumen de la musica
pygame.mixer.music.set_volume(0.01)
#indicamos cuando queremos que empiece la musica y que continue sonando
pygame.mixer.music.play(-1, 0.0)
sonido_muerte = pygame.mixer.Sound('assets/sonido_muerte.mp3')
sonido_muerte.set_volume(0.5)

#cargar imagenes
personaje = pygame.image.load(Config.instance().constantes["personaje"]).convert_alpha()
fondo = pygame.image.load(Config.instance().constantes["background"]).convert_alpha()
plataforma_imagen = pygame.image.load(Config.instance().constantes["plataforma"]).convert_alpha()
mariposas_imagen = pygame.image.load(Config.instance().constantes["mariposas_imagen"]).convert_alpha()
mariposas_sheet = SpriteSheet(mariposas_imagen)

#variables
max_plataformas = 10
scroll = 0
scroll_fondo = 0
game_over = False
puntuacion = 0
atenuacion = 0

#metodo para mostrar el texto
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#metodo para mostrar un panel de informacion
def draw_panel(fuente):
    pygame.draw.rect(screen, Config.instance().constantes["lila"], (0, 0, Config.instance().constantes["SCREEN_WIDTH"], 10))
    pygame.draw.line(screen, Config.instance().constantes["blanco"], (0, 10), (Config.instance().constantes["SCREEN_WIDTH"], 10), 2)
    draw_text('PUNTUACION: ' + str(puntuacion), fuente, Config.instance().constantes["blanco"], 0, 0)

#metodo para controlar el movimiento del fondo
def draw_fondo(scroll_fondo, scroll):
    #redibujar screen con un segmento de fondo un poco superior
    screen.blit(fondo, (0, - Config.instance().constantes["SCREEN_HEIGHT"] + scroll_fondo))
    if scroll_fondo >= Config.instance().constantes["SCREEN_HEIGHT"]:
        screen.blit(fondo, (0, - Config.instance().constantes["SCREEN_HEIGHT"] + scroll_fondo))
        scroll_fondo = 0
    scroll_fondo += scroll
    return scroll_fondo


saltarin = Player(Config.instance().constantes["SCREEN_WIDTH"] // 2, Config.instance().constantes["SCREEN_HEIGHT"] - 150, personaje)

#crear conjuntos de sprites
grupo_plataformas = pygame.sprite.Group()
enemigo_grupo = pygame.sprite.Group()

#crear plataforma de inicio
plataforma = Plataforma(Config.instance().constantes["SCREEN_WIDTH"] // 2 - 40, Config.instance().constantes["SCREEN_HEIGHT"]  - 50, 70, plataforma_imagen)
grupo_plataformas.add(plataforma)

#bucle principal del juego
run = True
while run:

    clock.tick(Config.instance().constantes["FPS"])

    if game_over == False: 
        scroll = saltarin.move(grupo_plataformas)
        
        #mostrar fondo
        
        scroll_fondo = draw_fondo(scroll_fondo, scroll)
        
        #crear plataformas
        if len(grupo_plataformas) < max_plataformas:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, Config.instance().constantes["SCREEN_WIDTH"] - p_w)
            p_y = plataforma.rect.y - random.randint(80, 120)
            plataforma = Plataforma(p_x, p_y, p_w, plataforma_imagen)
            grupo_plataformas.add(plataforma)

        #crear enemigos
        if len(enemigo_grupo) == 0 and puntuacion > 1000:
            enemigo = Enemy(Config.instance().constantes["SCREEN_WIDTH"], 100, mariposas_sheet, 1.5)
            enemigo_grupo.add(enemigo)

        #actualizar enemigos
        enemigo_grupo.update(scroll, Config.instance().constantes["SCREEN_WIDTH"])

        #actualizar plataformas
        grupo_plataformas.update(scroll)

        #actualizar puntuacion
        if scroll > 0: 
            puntuacion += scroll
        
        #mostrar sprites
        grupo_plataformas.draw(screen)
        enemigo_grupo.draw(screen)
        saltarin.draw(screen)


        #mostrar panel
        draw_panel(fuente_pequenya)

        #comprobar si es game over
        if saltarin.rect.top > Config.instance().constantes["SCREEN_HEIGHT"]:
            game_over = True
            sonido_muerte.play()
            
        #comprobar si el personaje ha chocado con el enemigo
        if pygame.sprite.spritecollide(saltarin, enemigo_grupo, False):
            if pygame.sprite.spritecollide(saltarin, enemigo_grupo, False, pygame.sprite.collide_mask):
                game_over = True
                sonido_muerte.play()
    
    else: #si game over es cierto
        if atenuacion < Config.instance().constantes["SCREEN_WIDTH"]: #ponemos la pantalla en negro dibujando un rectangulo
            atenuacion += 5
            pygame.draw.rect(screen, Config.instance().constantes["negro"], (0, 0, atenuacion, Config.instance().constantes["SCREEN_HEIGHT"]))
        
        draw_text('GAME OVER', fuente_grande, Config.instance().constantes["rosa"], 100, 200)
        draw_text('PUNTUACION: ' + str(puntuacion), fuente_grande, Config.instance().constantes["lila"], 75, 250)
        draw_text('PULSA ENTER PARA JUGAR DE NUEVO', fuente_mediana, Config.instance().constantes["rosa"], 40, 300)
        
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            #resetamos variables
            game_over = False
            puntuacion = 0
            scroll = 0
            atenuacion = 0
            #resposicionamos al personaje en la posicion donde estaba al comienzo del juego
            saltarin.rect.center = (Config.instance().constantes["SCREEN_WIDTH"] // 2, Config.instance().constantes["SCREEN_HEIGHT"] - 150)
            #resetear enemigos
            enemigo_grupo.empty()
            
            #resetamos plataformas
            grupo_plataformas.empty()

            #crear plataforma de inicio
            plataforma = Plataforma(Config.instance().constantes["SCREEN_WIDTH"] // 2 - 40, Config.instance().constantes["SCREEN_HEIGHT"]  - 50, 70, plataforma_imagen)
            grupo_plataformas.add(plataforma)
    

    #gestor de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #actualizar fondo
    pygame.display.update()

pygame.quit()

