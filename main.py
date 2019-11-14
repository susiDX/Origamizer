from fileInAndOut import *
from dataStructure import *
from window2d import *
from window3d import *
from conv3dTo2d import *

import sys
#model0 face=10
#model1 face=18
#model2 bunny170
#model3 bell
#model4 donut
#model5 donuts
#model6 mask
filepath = "C:\\Users\\katou\\Desktop\\origamizer\\Origamizer_self_now\\model3.obj"
model3d = loadOBJ(filepath)
model2d = conv3dTo2d(model3d)

def main():
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(910, 100)
    glutCreateWindow("2d")
    win2d = Window2d(model2d)
    win2d.init2d(400, 400)
    glutDisplayFunc(win2d.draw2d)
    glutReshapeFunc(win2d.resize2d)
    glutMouseFunc(win2d.mouseInput)
    glutKeyboardFunc(win2d.keyInput)

    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("3d")
    win3d = Window3d(model3d)
    win3d.init3d(400,400)
    glutDisplayFunc(win3d.draw3d)
    glutReshapeFunc(win3d.resize3d)
    glutMouseFunc(win3d.mouseInput)
    glutKeyboardFunc(win3d.keyInput)

    glutMainLoop()

if __name__ == "__main__":
    main()
