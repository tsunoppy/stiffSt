#! /Users/tsuno/.pyenv/shims/python3
# -*- coding: utf-8 -*-

# Calculation for Steel stiffnering following Building letter By BCJ
# Coded by tsunoppy on Sunday

import math


class Hmemb:

    # h,b,tw,tf,r mm
    # area: cm2
    # six: cm4
    # siy: cm4
    # szx: cm3
    # szy: cm3
    # ix: cm
    # iy: cm

    def __init__(self,h,b,tw,tf,r):
        self.tmp = []
        self.pi = math.pi
        self.h = h
        self.b = b
        self.tw = tw
        self.tf = tf
        self.r = r
    #
    # Young Modulus
    def sa(self):

        area = 2.0 * self.b * self.tf \
            + (self.h - 2.0 * self.tf) * self.tw + self.r**2 * (4.0 - self.pi)
        area = area/100.0
        return area

    def six(self):
        cc = self.r * (10.0 - 3.0 * self.pi) / (12.0 - 3.0 * self.pi)
        shI = self.b * self.tf**3 / 6.0 \
            + (self.h - 2.0 * self.tf)**3 * self.tw / 12.0 \
            + (self.h - self.tf)**2 * self.b * self.tf / 2.0
        shI = shI \
            + (4.0 - self.pi) * self.r**2 * (self.h / 2.0 - self.tf - cc)**2

        shI = shI/10000.0
        return shI

    def szx(self):

        shI = self.six()
        shZ = shI * 2.0 / (self.h/10)
        return shZ

    def siy(self):
        whI = self.tf * self.b**3 /12.0 / 10000.0
        return whI

    def szy(self):

        whI = self.siy()
        whZ = whI / (self.b/10) *  2.0
        return whZ

    def ix(self):
        shI = self.six()
        area = self.sa()
        return math.sqrt(shI/area)

    def iy(self):

        whI = self.siy()
        area = self.sa()
        return math.sqrt(whI/area)

    def print_prop(self):
        # Print
        print("# H-{:.0f} x {:.0f} x {:.0f} x {:.0f} x {:.0f}".format\
              (self.h,self.b,self.tw,self.tf,self.r) )
        print("\n# a  = {:10.0f}  [cm2]" \
              "\n# Zx = {:10.0f}  [cm3]  Zy = {:10.0f}  [cm3]" \
              "\n# Ix = {:10.0f}  [cm4]  Iy = {:10.0f}  [cm4]" \
              "\n# ix = {:10.2f}   [cm]  iy = {:10.2f}   [cm]\n" \
              .format(self.sa(),\
                      self.szx(),\
                      self.szy(),\
                      self.six(),\
                      self.siy(),\
                      self.ix(),\
                      self.iy()))

class HTB():

    def qa(self,x,ftype):
        # x: kei
        # ftype: "F10T" or "F8T"
        # return permissible shear strength

        if ftype == "F10T":

            if x =='M12':
                return 16.7
            elif x =='M16':
                return 29.6
            elif x =='M20':
                return 46.2
            elif x =='M22':
                return 55.9
            else:
                print("Err.")

        elif ftype == "F8T":

            if x =='M12':
                return 13.3
            elif x =='M16':
                return 23.6
            elif x =='M20':
                return 36.9
            elif x =='M22':
                return 44.7
            else:
                print("Err.")

        else:
            print("Err. Class HTB -- qa")


class Stud:

    def __init__(self):
        self.pi = math.pi

    def Ec(self,fc,gamma):
        # gamma: Dry density
        econ = 3.35 * 10**4 * ( gamma/24.0 )**(2) * (fc/60.0)**(1.0/3.0)
        return econ

    def qs(self,fc,gamma,phai,fac):

        ec = self.Ec(fc,gamma)
        print("ec",ec,"N/mm2")
        sca = (phai/2.0)**2 * self.pi
        print("sca",sca,"mm2")

        q = fac * 0.5 * sca * math.sqrt( fc*ec )
        q = q/1000.0

        print("qs",q,"kN")

        return q


# test

"""
beam = Hmemb(800,300,12,24,13)
print( beam.sa() )
print( beam.six() )
print( beam.szx() )
print( beam.siy() )
print( beam.szy() )
print( beam.ix() )
print( beam.iy() )
beam.print_prop()

"""
