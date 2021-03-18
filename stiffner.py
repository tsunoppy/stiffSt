#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

# Calculation for Steel stiffnering following Building letter By BCJ
# Coded by tsunoppy on Sunday

import math

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import steel

class Stiffner:

    def __init__(self):
        self.tmpdata = [] # test data
        self.xpos = [] # bolt position
        self.ypos = [] # bolt position
        self.totalnum = 0.0


    def makeModel(self,n21,n22,n23,xpitch,ypitch):

        for i in range(0,n21):
            self.xpos.append(0.0)
            self.ypos.append(ypitch*i)
            self.totalnum = self.totalnum + 1

        if n22 != "" or n22 != 0:
            for i in range(0,n22):
                self.xpos.append(xpitch)
                self.ypos.append(ypitch*i)
                self.totalnum = self.totalnum + 1

        if n23 != "" or n23 != 0:
            for i in range(0,n23):
                self.xpos.append(2.0*xpitch)
                self.ypos.append(ypitch*i)
                self.totalnum = self.totalnum + 1

    def return_xpos(self):
        return self.xpos

    def return_ypos(self):
        return self.ypos

    def solve(self,hh,bb,tw,tf,rr,fac,sig1,\
              hh2,bb2,tw2,tf2,rr2,ds,\
              n21,n22,n23,\
              xpitch,ypitch,\
              size,\
              qv,\
              bound,index,\
              tg,sigyg,\
              ll):

        if index == 0:
            e = (hh-tf)/1000.0
        else:
            e = ( (hh-tf/2.0) - (ds+hh2/2.0) )/1000.0

        beam = steel.Hmemb(hh,bb,tw,tf,rr)
        print("A=",beam.sa(),"cm2")
        if bound == 0:
            nn = fac * beam.sa()* sig1 /2.0 / 10.0
        elif bound ==1 :
            nn = fac * beam.sa()* sig1 /2.0 / 10.0 /2.0
        else:
            print("err. bound!=1or0")

        mm = nn * e

        print("Start Solve")
        print("N=",nn,"kN")
        print("e=",e,"m")
        print("M=",mm,"kN")
        print("Qv=",qv,"kN")


        ####################
        # calculate center of gravity
        xcen = 0.0
        ycen = 0.0
        for i in range(0,int(self.totalnum)):
            xcen = xcen + self.xpos[i]
            ycen = ycen + self.ypos[i]
        xcen = xcen/self.totalnum
        ycen = ycen/self.totalnum

        if index == 0:
            ycen = ds + hh2/2 + (n21-1)*ypitch/2.0

        print("Total Bolt Num.:" ,self.totalnum)
        #print(self.xpos,self.ypos)
        print("Center of gravity: x,y = ", xcen,ycen)

        ####################
        # Calclate sum ri2 & zb
        r = []
        m = 0.0
        r2 = 0.0
        for i in range(0,int(self.totalnum)):
            r.append(math.sqrt((self.xpos[i]-xcen)**2 + (self.ypos[i]-ycen)**2))
            #print("ri=",r[i])
            r2 = r2 + r[i]**2
            if r[i] > m:
                m = r[i]
                sinth = math.fabs(self.xpos[i]-xcen)/m
                costh = math.fabs(self.ypos[i]-ycen)/m
        zb = r2/m

        print("m=",m)
        print("zb=",zb,"sin=",sinth,"cos=",costh)

        qbmax = 0.0
        qvbar = qv/self.totalnum
        nnbar = nn/self.totalnum

        print("Qv/n = {:8.0f}, N/n = {:8.0f}".format(qvbar,nnbar))

        print("i, ","x, y, ", \
              "M/Zb*sin, ",\
              "M/Zb*cos, ",\
              "qb")

        qe = 0.0 # 水平反力

        for i in range(0,int(self.totalnum)):
            sinth = math.fabs(self.xpos[i]-xcen)/m
            costh = math.fabs(self.ypos[i]-ycen)/m
            qb1 = qv/self.totalnum + mm/zb*sinth*1000
            qb2 = nn/self.totalnum + mm/zb*costh*1000
            qb = math.sqrt(qb1**2 + qb2**2)

            rx = mm/r2*math.fabs(self.ypos[i]-ycen)*1000
            ry = mm/r2*math.fabs(self.xpos[i]-xcen)*1000
            qe = qe + rx

            if qbmax < qb:
                qbmax = qb
            print(i,self.xpos[i],self.ypos[i], \
                  "M/Zb*sin =", "{:.2f}".format(mm/zb*sinth*1000),\
                  "M/Zb*cos =", "{:.2f}".format(mm/zb*costh*1000),
                  "Rx","{:.2f}".format(rx),\
                  "Ry","{:.2f}".format(ry),\
                  "{:.2f}".format(qb))

        print( "qbmax =", qbmax )
        qe = qe - nn
        print( "qe =", qe )

        ########################################################################
        # start calculation gasset plate strength
        # G.PLの検定計算
        print("Start Gasset Plate Cal")
        if index == 0: ## 拘束あり
            dc = (n21-1)*ypitch/2.0
            e2 = (hh-tf/2.0) - ( ds + hh2/2.0 + dc )
        elif index ==1: ## 拘束なし
            e2 = (hh-tf/2.0) - ( ds + hh2/2.0 )
        else:
            print("Err fixtype")

        e2 = e2/1000.0 # convert mm to m
        print("e=",e2,"m" )

        mdg = nn*e2
        print("M=",mdg,"kN.m")
        reqd = math.sqrt( 6.0*mdg*10**6 / (tg*sigyg) )

        print("req(d)=",reqd,"mm")

        print("End Gasset Plate Cal")


        ####################
        # 横補剛剛性の算定
        e3 = ( (hh-tf/2.0) - (ds+hh2/2.0) )/1000.0
        mm3 = nn * e3
        es = 2.05 * 10 **5 # N/mm2
        subbeam = steel.Hmemb(hh2,bb2,tw2,tf2,rr2)

        if index == 0: ## 拘束あり
            dm = 0.0
        elif index ==1: ## 拘束なし
            theta = mm3*10**6 * ll*10**3 \
                / (3.0*es*subbeam.ix()*10**4 )
            dm = theta * e3
        else:
            print("Err fixtype")

        dv = nn*1000 * ll*1000 \
            / (es*subbeam.sa()*100)

        dtotal = dm + dv
        kk = nn*1000.0 / (dm+dv)

        print("dm=",dm,"dv",dv)
        print("K=",kk,"N/mm" )

        ####################
        # return parameter
        return beam.sa(), nn, e, mm, m, zb, qvbar, nnbar, qbmax, \
            e2,mdg,reqd,qe,dm,dv,dtotal,kk


    def kd(self,hh,bb,tw,tf,rr,sigy,lb):
        # hh,bb,tw,tf,rr: member of the beam
        # sigy: yield strength N/mm2
        # lb: m
        beam=steel.Hmemb(hh,bb,tw,tf,rr)
        reqkd = 5.0 * sigy * beam.sa()*100.0 / 2.0 / (lb*1000)
        return reqkd

    # matoplot
    #https://note.nkmk.me/python-matplotlib-patches-circle-rectangle/
    ##########################
    def model(self,hh,bb,tw,tf,rr,fac,sig1,\
              hh2,bb2,tw2,tf2,rr2,ds,\
              n21,n22,n23,\
              xpitch,ypitch,\
              size,\
              qv,\
              index,\
              obj_canvas,\
              obj_axes):


        fig = plt.figure()
        ax = plt.axes()

        # fc = face color, ec = edge color

        c = []
        yaxis = hh - ( ds + hh2/2 + (n21-1)*ypitch/2.0 )

        for i in range(0,int(self.totalnum)):
            #print(i,self.xpos[i],self.ypos[i])
            xposnew = self.xpos[i] + bb + 10.0 + 40.0
            yposnew = yaxis + self.ypos[i]
            c.append(patches.Circle(xy=(xposnew,yposnew),radius=size/2.0, fc='g', ec='r'))

        r = patches.Rectangle(xy=(0, 0), width=bb, height=tf, \
                              ec='#000000', fill=False)
        r2 = patches.Rectangle(xy=(bb/2-tw/2, tf), width=tw, height=(hh-2*tf), \
                               ec='#000000', fill=False)
        r3 = patches.Rectangle(xy=(0, hh-tf), width=bb, height=tf, \
                               ec='#000000', fill=False)


        subbeam = []
        subbeam.append( \
                        patches.Rectangle(xy=(bb+10.0, hh-ds-hh2), width=600, height=hh2, \
                                          ec='#000000', fill=False) )
        subbeam.append( \
                        patches.Rectangle(xy=(bb+10.0, hh-ds-hh2), width=600, height=tf2, \
                                          ec='#000000', fill=False) )
        subbeam.append( \
                        patches.Rectangle(xy=(bb+10.0, hh-ds-tf2), width=600, height=tf2, \
                                          ec='#000000', fill=False) )

        for i in range(0,int(self.totalnum)):
            ax.add_patch(c[i])

        ax.add_patch(r)
        ax.add_patch(r2)
        ax.add_patch(r3)

        for i in range(0,3):
            ax.add_patch(subbeam[i])

        plt.axis('scaled')
        #ax.axis('scaled')
        ax.set_aspect('equal')
        ax.axis("off")
        ax.set_ylim(hh-1450, hh+50)
        ax.set_xlim(-50, 1500)

        #plt.savefig('./db/sample.jpg')
        plt.show()
        plt.close(fig)
        #obj.draw()

########################################################################
# End Class

"""
obj = Stiffner()

# imput data
hh = 800.
bb = 550.
tw = 16.
tf = 32.
rr = 18.
fac = 0.02
sig1 = 325.0

hh2 = 450.
bb2 = 200.
tw2 = 8.
tf2 = 12.
rr2 = 10.
ds =  0.0

index = 0 # 0 上部拘束、 1 拘束なし
qv = 180 #kN
n21 = 5
n22 = 1
n23 = 1
ypitch = 60.0
xpitch = 60.0
size = 22

obj.solve(hh,bb,tw,tf,rr,fac,sig1,\
          hh2,bb2,tw2,tf2,rr2,ds,\
          n21,n22,n23,\
          xpitch,ypitch,\
          size,\
          qv,\
          index)

obj.model(hh,bb,tw,tf,rr,fac,sig1,\
          hh2,bb2,tw2,tf2,rr2,ds,\
          n21,n22,n23,\
          xpitch,ypitch,\
          size,\
          qv,\
          index)
"""
