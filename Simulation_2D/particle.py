import math

PARTICLE_MASS = 5
DELTA_T = 0.1

class Particle():

    def __init__(self, x, y, mass = PARTICLE_MASS, velocity = None):
        self.x = x
        self.y = y
        self.mass = mass
        self.velocity = velocity
        self.accel = [0, 0]


    def move_Particle(self):
        '''
        Simule le mouvement d'une particule en fonction de sa vitesse et de son accélération
        '''
        #Maj de la vitesse selon l'acceleration 
        self.velocity[0] += DELTA_T * self.accel[0]
        self.velocity[1] += DELTA_T * self.accel[1]

        #Remise de l'acceleration à 0
        self.accel = [0, 0]

        #Maj de la position 
        self.x += DELTA_T * self.velocity[0]
        self.y += DELTA_T * self.velocity[1] 

 

    def draw_particle(self, pd, surface):
        '''Dessine une particule dont le rayon depend de sa masse'''
        x = math.floor(self.x)
        y = math.floor(self.y)
       
        pd.circle(surface, (255,255,255), (x,y), 1 + math.floor(0.2*self.mass/PARTICLE_MASS), 0)

    

   