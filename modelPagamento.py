import geCDP
from dateutil.relativedelta import relativedelta
import datetime

class pagamento:
    def __init__(self,listaDedados,tipo=1):
        self.listaDedados = listaDedados
        if tipo == 1:
            self.ajustarDados()
        elif tipo == 2:
             self.ajustarDadosNovo()
        elif tipo == 3:
            self.ajustarDadosNovoAutomatico()

    def ajustarDados(self):
        # idContrato, dataDePagamento, valor, status, numeroDeProcesso
        self.id = self.listaDedados[0]
        self.idContrato = self.listaDedados[1]
        self.dataDePagamento = self.listaDedados[2]
        self.valor = self.listaDedados[3]
        self.status = self.listaDedados[4]
        self.numeroDeProcesso = self.listaDedados[5]

        self.dataDePagamentoTipoDate = datetime.datetime.strptime(self.dataDePagamento,"%Y-%m-%d").date()
    
        if self.valor == None:
            self.valor = ""
        
        if self.status == None:
            self.status = ""

        if self.numeroDeProcesso == None:
            self.numeroDeProcesso = ""
    
    def ajustarDadosNovo(self):
        
        self.idContrato = self.listaDedados[0]
        self.dataDePagamento = self.listaDedados[1]
        self.valor = self.listaDedados[2]
        self.status = self.listaDedados[3]
        self.numeroDeProcesso = self.listaDedados[4]

        
            
    def ajustarDadosNovoAutomatico(self):
        
        self.idContrato = self.listaDedados[0]
        self.dataDePagamento = self.listaDedados[1]

    def inserirNovoPagamentoAutomatico(self):
        geCDP.inserirNovoPagamentoAutomatico(idContrato=self.idContrato, dataDePagamento=self.dataDePagamento)

    def inserirNovoPagamentoManual(self):
        geCDP.inserirNovoPagamentoManual(idContrato=self.idContrato, dataDePagamento=self.dataDePagamento, valor=self.valor, status=self.status, numeroDeProcesso=self.numeroDeProcesso)
    

    def excluirPagamento(self):
        geCDP.excluirPagamento(idPagamento=self.id)

    def atulizarPagamento(self):

        geCDP.ataulizarPagamento(dataDePagamento=self.dataDePagamento, valor=self.valor, status=self.status, numeroDeProcesso=self.numeroDeProcesso, idPagamento=self.id)