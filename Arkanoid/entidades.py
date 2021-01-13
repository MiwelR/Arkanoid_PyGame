import pygame as pg
from pygame.locals import *
from Arkanoid import GAME_DIMENSIONS, FPS

import random
import sys


pg.init()


class Raqueta:
    def __init__(self, x, y, vx):
        self.x = x
        self.y = y
        self.vx = vx

        self.imagen = pg.image.load("resources/images/regular_racket.png")

    def actualizar(self):
        self.x += self.vx
        if self.x + 128 >= GAME_DIMENSIONS[0]:
            self.x = GAME_DIMENSIONS[0] - 128
        if self.x <= 0:
            self.x = 0


class Pelota:
    imagenes_files = ['brown_ball.png', 'blue_ball.png', 'red_ball.png', 'green_ball.png']
    num_img_explosion = 8
    retardo_animaciones = 5

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.imagenes = self.cargaImagenes()
        self.imagenes_explosion = self.cargaExplosion()
        self.imagen_act = 0
        self.ix_explosion = 0
        self.ciclos_tras_refresco = 0
        self.ticks_acumulados = 0
        self.ticks_por_frame_de_animacion = 1000//FPS * self.retardo_animaciones
        self.muriendo = False

        self.imagen = self.imagenes[self.imagen_act]

    def cargaExplosion(self):
        return [pg.image.load(f"resources/images/explosion0{i}.png") for i in range(self.num_img_explosion)]

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"resources/images/{img}"))

        return lista_imagenes

    @property
    def rect(self):
        return self.imagen.get_rect(topleft=(self.x, self.y))

    def actualizar_posicion(self):
        if self.muriendo:
            return
        # Gestionar posición de pelota
        if self.rect.left <= 0 or self.rect.right >= GAME_DIMENSIONS[0]:
            self.vx = -self.vx

        if self.rect.top <= 0:
            self.vy = -self.vy

        if self.rect.bottom >= GAME_DIMENSIONS[1]:
            self.muriendo = True
            self.ciclos_tras_refresco = 0
            return
        
        self.x += self.vx
        self.y += self.vy


    def actualizar_disfraz(self):
        # Gestionar imagen activa (disfraz)
        self.ciclos_tras_refresco += 1

        if self.ciclos_tras_refresco % self.retardo_animaciones == 0:
            self.imagen_act += 1
            if self.imagen_act >= len(self.imagenes):
                self.imagen_act = 0
            
        self.imagen = self.imagenes[self.imagen_act]


    def actualizar(self, dt):
        self.actualizar_posicion()

        if self.muriendo:
            self.explosion(dt)
        else:
            self.actualizar_disfraz()


    def explosion(self, dt):
        if self.ix_explosion >= len(self.imagenes_explosion):
            self.ix_explosion = 0

        self.imagen = self.imagenes_explosion[self.ix_explosion]

        self.ticks_acumulados += dt
        if self.ticks_acumulados >= self.ticks_por_frame_de_animacion:
            self.ix_explosion += 1
            self.ticks_acumulados = 0

        return False

class Game:
    def __init__(self):
        self.pantalla = pg.display.set_mode(GAME_DIMENSIONS)
        pg.display.set_caption("Futuro Arkanoid")

        self.pelota = Pelota(400, 300, 10, 10)
        self.raqueta = Raqueta(336, 550, 0)

        self.clock = pg.time.Clock()


    def bucle_principal(self):
        game_over = False

        while not game_over:
            dt = self.clock.tick(FPS)

            # Gestión de Eventos:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                """ if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        self.raqueta.x += 10
                        if self.raqueta.x + 128 >= GAME_DIMENSIONS[0]:
                            self.raqueta.x = GAME_DIMENSIONS[0] - 128

                    if event.key == pg.K_LEFT:
                        self.raqueta.x -= 10
                        if self.raqueta.x <= 0:
                            self.raqueta.x = 0 """

                teclas_pulsadas = pg.key.get_pressed()
                if teclas_pulsadas[K_RIGHT]:
                    self.raqueta.vx = 10
                elif teclas_pulsadas[K_LEFT]:
                    self.raqueta.vx = -10
                else:
                    self.raqueta.vx = 0

            # Actualización de elementos del juego:
            game_over = self.pelota.actualizar(dt)
            self.raqueta.actualizar()

            self.pantalla.fill((0,0,255))
            self.pantalla.blit(self.pelota.imagen, (self.pelota.x, self.pelota.y))
            self.pantalla.blit(self.raqueta.imagen, (self.raqueta.x, self.raqueta.y))

            # Refrescar pantalla:
            pg.display.flip()