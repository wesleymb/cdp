import geCDP

class fiscal:
    def __init__(self,listaDedadosServidor):
        self.listaDedadosServidor = listaDedadosServidor
        self.ajustarDados()

    def ajustarDados(self):
        self.idContrato = self.listaDedadosServidor[0]
        self.idServidor = self.listaDedadosServidor[1]


    def insertNaTabela(self):
        geCDP.inserNovoFiscal(idServidor=self.idServidor,idContrato=self.idContrato)

    def excluirFiscal(self):
        geCDP.excluirFiscal(idContrato=self.idContrato,idServidor=self.idServidor)