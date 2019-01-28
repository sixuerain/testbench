import wx, bistable

bi=bistable.bistable(0x24); bi.AT, bi.reg

class MainFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, wx.NewId(), "RELAY BOX")
        NBr=5; bouat = {}
        panel = wx.Panel(self,1)
        #sizer = wx.BoxSizer(wx.HORIZONTAL)
        boxsizer = wx.BoxSizer(wx.VERTICAL)
        for i in range(1,NBr+1, 1):
            bouat[i]=wx.CheckBox(panel, label="Relay {}".format(i))
            bouat[i].SetValue((bi.reg>>(i-1)&0x1))
        self.Bind(wx.EVT_CHECKBOX, self.OntextMetric)
        self.abt_Metric= wx.StaticText(panel, label='')
        [boxsizer.Add(bouat[i],flag=wx.LEFT, border=5) for i in range(1,NBr+1,1)]
        boxsizer.Add(self.abt_Metric, flag = wx.LEFT)
        panel.SetSizer(boxsizer)

    def OntextMetric(self,event):
        """
        reccup wx.CheckBox label des box vire Relay => nb
        """
        nb=event.GetEventObject().GetLabel().split(" ")[1]
        if event.IsChecked():
            CK=", checked!"
            bi.addreg(int(nb)-1)
        else:
            bi.rmreg(int(nb)-1)
            CK=", unchecked!"
        label=event.GetEventObject().GetLabel()+CK+"__"+nb
        self.abt_Metric.SetLabel(label)
        bi.set()
        print(bi)


class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

bi.set()#<== optionnel (si Rpi eteint => reset relay config
# or if file 'register.txt' had been modified by hand
app = MyApp(0)
app.MainLoop()
