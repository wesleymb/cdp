import wx
import modelServidor
import geCDP
import modelNovoServidor
import modelFiscal
import modelContrato

def main():
    gerenciarServidores()

class gerenciarServidores(object):
    """docstring for gerenciarServidores"""
    def __init__(self):
        super(gerenciarServidores, self).__init__()
        
        self.frame = wx.Frame(None, -1, 'Gerenciar servidores', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,550,450)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)

        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)
        
        wx.StaticText(self.panel, wx.ID_ANY, "Nome:", (25, 25))
        self.txtNome = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 50),size=(350, -1))
        
        wx.StaticText(self.panel, wx.ID_ANY, "ID funcional:", (25, 75))
        self.txtIdFuncional = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 100),size=(100, -1))

        self.buttonIncluir = wx.Button(self.panel, wx.ID_ANY, 'Incluir', (400, 50),size=(100,-1))


        wx.StaticText(self.panel, wx.ID_ANY, "Filtra", (25, 150))
        self.txtFiltro = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 175),size=(350, -1),style=wx.TE_PROCESS_ENTER)

        self.txtFiltro.Bind(wx.EVT_TEXT_ENTER, self.filtarServidor)

        self.buttonFiltar = wx.Button(self.panel, wx.ID_ANY, 'Filtar', (400, 175),size=(100,-1))
        
        
        # self.buttonAlterar = wx.Button(self.panel, wx.ID_ANY, 'Salvar', (525, 50),size=(100,-1))
        self.buttonAlterar = wx.Button(self.panel, wx.ID_ANY, 'Alterar', (400, 75),size=(100,-1))
        self.buttonExcluir = wx.Button(self.panel, wx.ID_ANY, 'Excluir', (400, 100),size=(100,-1))
        
        self.listaDeServidores =  wx.ListCtrl(self.panel,style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_AUTOARRANGE,size=(475,150), pos=(25,210))
        self.listaDeServidores.InsertColumn(0,"ID",width=50)
        self.listaDeServidores.InsertColumn(1,"Nome",width=300)
        self.listaDeServidores.InsertColumn(2,"ID funcional",width=125)

        self.buttonIncluir.Bind(wx.EVT_BUTTON, self.criarNovoServidor)
        self.buttonExcluir.Bind(wx.EVT_BUTTON, self.excluirServidor)
        self.buttonFiltar.Bind(wx.EVT_BUTTON, self.filtarServidor)
        self.buttonAlterar.Bind(wx.EVT_BUTTON, self.atulizarServidor)

        self.listaDeServidores.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.carregarParaAtulizarServidor)


        self.carregaDadosServidores()

        self.frame.Show()
        self.frame.Centre()
    
    
    
    def carregarParaAtulizarServidor(self,event):
        item = self.listaDeServidores.GetFocusedItem()
        if item != -1:
            idServidor = self.listaDeServidores.GetItem(itemIdx=item, col=0).GetText()
            for Servidor in geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna="id",dado=idServidor):
                objServidor = modelServidor.servidor(Servidor)
                self.txtNome.SetValue(objServidor.nome)
                self.txtIdFuncional.SetValue(objServidor.idFuncional)
    
    def atulizarServidor(self,event):
        item = self.listaDeServidores.GetFocusedItem()
        if item != -1:
            idServidor = self.listaDeServidores.GetItem(itemIdx=item, col=0).GetText()
            nome = self.txtNome.GetValue()
            idFuncional = self.txtIdFuncional.GetValue()
            
            if nome != '' and idFuncional != '':

                objServidor = modelServidor.servidor((idServidor,nome,idFuncional))
                objServidor.atulizarNaTabela()
                self.carregaDadosServidores()

                self.txtNome.SetValue('')
                self.txtIdFuncional.SetValue('')

                dlgServidorAtulizado = wx.MessageDialog(None , "Servidor atulizado com sucesso.","Pronto", wx.OK| wx.ICON_INFORMATION)
                dlgServidorAtulizado.ShowModal() 
            else:
                dlgServidorAtulizarErro = wx.MessageDialog(None , "Provavelmente o nome ou id funcinal estão em branco.","Pronto", wx.OK| wx.ICON_INFORMATION)
                dlgServidorAtulizarErro.ShowModal()  

    
    def filtarServidor(self,event):
        self.listaDeServidores.DeleteAllItems()
        self.index = 0
        
        texto = self.txtFiltro.GetValue()

        for Servidor in  geCDP.queryTabelaComWhereLike(tabela="SERVIDOR",coluna="NOME",dado=texto):
            objServidor = modelServidor.servidor(Servidor)
            self.listaDeServidores.InsertStringItem(self.index, str(objServidor.id))
            self.listaDeServidores.SetStringItem(self.index, 1, objServidor.nome)
            self.listaDeServidores.SetStringItem(self.index, 2, objServidor.idFuncional)
            self.index += 1

        self.txtFiltro.SetValue('')

    
    def verificarVinclulos(self,idServidor):
        listaServidoresFiscal = []
        listaServidoresGestor = []

        for ServidoresFiscal in geCDP.queryTabelaComWhere(tabela="FISCAL",coluna="idServidor",dado=idServidor):
            objFiscal = modelFiscal.fiscal(ServidoresFiscal)
            listaServidoresFiscal.append(objFiscal.numeroContrato)

        for GestorContrato in geCDP.queryTabelaComWhere(tabela="CONTRATO",coluna="idServidorGestor",dado=idServidor):
            objGestor = modelContrato.contrato(GestorContrato)
            listaServidoresGestor.append(objGestor.numeroDeProcesso)

        return listaServidoresFiscal,listaServidoresGestor
        

    def excluirServidor(self,event):
        item = self.listaDeServidores.GetFocusedItem()
        if item != -1:
            idServidor = self.listaDeServidores.GetItem(itemIdx=item, col=0).GetText()
            listaServidoresFiscal,listaServidoresGestor = self.verificarVinclulos(idServidor=idServidor)

            if listaServidoresFiscal == [] and listaServidoresGestor == []:
                for Servidor in geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna='id',dado=idServidor):
                    objServidor = modelServidor.servidor(Servidor)
                    objServidor.excluirServidorNaTabela()
                    self.carregaDadosServidores()
                    dlgServidorExcluido = wx.MessageDialog(None , "Servidor excluido com sucesso.","Pronto", wx.OK| wx.ICON_INFORMATION)
                    dlgServidorExcluido.ShowModal() 

            
            else:
                dlgServidorExcluir = wx.MessageDialog(None , "O servidor esta como fiscal: {listaServidoresFiscal}\n O servidor esta como gestor: {listaServidoresGestor}\n"
                .format(listaServidoresFiscal=", ".join(listaServidoresFiscal),listaServidoresGestor=", ".join(listaServidoresGestor)),"Erro", wx.OK| wx.ICON_INFORMATION)
                
                dlgServidorExcluir.ShowModal()

         
    
    def criarNovoServidor(self,event):
        nome = self.txtNome.GetValue()
        idFuncional = self.txtIdFuncional.GetValue()
        
        if nome != '' and idFuncional != '':
            objServidor = modelNovoServidor.servidor((nome,idFuncional))
            objServidor.inserirNovoServidorNaTabela()
            self.txtNome.SetValue('')
            self.txtIdFuncional.SetValue('')
            self.carregaDadosServidores()
            dlgServidorNovo = wx.MessageDialog(None , "Servidor criado com sucesso!","Pronto", wx.OK| wx.ICON_INFORMATION)
            dlgServidorNovo.ShowModal()  
        else:
            dlgServidorNovoErro = wx.MessageDialog(None , "Provavelmente o nome ou id funcinal estão em branco.","Pronto", wx.OK| wx.ICON_INFORMATION)
            dlgServidorNovoErro.ShowModal()  



    def carregaDadosServidores(self):
        self.listaDeServidores.DeleteAllItems()
        self.index = 0

        for Servidor in geCDP.queryTabela(tabela="SERVIDOR"):
            objServidor = modelServidor.servidor(Servidor)
            self.listaDeServidores.InsertStringItem(self.index, str(objServidor.id))
            self.listaDeServidores.SetStringItem(self.index, 1, objServidor.nome)
            self.listaDeServidores.SetStringItem(self.index, 2, objServidor.idFuncional)
            self.index += 1
            

if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()