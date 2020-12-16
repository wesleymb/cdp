import wx


def main():
    viwerContrato(statusEntrada='Novo')

class viwerContrato(object):
    """docstring for viwerContrato"""
    def __init__(self,statusEntrada):
        super(viwerContrato, self).__init__()
        self.statusEntrada = statusEntrada

        self.frame = wx.Frame(None, -1, 'Contrato', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,1224,600)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)
        self.statusbar.SetStatusText(self.statusEntrada)

        wx.StaticBox(self.panel, wx.ID_ANY, 'Dados do Contrato', (15, 5), size=(300, 150))

        wx.StaticText(self.panel, wx.ID_ANY, "* Contrato", (25, 25))
        self.contrato = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 25),size=(50, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "* Processo", (25, 75))
        self.processo = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 75),size=(125, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "* Empresa", (25, 125))
        self.empresa = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 125),size=(125, -1))


        self.frame.Show()
        self.frame.Centre()


if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()