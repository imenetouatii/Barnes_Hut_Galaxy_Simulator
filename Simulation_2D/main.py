import random
import pygame
from node import Node
from particle import Particle
from time import sleep

#Afficher les bordures des noeuds
DRAW_GRID = False


def create_particles(WIDTH, HEIGHT, n_particles, P_MASS):
    particles = []

    for _ in range(n_particles):
        
        #Génerer aléatoirement les positions x et y en utilisant une gausienne
        x = random.gauss(WIDTH / 2, WIDTH / 7)
        y = random.gauss(HEIGHT / 2, HEIGHT / 7)

        #Génerer la vélocité aléatoirement entre -50 et 50
        x_vel = random.uniform(-50, 50)
        y_vel = random.uniform(-50, 50)
        vel = [x_vel, y_vel]

        mass = random.random() * P_MASS * 10
        particles.append(Particle(x,y, mass, velocity=vel))

    return particles

def is_quit_required():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True

def draw_screen(screen, root_node):
    screen.fill((0, 0, 0))
    root_node.draw_node(pygame.draw, screen, DRAW_GRID)
    pygame.display.update()

def main():
    WIDTH = 1300
    HEIGHT = 900
    N_PARTICLES = 3000
    P_MASS = 5
    WAIT = 0.1

    size = (WIDTH, HEIGHT)

    root_node = Node(size, 0, 0)
    particles = create_particles(WIDTH, HEIGHT, N_PARTICLES, P_MASS)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Barnes Hut Galaxy Simulation')

    running = True
    while running:
        if is_quit_required():
            running = False

        sleep(WAIT)

        draw_screen(screen, root_node)

        #Appliquer les forces et faire bouger les particules
        for particle in particles:
            root_node.apply_Force(particle)
            particle.move_Particle()            

        #Réinsérer les particules mises à jour
        root_node = Node(size, 0, 0)  
        for particle in particles:
            root_node.add_Particle(particle)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
