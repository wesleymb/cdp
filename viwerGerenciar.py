import wx
import wx.adv
import geCDP
import modelServidor
import modelContrato
import modelFiscal
import modelNovoFiscal
import viwerGerenciarVencimentos
import geRelatorioContrato
import viwerGerenciarAditivo


LISTA_DE_FRAMES= []
def contador_de_frames(frame):
    LISTA_DE_FRAMES.append(frame)



def main():
    viwerGerenciar(idContrato=1)

class viwerGerenciar(object):
    """docstring for viwerGerenciar"""
    def __init__(self,idContrato):
        super(viwerGerenciar, self).__init__()
        self.idContrato = idContrato

        self.frame = wx.Frame(None, -1, 'Contrato', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,1100,550)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)
        
        
        self.frame.Bind(wx.EVT_CLOSE, self.fechar_todos_os_frames)
        self.statusbar.SetStatusText("ID contrato: {id}".format(id=self.idContrato))
        contador_de_frames(frame=self.frame)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)

        self.menu_arquivo = wx.Menu()
        self.abaGerenciarVencimentos = self.menu_arquivo.Append(wx.ID_ANY, "Gerenciar vencimentos", "Gerenciar vencimentos")
        self.abaGerarAditivos = self.menu_arquivo.Append(wx.ID_ANY, "Gerenciar aditivos", "Gerenciar aditivos")
        self.abaGerarRelatorico = self.menu_arquivo.Append(wx.ID_ANY, "Gerar relatório", "Gerar relatório")
        self.abaGerarOrdemDeServico = self.menu_arquivo.Append(wx.ID_ANY, "Gerar ordem de serviço", "Gerar ordem de serviço")

        self.menu_bar = wx.MenuBar()
        self.menu_bar.Append(self.menu_arquivo,"Arquivo")
        self.frame.SetMenuBar(self.menu_bar)
        
        wx.StaticBox(self.panel, wx.ID_ANY, 'Dados do Contrato', (15, 5), size=(500, 460))

        wx.StaticBox(self.panel, wx.ID_ANY, 'Gestores e Fiscais', (525, 5), size=(525, 350))

        wx.StaticText(self.panel, wx.ID_ANY, "Contrato", (25, 25))
        self.contrato = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 25),size=(50, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Processo", (25, 75))
        self.processo = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 75),size=(125, -1))


        wx.StaticText(self.panel, wx.ID_ANY, "Data de Vencimento:", (350, 75))
        self.calendarioVencimento = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (400, 100), style=wx.adv.DP_DROPDOWN)
        
        self.comboOpcoes = ['ATIVO','ENCERRADO']

        wx.StaticText(self.panel, wx.ID_ANY, "Status", (350, 25))
        self.comboStatus = wx.ComboBox(self.panel, wx.ID_ANY, pos = (400,25), choices = self.comboOpcoes, style=wx.CB_READONLY)
        
        wx.StaticText(self.panel, wx.ID_ANY, "Objeto", (25, 125))
        self.objeto = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 125),size=(200, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Empresa", (25, 175))
        self.empresa = wx.TextCtrl(self.panel, wx.ID_ANY,"", (100, 175),size=(200, -1))

        wx.StaticText(self.panel, wx.ID_ANY, "Data da assinatura:", (25, 225))
        self.calendarioAssinatura = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (25, 250), style=wx.adv.DP_DROPDOWN)

        wx.StaticText(self.panel, wx.ID_ANY, "Data de termino:", (150, 225))
        self.calendarioTermino = wx.adv.DatePickerCtrl(self.panel, wx.ID_ANY, pos= (150, 250), style=wx.adv.DP_DROPDOWN)

        wx.StaticText(self.panel, wx.ID_ANY, "Observação", (25, 300))
        self.observacao = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 325),size=(350, 125),style=wx.TE_MULTILINE)

        self.listaDeServidores = self.geraListaServidores()
        

        wx.StaticText(self.panel, wx.ID_ANY, "Gestor", (550, 20))
        self.comboGestor = wx.ComboBox(self.panel, wx.ID_ANY, pos = (550,45), choices =  self.listaDeServidores, style=wx.CB_READONLY,size=(250,-1))
        
        wx.StaticText(self.panel, wx.ID_ANY, "Fiscais", (550, 75))
        
        
        self.comboFiscais = wx.ComboBox(self.panel, wx.ID_ANY, pos = (550,105), choices =  self.listaDeServidores, style=wx.CB_READONLY,size=(250,-1))
        
        self.listaDeFiscais =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(475,150), pos=(550,170))
        self.listaDeFiscais.InsertColumn(0,"ID",width=50)
        self.listaDeFiscais.InsertColumn(1,"Nome",width=425)
        
        self.buttonIncluir = wx.Button(self.panel, wx.ID_ANY, 'Incluir', (825, 130),size=(100,-1))
        self.buttonIncluir .Bind(wx.EVT_BUTTON, self.incluirFiscal)

        self.buttonExcluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (925, 130),size=(100,-1))
        self.buttonExcluir.Bind(wx.EVT_BUTTON, self.apagarFiscal)

        self.buttonSalvar = wx.Button(self.panel, wx.ID_ANY, 'Salvar', (825, 400),size=(100,-1))
        self.buttonSalvar.Bind(wx.EVT_BUTTON, self.salvar)
        
        self.buttonFechar = wx.Button(self.panel, wx.ID_ANY, 'Fechar', (925, 400),size=(100,-1))
        self.buttonFechar.Bind(wx.EVT_BUTTON, self.fechar)
        
        self.frame.Bind(wx.EVT_MENU, self.abrirviwerGerenciarVencimentos , self.abaGerenciarVencimentos)
        self.frame.Bind(wx.EVT_MENU, self.gerarRelatorioDeContrato , self.abaGerarRelatorico)
        self.frame.Bind(wx.EVT_MENU, self.abrirviwerGerenciarAditivo , self.abaGerarAditivos)
        
        self.queryDeCarregamentoDeDadosContrato()
        self.queryDeCarregamentoDeDadosFiscais()

        self.frame.Show()
        self.frame.Centre()

    
    def abrirviwerGerenciarAditivo(self,event):
        telaGerenciarAditivo = viwerGerenciarAditivo.gerenciarAditivos(idContrato=self.idContrato)
        print(telaGerenciarAditivo.frame)
        contador_de_frames(telaGerenciarAditivo.frame)
    
    def gerarRelatorioDeContrato(self,event):
        dlgGerarRelatorio = wx.MessageDialog(None , "Deseja gerar relatório do contrato?", "Gerar relatório",wx.YES_NO | wx.ICON_INFORMATION)
        result = dlgGerarRelatorio.ShowModal()
        if result == wx.ID_YES:
            geRelatorioContrato.gerarRelatorio(idContrato=self.idContrato)
            dlgRelatorio = wx.MessageDialog(None , "Relatório gerado com sucesso","Pronto.", wx.OK| wx.ICON_INFORMATION)
            dlgRelatorio.ShowModal()  
             
    
    def abrirviwerGerenciarVencimentos(self,event):
        telaGerenciarVencimentos = viwerGerenciarVencimentos.gerenciarVencimentos(idContrato=self.idContrato)
        print(telaGerenciarVencimentos.frame)
        contador_de_frames(telaGerenciarVencimentos.frame)
        
    
    
    def salvar(self,event):
        contrato = self.contrato.GetValue()
        processo = self.processo.GetValue()
        objeto = self.objeto.GetValue()
        empresa = self.empresa.GetValue()
        assinatura = self.calendarioAssinatura.GetValue().FormatISODate()
        termino = self.calendarioTermino.GetValue().FormatISODate()
        vencimento = self.calendarioVencimento.GetValue().FormatISODate()
        gestor = self.comboGestor.GetValue()
        observacao = self.observacao.GetValue()
        status = self.comboStatus.GetValue()

        idServidor = ''
        
        for Servidor in geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna="NOME",dado=gestor):
            objServidor = modelServidor.servidor(Servidor)
            idServidor = objServidor.id
        
        
        tuplaDeDados = (self.idContrato,contrato,processo,objeto,empresa,assinatura,termino,vencimento,idServidor,status,observacao)

        objContrato = modelContrato.contrato(tuplaDeDados)
        objContrato.altulizarContrato()


        dlg_box_p = wx.MessageDialog(None , "Dados atulizados com sucesso.","Pronto", wx.OK| wx.ICON_INFORMATION)
        dlg_box_p.ShowModal()
        self.frame.Destroy()   

    def fechar(self,event):
        self.frame.Destroy()
    
    def geraListaServidores(self):
        listaServidores = []
        queryServidores = geCDP.queryTabela(tabela="SERVIDOR")
        for servidor in queryServidores:
            objServidor = modelServidor.servidor(servidor)
            listaServidores.append(objServidor.nome)
        return sorted(listaServidores)

    def incluirFiscal(self,event):
        gestor = self.comboGestor.GetValue()
        fiscal = self.comboFiscais.GetValue()
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
                
                for Servidor in geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna="NOME",dado=fiscal):
                    objServidor = modelServidor.servidor(Servidor)
                    objFiscal = modelNovoFiscal.fiscal((self.idContrato,objServidor.id))
                    objFiscal.insertNaTabela()
                
                self.queryDeCarregamentoDeDadosFiscais()

                    
        else:
            dlg_box_p = wx.MessageDialog(None , "O servidor {servidor} já é um fiscal".format(servidor=fiscal),"Ops..", wx.OK| wx.ICON_WARNING)
            dlg_box_p.ShowModal()
    
    def apagarFiscal(self,event):
        item = self.listaDeFiscais.GetFocusedItem()
        idFiscal = self.listaDeFiscais.GetItem(itemIdx=item, col=0).GetText()
        objFiscal = modelNovoFiscal.fiscal((self.idContrato,idFiscal))
        objFiscal.excluirFiscal()
        self.queryDeCarregamentoDeDadosFiscais()

    def queryDeCarregamentoDeDadosContrato(self):
       
        for Contrato in geCDP.queryTabelaComWhere(tabela="CONTRATO",coluna="id",dado=self.idContrato):
            queryContrato = modelContrato.contrato(Contrato)
            self.contrato.SetValue(queryContrato.contrato)
            self.processo.SetValue( queryContrato.numeroDeProcesso)
            self.objeto.SetValue(queryContrato.objeto)
            self.empresa.SetValue(queryContrato.empresa)
            self.comboStatus.SetValue(queryContrato.status)
            self.calendarioAssinatura.SetValue(queryContrato.dataAssinaturaTipoDate)
            self.calendarioTermino.SetValue(queryContrato.dataTerminoTipoDate)
            self.calendarioVencimento.SetValue(queryContrato.vencimentoTipoDate)
            self.comboGestor.SetValue(queryContrato.gestor)
            self.observacao.SetValue(queryContrato.observacao)
    
    def queryDeCarregamentoDeDadosFiscais(self):
        self.listaDeFiscais.DeleteAllItems()
        self.index = 0
        for Fiscal in geCDP.queryTabelaComWhere(tabela="FISCAL",coluna="idContrato",dado=self.idContrato):
            queryFiscal = modelFiscal.fiscal(Fiscal)
            self.listaDeFiscais.InsertStringItem(self.index, str(queryFiscal.idServidor))
            self.listaDeFiscais.SetStringItem(self.index, 1, queryFiscal.nomeFiscal)
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