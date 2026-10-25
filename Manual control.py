import pygame
import math
import time
import random
import numpy as np
import os
from collections import deque

render = True
running = True

if render:
    pygame.init()

    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Pendulum Simulation")

L = 100
G = 9.81

CART_MASS = 1

cart_x = 500
cart_v = 0
cart_a = 0

pendulum_angle = math.pi 
pendulum_av = 0
pendulum_aa = 0


while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            F = -5
        elif keys[pygame.K_RIGHT]:
            F  = 5
        else:
            F = 0

        cart_a = (F) / CART_MASS

        pendulum_aa = ((G * math.sin(pendulum_angle) - (cart_a * math.cos(pendulum_angle))) / L)

        pendulum_av += pendulum_aa * 0.1
        pendulum_angle += pendulum_av * 0.1

        cart_v += cart_a * 0.1
        cart_x += cart_v * 0.1

        if cart_x < 0:
            cart_x = 0
            cart_v = 0
        elif cart_x > 1000:
            cart_x = 1000
            cart_v = 0

        if render:
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 0), (cart_x - 25, 300 - 10, 50, 20), 0, 5)
            pygame.draw.line(screen, (0, 0, 0), (cart_x, 300), (cart_x + L * math.sin(pendulum_angle), 300 - L * math.cos(pendulum_angle)), 2)
            pygame.display.flip()
            pygame.time.Clock().tick(60)