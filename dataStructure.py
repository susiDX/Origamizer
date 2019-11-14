class Model3d:
    def __init__(self):
        self.faces = [] #ポインタのリスト
        self.halfedges = [] #ポインタのリスト
        self.vertices = [] #ポインタのリスト

class Vertex:
    def __init__(self, _x, _y, _z):
        self.x = _x #値
        self.y = _y #値
        self.z = _z #値
        self.halfedges = []
        self.vtm = None

class Halfedge:
    def __init__(self, _v):
        self.vertex = _v #ポインタ
        _v.halfedges.append(self)
        self.vertex_next = None #ポインタ
        self.pair = None #ポインタ
        self.next = None #ポインタ
        self.prev = None #ポインタ
        self.face = None
        self.halfedge2d = None #ポインタ
    def addNextvertex(self, _v):
        self.vertex_next = _v
        _v.halfedges.append(self)
    def addFace(self, _f):
        self.face = _f

class Face:
    def __init__(self, _he):
        self.halfedge = _he #ポインタ
        self.face2d = None
        self.NumOfEdges = None
        self.colorR = 1
        self.colorG = 1
        self.colorB = 1

class Model2d:
    def __init__(self):
        self.faces = [] #ポインタのリスト
        self.halfedges = [] #ポインタのリスト
        self.vertices = [] #ポインタのリスト
        self.vtms = []

class Vertex2d:
    def __init__(self, _x, _y, _z, _he):
        self.x = _x #値
        self.xDefo = _x
        self.y = _y #値
        self.yDefo = _y #値
        self.z = _z #値
        self.zDefo = _z #値
        self.halfedge = _he
        self.vtm = None
        self.sita = None
        self.sita_large = None

class Halfedge2d:
    def __init__(self, _he):
        self.vertex = None
        self.vertex_next = None
        self.halfedge3d = _he
        self.pair = None
        self.next = None
        self.prev = None
        self.face = None
        self.id = None

class Face2d:
    def __init__(self, _f):
        self.face3d = _f
        self.halfedge = None
        self.colorR = 0
        self.colorG = 1
        self.colorB = 0
        self.NumOfEdges = None

        self.flag_setBySita = False

class Vtm:
    def __init__(self, _v):
        self.vertex3d = _v
        self.halfedges = [] #境界から反時計回りに格納
        self.vertices = [] #境界から反時計回りに格納
        self.id = None
