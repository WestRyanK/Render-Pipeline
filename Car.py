import math
from Particles import *
import random
from Object3D import *
from Util3D import *
from Geometry import *

class Car(Object3D):
    def __init__(self, positionX = 0, positionZ = 0, rotationY = 0, driveAcceleration = 0.2, brakeAcceleration = 0.2, maxSpeed = 6, isBackingUp = False, steeringAngle = 0, maxSteeringAngle = 15):
        radianAngle = math.radians(rotationY)
        Object3D.__init__(self, positionX = positionX, positionZ = positionZ, rotationY = rotationY, frictionX = 0.0002, frictionZ = 0.005)
        self.homeDriveAcceleration = driveAcceleration
        self.homeBrakeAcceleration = brakeAcceleration
        self.homeMaxSpeed = maxSpeed
        self.checkCollisions = True
        self.homeIsBackingUp = isBackingUp
        self.homeSteeringAngle = steeringAngle
        self.homeMaxSteeringAngle = maxSteeringAngle
        self.steeringAngleChange = 2.0
        self.mass = 10
        self.bumperInset = 0.2 + random.random() * 0.4
        self.roofInset = 0.2 + random.random() * 0.4
        self.carLift = 1.5
        self.doorHeight = random.random() * 0.75 + 0.5
        self.bodyHeight = random.random() + 1.75
        self.paintR = random.random()
        self.paintG = random.random()
        self.paintB = random.random()
        self.particles = Particles()
        self.particles.decayRate = 0.2
        self.particles.emit = False
        length = random.random() + 5.5
        width = random.random() + 3.5
        self.size = np.array([length, self.carLift + self.bodyHeight, width], dtype=float)
        self.reset()

    def reset(self):
        Object3D.reset(self)
        self.driveAcceleration = self.homeDriveAcceleration
        self.brakeAcceleration = self.homeBrakeAcceleration
        self.maxSpeed = self.homeMaxSpeed
        self.isBackingUp = self.homeIsBackingUp
        self.isBraking = True
        self.steeringAngle = self.homeSteeringAngle
        self.maxSteeringAngle = self.homeMaxSteeringAngle
        self.tireRotation = 0
        self.particles.reset()
    
    def collisionCallback(self, otherObject, initialVelocitySelf, initialVelocityOther):
        speed = magnitude(initialVelocitySelf - initialVelocityOther) * 0.1
        self.velocity[1] = min(0.4, speed)
        self.particles.reset()
        impactPoint =  ((self.position + otherObject.position) / 2.0) 
        self.particles.emitting = True
        self.particles.position = impactPoint
        self.update()

    def accelerate(self):
        self.isBraking = self.isBackingUp
        if (self.position[1] <= 0):
            if not self.isBackingUp:
                self.velocity[0] +=  self.look[0] * self.driveAcceleration
                self.velocity[2] += self.look[2] * self.driveAcceleration
            else:
                self.velocity[0] -=  self.look[0] * self.driveAcceleration
                self.velocity[2] -= self.look[2] * self.driveAcceleration


    def brake(self):
        self.isBraking = True
        if (self.position[1] <= 0):
            brake = self.look * self.brakeAcceleration
            if (magnitude(self.velocity) < magnitude(brake)):
                self.velocity[0] = 0
                self.velocity[1] = 0
                self.velocity[2] = 0
            else:
                self.velocity -= brake

    def turnLeft(self):
        if (self.isBackingUp == False):
            self.isBraking = False
        if (math.fabs(self.steeringAngle) < 4):
            self.steeringAngle += self.steeringAngleChange * 0.25
        else:
            self.steeringAngle += self.steeringAngleChange
        if (self.steeringAngle > self.maxSteeringAngle):
            self.steeringAngle = self.maxSteeringAngle

    def turnRight(self):
        if (self.isBackingUp == False):
            self.isBraking = False
        if (math.fabs(self.steeringAngle) < 4):
            self.steeringAngle -= self.steeringAngleChange * 0.25
        else:
            self.steeringAngle -= self.steeringAngleChange
        if (self.steeringAngle < -self.maxSteeringAngle):
            self.steeringAngle = -self.maxSteeringAngle

    def update(self, elapsedTime = 0):
        changeAngle = self.steeringAngle * magnitude(self.velocity) * 0.5
        speedForward = self.look.dot(self.velocity)
        self.tireRotation -= speedForward * 15
        if (not self.isBackingUp):
            self.rotation[1] -= changeAngle
            self.updateLookAt()
        else:
            self.rotation[1] += changeAngle
            self.updateLookAt()
        self.particles.update(elapsedTime)
        Object3D.update(self)


    def drawObject(self):
        RenderEngine.pushMatrix()
        RenderEngine.rotateY(-self.rotation[1])
        RenderEngine.translate(-self.position[0], -self.position[1], -self.position[2])
        self.particles.draw()
        RenderEngine.popMatrix()
        carWidth = self.size[2] * 0.5
        carLength = self.size[0] * 0.5
        bumperWidth = carWidth - self.bumperInset
        tireLocation = carLength - 1.5
        self.drawTireInstance(self.tireRotation, tireLocation, 1, carWidth, self.steeringAngle)
        self.drawTireInstance(self.tireRotation, tireLocation, 1, -carWidth, self.steeringAngle)
        self.drawTireInstance(self.tireRotation, -tireLocation, 1, carWidth)
        self.drawTireInstance(self.tireRotation, -tireLocation, 1, -carWidth)

        self.drawCarBody()

    def drawTireInstance(self, tireRotation = 0, tireX = 0, tireY = 0, tireZ = 0, steeringAngle = 0):
        RenderEngine.pushMatrix()
        RenderEngine.translate(tireX, tireY, tireZ)
        RenderEngine.rotateY(-steeringAngle)
        RenderEngine.rotateZ(tireRotation)
        self.drawTire()
        RenderEngine.popMatrix()

    def drawCarBody(self):
        w = self.size[2] * 0.5 # car width
        rw = w - self.roofInset # rear window width
        fb = w - self.bumperInset # front bumper width
        li = self.carLift
        dh = self.doorHeight + li
        h = self.size[1]
        l = self.size[0] * 0.5
        wi = l - 1

        RenderEngine.setColor((self.paintR * 255, self.paintG * 255, self.paintB * 255))
        car = []
        # back windshield
        car.append(Line3D(Point3D(-l,dh,fb), Point3D(-wi,h,rw)))
        car.append(Line3D(Point3D(-wi,h,rw), Point3D(-wi,h,-rw)))
        car.append(Line3D(Point3D(-wi,h,-rw), Point3D(-l,dh,-fb)))
        car.append(Line3D(Point3D(-l,dh,-fb), Point3D(-l,dh,fb)))

        # front windshield
        car.append(Line3D(Point3D(l,dh,fb), Point3D(wi,h,rw)))
        car.append(Line3D(Point3D(wi,h,rw), Point3D(wi,h,-rw)))
        car.append(Line3D(Point3D(wi,h,-rw), Point3D(l,dh,-fb)))
        car.append(Line3D(Point3D(l,dh,-fb), Point3D(l,dh,fb)))

        # right window
        car.append(Line3D(Point3D(wi,dh,w), Point3D(-wi,dh,w)))
        car.append(Line3D(Point3D(-wi,dh,w), Point3D(-wi,h,rw)))
        car.append(Line3D(Point3D(-wi,h,rw), Point3D(wi,h,rw)))
        car.append(Line3D(Point3D(wi,h,rw), Point3D(wi,dh,w)))

        # left window
        car.append(Line3D(Point3D(wi,dh,-w), Point3D(-wi,dh,-w)))
        car.append(Line3D(Point3D(-wi,dh,-w), Point3D(-wi,h,-rw)))
        car.append(Line3D(Point3D(-wi,h,-rw), Point3D(wi,h,-rw)))
        car.append(Line3D(Point3D(wi,h,-rw), Point3D(wi,dh,-w)))

        # trunk
        car.append(Line3D(Point3D(-l,dh,fb), Point3D(-l,li,fb)))
        car.append(Line3D(Point3D(-l,li,fb), Point3D(-l,li,-fb)))
        car.append(Line3D(Point3D(-l,li,-fb), Point3D(-l,dh,-fb)))
        car.append(Line3D(Point3D(-l,dh,-fb), Point3D(-l,dh,fb)))

        # front bumper
        car.append(Line3D(Point3D(l,dh,fb), Point3D(l,li,fb)))
        car.append(Line3D(Point3D(l,li,fb), Point3D(l,li,-fb)))
        car.append(Line3D(Point3D(l,li,-fb), Point3D(l,dh,-fb)))
        car.append(Line3D(Point3D(l,dh,-fb), Point3D(l,dh,fb)))

        # back right panel
        car.append(Line3D(Point3D(-wi,dh,w), Point3D(-l,dh,fb)))
        car.append(Line3D(Point3D(-l,dh,fb), Point3D(-l,li,fb)))
        car.append(Line3D(Point3D(-l,li,fb), Point3D(-wi,li,w)))
        car.append(Line3D(Point3D(-wi,li,w), Point3D(-wi,dh,w)))

        # front right panel
        car.append(Line3D(Point3D(wi,dh,w), Point3D(l,dh,fb)))
        car.append(Line3D(Point3D(l,dh,fb), Point3D(l,li,fb)))
        car.append(Line3D(Point3D(l,li,fb), Point3D(wi,li,w)))
        car.append(Line3D(Point3D(wi,li,w), Point3D(wi,dh,w)))

        # back left panel
        car.append(Line3D(Point3D(-wi,dh,-w), Point3D(-l,dh,-fb)))
        car.append(Line3D(Point3D(-l,dh,-fb), Point3D(-l,li,-fb)))
        car.append(Line3D(Point3D(-l,li,-fb), Point3D(-wi,li,-w)))
        car.append(Line3D(Point3D(-wi,li,-w), Point3D(-wi,dh,-w)))

        # front left panel
        car.append(Line3D(Point3D(wi,dh,-w), Point3D(l,dh,-fb)))
        car.append(Line3D(Point3D(l,dh,-fb), Point3D(l,li,-fb)))
        car.append(Line3D(Point3D(l,li,-fb), Point3D(wi,li,-w)))
        car.append(Line3D(Point3D(wi,li,-w), Point3D(wi,dh,-w)))

        car.append(Line3D(Point3D(-wi,li,-w), Point3D(wi,li,-w)))
        car.append(Line3D(Point3D(-wi,li,w), Point3D(wi,li,w)))
        RenderEngine.renderObject(car)
        
    def drawTire(self):
        RenderEngine.setColor((64, 64, 64))
        tire = []
        #Front Side
        tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
        tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
        tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
        tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
        tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
        tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
        tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
        tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

        #Back Side
        tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
        tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
        tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
        tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
        tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
        tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
        tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
        tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

        #Connectors
        tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
        tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
        tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
        tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
        tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
        tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
        tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
        tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
        RenderEngine.renderObject(tire)