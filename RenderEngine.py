from Geometry import *
from Camera import *
from Util3D import *
import numpy as np
import pygame

# Define the colors we will use in RGB format
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)

matrixStack = []
clipMatrix = None
drawColor = BLUE
fieldOfView = None
aspectRatio = None
nearPlane = None
farPlane = None
screenMatrix = None


def init(width, height):
    # Set the height and width of the screen
    global screen
    size = [width, height]
    screen = pygame.display.set_mode(size)
    global aspectRatio
    aspectRatio = float(width) / float(height)
    global screenMatrix
    screenMatrix = np.array(
        [[width/2, 0.0, width/2],
        [ 0.0, -height/2, height/2],
        [0.0, 0.0, 1.0]], dtype=float)


def render(camera, sceneObjects):
    # Clear the screen and set the screen background
    screen.fill(BLACK)
    camera.projectCamera()
    for sceneObject in sceneObjects:
        sceneObject.draw()
    pygame.display.flip()


def renderObject(sceneObject):
    sceneObject2 = sceneObject
    sceneObject2 = worldToCamera(sceneObject2)
    sceneObject2 = clipObjectTransform(sceneObject2)
    # Quit trying to render if everything was clipped!
    if (len(sceneObject2) > 0):
        sceneObject2 = projectObject(sceneObject2)
        sceneObject2 = transformViewport(sceneObject2)
        draw(sceneObject2)
    # uncomment to see how many lines are being drawn vs total lines per object
    # print str(len(sceneObject2)) + "/" + str(len(sceneObject))

def draw(sceneObject):
    for line in sceneObject:
        pygame.draw.line(screen, drawColor, (line.start.vector[:-1]),(line.end.vector[:-1]))

    
def transformViewport( sceneObject):
    for line in sceneObject:
        startV = line.start.vector[:-1]
        startV[2] = 1
        startV = np.matmul(screenMatrix, startV)
        line.start.vector = startV
        endV = line.end.vector[:-1]
        endV[2] = 1
        endV = np.matmul(screenMatrix, endV)
        line.end.vector = endV
    return sceneObject

def projectObject(sceneObject):
    for line in sceneObject:
        startV = line.start.vector
        startV[0] = startV[0] / startV[3]
        startV[1] = startV[1] / startV[3]
        startV[2] = startV[2] / startV[3]
        startV[3] = startV[3] / startV[3]
        line.start.vector = startV

        endV = line.end.vector
        endV[0] = endV[0] / endV[3]
        endV[1] = endV[1] / endV[3]
        endV[2] = endV[2] / endV[3]
        endV[3] = endV[3] / endV[3]
        line.end.vector = endV
    return sceneObject
    
def worldToCamera(sceneObject):
    transformation = matrixStack[-1]
    transformedObject = []
    for line in sceneObject:
        startV = np.matmul(transformation , line.start.vector)
        endV = np.matmul(transformation , line.end.vector)
        transformedObject.append(Line3D(Point3D(startV[0], startV[1], startV[2]), Point3D(endV[0], endV[1], endV[2])))

    return transformedObject

def clipObjectTransform(sceneObject):
    clippedObject = []
    for line in sceneObject:
        startV = np.matmul(clipMatrix, line.start.vector)
        endV = np.matmul(clipMatrix, line.end.vector)
        line.start.vector = startV
        line.end.vector = endV
        if (not isLineClipped(line)):
            clippedObject.append(line)
    return clippedObject

def isLineClipped(line):
    start = line.start.vector
    end = line.end.vector
    isClipped = False
    startOutside = False
    endOutside = False
    if (start[0] < -start[3] or start[0] > start[3]):
        startOutside = True
    if (start[1] < -start[3] or start[1] > start[3]):
        startOutside = True
    if (start[2] > start[3]):
        startOutside = True
    if (end[0] < -end[3] or end[0] > end[3]):
        endOutside = True
    if (end[1] < -end[3] or end[1] > end[3]):
        endOutside = True
    if (end[2] > end[3]):
        endOutside = True
    if (startOutside and endOutside):
        isClipped = True
    if (start[2] < -start[3] or start[2] > start[3]):
        isClipped = True
    if (end[2] < -end[3] or end[2] > end[3]):
        isClipped = True
    return isClipped

def buildClipMatrix(fieldOfView, aspectRatio, nearPlane, farPlane):
    radianAngle = math.radians(fieldOfView)
    zoomY = 1 / float(math.tan(radianAngle / 2.0))
    # TODO: This could be divide here, not multiply!
    zoomX = zoomY / aspectRatio
    clipMatrix = np.array(
        [[zoomX, 0.0, 0.0, 0.0],
        [ 0.0, zoomY, 0.0, 0.0], 
        [ 0.0, 0.0, float(farPlane + nearPlane) / float(farPlane - nearPlane), float(-2 * nearPlane * farPlane) / float(farPlane - nearPlane)],
        [ 0.0, 0.0, 1.0, 0.0]])
    return clipMatrix


def pushMatrix():
    matrixStack.append(np.copy(matrixStack[-1]))


def popMatrix():
    topValue = matrixStack.pop()


def perspective(fov, near, far):
    global clipMatrix
    clipMatrix = buildClipMatrix(fov, aspectRatio, near, far)


def lookAt(pos, look, up):
    v = (look - pos)
    e2 = v / float(magnitude(v))
    v = np.cross(e2, up)
    e0 = v / float(magnitude(v))
    v = np.cross(e0, e2)
    e1 = v / float(magnitude(v))
    cameraRotate = np.array(
        [[e0[0], e0[1], e0[2], 0.0],
         [e1[0], e1[1], e1[2], 0.0],
         [e2[0], e2[1], e2[2], 0.0],
         [0.0,   0.0,   0.0,   1.0]], dtype=float)
    multiplyMatrix(cameraRotate)
    translate(-pos[0], -pos[1], -pos[2])


def loadIdentity():
    del matrixStack[:]
    matrixStack.append(np.array(
        [[1.0, 0.0, 0.0, 0.0],
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0, 1.0]], dtype=float))


def translate(x, y, z):
    translation = np.array(
        [[1.0, 0.0, 0.0, float(x)],
         [0.0, 1.0, 0.0, float(y)],
         [0.0, 0.0, 1.0, float(z)],
         [0.0, 0.0, 0.0, 1.0]], dtype=float)
    multiplyMatrix(translation)


def rotateY(angle):
    radianAngle = math.radians(angle)
    rotation = np.array(
        [[math.cos(radianAngle),  0.0, -math.sin(radianAngle), 0.0],
         [0.0,                    1.0, 0.0,                   0.0],
         [math.sin(radianAngle), 0.0, math.cos(radianAngle), 0.0],
         [0.0,                    0.0, 0.0,                 1.0]], dtype=float)
    multiplyMatrix(rotation)

def rotateZ(angle):
    radianAngle = math.radians(angle)
    rotation = np.array(
        [[math.cos(radianAngle), -math.sin(radianAngle), 0.0, 0.0],
         [math.sin(radianAngle), math.cos(radianAngle),  0.0, 0.0],
         [0.0,                   0.0,                    1.0, 0.0],
         [0.0,                   0.0,                    0.0, 1.0]], dtype=float)
    multiplyMatrix(rotation)

def setColor(color):
    global drawColor
    drawColor = color

def multiplyMatrix(matrix):
    lastMatrix = matrixStack[-1]
    matrixStack[-1] = np.matmul(lastMatrix, matrix)
