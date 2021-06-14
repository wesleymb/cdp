import wx
import modelNovoServidor
import modelServidor


def main():
    newServidores()

class newServidores(object):
    """docstring for newServidores"""
    def __init__(self,viwerServidoresOpened,status,idServidor,nome,idFuncional):
        super(newServidores, self).__init__()
        
        self.viwerServidoresOpened = viwerServidoresOpened
        self.status = status
        
        self.idServidor = idServidor
        self.nome = nome
        self.idFuncional = idFuncional

        print(self.idServidor,self.nome,self.idFuncional)

        self.frame = wx.Frame(None, -1, 'Novo servidores', style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.frame.SetDimensions(0,0,400,300)
        self.panel = wx.Panel(self.frame)
        self.index = 0
        self.statusbar =  self.frame.CreateStatusBar(1)


        self.icon = wx.Icon(wx.Image('icon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.frame.SetIcon(self.icon)
        
        wx.StaticText(self.panel, wx.ID_ANY, "Nome:", (25, 25))
        self.txtNome = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 50),size=(350, -1))
        
        wx.StaticText(self.panel, wx.ID_ANY, "ID funcional:", (25, 100))
        self.txtIdFuncional = wx.TextCtrl(self.panel, wx.ID_ANY,"", (25, 125),size=(100, -1))


        self.buttonFechar = wx.Button(self.panel, wx.ID_ANY, 'Fechar', (275, 175),size=(100,-1))
        
        self.buttonSalvar = wx.Button(self.panel, wx.ID_ANY, 'Salvar', (175, 175),size=(100,-1))

        self.buttonSalvar.Bind(wx.EVT_BUTTON, self.criarNovoServidor)
        self.buttonFechar.Bind(wx.EVT_BUTTON, self.fechar)
        
        self.carregarParaAtulizarServidor()
        self.frame.Show()
        self.frame.Centre()
    
    
    def fechar(self,event):
        self.frame.Destroy()

   
    def carregarParaAtulizarServidor(self):
        if self.status == "ATUALIZAR":
            self.txtNome.SetValue(self.nome)
            self.txtIdFuncional.SetValue(self.idFuncional)

    
    
    
    def criarNovoServidor(self,event):
        nome = self.txtNome.GetValue()
        idFuncional = self.txtIdFuncional.GetValue()
        
        if nome != '' and idFuncional != '':
            if self.status == "NOVO":
            
                objServidor = modelNovoServidor.servidor((nome,idFuncional))
                objServidor.inserirNovoServidorNaTabela()
                
                self.viwerServidoresOpened.txtFiltro.SetValue(nome)
                self.viwerServidoresOpened.filtarServidor(event)

                dlgServidorNovo = wx.MessageDialog(None , "Servidor criado com sucesso!","Pronto", wx.OK| wx.ICON_INFORMATION)
                dlgServidorNovo.ShowModal()
                self.frame.Destroy()


            if self.status == "ATUALIZAR":

                    nome = self.txtNome.GetValue()
                    idFuncional = self.txtIdFuncional.GetValue()
                    
                    if nome != '' and idFuncional != '':

                        objServidor = modelServidor.servidor((self.idServidor,nome,idFuncional))
                        objServidor.atulizarNaTabela()

                        self.viwerServidoresOpened.txtFiltro.SetValue(nome)
                        self.viwerServidoresOpened.filtarServidor(event)

                        dlgServidorAtulizado = wx.MessageDialog(None , "Servidor atulizado com sucesso.","Pronto", wx.OK| wx.ICON_INFORMATION)
                        dlgServidorAtulizado.ShowModal()
                        self.frame.Destroy() 
                    else:
                        dlgServidorAtulizarErro = wx.MessageDialog(None , "Provavelmente o nome ou id funcinal estão em branco.","Pronto", wx.OK| wx.ICON_INFORMATION)
                        dlgServidorAtulizarErro.ShowModal() 

        
        else:
            dlgServidorNovoErro = wx.MessageDialog(None , "Provavelmente o nome ou id funcinal estão em branco.","Pronto", wx.OK| wx.ICON_INFORMATION)
            dlgServidorNovoErro.ShowModal()  




if __name__ == '__main__':
    app = wx.App()
    main()  
    app.MainLoop()