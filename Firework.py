import RenderEngine 
import numpy as np
from Particles import *
from Object3D import *
from PhysicsSimulator import *

class Firework(Object3D):
    def __init__(self, positionX = 0, positionY = 0, positionZ = 0, velocityX = 0, velocityY = 0, velocityZ = 0, fuseDuration = 0.1):
        Object3D.__init__(self, positionX=positionX,
            positionY=positionY, positionZ=positionZ, velocityX = velocityX, velocityY = velocityY, velocityZ = velocityZ)
        self.mass = 400
        self.fuseDuration = fuseDuration
        self.checkCollisions = True
        self.drawAxes = False
        self.decayed = False
        self.reset()

    def reset(self):
        Object3D.reset(self)
        self.fuseTime = 0
        self.explode = False
        self.decayed = False
        self.particles = Particles()
        self.particles.simulator.simFloor = False
        self.particles.decayRate = 0.15
    
    def drawObject(self):
        if (self.explode):
            RenderEngine.pushMatrix()
            RenderEngine.translate(-self.position[0], -self.position[1], -self.position[2])
            self.particles.draw()
            RenderEngine.popMatrix()
            box = []
            box.append(Line3D(Point3D(-self.size[0], -self.size[1], -self.size[2]), Point3D(self.size[0], self.size[1], self.size[2])))
            box.append(Line3D(Point3D(self.size[0], -self.size[1], -self.size[2]), Point3D(-self.size[0], self.size[1], self.size[2])))
            box.append(Line3D(Point3D(-self.size[0], self.size[1], -self.size[2]), Point3D(self.size[0], -self.size[1], self.size[2])))
            box.append(Line3D(Point3D(-self.size[0], -self.size[1], self.size[2]), Point3D(self.size[0], self.size[1], -self.size[2])))
            RenderEngine.renderObject(box)
        if (not self.explode):
            s = 0.25
            r = 0.5
            g = 0.5
            b = 0.5
            RenderEngine.setColor((r * 255, g * 255, b * 255))
            particle = []
            # bottom
            particle.append(Line3D(Point3D(s, 0, s), Point3D(-s, 0, s)))
            particle.append(Line3D(Point3D(-s, 0, s), Point3D(-s, 0, -s)))
            particle.append(Line3D(Point3D(-s, 0, -s), Point3D(s, 0, -s)))
            particle.append(Line3D(Point3D(s, 0, -s), Point3D(s, 0, s)))

            # top
            particle.append(Line3D(Point3D(s, s * 2, s), Point3D(-s, s * 2, s)))
            particle.append(Line3D(Point3D(-s, s * 2, s), Point3D(-s, s * 2, -s)))
            particle.append(Line3D(Point3D(-s, s * 2, -s), Point3D(s, s * 2, -s)))
            particle.append(Line3D(Point3D(s, s * 2, -s), Point3D(s, s * 2, s)))

            # front
            particle.append(Line3D(Point3D(s, 0, s), Point3D(s, s * 2, s)))
            particle.append(Line3D(Point3D(s, s * 2, s), Point3D(-s, s * 2, s)))
            particle.append(Line3D(Point3D(-s, s * 2, s), Point3D(-s, 0, s)))
            particle.append(Line3D(Point3D(-s, 0, s), Point3D(s, 0, s)))

            # back
            particle.append(Line3D(Point3D(s, 0, -s), Point3D(s, s * 2, -s)))
            particle.append(Line3D(Point3D(s, s * 2, -s), Point3D(-s, s * 2, -s)))
            particle.append(Line3D(Point3D(-s, s * 2, -s), Point3D(-s, 0, -s)))
            particle.append(Line3D(Point3D(-s, 0, -s), Point3D(s, 0, -s)))

            # right
            particle.append(Line3D(Point3D(s, 0, s), Point3D(s, s * 2, s)))
            particle.append(Line3D(Point3D(s, s * 2, s), Point3D(s, s * 2, -s)))
            particle.append(Line3D(Point3D(s, s * 2, -s), Point3D(s, 0, -s)))
            particle.append(Line3D(Point3D(s, 0, -s), Point3D(s, 0, s)))

            # left
            particle.append(Line3D(Point3D(-s, 0, s), Point3D(-s, s * 2, s)))
            particle.append(Line3D(Point3D(-s, s * 2, s), Point3D(-s, s * 2, -s)))
            particle.append(Line3D(Point3D(-s, s * 2, -s), Point3D(-s, 0, -s)))
            particle.append(Line3D(Point3D(-s, 0, -s), Point3D(-s, 0, s)))
            RenderEngine.renderObject(particle)


        
    def update(self, elapsedTime):
        Object3D.update(self, elapsedTime)
        self.fuseTime += elapsedTime

        if (self.fuseTime > self.fuseDuration and not self.explode):
            self.explode = True
            self.particles.reset()
            self.particles.emit = True
            self.particles.emitting = True
            self.decayTime = 0
            self.size = np.array([6,6,6])
            self.particles.position = np.copy(self.position)
        if (self.explode):
            self.decayTime += elapsedTime
            if (self.decayTime > self.particles.decayRate):
                self.decayed = True
        self.particles.update(elapsedTime)
