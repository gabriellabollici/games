import pygame
from config import Config
 
#clase jugador
class Player():
    def __init__(self, x, y, personaje_image):
        self.image = pygame.transform.scale(personaje_image, (45,45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def update(self,scroll):
        #actualizar las plataformas en horizontal
        self.rect.y += scroll

    def move(self, grupo_plataformas):
        #resetear variables (delta x y delta y)
        scroll = 0
        dx = 0
        dy = 0

        #procesa las pulsaciones de las teclas
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            #tecla para que se mueva a la izquierda
            dx = -10
            self.flip = True
        if key[pygame.K_RIGHT]:
            #tecla para que se mueva a la derecha
            dx = 10
            self.flip = False

        #con cada iteracion, la velocidad aumenta 1
        self.vel_y += Config.instance().constantes["gravedad"]
        dy += self.vel_y

        #asegurarnos de que el personaje no se salga de los limites de la pantalla
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > (Config.instance().constantes["SCREEN_WIDTH"]):
            dx =  (Config.instance().constantes["SCREEN_WIDTH"]) - self.rect.right

        #hacemos que el personaje pise las plataformas
        for plataforma in grupo_plataformas:
            #colisionar en direccion a la coordenada 'y'
            if plataforma.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < plataforma.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = plataforma.rect.top
                        dy = 0
                        self.vel_y = -20


        #comprueba si el jugador ha avanzado hacia arriba
        if self.rect.top <= (Config.instance().constantes["scroll_thresh"]):
            if self.vel_y < 0:
                scroll = -dy
            


        #actualizar la posicion del rectangulo
        self.rect.x += dx
        self.rect.y += dy + scroll

        #esto resuelve los problemas de colision del personaje
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self, screen):
        #dibujamos al personaje mirando hacia ambos lados
        screen.blit( pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
