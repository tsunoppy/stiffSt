#! /Users/tsuno/.pyenv/shims/python3
# -*- coding:utf-8 -*-
import os, sys
#import Image
#import urllib2
#from cStringIO import StringIO


#zipアーカイブからファイルを読み込むため。通常は必要ないはず。
#sys.path.insert(0, 'reportlab.zip')

import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

#
import linecache
#

class Report():

    def __init__(self):
        #self.FONT_NAME = "Helvetica"
        self.FONT_NAME = "GenShinGothic"
        GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"
        # フォント登録
        pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))
        #font_size = 20
        #c.setFont('GenShinGothic', font_size)

    ########################################################################
    # 文字と画像を配置
    def create_row(self,c, index, data):
        y_shift = -240 * index
        #y_shift = -180 * index
        c.setFont(self.FONT_NAME, 9)
        """
        for i in range(0,len(data)):
            # txt
            c.drawString(300, 720-(i-1)*10 + y_shift, data[i])
        """
        c.drawString(55, self.ypos(0,y_shift), data[0].encode('utf-8'))
        c.drawString(55, self.ypos(1,y_shift), data[1].encode('utf-8'))

        # Slab Condition
        #lx = "{:.2f}".format(float(data[2]))
        #ly = "{:.2f}".format(float(data[3]))
        hh1 = data[2]
        bb1 = data[3]
        tw1 = data[4]
        tf1 = data[5]
        rr1 = data[6]
        # Sub Beam Member size
        hh2 = data[7]
        bb2 = data[8]
        tw2 = data[9]
        tf2 = data[10]
        rr2 = data[11]
        #
        ll  = data[12]
        ds  = data[13]
        #
        # Condition
        ## By Combo
        bound   = data[14]
        fixtype = data[15]
        ##
        qv = data[16]
        lb = data[17]
        fac = data[18]
        studfac = data[19]
        #
        # Connection
        htbsize  = data[20]
        friction = data[21]
        #
        n21 = data[22]
        n22 = data[23]
        n23 = data[24]
        #
        xpitch = data[25]
        ypitch = data[26]
        htbe   = data[27]
        #
        tg  = data[28]
        gassettype  = data[29]
        stud  = data[30]
        #
        # Material
        sigy1 = data[31]
        sigy2 = data[32]
        sigyg = data[33]
        htbm = data[34]
        #
        conc = data[35]
        fc   = data[36]
        gamma = data[37]
        #
        #result
        sa = data[38]
        ff = data[39]
        #
        # HTB
        e        = data[40]
        mm       = data[41]
        qvbar    = data[42]
        nnbar    = data[43]
        zb       = data[44]
        mmbyzb   = data[45]
        qbmax    = data[46]
        qa       = data[47]
        sfqb     = data[48]
        htbjudge = data[49]
        #
        # Gasset Plate
        e2       = data[50]
        mdg      = data[51]
        reqd     = data[52]
        # Stud bolt
        qs       = data[53]
        qe       = data[54]
        sfqe     = data[55]
        # stiffness
        dm       = data[56]
        dv       = data[57]
        dtotal   = data[58]
        kk       = data[59]
        kd       = data[60]
        sfkd     = data[61]
        kdjudge  = data[62]


        # Design Condition
        c.drawString(55, self.ypos(3,y_shift),
                     "大梁: H-" + hh1 + "x" + bb1 + "x"\
                     + tw1 + "x" + tf1 + "x" + rr1\
                     )
        c.drawString(170, self.ypos(3,y_shift),
                     "F=" + sigy1 + "N/mm2"\
                     )
        c.drawString(55, self.ypos(4,y_shift),
                     "小梁: H-" + hh2 + "x" + bb2 + "x"\
                     + tw2 + "x" + tf2 + "x" + rr2\
                     )
        c.drawString(170, self.ypos(4,y_shift),
                     "F=" + sigy2 + "N/mm2"\
                     )

        c.drawString(55, self.ypos(6,y_shift),
                     "設計条件"\
                     )
        #
        c.drawString(60, self.ypos(7,y_shift),
                     "横補剛長:" \
                     )
        c.drawString(160, self.ypos(7,y_shift),
                     "L=" + ll + "m"\
                     )
        #
        c.drawString(60, self.ypos(8,y_shift),
                     "小梁レベル差:"\
                     )
        c.drawString(160, self.ypos(8,y_shift),
                     "ds =" + ds + "mm"\
                     )
        #
        c.drawString(60, self.ypos(9,y_shift),
                     "小梁の取付き:"\
                     )
        if bound == "0":
            c.drawString(160, self.ypos(9,y_shift),
                         "片側" \
                         )
        elif bound == "1":
            c.drawString(160, self.ypos(9,y_shift),
                         "両側" \
                         )
        else:
            print("error bound")
        #
        c.drawString(60, self.ypos(10,y_shift),
                     "フランジの上部拘束:"\
                     )
        if fixtype == "0":
            c.drawString(160, self.ypos(10,y_shift),
                         "拘束あり" \
                         )
        elif fixtype == "1" :
            c.drawString(160, self.ypos(10,y_shift),
                         "拘束なし" \
                         )
        else:
            print("error bound")
        #
        c.drawString(60, self.ypos(11,y_shift),
                     "小梁の長期せん断力:"\
                     )
        c.drawString(160, self.ypos(11,y_shift),
                     "Qv=" + qv  + "kN" \
                     )
        #
        c.drawString(60, self.ypos(12,y_shift),
                     "横補剛区間:"\
                     )
        c.drawString(160, self.ypos(12,y_shift),
                     "lb=" + lb  + "m" \
                     )
        #
        c.drawString(60, self.ypos(13,y_shift),
                     "集中横力の係数"\
                     )
        c.drawString(160, self.ypos(13,y_shift),
                     "F=" + fac + "xσy・A/2" \
                     )
        #
        c.drawString(60, self.ypos(14,y_shift),
                     "スタッドのせん断耐力"\
                     )
        c.drawString(160, self.ypos(14,y_shift),
                     "qs=" + studfac + "x終局耐力" \
                     )

        #
        c.drawString(250, self.ypos(6,y_shift),
                     "JOINT"\
                     )
        c.drawString(260, self.ypos(7,y_shift),
                     gassettype + "-" + tg + "(" +  sigyg + "N/mm2)" \
                     )

        c.drawString(260, self.ypos(8,y_shift),
                     "HTB." + n21 + "+" + n22 + "+" + n23 + "-" + htbsize +\
                     "(" + htbm + ")"\
                     )

        c.drawString(260, self.ypos(9,y_shift),
                     " /px:@" + xpitch + ",py:@" + ypitch + ",e:" + htbe\
                     )
        #
        c.drawString(250, self.ypos(11,y_shift),
                     "スタッド"\
                     )
        if fixtype == "1":
            c.drawString(320, self.ypos(11,y_shift), "/使用しない" )

        c.drawString(260, self.ypos(12,y_shift),
                     "頭付きスタッド:φ" + stud \
                     )
        c.drawString(260, self.ypos(13,y_shift),
                     "コンクリート種別:" + conc \
                     )
        c.drawString(260, self.ypos(14,y_shift),
                     "Fc=" + fc + "N/mm2"\
                     )
        c.drawString(260, self.ypos(15,y_shift),
                     "γ=" + gamma + "kN/m3"\
                     )

        #
        c.drawString(250, self.ypos(17,y_shift),
                     "外力"\
                     )
        c.drawString(260, self.ypos(18,y_shift),
                     "A=" + sa + "cm2"\
                     )
        c.drawString(260, self.ypos(19,y_shift),
                     "F=" + ff + "kN"\
                     )

        #
        c.drawString(390, self.ypos(0,y_shift),
                     "- ボルトの設計"\
                     )
        c.drawString(400, self.ypos(1,y_shift),"e=")
        c.drawString(430, self.ypos(1,y_shift),
                     e + "m")
        c.drawString(470, self.ypos(1,y_shift),"M=")
        c.drawString(500, self.ypos(1,y_shift),
                     mm + "kN.m")
        c.drawString(400, self.ypos(2,y_shift),"Qv/n=")
        c.drawString(430, self.ypos(2,y_shift),
                     qvbar + "kN")
        c.drawString(470, self.ypos(2,y_shift),"F/n=")
        c.drawString(500, self.ypos(2,y_shift),
                     nnbar + "kN")
        c.drawString(400, self.ypos(3,y_shift),"Zb=")
        c.drawString(430, self.ypos(3,y_shift),
                     zb + "m")
        c.drawString(470, self.ypos(3,y_shift),"M/Zb=")
        c.drawString(500, self.ypos(3,y_shift),
                     mmbyzb + "kN")
        c.drawString(400, self.ypos(4,y_shift),"Qb=")
        c.drawString(430, self.ypos(4,y_shift),
                     qbmax + "kN")
        c.drawString(470, self.ypos(4,y_shift),"Qa=")
        c.drawString(500, self.ypos(4,y_shift),
                     qa + "kN")
        c.drawString(400, self.ypos(5,y_shift),"Qb/Qa=")
        c.drawString(430, self.ypos(5,y_shift),
                     sfqb )
        c.drawString(530, self.ypos(5,y_shift),"---" + htbjudge)
        #
        #
        c.drawString(390, self.ypos(7,y_shift),
                     "- ガセットプレートの必要せい"\
                     )
        c.drawString(400, self.ypos(8,y_shift),"e=")
        c.drawString(430, self.ypos(8,y_shift),
                     e2 + "m")
        c.drawString(470, self.ypos(8,y_shift),"M=")
        c.drawString(500, self.ypos(8,y_shift),
                     mdg + "kN.m")
        c.drawString(400, self.ypos(9,y_shift),"Qe/Qa=")
        c.drawString(430, self.ypos(9,y_shift),
                     reqd + "mm以上")
        #
        #
        c.drawString(390, self.ypos(11,y_shift),
                     "- スタッドボルトの必要本数"\
                     )
        c.drawString(400, self.ypos(12,y_shift),"Qe=")
        c.drawString(430, self.ypos(12,y_shift),
                     qe + "kN")
        c.drawString(470, self.ypos(12,y_shift),"qs=")
        c.drawString(500, self.ypos(12,y_shift),
                     qs + "kN")
        c.drawString(400, self.ypos(13,y_shift),"Qe/qs=")
        c.drawString(430, self.ypos(13,y_shift),
                     sfqe + "本")
        #
        #
        c.drawString(390, self.ypos(15,y_shift),
                     "- 補剛剛性の確認"\
                     )
        c.drawString(400, self.ypos(16,y_shift),"dm=")
        c.drawString(430, self.ypos(16,y_shift),
                     dm + "mm")
        c.drawString(470, self.ypos(16,y_shift),"dv=")
        c.drawString(500, self.ypos(16,y_shift),
                     dv + "mm")
        c.drawString(400, self.ypos(17,y_shift),"d=")
        c.drawString(430, self.ypos(17,y_shift),
                     dtotal + "m")
        c.drawString(400, self.ypos(18,y_shift),"K=F/d=")
        c.drawString(470, self.ypos(18,y_shift),
                     kk + "N/mm")
        c.drawString(400, self.ypos(19,y_shift),"Kd=5.0σyA/2lb=")
        c.drawString(470, self.ypos(19,y_shift),
                     kd + "N/mm")
        c.drawString(400, self.ypos(20,y_shift),"Kd/K=")
        c.drawString(430, self.ypos(20,y_shift),
                     sfkd )
        c.drawString(530, self.ypos(20,y_shift),"---" + kdjudge)
        #
