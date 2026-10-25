import pygame
import math
import numpy as np
import scipy.linalg as la

render = True

running = True

if render:
    pygame.init()

    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Pendulum Simulation")

L = 100
G = 9.81

CART_MASS = 1
Pendulum_MASS = 1
J = Pendulum_MASS * L**2

E0 = 2 * Pendulum_MASS * G * L

cart_x = 500
cart_v = 0
cart_a = 0

pendulum_angle = math.pi
pendulum_av = 0.01
pendulum_aa = 0

Controller = "LQR"

desired_cart_x = 500

A = np.array([[0, 1, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 1],
              [0, 0, G/L, 0]])
   
B = np.array([[0],
              [1 / CART_MASS],
              [0],
              [-1 / (CART_MASS * L)]])

Q = np.diag([10,5000,100,500])
R = np.array([[1]])


P = la.solve_continuous_are(A, B, Q, R)

K = np.linalg.inv(R) @ B.T @ P

K_energy = 0.01

def energy_controller(pendulum_angle, pendulum_av):
    E = 0.5 * J * pendulum_av**2 + Pendulum_MASS * G * L * (1 + math.cos(pendulum_angle))
    E_error = E - E0
    F = K_energy * E_error * pendulum_av * np.cos(pendulum_angle)
    F = np.clip(F, -10, 10)
    return F

while running:
        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            '''if keys[pygame.K_LEFT]:
                F = -50
            elif keys[pygame.K_RIGHT]:
                F  = 50
            else:
                F = 0'''

            if keys[pygame.K_LEFT]:
                desired_cart_x += -5
            elif keys[pygame.K_RIGHT]:
                desired_cart_x += 5
            elif keys[pygame.K_q]:
                pendulum_av += -0.01
            elif keys[pygame.K_e]:
                pendulum_av += 0.01

        X_desired = np.array([desired_cart_x, 0, 0, 0])
        X = np.array([cart_x, cart_v, pendulum_angle, pendulum_av])

        pendulum_angle = ((pendulum_angle + math.pi) % (2 * math.pi)) - math.pi

        if Controller == "Energy":
            if abs(pendulum_angle) < 0.4:
                Controller = "LQR"
                action = K @ (X_desired - X)
                action = action.item()
                F = np.clip(action, -10, 10)
            else:
                F = energy_controller(pendulum_angle, pendulum_av)
        elif Controller == "LQR":
            if abs(pendulum_angle) > 0.5:
                Controller = "Energy"
                F = energy_controller(pendulum_angle, pendulum_av)
            else:
                action = K @ (X_desired - X)
                action = action.item()
                F = np.clip(action, -10, 10)

        print(f"Cart X: {cart_x:.2f}, Pendulum Angle: {pendulum_angle:.2f}, Angular velocity: {pendulum_av:.2f}, Force: {F:.2f}, Controller: {Controller}")

        cart_a = (F) / CART_MASS

        pendulum_aa = ((G * math.sin(pendulum_angle) - (cart_a * math.cos(pendulum_angle))) / L)

        pendulum_av += pendulum_aa * 0.1
        pendulum_angle += pendulum_av * 0.1

        cart_v += cart_a * 0.1
        cart_x += cart_v * 0.1

        if cart_x <= 0+25:
            cart_v = 0
        elif cart_x >= 1000-25:
            cart_v = 0

        if render:
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 0), (cart_x - 25, 300 - 10, 50, 20), 0, 5)
            pygame.draw.line(screen, (0, 0, 0), (cart_x, 300), (cart_x + L * math.sin(pendulum_angle), 300 - L * math.cos(pendulum_angle)), 2)
            pygame.draw.circle(screen, (255, 0, 0), (int(desired_cart_x), 300), 5)
            pygame.display.flip()
            pygame.time.Clock().tick(60)