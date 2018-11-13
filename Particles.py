import random
import RenderEngine 
from Object3D import *
from PhysicsSimulator import *


class Particles(Object3D):
    def __init__(self, positionX=0, positionY=0, positionZ=0):
        Object3D.__init__(self, positionX=positionX,
                          positionY=positionY, positionZ=positionZ)
        self.particles = []
        self.emitting = False
        self.decayRate = 0.1
        self.emitRate = 6
        self.emitDuration = 0.01
        self.simulator = PhysicsSimulator(simulationSlowdown = 1)
        self.simulator.simulate = True
        self.reset()

    def reset(self):
        del self.particles[:]
        self.emitting = False
        self.emitTime = 0

    def update(self, elapsedTime=0):
        if (self.emitting):
            self.emitTime += elapsedTime
            if (self.emitTime > self.emitDuration):
                self.emitting = False
            for i in range(self.emitRate):
                vX = 0.5 - random.random() * 1
                vY = 0.25 + random.random() * 0.5
                vZ = 0.5 - random.random() * 1
                particle = Particle(0,0,
                                    0, vX, vY, vZ, self.decayRate)
                particle.mass = 10
                self.particles.append(particle)

        self.simulator.simulatePhysics(elapsedTime, self.particles)
        deadParticles = []
        for particle in self.particles:
            if (particle.decay >= particle.decayRate):
                deadParticles.append(particle)
        for deadParticle in deadParticles:
            self.particles.remove(deadParticle)


    def drawObject(self):
        for particle in self.particles:
            particle.draw()


class Particle(Object3D):
    def __init__(self, positionX=0, positionY=0, positionZ=0, velocityX = 0, velocityY = 0, velocityZ = 0, decayRate = 1):
        Object3D.__init__(self, positionX=positionX, positionY=positionY, positionZ=positionZ,
                          velocityX=velocityX, velocityY=velocityY, velocityZ=velocityZ)
        self.decayRate = decayRate
        self.colorR0 = 1.0
        self.colorG0 = 1.0
        self.colorB0 = 0.0
        self.colorR1 = 0.25
        self.colorG1 = 0.0
        self.colorB1 = 0.0
        self.drawAxes = False
        self.checkCollisions = False
        self.reset()
    
    def update(self, elapsedTime):
        Object3D.update(self, elapsedTime)
        self.decay += elapsedTime

    def reset(self):
        self.decay = 0

    def drawObject(self):
        p = self.decay / self.decayRate
        r = self.colorR1 * p + self.colorR0 * (1-p)
        g = self.colorG1 * p + self.colorG0 * (1-p)
        b = self.colorB1 * p + self.colorB0 * (1-p)
        s = (1 - p) * 0.25
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
