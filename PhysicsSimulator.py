import math
from Object3D import *
import numpy as np
from Util3D import *


class PhysicsSimulator:
    def __init__(self, simulationSlowdown=4000, gravityAcceleration=9.8, checkCollisions = True):
        self.simulationSlowdown = simulationSlowdown
        self.gravityAcceleration = gravityAcceleration
        self.checkCollisions = checkCollisions
        self.simFloor = True
        self.simGravity = True
        self.simulate = False

    def simulatePhysics(self, elapsedTime, sceneObjects):
        elapsedTime /= float(self.simulationSlowdown)
        if (self.simulate):
            for sceneObject in sceneObjects:
                sceneObject.update(elapsedTime)
            if (self.checkCollisions):
                self.simulateCollisions(elapsedTime, sceneObjects)
            if (self.simGravity):
                self.simulateGravity(elapsedTime, sceneObjects)
            if (self.simFloor):
                self.simulateFloor(elapsedTime, sceneObjects)

    def simulateCollisions(self, elapsedTime, sceneObjects):
        objectCount = len(sceneObjects)
        collision = False
        for i in range(objectCount):
            if (sceneObjects[i].checkCollisions):
                for j in range(i + 1, objectCount):
                    objectA = sceneObjects[i]
                    objectB = sceneObjects[j]
                    if (objectB.checkCollisions):
                        if (objectA.intersects(objectB)):
                            collision = True
                            v1 = objectA.velocity
                            v2 = objectB.velocity
                            # pull the two objects out of each other (because they've intersected)
                            objectA.position -= objectA.velocity * 2
                            objectA.update(elapsedTime)
                            objectB.position -= objectB.velocity * 2
                            objectB.update(elapsedTime)

                            # perform collision
                            self.collide(objectA, objectB, v1, v2)
                            objectA.update(elapsedTime)
                            objectB.update(elapsedTime)
                            # let each object have the chance to do something special on a collision
                            objectA.collisionCallback(objectB, v1, v2)
                            objectB.collisionCallback(objectA, v2, v1)

    # https://en.wikipedia.org/wiki/Elastic_collision
    def collide(self, objectA, objectB, v1, v2):
        # v1 = objectA.velocity
        # v2 = objectB.velocity
        m1 = float(objectA.mass)
        m2 = float(objectB.mass)
        x1 = objectA.position
        x2 = objectB.position
        bottom1 = math.pow(magnitude(x1 - x2), 2)
        bottom2 = math.pow(magnitude(x2 - x1), 2)
        if (bottom1 == 0):
            bottom1 = 1
        if (bottom2 == 0):
            bottom2 = 1
        v1New = v1 - ((2 * m2) / (m1 + m2)) * ((v1 - v2).dot(x1 - x2) / bottom1) * (x1 - x2)
        v2New = v2 - ((2 * m1) / (m1 + m2)) * ((v2 - v1).dot(x2 - x1) / bottom2) * (x2 - x1)
        objectA.velocity = v1New
        objectB.velocity = v2New

    def simulateGravity(self, elapsedTime, sceneObjects):
        for sceneObject in sceneObjects:
            sceneObject.velocity[1] -= self.gravityAcceleration * elapsedTime

    def simulateFloor(self, elapsedTime, sceneObjects):
        for sceneObject in sceneObjects:
            if (sceneObject.position[1] <= 0):
                sceneObject.position[1] = 0
                sceneObject.velocity[1] = 0
                # facingVector = sceneObject.look - sceneObject.position
                sideVector = np.array(
                    [-sceneObject.look[2], 0, sceneObject.look[0]], dtype=float)

                angle = angleBetween(sceneObject.look, sceneObject.velocity)
                percSide = (angle / 90.0)
                frictionCoefficient = (
                    1 - percSide) * sceneObject.friction[0] + percSide * sceneObject.friction[2]
                frictionMagnitude = sceneObject.mass * \
                    self.gravityAcceleration * frictionCoefficient
                velocityUnit = np.copy(sceneObject.velocity)
                velocityUnit[1] = 0
                velocityUnit = makeUnitVector(velocityUnit)
                friction = velocityUnit * frictionMagnitude
                objectSpeed = magnitude(sceneObject.velocity)
                if (objectSpeed < magnitude(friction) or objectSpeed < 0.001):
                    sceneObject.velocity[0] = 0
                    sceneObject.velocity[2] = 0
                else:
                    sceneObject.velocity -= friction
