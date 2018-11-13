from Geometry import *
import RenderEngine
from Firework import *
from Camera import *
from Ground import *
from House import *
from Car import *
import pygame
from math import pi


def controlCamera(pressed):
    if pressed[pygame.K_w]:
        camera.moveForward(speed)
    if pressed[pygame.K_s]:
        camera.moveBackward(speed)
    if pressed[pygame.K_a]:
        camera.moveLeft(speed)
    if pressed[pygame.K_d]:
        camera.moveRight(speed)
    if pressed[pygame.K_q]:
        camera.turnLeft(speed * 3.5)
    if pressed[pygame.K_e]:
        camera.turnRight(speed * 3.5)
    if pressed[pygame.K_r]:
        camera.moveUp(speed)
    if pressed[pygame.K_f]:
        camera.moveDown(speed)


def controlCar(pressed):
    global car
    if pressed[pygame.K_w]:
        car.accelerate()
    if pressed[pygame.K_s]:
        car.brake()
    if pressed[pygame.K_a]:
        car.turnLeft()
    if pressed[pygame.K_d]:
        car.turnRight()
    if pressed[pygame.K_r]:
        car.isBackingUp = True
    if pressed[pygame.K_f]:
        car.isBackingUp = False
    if pressed[pygame.K_t] and car.position[1] <= 0:
        car.velocity[1] += speed * 1.2
    if pressed[pygame.K_SPACE]:
        v = car.look * 3
        v[1] = v[1] + 0.5
        p = np.copy(car.position)
        p[1] = p[1] + 4
        firework = Firework(positionX=p[0], positionY=p[1], positionZ=p[2],
                            velocityX=v[0], velocityY=v[1], velocityZ=v[2])
        sceneObjects.append(firework)


def controller():
    global done
    global isControlCar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            done = True
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        done = True

    if (isControlCar):
        controlCar(pressed)
    else:
        controlCamera(pressed)

    if (pressed[pygame.K_x]):
        isControlObject = False
        isControlCar = False
    if (pressed[pygame.K_z]):
        isControlCar = True
        isControlObject = False
    if (pressed[pygame.K_l]):
        camera.follow = car
    if (pressed[pygame.K_k]):
        camera.follow = None
    if pressed[pygame.K_j]:
        for sceneObject in sceneObjects:
            sceneObject.reset()
        figure8Timer = 0
    if pressed[pygame.K_h]:
        for sceneObject in sceneObjects:
            sceneObject.reset()
        camera.reset()
        figure8Timer = 0


figure8Timer = 0
figure8Switch = 8000


def animate(elapsedTime):
    global figure8Timer
    global figure8Switch
    global car2
    global car3
    global car4
    figure8Timer += elapsedTime
    if (figure8Timer > figure8Switch):
        figure8Timer = figure8Timer % figure8Switch
        car2.steeringAngle = -car2.steeringAngle
    car2.accelerate()
    if (magnitude(car3.position) > 200):
        car3.reset()
    if (magnitude(car4.position) > 200):
        car4.reset()
    car3.accelerate()
    car4.accelerate()


def update(elapsedTime):
    global physicsSimulator
    global sceneObjects
    animate(elapsedTime)
    physicsSimulator.simulatePhysics(elapsedTime, sceneObjects)
    deadFireworks = []
    for sceneObject in sceneObjects:
        if (isinstance(sceneObject, Firework)):
            if(sceneObject.decayed):
                deadFireworks.append(sceneObject)
    for deadFirework in deadFireworks:
        sceneObjects.remove(deadFirework)


pygame.init()
RenderEngine.init(640, 480)
camera = Camera(-9, 4, -26, 70)
physicsSimulator = PhysicsSimulator()
physicsSimulator.simulate = True
isControlCar = False

sceneObjects = []
ground = Ground()
sceneObjects.append(ground)
sceneObjects.extend(generateNeighborhood())
car = Car(positionZ=20, rotationY=0)
car.mass = 15
sceneObjects.append(car)
car2 = Car(positionZ=40, positionX=-20, steeringAngle=10)
sceneObjects.append(car2)
car3 = Car(positionZ=11, positionX=-40, driveAcceleration=0.06)
car3.mass = 15
sceneObjects.append(car3)
car4 = Car(positionZ=11, positionX=40, rotationY=180, driveAcceleration=0.06)
sceneObjects.append(car4)
speed = 1

done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(30)
    controller()
    update(30)
    RenderEngine.render(camera, sceneObjects)

pygame.quit()
