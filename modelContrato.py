import datetime
from dateutil.relativedelta import relativedelta

class contrato:
	def __init__(self, numeroDeProcesso, dataAssinatura, gestor, vencimento, status):
		self.numeroDeProcesso = numeroDeProcesso
		self.dataAssinatura = dataAssinatura
		self.gestor = gestor
		self.vencimento = vencimento
		self.status = status


	def gerarVencimentos(self):

		meses = 0		
		listaDeDias = []
		while meses <= 12:
			dataMesQueVem = self.vencimento + relativedelta(months=meses)
			listaDeDias.append(dataMesQueVem)
			meses = meses + 1
		return listaDeDias			

if __name__ == "__main__":
	
	teste = contrato(
		numeroDeProcesso="E-17/0000/0000/0000",
		dataAssinatura= datetime.date(2020,3,5),
		gestor= "Wesley",
		vencimento= datetime.date(2020,12,12),
		status= "ATIVO"
		)
	
	vencimentos = teste.gerarVencimentos()
	print(teste.status)
	for dia in vencimentos:
		print(dia)
