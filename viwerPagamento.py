import wx
import wx.adv
import geCDP
import modelPagamento
import modelContrato
import datetime


def main():
    gerenciarVencimentos(idPagamento=1, valor=None, dataDeVencimento=None, numeroDeProcesso=None, status=None)

class gerenciarVencimentos(object):
    """docstring for viwerGerenciar"""
    def __init__(self,idPagamento,valor,dataDeVencimento,numeroDeProcesso,status):
        super(gerenciarVencimentos, self).__init__()
        self.idPagamento = idPagamento
        self.valor = valor
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
       

        self.buttonIncluir = wx.Button(self.panel, wx.ID_ANY, 'Salvar', (75, 200),size=(100,-1))
        self.buttonFechar = wx.Button(self.panel, wx.ID_ANY, 'Fechar', (200, 200),size=(100,-1))

        self.buttonFechar.Bind(wx.EVT_BUTTON, self.fechar)

        self.frame.Show()
        self.frame.Centre()

    def fechar(self,event):
        self.frame.Destroy()
        

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()