from particle import Particle
import math

GRAVITATIONAL_CTE = g = 6.673 * math.pow(10, -11)
THETA = 0.9 
TIME_CTE = 0.1


class Node():

    def __init__(self, size, x, y):
        self.width = size[0]
        self.height = size[1]
        self.x = x                  #Position du noeud (x,y)
        self.y = y  
        self.particle = None                
        self.childNodes = {"ne": None, "se": None, "sw": None, "nw": None}
        self.centreOfMass = None    #Position du centre de masse (x,y)
        self.totalMass = 0          #Masse du centre de masse initialisée à 0


    def add_Particle(self, newParticle):
        """
        Ajouter une particule dans le noeud
        Si le noeud est vide (pas de particules ni d'enfants (quadrants) -> On insère directement la particule
        Sinon si pas d'enfants -> on divise le noeud en 4 quadrants 
            -> On insère la particule qui s'y trouvait et celle qu'on souhaite ajouter
            dans les fils qui conviennent.
        """

        if (self.isEmpty()):
            self.particle = newParticle
            self.totalMass = newParticle.mass
            self.centreOfMass = [newParticle.x, newParticle.y]   #Maj du centre de masse

        else:
            if (self.noChildren()):                
                self.Divide()

            self.add_to_Child(self.particle)
            self.add_to_Child(newParticle)

            self.particle = None     #La particule se trouve maintenant dans un des fils du noeud


    def Divide(self):
        """
        Divise le noeud en 4 quadrants en affectant de nouveaux noeuds aux fils qui sont initialement à None
        """
        w = self.width / 2
        h = self.height / 2
        new_size = (w, h)
        x = self.x
        y = self.y
        self.childNodes["nw"] = Node(new_size, x, y)
        self.childNodes["ne"] = Node(new_size, x + w, y)
        self.childNodes["se"] = Node(new_size, x + w, y + h)
        self.childNodes["sw"] = Node(new_size, x, y + h)


    def add_to_Child(self, particle):
        """
        Ajoute une particule à un fils/quadrant
        """
        if (particle is None):
            return

        for node in self.childNodes.values():
            if (node.in_Quad(particle)):         #Vérifier si la particule est dans le quadrant
                node.add_Particle(particle)     
                self.update_COM(node)           #Maj du centre de masse du noeud père on y ajoutant celui du fils      
                return

        


    def update_COM(self, com2):
            """
            Combine deux centres de masses des noeuds tel que
            La position (x = (x1*m1 + x2*m2) / m1 + m2 , y = (y1*m1 + y2*m2) / m1 + m2)
            La masse totale : m1 + m2
            """
            if (com2.centreOfMass is None):     #Retourne directement le noeud, pour éviter les erreurs
                return self

            if (self.centreOfMass is None):
                return
            
            m = self.totalMass + com2.totalMass            #Nouvelle masse

            #Nouvelle position
            newX = (self.centreOfMass[0] * self.totalMass + com2.centreOfMass[0] * com2.totalMass) / m
            newY = (self.centreOfMass[1] * self.totalMass + com2.centreOfMass[1] * com2.totalMass) / m

            #Maj dans le noeud
            self.centreOfMass = [newX, newY]
            self.totalMass = m


    def in_Quad(self, particle):
        """
        Vérifie que la particule doit être dans le quadrant (à l'intérieur du carré)
        """
        return (particle.x >= self.x and particle.y >= self.y
                and particle.x < self.x + self.width
                and particle.y < self.y + self.height)
    

    #Determiner le fils/quadrant relatif auquel une particule devrait appartenir
    def get_quadrant(self, particle):
        cx = self.x
        cy = self.y

        if particle.x >= cx and particle.y < cy:
            return "ne"
        elif particle.x >= cx and particle.y >= cy:
            return "se"
        elif particle.x < cx and particle.y >= cy:
            return "sw"
        else:
            return "nw"
        

    ##Forces 

 
    @staticmethod
    def Gravity(p1, p2):
        """
        Calcule la force de gravité entre deux particules et met à jour l'accélération des particules tel que
            G = 6.673 x 10-11 Nm^2/kg^2
            Fgrav = (G*m1*m2)/d^2
            F = m*a
        """

        xpos = p1.x - p2.x 
        ypos = p1.y - p2.y 
        d = math.sqrt(xpos**2 + ypos**2)    #Distance entre P1 et P2

        #Calcul de la force
        f =  (GRAVITATIONAL_CTE * p1.mass * p2.mass) / d**2

        #maj de l'accélération des 2 particules
        p1.accel[0] -= f * xpos / p1.mass
        p1.accel[1] -= f * ypos / p1.mass
        p2.accel[0] += f * xpos / p2.mass
        p2.accel[1] += f * ypos / p2.mass



    @staticmethod   
    def Gravity_COM(p, node):
        """
        Calcule la force de gravité entre une particule et un centre de masse (d'un cluster) 
        et met à jour l'accélération tel que
            G = 6.673 x 10-11 Nm^2/kg^2
            Fgrav = (G*m1*m2)/d^2
            F = m*a
        """
        #Calcul de la distance
        com = node.centreOfMass
        xpos = p.x - com[0]
        ypos = p.y - com[1] 
        d = math.sqrt(xpos**2 + ypos**2) 

        #Calcul de la force 
        f =  (GRAVITATIONAL_CTE * p.mass * node.totalMass) / d*d
        
        #Maj de l'accélération de la particule
        p.accel[0] -= f * xpos / p.mass
        p.accel[1] -= f * ypos / p.mass


    def apply_Force(self, particle):
        '''
        Applique la force de gravité selon les configurations :
        - Noeud externe : Gravité entre 2 particules
        - L/distance < THETA : Gravité entre une particule et un cluster (on utilise le centre de mass) 
        - Si aucune des deux on applique récursivement la fonction sur les fils pour plus de précision
        '''
        if self.centreOfMass is not None:
            x = math.fabs(self.centreOfMass[0] - particle.x)
            y = math.fabs(self.centreOfMass[1] - particle.y)
            d = math.sqrt(x**2 + y**2)

        if (self.particle is particle or self.isEmpty()):   #Eviter les erreurs
            return
        elif (self.isExternalNode()):                       #Noeud externe
            Node.Gravity(particle, self.particle)
        elif (self.width / d < THETA):
            Node.Gravity_COM(particle, self)
        else:                                           #Récursion sur les fils
            for node in self.childNodes.values():
                node.apply_Force(particle)

 #Si pas de fils -> Il suffit de vérifier qu'un seul fils est à None
    def noChildren(self):
        '''Vérifie si le noeud n'a pas de fils -> Il suffit qu'un seul fils soit à None, ici le ne (premier)'''
        return self.childNodes['ne'] is None

    def isExternalNode(self):
        '''Vérifie si le noeud est externe -> contient une particule seulement'''
        return self.childNodes['ne'] is None and self.particle is not None

    def isEmpty(self):
        '''Vérifie si le noeud est vide'''
        return self.childNodes['ne'] is None and self.particle is None


    def draw_node(self, pd, screen, grid):
        '''Dessine le noeud et la particule qui s'y trouve'''

        if (grid):
            pd.rect(screen, (200, 200, 200),
                (self.x, self.y, self.width, self.height), 1)

        if (self.particle is None):
            for node in self.childNodes.values():
                if (node is not None):
                    node.draw_node(pd, screen,grid)
        else:
            self.particle.draw_particle(pd, screen)

        if (not self.centreOfMass is None):
            return

        
