import wx
import wx.adv
import geCDP
import modelPagamento
import modelContrato


def main():
    viwerGerenciarVencimentos(idContrato=3)

class viwerGerenciarVencimentos(object):
    """docstring for viwerGerenciar"""
    def __init__(self,idContrato):
        super(viwerGerenciarVencimentos, self).__init__()
        self.idContrato = idContrato

        self.frame = wx.Frame(None, -1, 'Gerenciar de Vencimentos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,575,450)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        wx.StaticText(self.panel, wx.ID_ANY, "Valor", (25, 25))
        # self.valor = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 50),size=(200, -1))

        self.valor = wx.SpinCtrlDouble(self.panel, wx.ID_ANY,pos=(25, 50),inc=000000.01,max=10000000000)        

        wx.StaticText(self.panel, wx.ID_ANY, "Data de Vencimento:", (200, 25))
        self.calendarioVencimento = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (200, 50), style=wx.adv.DP_DROPDOWN)

        wx.StaticText(self.panel, wx.ID_ANY, "Número de processo", (25, 100))
        self.numeroDeprocesso = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 125),size=(150, -1))
        
        self.comboOpcoes = ['PAGO','ABERTO','TRAMITANDO']

        wx.StaticText(self.panel, wx.ID_ANY, "Status", (200, 100))
        self.comboStatus = wx.ComboBox(self.panel, wx.ID_ANY, pos = (200,125), choices = self.comboOpcoes, style=wx.CB_READONLY)
        
        self.listaDeVencimentos =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(500,220), pos=(25,160))
        self.listaDeVencimentos.InsertColumn(0,"ID",width=50)
        self.listaDeVencimentos.InsertColumn(1,"Vencimento",width=100)
        self.listaDeVencimentos.InsertColumn(2,"Valor",width=100)
        self.listaDeVencimentos.InsertColumn(3,"Número de processo",width=150)
        self.listaDeVencimentos.InsertColumn(4,"Status",width=100)

        self.buttonSalvar = wx.Button(self.panel, wx.ID_ANY, 'Salvar', (425, 100),size=(100,50))
        self.buttonSalvar.Bind(wx.EVT_BUTTON, self.salvar)

        self.carregarDoBanco()

        self.frame.Show()
        self.frame.Centre()

    
    def salvar(self,event):
        valor = self.valor.GetValue()
        print(valor)
    

    
    
    def carregarDoBanco(self):
        self.listaDeVencimentos.DeleteAllItems()
        self.index = 0
        
        dados = geCDP.queryTabelaComWhere(tabela="PAGAMENTO",coluna="idContrato",dado=self.idContrato)

        if dados != []:

            for queryPagamento in dados:
                Pagamento = modelPagamento.pagamento(listaDedados=queryPagamento)
                
                self.listaDeVencimentos.InsertStringItem(self.index, str(Pagamento.id))
                self.listaDeVencimentos.SetStringItem(self.index, 1, Pagamento.dataDePagamento)
                self.listaDeVencimentos.SetStringItem(self.index, 2, "R$ {}".format(str(Pagamento.valor)))
                self.listaDeVencimentos.SetStringItem(self.index, 3, Pagamento.numeroDeProcesso)
                self.listaDeVencimentos.SetStringItem(self.index, 4, Pagamento.status)
                self.index += 1
        else:
            dados = geCDP.queryTabelaComWhere(tabela="CONTRATO",coluna="id",dado=self.idContrato)
            for queryContrato in dados:
                Contrato = modelContrato.contrato(queryContrato)
                vencimentos = Contrato.gerarVencimentos()
                for vencimento in vencimentos:
                    Pagamento = modelPagamento.pagamento((self.idContrato,vencimento),tipo=2)
                    Pagamento.inserirNovoPagamento()
            
            self.carregarDoBanco()

        

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()