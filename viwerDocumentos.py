import os
import wx
import shutil

def main(idContrato):
    pathDeDocumentos = os.path.join('documentos',str(idContrato))
    
    if str(idContrato) not in os.listdir("documentos"):
        os.makedirs(pathDeDocumentos)
        viwerDocumentos(idContrato=idContrato,pathDeDocumentos=pathDeDocumentos)
    else:
        viwerDocumentos(idContrato=idContrato,pathDeDocumentos=pathDeDocumentos)

class viwerDocumentos(object):
    """docstring for viwerDocumentos"""
    def __init__(self,idContrato,pathDeDocumentos):
        super(viwerDocumentos, self).__init__()
        
        self.pathDeDocumentos = pathDeDocumentos

        self.frame = wx.Frame(None, -1, 'Documentos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,650,325)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)
    
        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        wx.StaticText(self.panel, wx.ID_ANY, "Carregar", (25, 25))
        self.arquivo = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 50),size=(350, -1),style=wx.TE_PROCESS_ENTER)
        
        self.buttonCarregar = wx.Button(self.panel, wx.ID_ANY, 'Carregar', (400, 50),size=(100,-1))

        self.buttonCarregar.Bind(wx.EVT_BUTTON, self.buscarDocumento)

        self.listaDeDocumentos =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(475,150), pos=(25,100))
        self.listaDeDocumentos.InsertColumn(1,"Nome",width=475)
        
        self.listarDocumentosNaPasta()
        self.frame.Show()
        self.frame.Centre()
        
    def deletarItensDalista(self):
        self.listaDeDocumentos.DeleteAllItems()
        self.index = 0
    
    def listarDocumentosNaPasta(self):
        self.deletarItensDalista()
        listaDeDocumentos =  os.listdir(self.pathDeDocumentos)
        for documento in listaDeDocumentos:
            self.listaDeDocumentos.InsertStringItem(self.index, str(documento))
            self.index += 1

    def buscarDocumento(self,event):
        openFileDialog = wx.FileDialog (self.frame, "Selecione o PDF",wildcard="Arquivos (*.pdf,.*doc,*.docx,.*csv)|*.pdf;*.doc;*.docx;.*csv")
        openFileDialog.ShowModal()

        if openFileDialog.GetPath() != '' or openFileDialog.GetPath() != None: 
            pathDoDocumento = openFileDialog.GetPath()
            shutil.copy(pathDoDocumento, self.pathDeDocumentos)
            self.listarDocumentosNaPasta()

        

if __name__ == '__main__':
    app = wx.App()
    main(idContrato=3)
    app.MainLoop()