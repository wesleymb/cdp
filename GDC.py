import wx
import geCDP
import os
import viwerGerecnciadosDeContratos


def main():
    if "bd_cdp.db" not in os.listdir():
        geCDP.criarBanco()
    if "relatorios" not in os.listdir():
        os.makedirs("relatorios")
    if "documentos" not in os.listdir():
        os.makedirs("documentos")
    
    viwerPrincipal()

class viwerPrincipal(object):
    """docstring for viwerGDC"""
    def __init__(self):
        super(viwerPrincipal, self).__init__()
        self.frame = wx.Frame(None, -1, 'GDC',style=wx.CLOSE_BOX|wx.CAPTION)
        self.panel = wx.Panel(self.frame)
        self.frame.SetDimensions(0,0,1800,900)
        
        self.frame.Bind(wx.EVT_CLOSE, self.fechar_todos_os_frames)
       
        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        image = wx.Image('logoSEINFRA.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        wx.StaticBitmap(self.panel,wx.ID_ANY,image,pos=(650,200))

        
        self.menu_arquivo = wx.Menu()
        self.abaGerenciarContratos = self.menu_arquivo.Append(wx.ID_ANY, "Gerenciar contratos", "Gerenciar contratos")


        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu_arquivo,"Arquivo")
        self.frame.SetMenuBar(self.menu_bar)

        self.frame.Bind(wx.EVT_MENU, self.abrirviwerGDC, self.abaGerenciarContratos)
        
        self.frame.Show()
        self.frame.Centre()
        
    
    def abrirviwerGDC(self,event):
       viwerGerecnciadosDeContratos.viwerGDC()
       
    
    def fechar_todos_os_frames(self, event):
        for frame in wx.GetTopLevelWindows():
            try:
                frame.Destroy()
            except:
                continue

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()


