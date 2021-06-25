#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Escrito por Daniel Fuentes B.
# Licencia: X11/MIT license http://www.opensource.org/licenses/mit-license.php
# https://www.pythonmania.net/es/2010/04/07/tutorial-pygame-3-un-videojuego/

# ---------------------------
# Importacion de los módulos
# ---------------------------

import pygame
from pygame.locals import *
from pygame.math import Vector2
import os
import sys
import numpy as np

# -----------
# Constantes
# -----------

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
IMG_DIR = "imagenes"
SONIDO_DIR = "sonidos"

# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------


def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
        print("No se pudo cargar el sonido:" + ruta)
        sonido = None
    return sonido

# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("paleta.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = 0
        self.acceleration = 0
        self.bullets = bullets
        self.pos = Vector2([x,y])
        self.speed = Vector2(0, 0)

    def shoot(self):
        bulletAngle = self.angle
        bulletX = np.cos(self.angle)+self.rect.centerx
        bulletY = np.sin(self.angle)+self.rect.centery

        bulletSpeed = [np.cos(self.angle)*15, np.sin(self.angle)*15]

        newBullet = Bullet(bulletX, bulletY, bulletAngle, bulletSpeed)
        self.bullets.append(newBullet)

    def update(self):

        print(self.speed)

        self.image = pygame.transform.rotate(load_image("paleta.png", IMG_DIR, alpha=True), self.angle)

        self.speed += Vector2([np.cos(self.angle)*self.acceleration, np.sin(self.angle)*self.acceleration])
        
        self.pos += self.speed
        self.rect.center = self.pos
        
        self.acceleration = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.transform.scale(load_image("bola.png", IMG_DIR, alpha=True), (50, 50)), angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = angle
        self.speed = speed

    def update(self):
        self.rect.move_ip((self.speed[0], self.speed[1]))
        

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image("block.png", IMG_DIR, alpha=True), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = [0, 0]

# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    pygame.init()
    pygame.mixer.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ejemplo de un Pong Simple")

    # cargamos los objetos
    fondo = load_image("fondo.jpg", IMG_DIR, alpha=False)
    sonido_golpe = load_sound("tennis.ogg", SONIDO_DIR)
    sonido_punto = load_sound("aplausos.ogg", SONIDO_DIR)

    #enemy1 = Enemy()
    block1 = Block(300,300)
    block2 = Block(350,300)
    block3 = Block(400,300)

    block4 = Block(275,250)
    block5 = Block(425,250)

    allBlocks = [block1, block2, block3, block4, block5]

    bullets = [Bullet(300, 100, 15, [0,0])]

    player1 = Player(350, 150, bullets)

    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25)  # Activa repeticion de teclas
    pygame.mouse.set_visible(False)

    # el bucle principal del juego
    while True:
        clock.tick(60)
        # Obtenemos la posicon del mouse
        pos_mouse = pygame.mouse.get_pos()
        mov_mouse = pygame.mouse.get_rel()

        # Actualizamos los obejos en pantalla
        player1.update()
        #jugador1.humano()
        #jugador2.cpu(bola)
        #bola.update()

        # Comprobamos si colisionan los objetos
        #enemy1.colision(allBlocks)
        #bola.colision(jugador1)
        #bola.colision(jugador2)


        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    player1.acceleration = .1
                elif event.key == K_RIGHT:
                    player1.angle = (player1.angle+1)%360
                elif event.key == K_LEFT:
                    player1.angle = (player1.angle-1)%360
                elif event.key == K_DOWN:
                    player1.speed = [0,0]
                elif event.key == K_SPACE:
                    player1.shoot()
        #        elif event.key == K_ESCAPE:
        #            sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    player1.acceleration = 0
        #        elif event.key == K_DOWN:
        #            block1.rect.centery += 0
        #    # Si el mouse no esta quieto, mover la paleta a su posicion
        #    elif mov_mouse[1] != 0:
        #        player1.rect.centerx = pos_mouse[0]
        #        player1.rect.centery = pos_mouse[1]

        # actualizamos la pantalla
        screen.blit(fondo, (0, 0))
        todos = pygame.sprite.RenderPlain(allBlocks, player1, bullets)
        todos.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()