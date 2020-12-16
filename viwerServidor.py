import wx
import geCDP

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


        self.listaDeContratos = wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(1000,450), pos=(20,40))      
        self.listaDeContratos.InsertColumn(0,"Contrato",width=100)
        self.listaDeContratos.InsertColumn(1,"Processo",width=100)
        self.listaDeContratos.InsertColumn(2,"Objeto",width=200)
        self.listaDeContratos.InsertColumn(3,"Empresa",width=100)
        self.listaDeContratos.InsertColumn(4,"Início",width=100)
        self.listaDeContratos.InsertColumn(5,"Fim da vigencia",width=100)
        self.listaDeContratos.InsertColumn(6,"Vencimento",width=100)
        self.listaDeContratos.InsertColumn(7,"Gestor",width=100)
        self.listaDeContratos.InsertColumn(8,"Status",width=100)

        self.button_novo = wx.Button(self.panel, wx.ID_ANY, 'Novo', (1050, 40),size=(100,-1))
        self.button_alterar = wx.Button(self.panel, wx.ID_ANY, 'Altera', (1050, 65),size=(100,-1))
        self.button_excluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (1050, 95),size=(100,-1))

        self.carregaDadosContratos()

        self.frame.Show()
        self.frame.Centre()

    def carregaDadosContratos(self):
        dados = geCDP.queryTabela(tabela="CONTRATO")
        # print(dados)
        for dado in dados:
            contrato = dado[1]
            processo = dado[2]
            objeto = dado[3]
            empresa = dado[4]
            inicio = dado[5] 
            fimDaVigencia = dado[6]
            vencimento = dado[7]
            gestor = geCDP.queryTabelaServidorComContrato(servidor=dado[8])
            status = dado[9]

            self.listaDeContratos.InsertStringItem(self.index, contrato)
            self.listaDeContratos.SetStringItem(self.index, 1, processo)
            self.listaDeContratos.SetStringItem(self.index, 2, objeto)
            self.listaDeContratos.SetStringItem(self.index, 3, empresa)
            self.listaDeContratos.SetStringItem(self.index, 4, inicio)
            self.listaDeContratos.SetStringItem(self.index, 5, fimDaVigencia)
            self.listaDeContratos.SetStringItem(self.index, 6, vencimento)
            self.listaDeContratos.SetStringItem(self.index, 7, gestor[0][0])
            self.listaDeContratos.SetStringItem(self.index, 8, status)
            self.index += 1





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