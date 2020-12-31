import wx
import wx.adv
import geCDP
import modelNovoContrato
import datetime
import viwerCdp



def main():
    viwerNovoContrato()

class viwerNovoContrato(object):
    """docstring for viwerNovoContrato"""
    def __init__(self):
        super(viwerNovoContrato, self).__init__()
        
        self.frame = wx.Frame(None, -1, 'Novo contrato', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,550,350)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        wx.StaticBox(self.panel, wx.ID_ANY, 'Dados do Contrato', (15, 5), size=(500, 600))

        wx.StaticText(self.panel, wx.ID_ANY, "Contrato", (25, 25))
        self.contrato = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 25),size=(70, -1))

        self.radioOpcoes = ['ATIVO','ENCERRADO']
        
        wx.StaticText(self.panel, wx.ID_ANY, "Status", (350, 25))
        self.radioStatus = wx.ComboBox(self.panel, wx.ID_ANY, pos = (400,25), choices = self.radioOpcoes, style=wx.CB_READONLY)
        
        wx.StaticText(self.panel, wx.ID_ANY, "Processo", (25, 75))
        self.processo = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 75),size=(125, -1))

       
        wx.StaticText(self.panel, wx.ID_ANY, "Data de Vencimento:", (350, 75))
        self.calendarioVencimento = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (400, 100), style=wx.adv.DP_DROPDOWN)
        
                
        wx.StaticText(self.panel, wx.ID_ANY, "Objeto", (25, 125))
        self.objeto = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 125),size=(200, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Empresa", (25, 175))
        self.empresa = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 175),size=(200, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Data da assinatura:", (25, 225))
        self.calendarioAssinatura = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (25, 250), style=wx.adv.DP_DROPDOWN)

        wx.StaticText(self.panel, wx.ID_ANY, "Data de termino:", (150, 225))
        self.calendarioTermino = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (150, 250), style=wx.adv.DP_DROPDOWN)

        self.buttonCriar = wx.Button(self.panel, wx.ID_ANY, 'Criar', (400, 250),size=(100,-1))

        self.buttonCriar.Bind(wx.EVT_BUTTON, self.criarNovoContrato)


        self.frame.Show()
        self.frame.Centre()

    def criarNovoContrato(self,event):
                
        contrato = self.contrato.GetValue()
        status = self.radioStatus.GetValue()
        processo = self.processo.GetValue()
        objeto = self.objeto.GetValue()
        vencimento = self.calendarioVencimento.GetValue().FormatISODate()
        empresa = self.empresa.GetValue()
        dataDeAssinatura = self.calendarioAssinatura.GetValue().FormatISODate()
        dataDeTermino = self.calendarioTermino.GetValue().FormatISODate()

        if contrato !='' and status !='' and processo !='' and objeto !='' and empresa != '':
            tuplaDeDados = (contrato,processo,objeto,empresa,dataDeAssinatura,dataDeTermino,vencimento,status)
            objetoContrato = modelNovoContrato.contrato(listaDedadosContrato=tuplaDeDados) 
            objetoContrato.criarNovoContrato()
            dlg_box_p = wx.MessageDialog(None , "Contrato criado com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
            dlg_box_p.ShowModal()  
            self.frame.Destroy()
            

        else:
            dlg_box_p = wx.MessageDialog(None , "Desculpe verifique os campo provelmente algum esta vazio","Erro...", wx.OK| wx.ICON_WARNING)
            dlg_box_p.ShowModal()  
        

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()