import cv2
import numpy as np
import random

class drawPicture():
    __canvasFront= 0#前景画布
    __canvasBack = 0#后置画布
    __paintBrush = (255,0,0)#画笔
    __canvasColor = (255,255,255)#画布背景色
    __girdLineColor = (255,0,0)#网格线色彩
    __verticalInterval = 0#网格线间距
    __canvasWidth = 0
    __canvasHeight = 0
    __girdLineRect = [[]]#网格线单元格信息[左上角x坐标,左上角y坐标,右下角x坐标,右下角y坐标,单元格情况]
    __windowNum = 0
    def __init__(self,canvasWidth,canvasHeight,verticalInterval):
        self.__windowNum = random.randint(0,99)
        #生成前置画布与后置画布
        self.__canvasWidth = canvasWidth
        self.__canvasHeight = canvasHeight
        self.__canvasFront = np.zeros((self.__canvasWidth,self.__canvasHeight,3),np.uint8)
        self.__canvasBack = np.zeros((self.__canvasWidth,self.__canvasHeight,3),np.uint8)
        self.__verticalInterval = verticalInterval
        #设置鼠标操作
        #为画布设置背景，初始为白色
        for i in range(0,self.__canvasFront.shape[1]):
          cv2.line(self.__canvasFront,(i,0),(i,self.__canvasFront.shape[0]),self.__canvasColor,1)
        for i in range(0,self.__canvasBack.shape[1]):
          cv2.line(self.__canvasBack,(i,0),(i,self.__canvasBack.shape[0]),self.__canvasColor,1)
        #绘制网格线
        print("drawing")
        self.drawGirdLine()
        self.showCanvas()
        cv2.setMouseCallback(str(self.__windowNum),self.filling)

    def getCanvas(self,flag = "Back"):
      if flag == "Back":
        return self.__canvasBack
      elif flag == "Front":
        return self.__canvasFront

    def showCanvas(self,flag = "Front"):
      if flag == "Front":
        #cv2.namedWindow(str(self.__windowNum))
        cv2.imshow(str(self.__windowNum),self.__canvasFront)
      elif flag == "Back":
        #cv2.namedWindow(str(self.__windowNum))
        cv2.imshow(str(self.__windowNum),self.__canvasBack)

    def setPaintBrushColor(self,B,G,R):
      print(B,G,R)
      self.__paintBrush = (int(B),int(G),int(R))

    def setCanvasColor(self,R,G,B):
      self.__canvasColor = (B,G,R)

    def drawGirdLine(self):#绘制网格线于前置画布
      #shape[0]高，shape[1]宽
      for i in range(0,self.__canvasFront.shape[1]):
          cv2.line(self.__canvasFront,(i,0),(i,self.__canvasFront.shape[0]),self.__canvasColor,1)
          cv2.line(self.__canvasBack,(i,0),(i,self.__canvasFront.shape[0]),self.__canvasColor,1)

      #绘制竖线
      i = 0
      while i < self.__canvasFront.shape[1]:
          cv2.line(self.__canvasFront,(i,0),(i,self.__canvasFront.shape[0]),self.__girdLineColor,1)
          i += self.__verticalInterval
      #绘制横线
      i = 0
      while i < self.__canvasFront.shape[0]:
          cv2.line(self.__canvasFront,(0,i),(self.__canvasFront.shape[1],i),self.__girdLineColor,1)
          i += self.__verticalInterval
      self.setGirdLineInformation()

    def setGirdLineInformation(self):
      i = 0
      j = 0
      length = 0
      height = 0
      while height < self.__canvasFront.shape[0]:
        self.__girdLineRect.append([])
        length = 0
        while length < self.__canvasFront.shape[1]:
          self.__girdLineRect[i].append([length,height,length+self.__verticalInterval,height+self.__verticalInterval,0])
          length += self.__verticalInterval
          j += 1
        i += 1
        height += self.__verticalInterval

    def filling(self,event,x,y,flags,param):
      if event == cv2.EVENT_LBUTTONDOWN:
        ix,iy = x,y
        h = int(iy / 10)
        w = int(ix / 10)
        print(w,h)
        print(self.__girdLineRect[h][w])
        if self.__girdLineRect[h][w][4] == 0:
          self.__girdLineRect[h][w][4] = 1
          i = self.__girdLineRect[h][w][1]
          while i < self.__girdLineRect[h][w][3]:
            cv2.line(self.__canvasFront,(self.__girdLineRect[h][w][0],i),
                     (self.__girdLineRect[h][w][2],i),self.__paintBrush,1)
            cv2.line(self.__canvasBack,(self.__girdLineRect[h][w][0],i),
                     (self.__girdLineRect[h][w][2],i),self.__paintBrush,1)
            i += 1
        else:
          self.__girdLineRect[h][w][4] = 0
          i = self.__girdLineRect[h][w][1]
          while i < self.__girdLineRect[h][w][3]:
            cv2.line(self.__canvasFront,(self.__girdLineRect[h][w][0],i),
                     (self.__girdLineRect[h][w][2],i),self.__canvasColor,1)
            cv2.line(self.__canvasBack,(self.__girdLineRect[h][w][0],i),
                     (self.__girdLineRect[h][w][2],i),self.__canvasColor,1)
            i += 1
          cv2.rectangle(self.__canvasFront,(self.__girdLineRect[h][w][0],self.__girdLineRect[h][w][1]),
                        (self.__girdLineRect[h][w][2],self.__girdLineRect[h][w][3]),self.__girdLineColor,1)
        self.showCanvas()
