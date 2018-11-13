import random
from Object3D import *
from Geometry import *

def generateNeighborhood():
    neighborhood = []
    spacing = 15
    blockSize = 3
    streetSize = 30
    addBlock(neighborhood, blockSize, blockSize, spacing, 30, -10)
    addBlock(neighborhood, blockSize, blockSize, spacing, 30, 55)

    return neighborhood

def addBlock(neighborhood, blockX = 6, blockZ = 6, spacing = 15, x = 0, z = 0):
    addStreet(neighborhood, blockX - 1, 15, 0, x, z)
    addStreet(neighborhood, blockZ - 1, 15, -90, x + spacing * (blockX - 1), z)
    addStreet(neighborhood, blockX - 1, 15, -180, x + spacing * (blockX - 1), z - spacing * (blockZ - 1))
    addStreet(neighborhood, blockZ - 1, 15, 90, x, z - spacing * (blockZ - 1))

def addStreet(neighborhood, lineCount = 6, spacing = 15, angle = 0, x = 0, z = 0):
    radianAngle = math.radians(angle)
    for i in range(lineCount):
        w = random.random() * 8 + 5
        l = random.random() * 10 + 5
        h = random.random() * 2 + 4
        house = House(x + math.cos(radianAngle) * i * spacing, z + math.sin(radianAngle) * i * spacing, angle, w, h, l)
        neighborhood.append(house)


class House(Object3D):
    def __init__(self, positionX = 0, positionZ = 0, rotationY = 0, width = 10, height = 5, length = 10): 
        Object3D.__init__(self, positionX = positionX, positionZ = positionZ, rotationY = rotationY)
        self.colorR = random.random()
        self.colorG = random.random()
        self.colorB = random.random()
        self.checkCollisions = True
        self.mass = 10
        self.size = np.array([width, height, length], dtype=float)

    def collisionCallback(self, otherObject, initialVelocitySelf, initialVelocityOther):
        speed = magnitude(initialVelocitySelf - initialVelocityOther) * 0.1
        self.velocity[1] = min(0.4, speed)
        self.update()

    def drawObject(self):
        w= self.size[0] / 2.0
        h= self.size[1]
        r = h + 3
        l= self.size[2] / 2.0

        RenderEngine.setColor((self.colorR * 255, self.colorG * 255, self.colorB * 255))
        house = []
        #Floor
        house.append(Line3D(Point3D(-w, 0, -l), Point3D(w, 0, -l)))
        house.append(Line3D(Point3D(w, 0, -l), Point3D(w, 0, l)))
        house.append(Line3D(Point3D(w, 0, l), Point3D(-w, 0, l)))
        house.append(Line3D(Point3D(-w, 0, l), Point3D(-w, 0, -l)))
        #Ceiling
        house.append(Line3D(Point3D(-w, h, -l), Point3D(w, h, -l)))
        house.append(Line3D(Point3D(w, h, -l), Point3D(w, h, l)))
        house.append(Line3D(Point3D(w, h, l), Point3D(-w, h, l)))
        house.append(Line3D(Point3D(-w, h, l), Point3D(-w, h, -l)))
        #Walls
        house.append(Line3D(Point3D(-w, 0, -l), Point3D(-w, h, -l)))
        house.append(Line3D(Point3D(w, 0, -l), Point3D(w, h, -l)))
        house.append(Line3D(Point3D(w, 0, l), Point3D(w, h, l)))
        house.append(Line3D(Point3D(-w, 0, l), Point3D(-w, h, l)))
        #Door
        house.append(Line3D(Point3D(-1, 0, l), Point3D(-1, 3, l)))
        house.append(Line3D(Point3D(-1, 3, l), Point3D(1, 3, l)))
        house.append(Line3D(Point3D(1, 3, l), Point3D(1, 0, l)))
        #Roof
        house.append(Line3D(Point3D(-w, h, -l), Point3D(0, r, -l)))
        house.append(Line3D(Point3D(0, r, -l), Point3D(w, h, -l)))
        house.append(Line3D(Point3D(-w, h, l), Point3D(0, r, l)))
        house.append(Line3D(Point3D(0, r, l), Point3D(w, h, l)))
        house.append(Line3D(Point3D(0, r, l), Point3D(0, r, -l)))
        RenderEngine.renderObject(house)