import wx
import wx.adv
import geCDP
import modelPagamento
import modelContrato
import datetime


def main():
    pagamento(viwerOpened=None, idPagamento=1, valor=None, dataDeVencimento=None, numeroDeProcesso=None, status=None)

class pagamento(object):
    """docstring for viwerGerenciar"""
    def __init__(self, viwerOpened, idPagamento=None, idContrato=None,valor=None, dataDeVencimento=None, numeroDeProcesso=None, status='NOVO'):
        super(pagamento, self).__init__()
        self.viwerOpened = viwerOpened
        self.idPagamento = idPagamento
        self.idContrato = idContrato
        self.valorPagamento = valor
        self.dataDeVencimento = dataDeVencimento
        self.numeroDeProcesso = numeroDeProcesso
        self.status = status

        self.frame = wx.Frame(None, -1, 'Vencimento', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,350,350)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        self.statusbar.SetStatusText("ID pagamento: {id}".format(id=self.idPagamento))

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
       

        self.buttonSalvar = wx.Button(self.panel, wx.ID_ANY, 'Salvar', (75, 200),size=(100,-1))
        self.buttonFechar = wx.Button(self.panel, wx.ID_ANY, 'Fechar', (200, 200),size=(100,-1))


        self.buttonSalvar.Bind(wx.EVT_BUTTON, self.salvar)

        self.buttonFechar.Bind(wx.EVT_BUTTON, self.fechar)

        if self.status !='NOVO':
            self.carregarDados()

        self.frame.Show()
        self.frame.Centre()

    
    def carregarDados(self):
        
        self.valor.SetValue(self.valorPagamento)
        self.calendarioVencimento.SetValue(self.dataDeVencimento)
        self.numeroDeprocesso.SetValue(self.numeroDeProcesso)
        self.comboStatus.SetValue(self.status)
                
        self.statusbar.SetStatusText("ID pagamento: {id}".format(id=self.idPagamento))

    
    def fechar(self,event):
        self.frame.Destroy()
        

    def salvar(self,event):
        if self.status == 'NOVO':
            dataDePagamento = self.calendarioVencimento.GetValue().FormatISODate()
            valor = self.valor.GetValue()
            status = self.comboStatus.GetValue()
            numeroDeProcesso = self.numeroDeprocesso.GetValue()

            Pagamento = modelPagamento.pagamento((self.idContrato,dataDePagamento,valor,status,numeroDeProcesso),tipo=2)
            Pagamento.inserirNovoPagamentoManual()
            
           
            dlgAtulizacao = wx.MessageDialog(None , "Pagamento incluido com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
            dlgAtulizacao.ShowModal()  
            
        
        else:
            
            dataDePagamento = self.calendarioVencimento.GetValue().FormatISODate()
            valor = self.valor.GetValue()
            status = self.comboStatus.GetValue()
            numeroDeProcesso = self.numeroDeprocesso.GetValue()

            

            Pagamento = modelPagamento.pagamento((self.idPagamento,self.idContrato,dataDePagamento,valor,status,numeroDeProcesso))
            Pagamento.atulizarPagamento()

            self.viwerOpened.carregarDoBanco()
            
            dlgAtulizacao = wx.MessageDialog(None , "Pagamento atulizado com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
            dlgAtulizacao.ShowModal()
        
        self.frame.Destroy()
        self.viwerOpened.carregarDoBanco()

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()