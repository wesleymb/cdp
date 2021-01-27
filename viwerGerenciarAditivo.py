import wx
import wx.adv
import geCDP
import modelAditivo
import datetime



def main():
    gerenciarAditivos(idContrato=1)

class gerenciarAditivos(object):
    """docstring for viwerGerenciar"""
    def __init__(self,idContrato):
        super(gerenciarAditivos, self).__init__()
        self.idContrato = idContrato

        self.frame = wx.Frame(None, -1, 'Gerenciar de Aditivos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,575,450)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        self.statusbar.SetStatusText("ID contrato: {id}".format(id=self.idContrato))

        wx.StaticText(self.panel, wx.ID_ANY, "Valor", (25, 25))
        # self.valor = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 50),size=(200, -1))

        self.valor = wx.SpinCtrlDouble(self.panel, wx.ID_ANY,pos=(25, 50),inc=000000.01,max=10000000000)        

        wx.StaticText(self.panel, wx.ID_ANY, "Data de assinatura:", (200, 25))
        self.calendarioAssinatura = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (200, 50), style=wx.adv.DP_DROPDOWN)

        wx.StaticText(self.panel, wx.ID_ANY, "Data de termino:", (200, 105))
        self.calendarioTermino = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (200, 125), style=wx.adv.DP_DROPDOWN)

        
        self.comboOpcoes = ['ATIVO','ENCERRADO','TRAMITANDO']

        wx.StaticText(self.panel, wx.ID_ANY, "Status", (25, 100))
        self.comboStatus = wx.ComboBox(self.panel, wx.ID_ANY, pos = (25,125), choices = self.comboOpcoes, style=wx.CB_READONLY)
        
        self.listaDeAditivos =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(500,220), pos=(25,160))
        self.listaDeAditivos.InsertColumn(0,"ID",width=50)
        self.listaDeAditivos.InsertColumn(1,"Data de assinatura",width=100)
        self.listaDeAditivos.InsertColumn(2,"Data de termino",width=100)
        self.listaDeAditivos.InsertColumn(3,"Valor",width=150)
        self.listaDeAditivos.InsertColumn(4,"Status",width=100)

        self.buttonIncluir = wx.Button(self.panel, wx.ID_ANY, 'Incluir', (425, 50),size=(100,-1))
        self.buttonExcluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (425, 75),size=(100,-1))
        self.buttonAlterar = wx.Button(self.panel, wx.ID_ANY, 'Alterar', (425, 100),size=(100,-1))
        
        self.listaDeAditivos.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.carregarCampos)
        
        self.buttonAlterar.Bind(wx.EVT_BUTTON, self.alterar)
        self.buttonIncluir.Bind(wx.EVT_BUTTON, self.incluir)
        self.buttonExcluir.Bind(wx.EVT_BUTTON, self.excluir)

        
        self.carregarDoBanco()

        self.frame.Show()
        self.frame.Centre()

    def alterar (self,event):
        idAditivo = self.idAditivo
        idContrato = self.idContrato
        valor = self.valor.GetValue()
        status = self.comboStatus.GetValue()
        assinatura = self.calendarioAssinatura.GetValue().FormatISODate()
        termino = self.calendarioTermino.GetValue().FormatISODate()
        tuplaDeDados = (idAditivo,idContrato,valor,assinatura,termino,status)
        Aditivo = modelAditivo.aditivo(tuplaDeDados)
        Aditivo.ataulizarAditivo()

        
        self.valor.SetValue(0)
        self.comboStatus.SetValue('')
        self.calendarioAssinatura.SetValue(datetime.date.today())
        self.calendarioTermino.SetValue(datetime.date.today())

        self.idAditivo = ''

        self.statusbar.SetStatusText("ID contrato: {id}".format(id=self.idContrato))

        self.carregarDoBanco()
        
        dlgAtulizacao = wx.MessageDialog(None , "Aditivo atulizado com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
        dlgAtulizacao.ShowModal()  



    def carregarCampos(self,event):
        item = self.listaDeAditivos.GetFocusedItem()
        
        if item != -1:
            self.idAditivo = self.listaDeAditivos.GetItem(itemIdx=item, col=0).GetText()

            for queryAditivo in geCDP.queryTabelaComWhere(tabela="ADITIVO",coluna="ID",dado=self.idAditivo):
                Aditivo = modelAditivo.aditivo(queryAditivo)
                self.valor.SetValue(Aditivo.valor)
                self.comboStatus.SetValue(Aditivo.status)
                self.calendarioAssinatura.SetValue(Aditivo.dataAssinaturaTipoDate)
                self.calendarioTermino.SetValue(Aditivo.dataTerminoTipoDate)

                self.statusbar.SetStatusText("ID aditivo: {id}".format(id=self.idAditivo))

    def carregarDoBanco(self):
        self.index = 0
        self.listaDeAditivos.DeleteAllItems()

        for queryAditivo in geCDP.queryTabelaComWhere(tabela="ADITIVO", coluna="idContrato", dado=self.idContrato):
            Aditivo = modelAditivo.aditivo(listaDedadosContrato=queryAditivo)
            self.listaDeAditivos.InsertStringItem(self.index, str(Aditivo.id))
            self.listaDeAditivos.SetStringItem(self.index, 1, Aditivo.dataAssinatura)
            self.listaDeAditivos.SetStringItem(self.index, 2, Aditivo.dataTermino)
            self.listaDeAditivos.SetStringItem(self.index, 3, str(Aditivo.valor))
            self.listaDeAditivos.SetStringItem(self.index, 4, Aditivo.status)
            self.index += 1
    
    def incluir(self,event):

        dataDeAssinatura = self.calendarioAssinatura.GetValue().FormatISODate()
        dataDeTermino = self.calendarioTermino.GetValue().FormatISODate()
        valor = self.valor.GetValue()
        status = self.comboStatus.GetValue()

        tuplaDeDados = (self.idContrato,valor,dataDeAssinatura,dataDeTermino,status)
        Aditivo = modelAditivo.aditivo(listaDedadosContrato=tuplaDeDados,tipo=2)
        Aditivo.inserNovoAditivo()
        
        self.calendarioAssinatura.SetValue(datetime.date.today())
        self.calendarioTermino.SetValue(datetime.date.today())
        self.valor.SetValue(0)
                     
        self.carregarDoBanco()
        
        dlgAtulizacao = wx.MessageDialog(None , "Aditivo incluido com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
        dlgAtulizacao.ShowModal() 
        
    def excluir(self,event):

        dlgApagarAditivo = wx.MessageDialog(None , "Tem certeza que quer excluir esse Aditivo?", "Alerta",wx.YES_NO | wx.ICON_WARNING)
        result = dlgApagarAditivo.ShowModal()
        
        if result == wx.ID_YES: 

            item = self.listaDeAditivos.GetFocusedItem()
            if item != -1:
                
                idAditivo = self.listaDeAditivos.GetItem(itemIdx=item, col=0).GetText()

                for queryAditivo in geCDP.queryTabelaComWhere(tabela="ADITIVO",coluna="ID",dado=idAditivo):
                    Aditivo = modelAditivo.aditivo(queryAditivo)
                    Aditivo.excluirAditivo()
                
                self.carregarDoBanco()
                dlgExclusao = wx.MessageDialog(None , "Aditivo excluido com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
                dlgExclusao.ShowModal() 



if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()