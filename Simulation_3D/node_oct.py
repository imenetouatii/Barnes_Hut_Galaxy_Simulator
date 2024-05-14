import math


DRAW_GRID = False
NODE_BORDER_COLOUR = (200, 200, 200)
GRAVITATIONAL_CTE = g = 6.673 * math.pow(10, -11)
THETA = 0.9  # quotient to determine accuracy / speed. 0 slow
TIME_CTE = 0.1


class Node():

    def __init__(self, size, x, y, z):
        self.width = size[0]
        self.height = size[1]
        self.depth = size[2]
        self.x = x  #Position du noeud (x, y, z)
        self.y = y
        self.z = z
        self.particle = None  
        self.childNodes = {"1": None, "2": None, "3": None, "4": None,  #Octree -> 8 fils
                           "5": None, "6": None, "7": None, "8": None} 
        self.centreOfMass = None  #Position du centre de masse (x, y, z)
        self.totalMass = 0  #Masse du centre de masse initialisée à 0

    def add_Particle(self, newParticle):
        """
        Ajouter une particule dans le noeud
        Si le noeud est vide (pas de particules ni d'enfants (quadrants) -> On insère directement la particule
        Sinon si pas d'enfants -> on divise le noeud en 4 quadrants 
            -> On insère la particule qui s'y trouvait et celle qu'on souhaite ajouter
            dans les fils qui conviennent.
        """
        if self.isEmpty():
            self.particle = newParticle
            self.totalMass = newParticle.mass
            self.centreOfMass = [newParticle.x, newParticle.y,newParticle.z] 
        else:
            if self.childNodes['1'] is None:
                self.Divide()
            self.add_to_Child(self.particle)
            self.add_to_Child(newParticle)
            self.particle = None


    def Divide(self):
        """
        Divise le noeud en 8 quadrants en affectant de nouveaux noeuds aux fils qui sont initialement à None
        """
        w = self.width / 2
        h = self.height / 2
        d = self.depth / 2
        new_size = (w, h, d)
        x, y, z = self.x, self.y, self.z
        self.childNodes["4"] = Node(new_size, x, y, z)
        self.childNodes["1"] = Node(new_size, x + w, y, z)
        self.childNodes["2"] = Node(new_size, x + w, y + h, z)
        self.childNodes["3"] = Node(new_size, x, y + h, z)
        self.childNodes["8"] = Node(new_size, x, y, z + d)
        self.childNodes["5"] = Node(new_size, x + w, y, z + d)
        self.childNodes["6"] = Node(new_size, x + w, y + h, z + d)
        self.childNodes["7"] = Node(new_size, x, y + h, z + d)


    def add_to_Child(self, particle):
        """
        Ajoute une particule à un fils/quadrant
        """
        if particle is None:
            return

        for node in self.childNodes.values():
            if node.in_Octant(particle):
                node.add_Particle(particle)
                self.update_COM(node)
                return


    def update_COM(self, com2):
        """
        Combine deux centres de masses des noeuds tel que
        La position (x = (x1*m1 + x2*m2) / m1 + m2 , y = (y1*m1 + y2*m2) / m1 + m2)
        La masse totale : m1 + m2
        """

        if com2.centreOfMass is None:
            return self

        if self.centreOfMass is None:
            return

        m = self.totalMass + com2.totalMass
        newX = (self.centreOfMass[0] * self.totalMass + com2.centreOfMass[0] * com2.totalMass) / m
        newY = (self.centreOfMass[1] * self.totalMass + com2.centreOfMass[1] * com2.totalMass) / m
        newZ = (self.centreOfMass[2] * self.totalMass + com2.centreOfMass[2] * com2.totalMass) / m
        self.centreOfMass = [newX, newY, newZ]
        self.totalMass = m


    def in_Octant(self, particle):
        """
        Vérifie que la particule doit être dans le quadrant (à l'intérieur du carré)
        """
        return (
            particle.x >= self.x and particle.y >= self.y and particle.z >= self.z and
            particle.x < self.x + self.width and particle.y < self.y + self.height and particle.z < self.z + self.depth
        )

    

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
        zpos = p1.z - p2.z
        d = math.sqrt(xpos**2 + ypos**2 + zpos**2)

        f = TIME_CTE * (GRAVITATIONAL_CTE * p1.mass * p2.mass) / d**2
        p1.accel[0] -= f * xpos / p1.mass
        p1.accel[1] -= f * ypos / p1.mass
        p1.accel[2] -= f * zpos / p1.mass
        p2.accel[0] += f * xpos / p2.mass
        p2.accel[1] += f * ypos / p2.mass
        p2.accel[2] += f * zpos / p2.mass

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
        zpos = p.z - com[2]
        d = math.sqrt(xpos**2 + ypos**2 + zpos**2)
        
        #Calcul de la force 
        f = TIME_CTE * (GRAVITATIONAL_CTE * p.mass * node.totalMass) / d**2
       
        #Maj de l'accélération de la particule
        p.accel[0] -= f * xpos / p.mass
        p.accel[1] -= f * ypos / p.mass
        p.accel[2] -= f * zpos / p.mass



    def apply_Force(self, particle):
        '''
        Applique la force de gravité selon les configurations :
        - Noeud externe : les particules sont proches -> Gravité entre 2 particules
        - L/distance < THETA : Gravité entre une particule et un cluster (on utilise le centre de mass) 
        - Si aucune des deux on applique récursivement la fonction sur les fils pour plus de précision
        '''
        if self.centreOfMass is not None :
            x = math.fabs(self.centreOfMass[0] - particle.x)
            y = math.fabs(self.centreOfMass[1] - particle.y)
            z = math.fabs(self.centreOfMass[2] - particle.y)
            d = math.sqrt(x**2 + y**2 + z**2)
        
        if self.particle is particle or self.isEmpty():
            return
        elif self.isExternalNode():
            Node.Gravity(particle, self.particle)
        elif self.width / d < THETA:
            Node.Gravity_COM(particle, self)
        else:
            for node in self.childNodes.values():
                node.apply_Force(particle)




    def draw_node(self, ax):
        '''Dessine le noeud et la particule qui s'y trouve'''

        if (self.particle is None):
            for node in self.childNodes.values():
                if (node is not None):
                    node.draw_node(ax)
        else:
            self.particle.draw_particle(ax)

        if (not self.centreOfMass is None):
            return   
            
            
    def isInternalNode(self):
        return self.particle is None and self.childNodes['1'] is not None

    def isExternalNode(self):
        return self.childNodes['1'] is None and self.particle is not None

    def isEmpty(self):
        return self.childNodes['1'] is None and self.particle is None