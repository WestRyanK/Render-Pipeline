import math
import RenderEngine
from Object3D import *


class Camera(Object3D):
    def __init__(self, positionX=0, positionY=0, positionZ=0, rotationY=0, usePerspective=True, follow=None, followDistance=np.array([15.0, 5.0, 0.0], dtype=float)):
        Object3D.__init__(self, positionX=positionX, positionY=positionY,
                          positionZ=positionZ, rotationY=rotationY)
        self.homeUsePerspective = usePerspective
        self.follow = follow
        self.followDistance = followDistance
        self.reset()

    def setX(self, x):
        self.position[0] = x
        self.update()

    def setY(self, y):
        self.position[1] = y
        self.update()

    def setZ(self, z):
        self.position[2] = z
        self.update()

    def moveForward(self, speed):
        radianAngle = math.radians(self.rotation[1])
        self.position[0] += (math.cos(radianAngle)) * speed
        self.position[2] += (math.sin(radianAngle)) * speed
        self.update()

    def moveBackward(self, speed):
        radianAngle = math.radians(self.rotation[1])
        self.position[0] -= (math.cos(radianAngle)) * speed
        self.position[2] -= (math.sin(radianAngle)) * speed
        self.update()

    def moveLeft(self, speed):
        radianAngle = math.radians(self.rotation[1] + 90)
        self.position[0] -= (math.cos(radianAngle)) * speed
        self.position[2] -= (math.sin(radianAngle)) * speed
        self.update()

    def moveRight(self, speed):
        radianAngle = math.radians(self.rotation[1] + 90)
        self.position[0] += (math.cos(radianAngle)) * speed
        self.position[2] += (math.sin(radianAngle)) * speed
        self.update()

    def moveUp(self, speed):
        self.position[1] += speed
        self.update()

    def moveDown(self, speed):
        self.position[1] -= speed
        self.update()

    def turnLeft(self, speed):
        self.setRotationY(self.rotation[1] - speed)

    def turnRight(self, speed):
        self.setRotationY(self.rotation[1] + speed)

    def reset(self):
        Object3D.reset(self)
        self.usePerspective = self.homeUsePerspective
        self.update()

    def projectCamera(self):
        RenderEngine.loadIdentity()
        self.setPerspectiveProjection()

        up = np.array([0.0, 1.0, 0.0], dtype=float)
        if (self.follow != None):
            offset = self.follow.position - self.follow.look
            offset = np.array([-self.follow.look[0] * self.followDistance[0],
                               self.followDistance[1], -self.follow.look[2] * self.followDistance[0]])
            RenderEngine.lookAt(self.follow.position +
                                offset, self.follow.position, up)
        else:
            RenderEngine.lookAt(self.position, self.position + self.look, up)

    def setPerspectiveProjection(self):
        RenderEngine.perspective(60, 5, 1000)