#        c.drawString(260, self.ypos(2,y_shift),
#                     "fc = "
#                     )

        """
        for i in range(2,len(data)):
            # txt
            #c.drawString(300, 720-(i-1)*10 + y_shift, data[i])
            c.drawString(500, 720-(i-1)*10 + y_shift, data[i])
        """
        # png
        #imagefile=self.boundimage(ind_bound)
        #c.drawImage(imagefile, 70,  y_shift + 540, width=5*cm , preserveAspectRatio=True)

    def boundimage(self,index):
        if index == 0 or index == 1: # ４辺固定
            image_data = "./images/4sideFix.jpg"
        elif index == 2: # ３辺固定
            image_data = "./images/m3_1.jpg"
        elif index == 3:# ３辺固定
            image_data = "./images/m3_2.jpg"
        elif index == 4:# ２辺固定
            image_data = "./images/m2.jpg"
        elif index ==5: # 4辺支持
            image_data = "./images/m4pin.jpg"
        elif index ==6: # 3辺支持長辺支持
            image_data = "./images/m3_1pin.jpg"
        elif index ==7: # ３辺固定短辺支持
            image_data = "./images/m3-1pin2.jpg"
        elif index ==8: # 2辺固定2辺支持
            image_data = "./images/m2_2pin.jpg"
        elif index ==9: # 2辺固定2辺支持
            image_data = "./images/m2_2pin2.jpg"
        elif index ==10: # 2辺固定2辺支持
            image_data = "./images/m2_2pin3.jpg"
        elif IdBound ==11: # 短辺1辺固定3辺支持
            image_data = "./images/m1-3pin1.jpg"
        elif IdBound ==12: # 長辺1辺固定3辺支持
            image_data = "./images/m1-3pin2.jpg"
        else:
            print("Error report/def")

        return image_data

    def ypos(self,ipos,y_shift):
        return 730-(ipos-1)*10 + y_shift

    ########################################################################
    # pdfの作成
    def print_page(self, c, index, nCase):


        #タイトル描画
        c.setFont(self.FONT_NAME, 20)
        #c.drawString(50, 795, u"Design of the twoway slab")
        c.drawString(50, 795, u"横補剛接合部の設計")

        #グリッドヘッダー設定
        xlist = [40, 380, 560]
        ylist = [760, 780]
        c.grid(xlist, ylist)

        #sub title
        c.setFont(self.FONT_NAME, 12)
        c.drawString(55, 765, u"符号")
        c.drawString(390, 765, u"設計")

        #データを描画
        ########################################################################
        #for i, data in range(0,int(nCase)):

        for i in range(0,nCase):
