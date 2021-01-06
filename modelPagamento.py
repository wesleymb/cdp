import geCDP
from dateutil.relativedelta import relativedelta
import datetime

class pagamento:
    def __init__(self,listaDedados,tipo=1):
        self.listaDedados = listaDedados
        if tipo == 1:
            self.ajustarDados()
        else:
            self.ajustarDadosNovo()

    def ajustarDados(self):
        # idContrato, dataDePagamento, valor, status, numeroDeProcesso
        self.id = self.listaDedados[0]
        self.idContrato = self.listaDedados[1]
        self.dataDePagamento = self.listaDedados[2]
        self.valor = self.listaDedados[3]
        self.status = self.listaDedados[4]
        self.numeroDeProcesso = self.listaDedados[5]
    
        if self.valor == None:
            self.valor = ""
        
        if self.status == None:
            self.status = ""

        if self.numeroDeProcesso == None:
            self.numeroDeProcesso = ""
    
    def ajustarDadosNovo(self):
        
        self.idContrato = self.listaDedados[0]
        self.dataDePagamento = self.listaDedados[1]

    def inserirNovoPagamento(self):
        geCDP.inserirNovoPagamento(idContrato=self.idContrato,dataDePagamento=self.dataDePagamento)