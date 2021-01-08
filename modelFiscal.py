import geCDP
import modelServidor

class fiscal:
    def __init__(self,listaDedadosServidor):
        self.listaDedadosServidor = listaDedadosServidor
        self.ajustarDados()

    def ajustarDados(self):
        self.id = self.listaDedadosServidor[0]
        self.idContrato = self.listaDedadosServidor[1]
        self.idServidor = self.listaDedadosServidor[2]
         
        for queryServidor in geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna="id",dado=self.idServidor):
            Servidor = modelServidor.servidor(queryServidor)
            self.nomeFiscal = Servidor.nome
            self.idFuncional = Servidor.idFuncional



        numeroContrato = geCDP.queryTabelaComWhere(tabela="CONTRATO",coluna="id",dado=self.idContrato)
        for nome in numeroContrato:
            self.numeroContrato = nome[2]

        
        
           

    def excluirDaTabela(self):
        geCDP.excluirFiscal(idContrato=self.idContrato,idServidor=self.idServidor)

