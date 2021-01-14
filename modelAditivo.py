import geCDP

class aditivo:
    def __init__(self, listaDedadosContrato, tipo=1):
        self.listaDedadosContrato = listaDedadosContrato
        
        if tipo == 1:
            self.ajustarDados()
        
        if tipo == 2:
            self.ajustarDadosNovo()

    def ajustarDados(self):
        self.id = self.listaDedadosContrato[0]
        self.idcontrato = self.listaDedadosContrato[1]
        self.valor = self.listaDedadosContrato[2]
        self.dataAssinatura = self.listaDedadosContrato[3]
        self.dataTermino = self.listaDedadosContrato[4]
        self.status = self.listaDedadosContrato[5]
    
    def ajustarDadosNovo(self):
        self.idcontrato = self.listaDedadosContrato[0]
        self.valor = self.listaDedadosContrato[1]
        self.dataAssinatura = self.listaDedadosContrato[2]
        self.dataTermino = self.listaDedadosContrato[3]
        self.status = self.listaDedadosContrato[4]

    def inserNovoAditivo(self):
        geCDP.inserNovoAditivo(idContrato=self.idcontrato,valor=self.valor,dataAssinatura=self.dataAssinatura,dataTermino=self.dataTermino,status=self.status)

    def excluirAditivo(self):
        geCDP.excluirAditivo(idAditivo=self.id)