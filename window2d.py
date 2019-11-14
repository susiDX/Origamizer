from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math
import time

class Window2d:
    model2d = None

    def __init__(self, m):
        self.model2d = m

    def update(self):
        self.draw2d()

    def drawModel2d(self):
        """ #反時計回りの構造チェック
        vtm = self.model2d.vtms[20]
        print(len(vtm.vertices), flush=True)
        for i in range(int(len(vtm.halfedges)/2)):
            vtm.halfedges[i*2].face.colorR = i/len(vtm.halfedges)
            vtm.halfedges[i*2].face.colorG = i/len(vtm.halfedges)
            vtm.halfedges[i*2].face.colorB = i/len(vtm.halfedges)

        vtm = self.model2d.vtms[30]
        print(len(vtm.vertices), flush=True)
        for i in range(int(len(vtm.halfedges)/2)):
            vtm.halfedges[i*2].face.colorR = i/len(vtm.halfedges)
            vtm.halfedges[i*2].face.colorG = i/len(vtm.halfedges)
            vtm.halfedges[i*2].face.colorB = i/len(vtm.halfedges)
        """

        for f in self.model2d.faces:
            glColor3f(f.colorR, f.colorG, f.colorB)
            he = f.halfedge
            count = 0

            glBegin(GL_LINE_LOOP)
            while True:
                glVertex3f(he.vertex.x, he.vertex.y, he.vertex.z)
                he = he.next
                count += 1
                if count == f.NumOfEdges:
                    break
            glEnd()


    def draw2d(self):
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
        for v in self.model2d.vertices:
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
        self.drawModel2d()
        #glutSolidTeapot(1.0)  # solid
        glFlush()  # enforce OpenGL command

    def init2d(self, width, height):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST) # enable shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        ##set perspective
        gluPerspective(45.0, float(width)/float(height), 0.1, 10000.0)

    def resize2d(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(w)/float(h), 0.1, 10000.0)

    def mouseInput(self, button, state, x, y):
        self.update()

    def keyInput(self, key, x, y):
        if key == b' ':
            self.polygonsInfo()
        if key == b'p':
            self.toPlane()
        if key == b's':
            self.calucSita()
        self.update()

    def calucW(self, sitas, idVtm, idEtm):
        np.set_printoptions(suppress=True, threshold = 1000000, linewidth=200)
        c = np.zeros((idVtm*2, idEtm))
        ws = np.zeros((idEtm, 1))
        b = np.zeros((idVtm*2, 1))

        """
        #シータの計算結果の確認、あってる！！　よって、sita_largeの計算が間違い
        z = 0
        for vtm in self.model2d.vtms:
            #print("--------------------------------")
            x = 0
            y = 0
            for i in range(len(vtm.halfedges)):
                he = vtm.halfedges[i]
                if (i % 2 == 1):
                    #表面多角形の角度が崩れてないか
                    truth = he.vertex_next.sita #２Dに配置後に保存しておいた角度
                    now = self.getSita(he.next.vertex, he.next.vertex_next, he.vertex_next, he.vertex)
                    x += truth
                    y += now
                    #print(abs(truth - now))
                    #sitasの角度通りに配置されているか
                    if he.pair != None:
                        truth = None
                        if vtm.id < he.vertex.vtm.id:
                            truth = sitas[he.id, 0]
                        else:
                            truth = -1 * sitas[he.id, 0]
                        now = self.getSita(he.vertex_next, he.vertex, he.pair.vertex, he.pair.vertex_next)
                        if now > math.pi:
                            now -= 2* math.pi
                        x += truth
                        y += now
                        #print(abs(truth - now))
                    #ボーダーの角度通りに配置されているか
                    else:
                        truth = sitas[he.id, 0]
                        now = self.getSita(he.vertex_next, he.vertex, vtm.halfedges[0].vertex, vtm.halfedges[0].vertex_next)
                        x += truth
                        y += now
                        #print(abs(truth - now))
            z += (x-y)**2
        print(z)
        """


        """
        y = 0
        #シータラージが一周2πになっているか確認
        for vtm in self.model2d.vtms:
            x = 0
            for i in range(len(vtm.halfedges)):
                he = vtm.halfedges[i]
                if (i % 2 == 1):
                    x += he.vertex_next.sita_large
            print(abs(2*math.pi - x))
            y += abs(2*math.pi - x)
        print(y)
        """

        for vtm in self.model2d.vtms:
            sita_sum = 0
            for i in range(len(vtm.halfedges)):
                he = vtm.halfedges[i]
                if (i % 2 == 1):
                    sita_sum += he.vertex_next.sita_large
                    if he.pair == None:
                        c[vtm.id*2, he.id] = math.cos(sita_sum)
                        c[vtm.id*2+1, he.id] = math.sin(sita_sum)
                    else:
                        if vtm.id < he.vertex.vtm.id:
                            c[vtm.id*2, he.id] = math.cos(sita_sum)
                            c[vtm.id*2+1, he.id] = math.sin(sita_sum)
                        else:
                            c[vtm.id*2, he.id] = math.cos(sita_sum)
                            c[vtm.id*2+1, he.id] = math.sin(sita_sum)
                            b[vtm.id*2, 0] += math.cos(sita_sum)*2*self.getLength(he.vertex, he.vertex_next)*math.sin(-0.5*sitas[he.id, 0])
                            b[vtm.id*2+1, 0] += math.sin(sita_sum)*2*self.getLength(he.vertex, he.vertex_next)*math.sin(-0.5*sitas[he.id, 0])

        cPlus = np.linalg.pinv(c)
        #cPlus = np.dot(c.T, np.linalg.inv(np.dot(c, c.T)))
        #print(c.shape)
        #print("cPlus = \n" + str(cPlus))
        #print("c*cPlus = \n" + str(np.dot(c, cPlus)))
        #print("cPlus*c = \n" + str(np.dot(cPlus, c)))
        #print("cPlus*c*cPlus = \n" + str(np.dot(np.dot(cPlus, c), cPlus)))
        #print("c*cPlus*c = " + str(np.dot(np.dot(c, cPlus), c)))
        #print("teigi:0 cPlus*c - (cPlus*c)^t = \n" + str(np.dot(cPlus, c) - np.dot(cPlus, c).T))
        #print("teigi:0 c*cPlus - (c*cPlus)^t = \n" + str(np.dot(cPlus, c) - np.dot(cPlus, c).T))
        #print("teigi:0 cPlus*c*cPlus - cPlus= \n" + str(np.dot(np.dot(cPlus, c), cPlus) - cPlus))
        #print("teigi:0 c*cPlus*c - c = \n" + str(np.dot(np.dot(c, cPlus), c) - c))
        ws = np.dot(cPlus, b) + np.dot((np.eye(c.shape[1]) - np.dot(cPlus, c)), ws)
        #print("ws = \n" + str(ws))
        #print("C*ws = \n" + str(np.dot(c,ws)))
        #print("c = \n" + str(c))
        #print("rank(c) = " + str(np.linalg.matrix_rank(c)))
        #print("b = \n" + str(b))
        #print("C*ws - b = \n" + str(np.dot(c,ws)-b))
        print("norm(C*ws - b) = " + str(np.linalg.norm(np.dot(c,ws)-b)))


    def calucSita(self):
        #初期設定：c,g,θの初期値の決定、vertexに角度情報の格納
        np.set_printoptions(suppress=True, threshold = 1000000, linewidth=200)
        idEtm = 0
        for he in self.model2d.halfedges:
            if he.id == None: #２回連続でcalucSita呼び出してもこれが原因でうまくいかない、まあ放置
                if he.pair == None:
                    he.id = idEtm
                else:
                    he.id = idEtm
                    he.pair.id = idEtm
                idEtm += 1
        idVtm = 0
        for vtm in self.model2d.vtms:
            vtm.id = idVtm
            idVtm += 1

        c = np.zeros((idVtm, idEtm))
        sitas = np.zeros((idEtm, 1))
        g = np.zeros((idVtm, 1))
        #print(c.shape)
        #print(sitas.shape)
        #print(g.shape)

        for vtm in self.model2d.vtms:
            gValue = 2*math.pi
            for i in range(len(vtm.halfedges)):
                he = vtm.halfedges[i]
                if (i % 2 == 1):
                    if he.pair == None:
                        c[vtm.id, he.id] = 1
                    else:
                        if (vtm.id < he.vertex.vtm.id):
                            c[vtm.id, he.id] = 1
                        else:
                            c[vtm.id, he.id] = -1
                    sita = self.getSita(he.next.vertex, he.next.vertex_next, he.vertex_next, he.vertex)
                    he.vertex_next.sita = sita
                    gValue -= sita
            g[vtm.id, 0] = gValue

        """ 正しいかチェック
        for j in range(idVtm):
            count = 0
            for i in range(idEtm):
                if c[j,i] <= -1:
                    #print(c[j,i])
                    count += 1
                if c[j,i] >= 1:
                    #print(c[j,i])
                    count += 1
            if count != int(len(self.model2d.vtms[j].vertex3d.halfedges)/2):
                print(count)
                print(len(self.model2d.vtms[j].vertex3d.halfedges)/2)
        """

        cPlus = np.linalg.pinv(c)
        IminusCC = np.eye(c.shape[1]) - np.dot(cPlus, c)
        #cPlus = np.dot(c.T, np.linalg.inv(np.dot(c, c.T)))
        #print("cPlus = \n" + str(cPlus))
        #print("c*cPlus = \n" + str(np.dot(c, cPlus)))
        #print("cPlus*c = \n" + str(np.dot(cPlus, c)))
        #print("cPlus*c*cPlus = \n" + str(np.dot(np.dot(cPlus, c), cPlus)))
        #print("c*cPlus*c = " + str(np.dot(np.dot(c, cPlus), c)))
        #print("teigi:0 cPlus*c - (cPlus*c)^t = \n" + str(np.dot(cPlus, c) - np.dot(cPlus, c).T))
        #print("teigi:0 c*cPlus - (c*cPlus)^t = \n" + str(np.dot(cPlus, c) - np.dot(cPlus, c).T))
        #print("teigi:0 cPlus*c*cPlus - cPlus= \n" + str(np.dot(np.dot(cPlus, c), cPlus) - cPlus))
        #print("teigi:0 c*cPlus*c - c = \n" + str(np.dot(np.dot(c, cPlus), c) - c))
        sitas = np.dot(cPlus, g) + np.dot(IminusCC, sitas)
        #print("sitas = \n" + str(sitas))
        #print("C*sitas = \n" + str(np.dot(c,sitas)))
        #print("c = \n" + str(c))
        #print("rank(c) = " + str(np.linalg.matrix_rank(c)))
        #print("g = \n" + str(g))
        #print("C*sitas - g = \n" + str(np.dot(c,sitas)-g))
        #print("norm(C*sitas - g) = " + str(np.linalg.norm(np.dot(c,sitas)-g)))
        """
        #簡単な行列ならできる？→できる
        c = np.array([[1,10,2, 5], [3, 14, 9, 7], [2, 4, 7, 2]])
        g = np.array([[2], [5], [2]])
        sitas = np.zeros((c.shape[1],1))

        #cPlus = np.linalg.pinv(c)
        cPlus = np.dot(c.T, np.linalg.inv(np.dot(c, c.T)))
        print("cPlus = \n" + str(cPlus))
        print("c*cPlus = \n" + str(np.dot(c, cPlus)))
        print("cPlus*c = \n" + str(np.dot(cPlus, c)))
        print("cPlus*c*cPlus = \n" + str(np.dot(np.dot(cPlus, c), cPlus)))
        print("c*cPlus*c = " + str(np.dot(np.dot(c, cPlus), c)))
        print("teigi:0 cPlus*c - (cPlus*c)^t = \n" + str(np.dot(cPlus, c) - np.dot(cPlus, c).T))
        print("teigi:0 c*cPlus - (c*cPlus)^t = \n" + str(np.dot(cPlus, c) - np.dot(cPlus, c).T))
        print("teigi:0 cPlus*c*cPlus - cPlus= \n" + str(np.dot(np.dot(cPlus, c), cPlus) - cPlus))
        print("teigi:0 c*cPlus*c - c = \n" + str(np.dot(np.dot(c, cPlus), c) - c))
        sitas = np.dot(cPlus, g) + np.dot((np.eye(c.shape[1]) - np.dot(cPlus, c)), sitas)
        print("sitas = \n" + str(sitas))
        print("C*sitas = \n" + str(np.dot(c,sitas)))
        print("c = \n" + str(c))
        print("rank(c) = " + str(np.linalg.matrix_rank(c)))
        print("g = \n" + str(g))
        print("C*sitas - g = \n" + str(np.dot(c,sitas)-g))
        """

        iter = 0
        while True:
            E = 0
            deltaE = np.zeros((idEtm, 1))
            #最適化計算　式4,6,8を満たすようにする
            for vtm in self.model2d.vtms:
                sita_large_right = None
                idx_sita_large_right = None
                flag_rightEtmRev = False
                if vtm.halfedges[0].pair == None:
                    sita_large_right = sitas[vtm.halfedges[-1].id, 0]
                    flag_rightEtmRev = False
                    idx_sita_large_right = vtm.halfedges[-1].id
                else:
                    if (vtm.id < vtm.halfedges[0].vertex_next.vtm.id):
                        sita_large_right = sitas[vtm.halfedges[0].id, 0]
                        flag_rightEtmRev = False
                        idx_sita_large_right = vtm.halfedges[0].id
                    else:
                        sita_large_right = -1 * sitas[vtm.halfedges[0].id, 0]
                        flag_rightEtmRev = True
                        idx_sita_large_right = vtm.halfedges[0].id

                #ラージシータ、シータ、境界のシータの確認
                for i in range(len(vtm.halfedges)):
                    he = vtm.halfedges[i]
                    sita_etm = None
                    sita_boarder = None
                    sita_large = None
                    sita_large_left = None
                    flag_leftEtmRev = False
                    if (i % 2 == 1):
                        if he.pair == None:
                            sita_boarder = sitas[he.id, 0]
                            sita_large_left = sita_boarder
                            flag_leftEtmRev = False
                        else:
                            # vtm方向から見たsitaに変換
                            if (vtm.id < he.vertex.vtm.id):
                                sita_etm = sitas[he.id, 0]
                                sita_large_left = sita_etm
                                flag_leftEtmRev = False
                            else:
                                sita_etm = -1 * sitas[he.id, 0]
                                sita_large_left = sita_etm
                                flag_leftEtmRev = True
                        #print(" " + str(sita_etm) + " " + str(sita_boarder) + " " + str(sita_large))
                        sita_large = sita_large_right/2 + he.vertex_next.sita + sita_large_left/2
                        he.vertex_next.sita_large = sita_large

                        k = math.pi
                        #それぞれが条件を満たしているか
                        if sita_etm != None:
                            if sita_etm <= -1 * math.pi:
                                #print("NG at sita_etm")
                                E += (sita_etm + math.pi)**2
                                if flag_leftEtmRev:
                                    deltaE[he.id, 0] = -1 * (2*sita_etm + 2*math.pi - 2*k)
                                else:
                                    deltaE[he.id, 0] = 2*sita_etm + 2*math.pi - 2*k
                            elif sita_etm >= math.pi:
                                #print("NG at sita_etm")
                                E += (sita_etm - math.pi)**2
                                if flag_leftEtmRev:
                                    deltaE[he.id, 0] = -1 * (2*sita_etm - 2*math.pi + 2*k)
                                else:
                                    deltaE[he.id, 0] = 2*sita_etm - 2*math.pi + 2*k
                            else:
                                #print("OK at sita_etm")
                                x = 1
                        # 境界部分のラージシータは考慮しないかもしれない、連結多角形数２のとき絶対成り立たない（式8）
                        if sita_large != None and he.pair != None and vtm.halfedges[0].pair != None:
                            if sita_large < 0:
                                #print("NG at sita_largem")
                                E += (sita_large)**2
                                if flag_leftEtmRev:
                                    deltaE[he.id, 0] = -1 * (0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - 0.5*k)
                                else:
                                    deltaE[he.id, 0] = 0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - 0.5*k
                                if flag_rightEtmRev:
                                    deltaE[idx_sita_large_right, 0] = -1 * (0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - 0.5*k)
                                else:
                                    deltaE[idx_sita_large_right, 0] = 0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - 0.5*k
                            elif sita_large >= math.pi:
                                #print("NG at sita_large")
                                E += (sita_large - math.pi)**2
                                if flag_leftEtmRev:
                                    deltaE[he.id, 0] = -1 * (0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - math.pi + 0.5*k)
                                else:
                                    deltaE[he.id, 0] = 0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - math.pi + 0.5*k
                                if flag_rightEtmRev:
                                    deltaE[idx_sita_large_right, 0] = -1 * (0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - math.pi + 0.5*k)
                                else:
                                    deltaE[idx_sita_large_right, 0] = 0.5*sita_large_right + 0.5*sita_large_left + he.vertex_next.sita - math.pi + 0.5*k
                            else:
                                #print("OK at sita_large")
                                x = 1
                        if sita_boarder != None:
                            if sita_boarder < math.pi:
                                #print("NG at sita_boarder")
                                E += (sita_boarder - math.pi)**2
                                if flag_leftEtmRev:
                                    deltaE[he.id, 0] = -1 * (2*sita_boarder - 2*math.pi - 2*k)
                                else:
                                    deltaE[he.id, 0] = 2*sita_boarder - 2*math.pi - 2*k
                            else:
                                #print("OK at sita_boarder")
                                x = 1
                        idx_sita_large_right = he.id
                        sita_large_right = sita_large_left
                        flag_rightEtmRev = flag_leftEtmRev
            iter += 1
            alpha = 0.1
            print("E_sitas = " + str(E))
            if E < 0.00000000000001 or iter > 100:
                break
            else:
                #print(IminusCC)
                #print(deltaE)
                deltaE = np.dot(IminusCC, deltaE)
                sitas = sitas - alpha*deltaE
                self.update()

        #sitasのとおりに配置
        self.setBySita(self.model2d.faces[5], sitas)
        self.update()
        self.calucW(sitas, idVtm, idEtm)

        """
         #三角形が崩れていないか確認
        for f in self.model2d.faces:
            he = f.halfedge
            length_next = math.sqrt(((he.vertex.xDefo - he.vertex_next.xDefo) ** 2) + ((he.vertex.yDefo - he.vertex_next.yDefo) ** 2) + ((he.vertex.zDefo - he.vertex_next.zDefo) ** 2))
            length_next2 = math.sqrt(((he.vertex.x - he.vertex_next.x) ** 2) + ((he.vertex.y - he.vertex_next.y) ** 2) + ((he.vertex.z - he.vertex_next.z) ** 2))
            print(length_next - length_next2)
            length_prev = math.sqrt(((he.prev.vertex.xDefo - he.vertex.xDefo) ** 2) + ((he.prev.vertex.yDefo - he.vertex.yDefo) ** 2) + ((he.prev.vertex.zDefo - he.vertex.zDefo) ** 2))
            length_prev2 = math.sqrt(((he.prev.vertex.x - he.vertex.x) ** 2) + ((he.prev.vertex.y - he.vertex.y) ** 2) + ((he.prev.vertex.z - he.vertex.z) ** 2))
            print(length_prev - length_prev2)
            length_DX = math.sqrt(((he.vertex_next.xDefo - he.prev.vertex.xDefo) ** 2) + ((he.vertex_next.yDefo - he.prev.vertex.yDefo) ** 2) + ((he.vertex_next.zDefo - he.prev.vertex.zDefo) ** 2))
            length_DX2 = math.sqrt(((he.vertex_next.x - he.prev.vertex.x) ** 2) + ((he.vertex_next.y - he.prev.vertex.y) ** 2) + ((he.vertex_next.z - he.prev.vertex.z) ** 2))
            print(length_DX - length_DX2)
        """
        """
        #角度があってるか確認
        for vtm in self.model2d.vtms:
            he = vtm.halfedges[-1]
            if he.pair == None:
                sita_boarder = sitas[he.id, 0]
                sita_now = self.getSita(he.vertex_next, he.vertex, vtm.halfedges[0].vertex, vtm.halfedges[0].vertex_next)
                print(sita_boarder - sita_now)
        """

    def setBySita(self, f, sitas):
        f.flag_setBySita = True
        heStart = f.halfedge
        he = heStart
        while True:
            if he.pair != None:
                if not he.pair.face.flag_setBySita:
                    # fを基準にhe.pair.faceの角度を決定、he.pairでポインタを持っている
                    #print(sitas)
                    if he.vertex.vtm.id < he.vertex_next.vtm.id:
                        sita_will = -1 * sitas[he.id, 0]
                    elif he.vertex.vtm.id > he.vertex_next.vtm.id:
                        sita_will = sitas[he.id, 0]
                    else:
                        print("なにかがおかしい")
                    #print(sita_will)
                    sita_now = self.getSita(he.vertex_next, he.vertex, he.pair.vertex, he.pair.vertex_next)
                    sita_rotate = sita_will - sita_now
                    # 一つ目の座標回転
                    a = he.pair.vertex_next.x
                    b = he.pair.vertex_next.y
                    c = he.pair.vertex.x
                    d = he.pair.vertex.y
                    x = c + (a-c)*math.cos(sita_rotate) - (b-d)*math.sin(sita_rotate)
                    y = d + (a-c)*math.sin(sita_rotate) + (b-d)*math.cos(sita_rotate)
                    he.pair.vertex_next.x = x
                    he.pair.vertex_next.y = y
                    # 二つ目の座標回転
                    a = he.pair.next.vertex_next.x
                    b = he.pair.next.vertex_next.y
                    c = he.pair.vertex.x
                    d = he.pair.vertex.y
                    x = c + (a-c)*math.cos(sita_rotate) - (b-d)*math.sin(sita_rotate)
                    y = d + (a-c)*math.sin(sita_rotate) + (b-d)*math.cos(sita_rotate)
                    he.pair.next.vertex_next.x = x
                    he.pair.next.vertex_next.y = y
                    #sita_now = self.getSita(he.vertex_next, he.vertex, he.pair.vertex, he.pair.vertex_next)
                    self.setBySita(he.pair.face, sitas)
            he = he.next
            if he == heStart:
                break


    def polygonsInfo(self):
        print("----------model2d-----------")
        print("len(faces) = " + str(len(self.model2d.faces)))
        print("len(halfedges) = " + str(len(self.model2d.halfedges)))
        print("len(vertices) = " + str(len(self.model2d.vertices)))
        print("len(vtms) = " + str(len(self.model2d.vtms)))

    def toPlane(self): #制約：三角形
        for f in self.model2d.faces:
            if f.NumOfEdges == 3:
                he = f.halfedge
                length_next = self.getLength(he.vertex, he.vertex_next)
                length_prev = self.getLength(he.prev.vertex_next, he.prev.vertex)
                sita = self.getSita(he.vertex, he.vertex_next, he.prev.vertex_next, he.prev.vertex)
                if sita > math.pi:
                    sita = 2*math.pi - sita
                he.vertex.x = 0
                he.vertex.y = 0
                he.vertex.z = 0
                he.vertex_next.x = length_next
                he.vertex_next.y = 0
                he.vertex_next.z = 0
                he.prev.vertex.x = length_prev * math.cos(sita)
                he.prev.vertex.y = length_prev * math.sin(sita)
                he.prev.vertex.z = 0
            else:
                print("face.NumOfEdges != 3")

        """ #正しく投影できてるか確認
        for f in self.model2d.faces:
            he = f.halfedge
            gaisekiZ = (he.vertex_next.x - he.vertex.x) * (he.prev.vertex.y - he.vertex.y) - (he.prev.vertex.x - he.vertex.x) * (he.vertex_next.y - he.vertex.y)
            print("gaiseki = " + str(gaisekiZ))
            length_next = math.sqrt(((he.vertex.xDefo - he.vertex_next.xDefo) ** 2) + ((he.vertex.yDefo - he.vertex_next.yDefo) ** 2) + ((he.vertex.zDefo - he.vertex_next.zDefo) ** 2))
            length_next2 = math.sqrt(((he.vertex.x - he.vertex_next.x) ** 2) + ((he.vertex.y - he.vertex_next.y) ** 2) + ((he.vertex.z - he.vertex_next.z) ** 2))
            print(length_next - length_next2)
            length_prev = math.sqrt(((he.prev.vertex.xDefo - he.vertex.xDefo) ** 2) + ((he.prev.vertex.yDefo - he.vertex.yDefo) ** 2) + ((he.prev.vertex.zDefo - he.vertex.zDefo) ** 2))
            length_prev2 = math.sqrt(((he.prev.vertex.x - he.vertex.x) ** 2) + ((he.prev.vertex.y - he.vertex.y) ** 2) + ((he.prev.vertex.z - he.vertex.z) ** 2))
            print(length_prev - length_prev2)
            length_DX = math.sqrt(((he.vertex_next.xDefo - he.prev.vertex.xDefo) ** 2) + ((he.vertex_next.yDefo - he.prev.vertex.yDefo) ** 2) + ((he.vertex_next.zDefo - he.prev.vertex.zDefo) ** 2))
            length_DX2 = math.sqrt(((he.vertex_next.x - he.prev.vertex.x) ** 2) + ((he.vertex_next.y - he.prev.vertex.y) ** 2) + ((he.vertex_next.z - he.prev.vertex.z) ** 2))
            print(length_DX - length_DX2)
        """
        #print("OK")

    def getSita(self, v1, v2, v3, v4):#v1->v2, v3->v4間の反時計回り角度
        v1v2_length = self.getLength(v1,v2)
        v3v4_length = self.getLength(v3,v4)
        sitaCos = ((v2.x - v1.x) * (v4.x - v3.x) + (v2.y - v1.y) * (v4.y - v3.y) + + (v2.z - v1.z) * (v4.z - v3.z)) / (v1v2_length * v3v4_length)
        sita = math.acos(sitaCos)
        if self.getGaisekiZ(v1, v2, v3, v4) < 0:
            sita = 2*math.pi - sita
        #print(self.getGaisekiZ(v1, v2, v3, v4))
        #print(sita)
        return sita

    def getLength(self, v1, v2):
        return math.sqrt(((v2.x - v1.x) ** 2) + ((v2.y - v1.y) ** 2) + ((v2.z - v1.z) ** 2))

    def getGaisekiZ(self, v1, v2, v3, v4):
        return (v2.x - v1.x) * (v4.y - v3.y) - (v2.y - v1.y) * (v4.x - v3.x)