#            f = open(inputf[index+i],'r')

            """
            tmpData = []
            while True:
                line = f.readline()
                if line:
                    if line != '\n':
                        tmpData.append(line.replace('\n',''))
                    else:
                        tmpData.append('')
                else:
                    break
            """
            line = linecache.getline('./db/rcslab.txt', index+i+1 )
            data = line.split(', ')
            linecache.clearcache()
            #f.close()
            #data = tmpData
            self.create_row( c, i, data )

        #最後にグリッドを更新
        ylist = [40,  280,  520,  760]
        #ylist = [40,  160, 280, 400, 520, 640, 760]
        #ylist = [40,  220,  400, 580, 760]4bunnkatsu
        c.grid(xlist, ylist[3 - nCase:])
        #ページを確定
        c.showPage()

    ########################################################################
    # pdfの作成
    def print_head(self, c , title):

        #title = 'Sample Project'

        #タイトル描画
        c.setFont(self.FONT_NAME, 20)
        c.drawString(50, 795, title)

        #sub title
        c.setFont(self.FONT_NAME, 12)

        #データを描画
        ########################################################################
        inputf = './db/input.txt'
        f = open(inputf,'r', encoding='utf-8')
        tmpData = []
        while True:
            line = f.readline()
            if line:
                if line != '\n':
                    tmpData.append(line.replace('\n',''))
                else:
                    tmpData.append('')
            else:
                break
        f.close()
        data = tmpData
        #c.setFont(self.FONT_NAME, 9)
        for i in range(0,len(data)):
            # txt
            c.drawString(55, 720-(i-1)*14, data[i])
        """
        # Model Diagram
        imagefile = './db/model.png'
        c.drawImage(imagefile, 60,  -300, width=18*cm , preserveAspectRatio=True)
        """
        #ページを確定
        c.showPage()
    ########################################################################
    # whole control
    def create_pdf(self, dataNum, pdfFile, title):

        # Parameter -------
        # inputf   : path to text file
        # imagefile: path to png file
        # pdfFile  : name of making pdf file

        #フォントファイルを指定して、フォントを登録
        #folder = os.path.dirname(reportlab.__file__) + os.sep + 'fonts'
        #pdfmetrics.registerFont(TTFont(FONT_NAME, os.path.join(folder, 'ipag.ttf')))
        #出力するPDFファイル
        c = canvas.Canvas(pdfFile)

        # ページ数
        ########################################################################
        #dataNum = len(inputf)
        numPage = dataNum // 3
        numMod = dataNum % 3
        #print(numPage,numMod)
        if numMod >= 1:
            numPage = numPage + 1

        # pdfの作成
        ########################################################################
        #self.print_head( c , title)

        for i in range(0,numPage):
            index = 3*i # index: 参照データのインデックス
            if numPage == 1:
                self.print_page( c, index, dataNum)
            elif i != numPage-1 and numPage != 1:
                self.print_page( c, index, 3)
            else:
                if numMod != 0:
                    self.print_page( c, index, numMod)
                else:
                    self.print_page( c, index, 3 )

        #pdfファイル生成
        ########################################################################
        c.save()
        print ("repot.py is Okay!!.")

########################################################################
# END CLASS


"""
########################################################################
# test script

pathname = "./test.pdf"
obj = Report()
# テキストの読み込み
########################################################################
inputf = []
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")

title = "sample"

obj.create_pdf(3,pathname,title)
"""
