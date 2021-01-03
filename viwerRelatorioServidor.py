import wx
import modelServidor
import geCDP
import modelNovoServidor
import modelFiscal
import modelContrato
import geRelatorioServidor


def main():
    relatorioServidores()

class relatorioServidores(object):
    """docstring for relatorioServidores"""
    def __init__(self):
        super(relatorioServidores, self).__init__()
        
        self.frame = wx.Frame(None, -1, 'Relatório servidores', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,650,325)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)
        

        wx.StaticText(self.panel, wx.ID_ANY, "Filtra", (25, 25))
        self.txtFiltro = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 50),size=(350, -1),style=wx.TE_PROCESS_ENTER)

        self.txtFiltro.Bind(wx.EVT_TEXT_ENTER, self.filtarServidor)

        self.buttonFiltar = wx.Button(self.panel, wx.ID_ANY, 'Filtar', (400, 50),size=(100,-1))


        self.buttonGerar = wx.Button(self.panel, wx.ID_ANY, 'Gerar', (525, 100),size=(100,-1))

        
        self.listaDeServidores =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(475,150), pos=(25,100))
        self.listaDeServidores.InsertColumn(0,"ID",width=50)
        self.listaDeServidores.InsertColumn(1,"Nome",width=300)
        self.listaDeServidores.InsertColumn(2,"ID funcional",width=125)


        self.buttonGerar.Bind(wx.EVT_BUTTON, self.gerarRelatorio)
    
        self.buttonFiltar.Bind(wx.EVT_BUTTON, self.filtarServidor)


        self.carregaDadosServidores()

        self.frame.Show()
        self.frame.Centre()
    

    def gerarRelatorio(self,event):

        item = self.listaDeServidores.GetFocusedItem()
        if item != -1:
            idServidor = self.listaDeServidores.GetItem(itemIdx=item, col=0).GetText()
            nome = self.listaDeServidores.GetItem(itemIdx=item, col=1).GetText()
            idFuncional = self.listaDeServidores.GetItem(itemIdx=item, col=2).GetText()
            listaServidoresFiscal,listaServidoresGestor = self.verificarVinclulos(idServidor=idServidor)
            relatorio = geRelatorioServidor.relatorio(nome=nome,idFuncional=idFuncional,listaServidoresFiscal=listaServidoresFiscal,listaServidoresGestor=listaServidoresGestor)
            relatorio.gerarRelatorio()

            dlgRelatorio = wx.MessageDialog(None , "Relatório gerado com sucesso","Pronto.", wx.OK| wx.ICON_INFORMATION)
            dlgRelatorio.ShowModal()  


    def filtarServidor(self,event):
        self.listaDeServidores.DeleteAllItems()
        self.index = 0
        
        texto = self.txtFiltro.GetValue()

        for Servidor in  geCDP.queryTabelaComWhereLike(tabela="SERVIDOR",coluna="NOME",dado=texto):
            objServidor = modelServidor.servidor(Servidor)
            self.listaDeServidores.InsertStringItem(self.index, str(objServidor.id))
            self.listaDeServidores.SetStringItem(self.index, 1, objServidor.nome)
            self.listaDeServidores.SetStringItem(self.index, 2, objServidor.idFuncional)
            self.index += 1

        self.txtFiltro.SetValue('')

    
    def verificarVinclulos(self,idServidor):
        listaServidoresFiscal = []
        listaServidoresGestor = []
        
        for ServidorFiscal in geCDP.queryTabelaFiscalComContrato(idServidor=idServidor):
            objFiscal = modelContrato.contrato(ServidorFiscal)
            listaServidoresFiscal.append(objFiscal)
            
            
        
        for GestorContrato in geCDP.queryTabelaComWhere(tabela="CONTRATO",coluna="idServidorGestor",dado=idServidor):
            objGestor = modelContrato.contrato(GestorContrato)
            listaServidoresGestor.append(objGestor)

        return listaServidoresFiscal,listaServidoresGestor
        
   


    def carregaDadosServidores(self):
        self.listaDeServidores.DeleteAllItems()
        self.index = 0

        for Servidor in geCDP.queryTabela(tabela="SERVIDOR"):
            objServidor = modelServidor.servidor(Servidor)
            self.listaDeServidores.InsertStringItem(self.index, str(objServidor.id))
            self.listaDeServidores.SetStringItem(self.index, 1, objServidor.nome)
            self.listaDeServidores.SetStringItem(self.index, 2, objServidor.idFuncional)
            self.index += 1
            

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()