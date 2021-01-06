import datetime
import geCDP
from dateutil.relativedelta import relativedelta


class contrato:
    def __init__(self,listaDedadosContrato):
        self.listaDedadosContrato = listaDedadosContrato
        self.ajustarDados()
    
    def ajustarDados(self):
        self.id = self.listaDedadosContrato[0]
        self.contrato = self.listaDedadosContrato[1]
        self.numeroDeProcesso = self.listaDedadosContrato[2]
        self.objeto = self.listaDedadosContrato[3]
        self.empresa = self.listaDedadosContrato[4]
        self.dataAssinatura = self.listaDedadosContrato[5]
        self.dataTermino = self.listaDedadosContrato[6]
        self.vencimento = self.listaDedadosContrato[7]
        self.idServidorGestor = self.listaDedadosContrato[8]
        self.status = self.listaDedadosContrato[9]
        self.observacao = self.listaDedadosContrato[10]

        self.dataAssinaturaTipoDate = datetime.datetime.strptime(self.dataAssinatura,"%Y-%m-%d").date()
        self.dataTerminoTipoDate = datetime.datetime.strptime(self.dataTermino,"%Y-%m-%d").date()
        self.vencimentoTipoDate = datetime.datetime.strptime(self.vencimento,"%Y-%m-%d").date()

        
        if self.observacao == None:
            self.observacao = ''
        
        if self.idServidorGestor != None:
            nomegestor = geCDP.queryTabelaComWhere(tabela="SERVIDOR",coluna="id",dado=self.idServidorGestor)
            for nome in nomegestor:
               self.gestor = nome[1]
        
        
        else:
            self.idServidorGestor = ''
            self.gestor = ''



    def gerarVencimentos(self):

        vencimento = datetime.datetime.strptime(self.vencimento,"%Y-%m-%d").date()
        
        meses = 0		
        listaDeDias = []
        while meses <= 12:
            dataMesQueVem = vencimento + relativedelta(months=meses)
            listaDeDias.append(dataMesQueVem)
            meses = meses + 1
        return listaDeDias	

    def altulizarContrato(self):
        geCDP.ataulizarContrato(
            contrato=self.contrato,
            numeroDeProcesso=self.numeroDeProcesso,
            objeto=self.objeto,
            empresa=self.empresa,
            dataAssinatura=self.dataAssinatura,
            dataTermino=self.dataTermino,
            vencimento=self.vencimento,
            idServidorGestor=self.idServidorGestor,
            status=self.status,
            observacao = self.observacao,
            idContrato=self.id)

if __name__ == "__main__":
    listaDeDados = ['1','006/17',"E-17/0000/0000/0000",'impressora A3','Chada',"2020-12-22","2021-12-22","2021-01-10",'1','ATIVO']
    contratoTeste = contrato(listaDedadosContrato=listaDeDados)
    
    print(contratoTeste.idServidorGestor)
    
    # vencimentos = contratoTeste.gerarVencimentos()
    # for dia in vencimentos:
    # 	print(dia)
