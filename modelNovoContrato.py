import geCDP

class contrato:
    def __init__(self,listaDedadosContrato):
        self.listaDedadosContrato = listaDedadosContrato
        self.ajustarDados()

    def ajustarDados(self):
        self.contrato = self.listaDedadosContrato[0]
        self.numeroDeProcesso = self.listaDedadosContrato[1]
        self.objeto = self.listaDedadosContrato[2]
        self.empresa = self.listaDedadosContrato[3]
        self.dataAssinatura = self.listaDedadosContrato[4]
        self.dataTermino = self.listaDedadosContrato[5]
        self.vencimento = self.listaDedadosContrato[6]
        self.status = self.listaDedadosContrato[7]

    def criarNovoContrato(self):
        geCDP.inserNovoContrato(
            contrato = self.contrato, 
            numeroDeProcesso = self.numeroDeProcesso, 
            objeto = self.objeto,
            empresa = self.empresa,
            dataAssinatura = self.dataAssinatura,
            dataTermino = self.dataTermino,
            vencimento = self.vencimento,
            status = self.status)
