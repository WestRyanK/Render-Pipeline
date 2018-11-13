import math
from Geometry import *
import RenderEngine
import numpy as np
from Util3D import *

class Object3D:
    def __init__(self, positionX = 0, positionY = 0, positionZ = 0, rotationX = 0, rotationY = 0, rotationZ = 0, velocityX = 0, velocityY = 0, velocityZ = 0, frictionX = 0.001, frictionZ = 0.001):
        self.homePosition = np.array([positionX, positionY, positionZ], dtype=float)
        self.homeRotation = np.array([rotationX, rotationY, rotationZ], dtype=float)
        self.homeVelocity = np.array([velocityX, velocityY, velocityZ], dtype=float)
        self.checkCollisions = False
        self.size = np.array([2.0, 2.0, 2.0], dtype=float)
        self.look = np.array([0.0, 0.0, 0.0], dtype=float)
        self.homeFriction = np.array([frictionX, 0, frictionZ], dtype=float)
        self.mass = 0
        self.drawAxes = False
        Object3D.reset(self)

    def beginDraw(self):
        RenderEngine.pushMatrix()
        RenderEngine.translate(self.position[0], self.position[1], self.position[2])
        RenderEngine.rotateY(self.rotation[1])

    def endDraw(self):
        RenderEngine.popMatrix()

    def drawObject(self):
        axes = []
        RenderEngine.setColor((255,0,0))
        axes.append(Line3D(Point3D(0,0,0), Point3D(1,0,0)))
        RenderEngine.renderObject(axes)
        axes = []
        RenderEngine.setColor((0,255,0))
        axes.append(Line3D(Point3D(0,0,0), Point3D(0,1,0)))
        RenderEngine.renderObject(axes)
        axes = []
        RenderEngine.setColor((0,0,255))
        axes.append(Line3D(Point3D(0,0,0), Point3D(0,0,1)))
        RenderEngine.renderObject(axes)

    def draw(self):
        self.beginDraw()
        self.drawObject()
        if self.drawAxes:
            Object3D.drawObject(self)
        self.endDraw()

    def reset(self):
        self.position = np.copy(self.homePosition)
        self.rotation = np.copy(self.homeRotation)
        self.velocity = np.copy(self.homeVelocity)
        self.friction = np.copy(self.homeFriction)
        Object3D.updateLookAt(self)

    def setRotationY(self, value):
        self.rotation[1] = value
        self.updateLookAt()

    def updateLookAt(self):
        radianAngle = math.radians(self.rotation[1])
        # self.look[0] = self.position[0] + math.cos(radianAngle)
        # self.look[2] = self.position[2] + math.sin(radianAngle)
        # self.look[1] = self.position[1] 
        self.look[0] = math.cos(radianAngle)
        self.look[2] = math.sin(radianAngle)
        self.look[1] = 0
    
    def update(self, elapsedTime = 0):
        self.position += self.velocity
        self.updateLookAt()
    
    def intersects(self, otherObject):
        intersects = True
        for i in range(3):
            distance = math.fabs(self.position[i] - otherObject.position[i])
            radius = (self.size[0]/ 2.0 + otherObject.size[0] / 2.0)
            intersectDimension  =  distance < radius
            intersects = intersects and intersectDimension
        return intersects

    def collisionCallback(self, otherObject, initialVelocitySelf, initialVelocityOther):
        pass