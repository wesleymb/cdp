import wx
import wx.adv
import geCDP
import modelServidor



def main():
    viwerContrato(statusEntrada='Novo')

class viwerContrato(object):
    """docstring for viwerContrato"""
    def __init__(self,statusEntrada):
        super(viwerContrato, self).__init__()
        self.statusEntrada = statusEntrada

        self.frame = wx.Frame(None, -1, 'Contrato', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,550,700)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)
        self.statusbar.SetStatusText(self.statusEntrada)

        wx.StaticBox(self.panel, wx.ID_ANY, 'Dados do Contrato', (15, 5), size=(500, 600))

        wx.StaticText(self.panel, wx.ID_ANY, "Contrato", (25, 25))
        self.contrato = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 25),size=(50, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Processo", (25, 75))
        self.processo = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 75),size=(125, -1))

        self.radioOpcoes = ['ATIVO','ENCERRADO']

        wx.StaticText(self.panel, wx.ID_ANY, "Data de Vencimento:", (350, 75))
        self.calendarioVencimento = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (400, 100), style=wx.adv.DP_DROPDOWN)
        
        wx.StaticText(self.panel, wx.ID_ANY, "Status", (350, 25))
        self.radioStatus = wx.ComboBox(self.panel, wx.ID_ANY, pos = (400,25), choices = self.radioOpcoes, style=wx.CB_READONLY)
        
        wx.StaticText(self.panel, wx.ID_ANY, "Objeto", (25, 125))
        self.objeto = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 125),size=(200, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Empresa", (25, 175))
        self.empresa = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 175),size=(200, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Data da assinatura:", (25, 225))
        self.calendarioAssinatura = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (25, 250), style=wx.adv.DP_DROPDOWN)

        wx.StaticText(self.panel, wx.ID_ANY, "Data de termino:", (150, 225))
        self.calendarioTermino = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (150, 250), style=wx.adv.DP_DROPDOWN)

        self.listaDeServidores = self.geraListaServidores()
        

        wx.StaticText(self.panel, wx.ID_ANY, "Gestor", (25, 300))
        self.radioGestor = wx.ComboBox(self.panel, wx.ID_ANY, pos = (25,325), choices =  self.listaDeServidores, style=wx.CB_READONLY,size=(250,-1))
        
        wx.StaticText(self.panel, wx.ID_ANY, "Fiscais", (25, 375))
        
        
        self.radioFiscais = wx.ComboBox(self.panel, wx.ID_ANY, pos = (25,400), choices =  self.listaDeServidores, style=wx.CB_READONLY,size=(250,-1))
        
        self.listaDeFiscais =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(475,150), pos=(25,450))
        self.listaDeFiscais.InsertColumn(0,"ID",width=50)
        self.listaDeFiscais.InsertColumn(1,"Nome",width=425)
        
        self.buttonIncluir = wx.Button(self.panel, wx.ID_ANY, 'Incluir', (300, 400),size=(100,-1))
        self.buttonIncluir .Bind(wx.EVT_BUTTON, self.incluirFiscal)

        self.buttonExcluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (400, 400),size=(100,-1))
        self.buttonExcluir.Bind(wx.EVT_BUTTON, self.apagarFiscal)

        self.frame.Show()
        self.frame.Centre()

    def geraListaServidores(self):
        listaServidores = geCDP.queryNomeServidores()
        return listaServidores

    def incluirFiscal(self,event):
        gestor = self.radioGestor.GetValue()
        fiscal = self.radioFiscais.GetValue()
        listDeNomes = []
        numeroDeLinhas = self.listaDeFiscais.GetItemCount()
        if numeroDeLinhas != 0:
            for linha in range(numeroDeLinhas):
                nome = self.listaDeFiscais.GetItem(itemIdx=linha, col=1)
                listDeNomes.append(nome.GetText())
        if fiscal not in listDeNomes:
            pass
            if gestor == '':
                dlg_box_p = wx.MessageDialog(None , "Primiro temos que ter um gestor antes dos fiscais","Ops..", wx.OK| wx.ICON_WARNING)
                dlg_box_p.ShowModal()            
            elif gestor == fiscal:
                dlg_box_p = wx.MessageDialog(None , "O gestor não pode ser o fiscal ao mesmo tempo","Ops..", wx.OK| wx.ICON_WARNING)
                dlg_box_p.ShowModal()  
            else:
                queryServidor = modelServidor.servidor(geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna="NOME",dado=fiscal))
                id = str(queryServidor.id)
                nome = queryServidor.nome
                self.listaDeFiscais.InsertStringItem(self.index, id)
                self.listaDeFiscais.SetStringItem(self.index, 1, nome)
                self.index += 1
        else:
            dlg_box_p = wx.MessageDialog(None , "O servidor {servidor} já é um fiscal".format(servidor=fiscal),"Ops..", wx.OK| wx.ICON_WARNING)
            dlg_box_p.ShowModal()
    
    def apagarFiscal(self,event):
        item = self.listaDeFiscais.GetFocusedItem()
        self.listaDeFiscais.DeleteItem(item)
        self.index -= 1


if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()