import datetime
from dateutil.relativedelta import relativedelta

class contrato:
	def __init__(self, numeroDeProcesso, assinatura, gestor,  fiscais, vencimento, status):
		self.numeroDeProcesso = numeroDeProcesso
		self.assinatura = assinatura
		self.gestor = gestor
		self.fiscais = fiscais
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
		assinatura= datetime.date(2020,3,5),
		gestor= "Wesley",
		fiscais= ["Bruno", "Wesley", "Marco"],
		vencimento= datetime.date(2020,12,12),
		status= "ATIVO"
		)
	
	vencimentos = teste.gerarVencimentos()
	print(teste.status)
	for dia in vencimentos:
		print(dia)
