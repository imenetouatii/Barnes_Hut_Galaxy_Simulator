import random
import pygame
from node import Node
from particle import Particle
from time import sleep

#Simulation de l'insertion successive de particules statiques dans un quadtree

def create_particles(width, height, n_particles, p_mass):
    particles = []

    for _ in range(n_particles):
        #Génerer aléatoirement les positions x et y 
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        
        mass = p_mass

        particles.append(Particle(x,y, mass, (0, 0)))

    return particles

def is_quit_required():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

def draw_screen(screen, root_node):
    screen.fill((0, 0, 0))
    root_node.draw_node(pygame.draw, screen, True)
    pygame.display.update()

def main():

    WIDTH = 700
    HEIGHT = 700
    N_PARTICLES = 50
    PARTICLE_MASS = 50
    WAIT = 1

    size = (WIDTH, HEIGHT)

    root_node = Node(size, 0, 0)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Simulation Insertion Quadtree')

    particles = create_particles(WIDTH, HEIGHT, N_PARTICLES, PARTICLE_MASS)

    running = True
    i = 0
    while running:
        sleep(WAIT)

        draw_screen(screen, root_node)

        if i < len(particles):
            particle = particles[i]
            root_node.add_Particle(particle)
            i += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
