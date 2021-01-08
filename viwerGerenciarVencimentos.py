import wx
import wx.adv
import geCDP
import modelPagamento
import modelContrato
import datetime


def main():
    gerenciarVencimentos(idContrato=1)

class gerenciarVencimentos(object):
    """docstring for viwerGerenciar"""
    def __init__(self,idContrato):
        super(gerenciarVencimentos, self).__init__()
        self.idContrato = idContrato

        self.frame = wx.Frame(None, -1, 'Gerenciar de Vencimentos', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,575,450)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.statusbar.SetStatusText("ID contrato: {id}".format(id=self.idContrato))

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

        self.buttonIncluir = wx.Button(self.panel, wx.ID_ANY, 'Incluir', (425, 50),size=(100,-1))
        self.buttonExcluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (425, 75),size=(100,-1))
        self.buttonAlterar = wx.Button(self.panel, wx.ID_ANY, 'Alterar', (425, 100),size=(100,-1))
        
        self.listaDeVencimentos.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.carregarCampos)
        
        self.buttonAlterar.Bind(wx.EVT_BUTTON, self.alterar)
        self.buttonIncluir.Bind(wx.EVT_BUTTON, self.incluir)
        self.buttonExcluir.Bind(wx.EVT_BUTTON, self.excluir)

        
        self.carregarDoBanco()

        self.frame.Show()
        self.frame.Centre()

    
    def carregarCampos(self,event):
        item = self.listaDeVencimentos.GetFocusedItem()
        if item != -1:
        

            self.idPagamentoParaUpdate = self.listaDeVencimentos.GetItem(itemIdx=item, col=0).GetText()
            for queryVencimento in geCDP.queryTabelaComWhere(tabela="PAGAMENTO",coluna="ID",dado=self.idPagamentoParaUpdate):
                Pagamento = modelPagamento.pagamento(queryVencimento)
                self.valor.SetValue(Pagamento.valor)
                self.calendarioVencimento.SetValue(Pagamento.dataDePagamentoTipoDate)
                self.numeroDeprocesso.SetValue(Pagamento.numeroDeProcesso)
                self.comboStatus.SetValue(Pagamento.status)
                
                self.statusbar.SetStatusText("ID pagamento: {id}".format(id=self.idPagamentoParaUpdate))
                

    
    
    def alterar(self,event):
        item = self.listaDeVencimentos.GetFocusedItem()
        if item != -1:
            
            dataDePagamento = self.calendarioVencimento.GetValue().FormatISODate()
            valor = self.valor.GetValue()
            status = self.comboStatus.GetValue()
            numeroDeProcesso = self.numeroDeprocesso.GetValue()

            

            Pagamento = modelPagamento.pagamento((self.idPagamentoParaUpdate,self.idContrato,dataDePagamento,valor,status,numeroDeProcesso))
            Pagamento.atulizarPagamento()

            dataDePagamento = self.calendarioVencimento.SetValue(datetime.date.today())
            valor = self.valor.SetValue(0)
            status = self.comboStatus.SetValue('')
            numeroDeProcesso = self.numeroDeprocesso.SetValue('')

            self.idPagamentoParaUpdate = ''

            self.statusbar.SetStatusText("ID contrato: {id}".format(id=self.idContrato))

            self.carregarDoBanco()
            
            dlgAtulizacao = wx.MessageDialog(None , "Pagamento atulizado com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
            dlgAtulizacao.ShowModal()  

                    
    
    def incluir(self,event):
        dataDePagamento = self.calendarioVencimento.GetValue().FormatISODate()
        valor = self.valor.GetValue()
        status = self.comboStatus.GetValue()
        numeroDeProcesso = self.numeroDeprocesso.GetValue()

        Pagamento = modelPagamento.pagamento((self.idContrato,dataDePagamento,valor,status,numeroDeProcesso),tipo=2)
        Pagamento.inserirNovoPagamentoManual()
        
        dataDePagamento = self.calendarioVencimento.SetValue(datetime.date.today())
        valor = self.valor.SetValue(0)
        status = self.comboStatus.SetValue('')
        numeroDeProcesso = self.numeroDeprocesso.SetValue('')
        
        dlgAtulizacao = wx.MessageDialog(None , "Pagamento incluido com sucesso","Pronto", wx.OK| wx.ICON_INFORMATION)
        dlgAtulizacao.ShowModal()  
        
        self.statusbar.SetStatusText("ID contrato: {id}".format(id=self.idContrato))
        self.carregarDoBanco()

    def excluir(self,event):

        dlgApagarPagamento = wx.MessageDialog(None , "Tem certeza que quer excluir esse pagamento?", "Alerta",wx.YES_NO | wx.ICON_WARNING)
        result = dlgApagarPagamento.ShowModal()
        if result == wx.ID_YES: 

            item = self.listaDeVencimentos.GetFocusedItem()
            if item != -1:
            
                idPagamento = self.listaDeVencimentos.GetItem(itemIdx=item, col=0).GetText()

                for queryVencimento in geCDP.queryTabelaComWhere(tabela="PAGAMENTO",coluna="ID",dado=idPagamento):
                    Pagamento = modelPagamento.pagamento(queryVencimento)
                    Pagamento.excluirPagamento() 

                self.carregarDoBanco()
                self.statusbar.SetStatusText("ID contrato: {id}".format(id=self.idContrato))
    
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
            
            dlgParcelas = wx.TextEntryDialog(self.panel,"Quandos meses terá esse contrato?", "Parcelas de pagamento", style=wx.OK|wx.CANCEL)
            resultado = dlgParcelas.ShowModal()
            
            if resultado == wx.ID_OK:
               parcelas = int(dlgParcelas.GetValue())

            
            count = 0
            dlg_carregar = wx.ProgressDialog("Processando", "Criando vencimentos", maximum=parcelas, parent=self.frame ,style= wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
            for queryContrato in dados:
                Contrato = modelContrato.contrato(queryContrato)
                vencimentos = Contrato.gerarVencimentos(total=parcelas)
                for vencimento in vencimentos:
                    Pagamento = modelPagamento.pagamento((self.idContrato,vencimento),tipo=3)
                    Pagamento.inserirNovoPagamentoAutomatico()
                    if count < parcelas: 
                        dlg_carregar.Update(count+1)
            
            
            
            dlg_carregar.Destroy()
            self.carregarDoBanco()

        

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()