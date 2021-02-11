import os
import wx
import shutil

def main(idContrato):
    viwerDocumentos(idContrato=idContrato)

class viwerDocumentos(object):
    """docstring for viwerDocumentos"""
    def __init__(self,idContrato):
        super(viwerDocumentos, self).__init__()
    
        if str(idContrato) not in os.listdir("documentos"):
            os.makedirs(os.path.join('documentos', str(idContrato)))
            
        self.pathDeDocumentos = os.path.join('documentos',str(idContrato))

        self.frame = wx.Frame(None, -1, 'Documentos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,650,300)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.statusbar.SetStatusText("ID contrato: {id}".format(id=idContrato))

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        
        self.buttonCarregar = wx.Button(self.panel, wx.ID_ANY, 'Incluir', (525, 25),size=(100,-1))
        self.buttonAbrir = wx.Button(self.panel, wx.ID_ANY, 'Abrir', (525, 50),size=(100,-1))
        self.buttonDownload = wx.Button(self.panel, wx.ID_ANY, 'Download', (525, 75),size=(100,-1))
        self.buttonExcluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (525, 100),size=(100,-1))
        self.buttonFechar = wx.Button(self.panel, wx.ID_ANY, 'Fechar', (525, 200),size=(100,-1))
        
        self.buttonCarregar.Bind(wx.EVT_BUTTON, self.buscarDocumento)
        self.buttonAbrir.Bind(wx.EVT_BUTTON, self.abrir)
        self.buttonDownload.Bind(wx.EVT_BUTTON, self.download)
        self.buttonExcluir.Bind(wx.EVT_BUTTON, self.excluir)
        self.buttonFechar.Bind(wx.EVT_BUTTON, self.fechar)


        self.listaDeDocumentos =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(475,200), pos=(25,25))
        self.listaDeDocumentos.InsertColumn(1,"Nome",width=475)
        
        self.listaDeDocumentos.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.abrir)

        self.listarDocumentosNaPasta()
        self.frame.Show()
        self.frame.Centre()
    
    
    def fechar(self,event):
        self.frame.Destroy()
    
    def excluir(self,event):
        dlgApagarDocumento = wx.MessageDialog(None , "Tem certeza que quer excluir esse documento?", "Excluir",wx.YES_NO | wx.ICON_WARNING)
        result = dlgApagarDocumento.ShowModal()
        
        if result == wx.ID_YES:
            item = self.listaDeDocumentos.GetFocusedItem()
            if item != -1:
                pathDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
                print(pathDesktop)
                documento = self.listaDeDocumentos.GetItem(itemIdx=item, col=0).GetText()
                os.remove(os.path.join(self.pathDeDocumentos, documento))
                self.listarDocumentosNaPasta()
               

    
    def download(self,event):
        item = self.listaDeDocumentos.GetFocusedItem()
        if item != -1:
            pathDesktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            documento = self.listaDeDocumentos.GetItem(itemIdx=item, col=0).GetText()
            shutil.copy(os.path.join(self.pathDeDocumentos, documento), pathDesktop)
            dlgRelatorio = wx.MessageDialog(None , "O arquivo foi baixado com sucesso","Pronto.", wx.OK| wx.ICON_INFORMATION)
            dlgRelatorio.ShowModal()  
             
    
    def abrir(self,event):
        item = self.listaDeDocumentos.GetFocusedItem()
        if item != -1:
            documento = self.listaDeDocumentos.GetItem(itemIdx=item, col=0).GetText()
            os.startfile(os.path.join(self.pathDeDocumentos, documento))    
    
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
    main(idContrato=1)
    app.MainLoop()