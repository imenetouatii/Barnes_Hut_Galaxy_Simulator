from node_oct import Node
from particle_3D import Particle
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def generateParticles(width, height, depth, n_particules, p_mass):
    particles = []

    for _ in range(n_particules):
        x = random.gauss(width / 2, width / 7)
        y = random.gauss(height / 2, height / 7)
        z = random.gauss(depth / 2, depth / 7)
        
        x_vel = (random.random() - 0.5) * 40
        y_vel = (random.random() - 0.5) * 40
        z_vel = (random.random() - 0.5) * 40
        vel = [x_vel, y_vel, z_vel]
        mass = random.random() * p_mass * 10
        particles.append(Particle(x, y ,z , mass, velocity=vel))

    return particles


def main():
    WIDTH = 1300
    HEIGHT = 900
    DEPTH = 600
    N_PARTICLES = 1000
    P_MASS = 5

    size = (WIDTH, HEIGHT, DEPTH)

    root_node = Node(size, 0, 0, 0)
    particles = generateParticles(WIDTH, HEIGHT, DEPTH, N_PARTICLES, P_MASS)

    plt.ion()  #Activer le mode interactif de matplotlib

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    running = True
    while running:

        ax.cla()  #Effacer le graphique à chaque itération

        root_node.draw_node(ax)

        for particle in particles:
            particle.draw_particle(ax)

        plt.pause(0.001)  #Mettre à jour l'affichage

    

        for particle in particles:
            root_node.apply_Force(particle)

        root_node = Node(size, 0, 0, 0)
        for particle in particles:
            particle.move_Particle()
            root_node.add_Particle(particle)

    plt.ioff()  #Désactiver le mode interactif à la fin
    plt.show()


if __name__ == "__main__":
    main()
