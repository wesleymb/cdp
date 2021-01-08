import wx
import geCDP
import viwerNovoContrato
import modelContrato
import viwerGerenciar
import viwerServidores
import viwerRelatorioServidor

LISTA_DE_FRAMES= []
def contador_de_frames(frame):
    LISTA_DE_FRAMES.append(frame)


def main():
    viwerGDC()

class viwerGDC(object):
    """docstring for viwerGDC"""
    def __init__(self):
        super(viwerGDC, self).__init__()

        self.frame = wx.Frame(None, -1, 'Gerenciador de contratos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,1224,600)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        contador_de_frames(frame=self.frame)
        self.frame.Bind(wx.EVT_CLOSE, self.fechar_todos_os_frames)
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        self.menu_arquivo = wx.Menu()
        self.abaNovoContrato = self.menu_arquivo.Append(wx.ID_ANY, "Novo Contrato", "Novo Contrato")
        self.abaGerenciarServidores = self.menu_arquivo.Append(wx.ID_ANY, "Gerenciar servidores", "Gerenciar servidores")

        self.menuRelatorio = wx.Menu()
        self.abaRelatorioServidor = self.menuRelatorio.Append(wx.ID_ANY, "Relatório servidor", "Relatório servidor")

        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu_arquivo,"Arquivo")
        self.menu_bar.Append(self.menuRelatorio,"Relatórios")
        self.frame.SetMenuBar(self.menu_bar)


        wx.StaticText(self.panel, wx.ID_ANY, "Filtra", (25, 25))
        self.txtFiltro = wx.TextCtrl(self.panel, wx.ID_ANY,"", (60, 25),size=(500, -1),style=wx.TE_PROCESS_ENTER)
        self.txtFiltro.Bind(wx.EVT_TEXT_ENTER, self.carregaDadosContratosFiltrados)

        self.comboOpcoes = ['ID','Contrato','Processo','Objeto','Empresa']

        self.comboFiltro = wx.ComboBox(self.panel, wx.ID_ANY, pos = (575,25), choices = self.comboOpcoes, style=wx.CB_READONLY)

        self.buttonFiltar = wx.Button(self.panel, wx.ID_ANY, 'Filtar', (675, 25),size=(100,-1))

        self.listaDeContratos = wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(1055,450), pos=(20,60))      
        self.listaDeContratos.InsertColumn(0,"ID",width=50)
        self.listaDeContratos.InsertColumn(1,"Contrato",width=100)
        self.listaDeContratos.InsertColumn(2,"Processo",width=100)
        self.listaDeContratos.InsertColumn(3,"Objeto",width=200)
        self.listaDeContratos.InsertColumn(4,"Empresa",width=100)
        self.listaDeContratos.InsertColumn(5,"Início",width=100)
        self.listaDeContratos.InsertColumn(6,"Fim da vigência",width=100)
        self.listaDeContratos.InsertColumn(7,"Vencimento",width=100)
        self.listaDeContratos.InsertColumn(8,"Gestor",width=100)
        self.listaDeContratos.InsertColumn(9,"Status",width=100)
        

        self.listaDeContratos.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.abrirviwerGerenciar)


        self.button_novo = wx.Button(self.panel, wx.ID_ANY, 'Novo', (1090, 60),size=(100,-1))
        self.buttonGerenciar = wx.Button(self.panel, wx.ID_ANY, 'Gerenciar', (1090, 85),size=(100,-1))
        self.button_atulizar = wx.Button(self.panel, wx.ID_ANY, 'Atulizar', (1090, 115),size=(100,-1))
        
        self.button_excluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (1090, 160),size=(100,-1))

        self.buttonFechar = wx.Button(self.panel, wx.ID_ANY, 'Fechar', (1090, 475),size=(100,-1))


        self.button_novo.Bind(wx.EVT_BUTTON, self.abrirviwerNovoContrato)
        self.button_excluir.Bind(wx.EVT_BUTTON, self.exluirContrato)
        self.button_atulizar.Bind(wx.EVT_BUTTON, self.atulizarLista)
        self.buttonGerenciar.Bind(wx.EVT_BUTTON, self.abrirviwerGerenciar)
        self.buttonFiltar.Bind(wx.EVT_BUTTON, self.carregaDadosContratosFiltrados)
        self.buttonFechar.Bind(wx.EVT_BUTTON, self.fechar)

        self.frame.Bind(wx.EVT_MENU, self.abrirviwerServidores, self.abaGerenciarServidores)
        self.frame.Bind(wx.EVT_MENU, self.abrirviwerNovoContrato, self.abaNovoContrato)
        self.frame.Bind(wx.EVT_MENU, self.abrirviwerRelatorioServidor, self.abaRelatorioServidor)
            


        self.carregaDadosContratos()

        self.frame.Show()
        self.frame.Centre()

    
    def fechar(self,event):
        self.frame.Destroy()
    
    
    def atulizarLista(self,event):
        self.carregaDadosContratos()
    
    def carregaDadosContratosFiltrados(self,event):

        coluna = self.comboFiltro.GetValue()
        texto = self.txtFiltro.GetValue()
        
        if coluna == "Processo":
            coluna = "numeroDeProcesso"

        self.listaDeContratos.DeleteAllItems()
        self.index = 0
        dados = geCDP.queryTabelaComWhereLike(tabela="CONTRATO",coluna=coluna,dado=texto)
        
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


    def abrirviwerGerenciar(self,event):
        item = self.listaDeContratos.GetFocusedItem()
        if item != -1:
            idContrato = self.listaDeContratos.GetItem(itemIdx=item, col=0).GetText()
        
            telaContrato = viwerGerenciar.viwerGerenciar(idContrato=idContrato)
            contador_de_frames(telaContrato.frame)


    def abrirviwerNovoContrato(self,event):
        telaContrato = viwerNovoContrato.viwerNovoContrato()
        contador_de_frames(telaContrato.frame)

    def abrirviwerServidores(self,event):
        telaContrato = viwerServidores.gerenciarServidores()
        contador_de_frames(telaContrato.frame)

    def abrirviwerRelatorioServidor(self,event):
        telaContrato = viwerRelatorioServidor.relatorioServidores()
        contador_de_frames(telaContrato.frame)

    def exluirContrato(self,event):
        item = self.listaDeContratos.GetFocusedItem()
        
        if item != -1:
            dlgApagarContrato = wx.MessageDialog(None , "Tem certeza que quer excluir esse contrato?", "Alerta",wx.YES_NO | wx.ICON_WARNING)
            result = dlgApagarContrato.ShowModal()
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