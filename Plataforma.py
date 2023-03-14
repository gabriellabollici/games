import pygame
from config import Config
#clase para las plataformas
class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, plataforma_imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(plataforma_imagen, (width, 25))
        self.width = 1000
        self.height = 320
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    #metodo que actualiza la posicion de las plataformas en vertical
    def update(self, scroll):
        self.rect.y += scroll
        #comprueba que la plataforma ya no aparezca en la pantalla y si es así la borra
        #esto lo hacemos para que no ocupen memoria en nuestro juego y puedan seguir creandose nuevas
        if self.rect.top > Config.instance().constantes["SCREEN_HEIGHT"]:
            self.kill()
