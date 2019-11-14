from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Window3d:
    model3d = None

    def __init__(self, m):
        self.model3d = m

    def update(self):
        self.draw3d()

    def drawModel3d(self):
        for f in self.model3d.faces:
            he = f.halfedge
            count = 0
            glColor3f(f.colorR, f.colorG, f.colorB)
            glBegin(GL_LINE_LOOP)
            while True:
                glVertex3f(he.vertex.x, he.vertex.y, he.vertex.z)
                he = he.next
                count += 1
                if count == f.NumOfEdges:
                    break
            glEnd()


    def draw3d(self):
        #print("draw",flush=True)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        ##set camera
        maxX = -1000000
        minX = 1000000
        maxY = -1000000
        minY = 1000000
        maxZ = -1000000
        minZ = 1000000
        for v in self.model3d.vertices:
            if v.x > maxX:
                maxX = v.x
            if v.x < minX:
                minX = v.x
            if v.y > maxY:
                maxY = v.y
            if v.y < minY:
                minY = v.y
            if v.z > maxZ:
                maxZ = v.z
            if v.z < minZ:
                minZ = v.z
        gluLookAt((minX+maxX)/2, (minY+maxY)/2, 1.3*max((maxY-minY), (maxX-minX)) + maxZ, (minX+maxX)/2, (minY+maxY)/2, (minZ+maxZ)/2, 0.0, 1.0, 0.0)
        ##draw a teapot
        self.drawModel3d()
        #glutSolidTeapot(1.0)  # solid
        glFlush()  # enforce OpenGL command

    def init3d(self, width, height):
        #print("init",flush=True)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST) # enable shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        ##set perspective
        gluPerspective(45.0, float(width)/float(height), 0.1, 10000.0)

    def resize3d(self, w, h):
        #print("resize",flush=True)
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w)/float(h), 0.1, 10000.0)

    def mouseInput(self, button, state, x, y):
        self.update()

    def keyInput(self, key, x, y):
        if key == b' ':
            self.polygonsInfo()
        self.update()

    def polygonsInfo(self):
        print("----------model3d-----------")
        print("len(faces) = " + str(len(self.model3d.faces)))
        print("len(halfedges) = " + str(len(self.model3d.halfedges)))
        print("len(vertices) = " + str(len(self.model3d.vertices)))
