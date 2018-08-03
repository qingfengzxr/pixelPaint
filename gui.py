import wx
import cv2
from DrawPicture import drawPicture


class MDIFrame(wx.MDIParentFrame):
  __B = 255
  __G = 0
  __R = 0
  __childNum = 0
  def __init__(self):
    color = [255,0,0]
    wx.MDIParentFrame.__init__(self, None, -1, "MDI Parent - www.yiibai.com", size = (600,400))
    #创建菜单
    menu = wx.Menu()
    menu2 = wx.Menu()
    #菜单布局
    menu.Append(5000, "&New Window")
    menu.Append(5001, "&Exit")
    menu2.Append(1000,"&color")

    menubar = wx.MenuBar()
    menubar.Append(menu, "&File")
    menubar.Append(menu2,"&tools")

    self.SetMenuBar(menubar)
    self.Bind(wx.EVT_MENU, self.OnNewWindow, id = 5000)
    self.Bind(wx.EVT_MENU, self.OnExit, id = 5001)


  def OnExit(self, event):
    self.Close(True)

  def OnNewWindow(self,event):
    win = wx.MDIChildFrame(self, -1,str(self.__childNum))
    self.__childNum += 1


    b = 0
    print(b)
    b += 1

    picture = drawPicture(200,200,10)
    #self.__pictureCount += 1

    def previewButton(event):
      picture.showCanvas("Back")

    def changeColor(event):
      print("true to setColor")
      print(self.__B)
      B = self.__B.GetValue()
      G = self.__G.GetValue()
      R = self.__R.GetValue()
      print(B,G,R)
      picture.setPaintBrushColor(B,G,R)

    def getColor(event):
        data = wx.ColourData()
        data.SetChooseFull(True)

        for i in range(0,16):
            colour = wx.Colour(i*16, i*16, i*16)
            data.SetCustomColour(i, colour)

        dialog = wx.ColourDialog(self, data)
        if dialog.ShowModal() == wx.ID_OK:
            retData = dialog.GetColourData()
            col = retData.GetColour()
            brush = wx.Brush(col, wx.SOLID)
            picture.setPaintBrushColor(col[2],col[1],col[0],)
            #myWindow.SetBackground(brush)
            #myWindow.Clear()
            #myWindow.Refresh()

    def saveButton(event):
      with wx.FileDialog(self, "Save jpg file", wildcard="jpg files (*.jpg)|*.png",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # save the current contents in the file
        pathname = fileDialog.GetPath()
        try:
            with open(pathname, 'w') as file:
                cv2.imwrite(pathname,picture.getCanvas())
        except IOError:
            wx.LogError("Cannot save current data in file '%s'." % pathname)



    panel = wx.Panel(win)#背景组件
    vbox = wx.BoxSizer(wx.VERTICAL)

    #窗口按钮布局
    btnPreview= wx.Button(panel,-1,u"预览",pos=(0,0),size=(50,30))
    vbox.Add(btnPreview,0,wx.ALIGN_CENTER)
    btnChangeColor = wx.Button(panel,-1,u"自定义色彩",pos=(70,0),size=(50,30))
    vbox.Add(btnChangeColor,0,wx.ALIGN_CENTER)
    btnSave = wx.Button(panel, -1, u"保存",pos = (150,0),size = (50,30))
    #vbox.Add(btnChangeColor,0,wx.ALIGN_CENTER)
    btnGetColor = wx.Button(panel, -1, u"色彩选择",pos = (210,0),size = (50,30))
    #vbox.Add(btnChangeColor,0,wx.ALIGN_CENTER)

    btnPreview.Bind(wx.EVT_BUTTON,previewButton)
    btnChangeColor.Bind(wx.EVT_BUTTON,changeColor)
    btnSave.Bind(wx.EVT_BUTTON,saveButton)
    btnGetColor.Bind(wx.EVT_BUTTON,getColor)


    #窗口参数输入框布局
    hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    self.__B = wx.TextCtrl(panel,style=wx.TE_RICH,pos=(3,40),size=(60,20))
    self.__G = wx.TextCtrl(panel,style=wx.TE_RICH,pos=(73,40),size=(60,20))
    self.__R = wx.TextCtrl(panel,style=wx.TE_RICH,pos=(143,40),size=(60,20))
    hbox1.Add(self.__R,1,wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5)
    hbox1.Add(self.__G,1,wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5)
    hbox1.Add(self.__B,1,wx.EXPAND|wx.ALIGN_CENTER|wx.ALL,5)
    #cv2.imshow("hello",cv2.imread('F:\example.jpeg'))

    win.Show(True)

app = wx.App()
frame = MDIFrame()
frame.Show()
app.MainLoop()


