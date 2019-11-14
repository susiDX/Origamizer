from dataStructure import *

def loadOBJ(fliePath):
    vertices = []
    faces = []
    numVertices = 0
    numFaces = 0
    for line in open(fliePath, "r"):
        vals = line.split()
        if len(vals) == 0:
            continue
        if vals[0] == "v":
            v = [float(vals[1]), float(vals[2]), float(vals[3])]
            vertices.append(v)
            numVertices += 1
        if vals[0] == "f":
            fvID = []
            for f in vals[1:]:
                w = f.split("/")
                fvID.append(int(w[0])-1)
            faces.append(fvID)
            numFaces += 1
    return convToDataStructure(vertices, faces)

def convToDataStructure(vertices, faces):
    # dataStructureへ変換
    model = Model3d()
    for v in vertices:
        v = Vertex(v[0],v[1],v[2])
        model.vertices.append(v)

    for f in faces:
        count = 0

        heStart = Halfedge(model.vertices[f[0]])
        count += 1
        newFace = Face(heStart)
        heStart.addFace(newFace)

        model.halfedges.append(heStart)
        model.faces.append(newFace)
        #print(heStart.next,flush=True)
        heBefore = heStart
        for i in range(1, len(f)-1):
            he = Halfedge(model.vertices[f[i]])
            count += 1
            he.addFace(newFace)

            model.halfedges.append(he)

            heBefore.next = he
            heBefore.addNextvertex(he.vertex)
            he.prev = heBefore

            heBefore = he

        heEnd = Halfedge(model.vertices[f[-1]])
        count += 1
        heEnd.addFace(newFace)
        newFace.NumOfEdges = count

        model.halfedges.append(heEnd)

        heBefore.next = heEnd
        heBefore.addNextvertex(heEnd.vertex)
        heEnd.prev = heBefore

        heEnd.next = heStart
        heEnd.addNextvertex(heStart.vertex)
        heStart.prev = heEnd

        addHalfedgePair(count, model)

    return model

def addHalfedgePair(count, model):
    allHalfedges = model.halfedges
    existedHalfedges = allHalfedges[:len(allHalfedges)-count]
    newHalfedges = allHalfedges[len(allHalfedges)-count:]
    for newHe in newHalfedges:
        for existedHe in existedHalfedges:
            if (newHe.vertex == existedHe.vertex and newHe.vertex_next == existedHe.vertex_next) or (newHe.vertex == existedHe.vertex_next and newHe.vertex_next == existedHe.vertex):
                newHe.pair = existedHe
                existedHe.pair = newHe
