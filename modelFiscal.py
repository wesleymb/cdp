import geCDP

class fiscal:
    def __init__(self,listaDedadosServidor):
        self.listaDedadosServidor = listaDedadosServidor
        self.ajustarDados()

    def ajustarDados(self):
        self.id = self.listaDedadosServidor[0]
        self.idContrato = self.listaDedadosServidor[1]
        self.idServidor = self.listaDedadosServidor[2]
        nomeFiscal = geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna="id",dado=self.idServidor)
        for nome in nomeFiscal:
            self.nomeFiscal = nome[1]

    def excluirDaTabela(self):
        geCDP.excluirFiscal(idContrato=self.idContrato,idServidor=self.idServidor)