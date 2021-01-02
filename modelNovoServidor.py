import geCDP

class servidor:
    def __init__(self,listaDedadosServidor):
        self.listaDedadosServidor = listaDedadosServidor
        self.ajustarDados()

    def ajustarDados(self):
        self.nome = self.listaDedadosServidor[0]
        self.idFuncional = self.listaDedadosServidor[1]

    def inserirNovoServidorNaTabela(self):
        geCDP.inserirNovoServidor(nome=self.nome,idFuncional=self.idFuncional)