import wx
import geCDP
import viwerNovoContrato
import modelContrato

LISTA_DE_FRAMES= []
def contador_de_frames(frame):
    LISTA_DE_FRAMES.append(frame)


def main():
    viwerCdp()

class viwerCdp(object):
    """docstring for viwerCdp"""
    def __init__(self):
        super(viwerCdp, self).__init__()

        self.frame = wx.Frame(None, -1, 'CPD', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,1224,600)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        contador_de_frames(frame=self.frame)
        self.frame.Bind(wx.EVT_CLOSE, self.fechar_todos_os_frames)
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        self.menu_arquivo = wx.Menu()
        self.aba_novo_contrato = self.menu_arquivo.Append(wx.ID_ANY, "Novo Contrato", "Novo Contrato")


        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu_arquivo,"Arquivo")
        self.frame.SetMenuBar(self.menu_bar)


        self.listaDeContratos = wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(1055,450), pos=(20,40))      
        self.listaDeContratos.InsertColumn(0,"ID",width=50)
        self.listaDeContratos.InsertColumn(1,"Contrato",width=100)
        self.listaDeContratos.InsertColumn(2,"Processo",width=100)
        self.listaDeContratos.InsertColumn(3,"Objeto",width=200)
        self.listaDeContratos.InsertColumn(4,"Empresa",width=100)
        self.listaDeContratos.InsertColumn(5,"Início",width=100)
        self.listaDeContratos.InsertColumn(6,"Fim da vigencia",width=100)
        self.listaDeContratos.InsertColumn(7,"Vencimento",width=100)
        self.listaDeContratos.InsertColumn(8,"Gestor",width=100)
        self.listaDeContratos.InsertColumn(9,"Status",width=100)
        

        self.button_novo = wx.Button(self.panel, wx.ID_ANY, 'Novo', (1080, 40),size=(100,-1))
        self.buttonGerenciar = wx.Button(self.panel, wx.ID_ANY, 'Gerenciar', (1080, 65),size=(100,-1))
        self.button_atulizar = wx.Button(self.panel, wx.ID_ANY, 'Atulizar', (1080, 95),size=(100,-1))
        
        self.button_excluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (1080, 175),size=(100,-1))


        self.button_novo.Bind(wx.EVT_BUTTON, self.abrirviwerNovoContrato)
        self.button_excluir.Bind(wx.EVT_BUTTON, self.exluirContrato)
        self.button_atulizar.Bind(wx.EVT_BUTTON, self.atulizarLista)

        self.carregaDadosContratos()

        self.frame.Show()
        self.frame.Centre()

    def atulizarLista(self,event):
        self.carregaDadosContratos()
    
    def carregaDadosContratos(self):
        self.listaDeContratos.DeleteAllItems()
        self.index = 0
        dados = geCDP.queryTabela(tabela="CONTRATO")
        
        for dado in dados:
            contratoQuery = modelContrato.contrato(listaDedadosContrato=dado)
            id = str(contratoQuery.id)
            contrato = contratoQuery.contrato
            processo = contratoQuery.numeroDeProcesso
            objeto = contratoQuery.objeto
            empresa = contratoQuery.empresa
            inicio = contratoQuery.dataAssinatura 
            fimDaVigencia = contratoQuery.dataTermino
            vencimento = contratoQuery.vencimento
            gestor = contratoQuery.gestor
            
            status = contratoQuery.status
            

            self.listaDeContratos.InsertStringItem(self.index, id)
            self.listaDeContratos.SetStringItem(self.index, 1, contrato)
            self.listaDeContratos.SetStringItem(self.index, 2, processo)
            self.listaDeContratos.SetStringItem(self.index, 3, objeto)
            self.listaDeContratos.SetStringItem(self.index, 4, empresa)
            self.listaDeContratos.SetStringItem(self.index, 5, inicio)
            self.listaDeContratos.SetStringItem(self.index, 6, fimDaVigencia)
            self.listaDeContratos.SetStringItem(self.index, 7, vencimento)
            self.listaDeContratos.SetStringItem(self.index, 8, gestor)
            self.listaDeContratos.SetStringItem(self.index, 9, status)
            self.index += 1



    def abrirviwerNovoContrato(self,event):
        telaContrato = viwerNovoContrato.viwerNovoContrato()
        contador_de_frames(telaContrato.frame)

    def exluirContrato(self,event):
        item = self.listaDeContratos.GetFocusedItem()
        
        if item != -1:
            dlg_juntar_pdf_em_massa = wx.MessageDialog(None , "Tem certeza que quer excluir esse processo?", "Juntar",wx.YES_NO | wx.ICON_WARNING)
            result = dlg_juntar_pdf_em_massa.ShowModal()
            if result == wx.ID_YES: 
                idContrato = self.listaDeContratos.GetItem(itemIdx=item,col=0).GetText()
                geCDP.excluirContrato(idContrato=idContrato)
                self.carregaDadosContratos()    


    def fechar_todos_os_frames(self, event):
        for frame in LISTA_DE_FRAMES:
            try:
                frame.Destroy()
            except:
                continue

    


if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()