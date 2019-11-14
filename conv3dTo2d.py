from dataStructure import *

def conv3dTo2d(model3d):
    model2d = Model2d()

    for he in model3d.halfedges:
        he.halfedge2d = Halfedge2d(he)
        model2d.halfedges.append(he.halfedge2d)
    for f in model3d.faces:
        f.face2d = Face2d(f)
        f.face2d.NumOfEdges = f.NumOfEdges
        model2d.faces.append(f.face2d)

    for f in model2d.faces:
        f.halfedge = f.face3d.halfedge.halfedge2d
    for he in model2d.halfedges:
        pairX = he.halfedge3d.pair
        if pairX != None:
            he.pair = pairX.halfedge2d
        he.next = he.halfedge3d.next.halfedge2d
        he.prev = he.halfedge3d.prev.halfedge2d
        he.face = he.halfedge3d.face.face2d

    for f in model2d.faces:
        heStart = f.halfedge
        he = heStart
        he.vertex = Vertex2d(he.halfedge3d.vertex.x, he.halfedge3d.vertex.y, he.halfedge3d.vertex.z, he)
        model2d.vertices.append(he.vertex)
        while True:
            he = he.next
            if he == heStart:
                break
            he.vertex = Vertex2d(he.halfedge3d.vertex.x, he.halfedge3d.vertex.y, he.halfedge3d.vertex.z, he)
            he.prev.vertex_next = he.vertex
            model2d.vertices.append(he.vertex)
        heStart.prev.vertex_next = heStart.vertex

    # for vtm
    for v in model3d.vertices:
        v.vtm = Vtm(v)
        model2d.vtms.append(v.vtm)

        heStart = None
        for he in v.halfedges:
            if he.vertex == v:
                heStart = he
                break
        he = heStart
        while True:
            if he.pair == None:
                heStart = he
                break
            he = he.pair.next
            if heStart == he:
                break

        v.vtm.halfedges.append(heStart.halfedge2d)
        v.vtm.halfedges.append(heStart.prev.halfedge2d)
        v.vtm.vertices.append(heStart.halfedge2d.vertex)
        heStart.halfedge2d.vertex.vtm = v.vtm
        he = heStart
        while True:
            if he.prev.pair == None or he.prev.pair == heStart:
                break
            he = he.prev.pair
            v.vtm.halfedges.append(he.halfedge2d)
            v.vtm.halfedges.append(he.prev.halfedge2d)
            v.vtm.vertices.append(he.halfedge2d.vertex)
            he.halfedge2d.vertex.vtm = v.vtm

    return model2d
