import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self) #nos permite heredar las funcionalidades de sprites de pygame

        #variables
        self.lista_animacion = []
        #situamos el indice en el primer frame
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        #cargamos las imagenes del spritesheet
        pasos_animacion = 3
        for animacion in range(pasos_animacion):
            image = sprite_sheet.get_image(animacion, 50, 23, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            image.set_colorkey(0, 0)
            self.lista_animacion.append(image)
        
        #seleccionamos la imagen de inicio y creamos un rectangulo a partir de esta
        self.image = self.lista_animacion[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = SCREEN_WIDTH
        self.rect.y = y

    def update(self, scroll, SCREEN_WIDTH):
        #actualizamos la animacion
        ANIMATION_COOLDOWN = 80
        #actilizamos la animacion en funcion del frame actual
        self.image = self.lista_animacion[self.frame_index]
        #comprobar cuanto ha pasado desde la ultima actualizacion
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #resetar al comienzo de los frames si ya se han terminado
        if self.frame_index >= len(self.lista_animacion):
            self.frame_index = 0

        #movemos al enemigo
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        #que no se salga de la pantalla
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()