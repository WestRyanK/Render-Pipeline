from Object3D import *
import RenderEngine


class Ground(Object3D):

    def __init__(self):
        Object3D.__init__(self)
        self.checkCollisions = False

    def drawLines(self, count, spacing, angle, x, z):
        w = 0.3
        l = 1.5
        RenderEngine.pushMatrix()
        RenderEngine.translate(x, 0, z)
        RenderEngine.rotateY(angle)
        for i in range(count):
            RenderEngine.pushMatrix()
            line = []
            RenderEngine.translate(i * spacing, 0, 0)
            line.append(Line3D(Point3D(l, 0.02, w),  Point3D(l, 0.02, -w)))
            line.append(Line3D(Point3D(l, 0.02, -w),  Point3D(-l, 0.02, -w)))
            line.append(Line3D(Point3D(-l, 0.02, -w),  Point3D(-l, 0.02, w)))
            line.append(Line3D(Point3D(-l, 0.02, w),  Point3D(l, 0.02, w)))
            RenderEngine.renderObject(line)
            RenderEngine.popMatrix()
        RenderEngine.popMatrix()

    def drawObject(self):
        RenderEngine.setColor((255, 255, 0))
        self.drawLines(10, 5, 0, 15, 7.5)
        self.drawLines(10, 5, 180, -3, 7.5)
        self.drawLines(10, 5, -90, 7.5, 0)
        self.drawLines(10, 5, 90, 7.5, 15)
