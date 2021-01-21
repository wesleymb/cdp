from datetime import date
from dateutil.relativedelta import relativedelta

# 31 de janeiro de 2016
d = date(2021, 3, 22)
# somar 1 mês = 29 de fevereiro de 2016
d = d + relativedelta(months=1)
# print(d)
# somar 1 ano = 28 de fevereiro de 2017
d = d + relativedelta(years=1)
# print(d)
vencimento = date(2021, 3, 21)
prazoDeVencimento = (date.today() + relativedelta(month=3))

print(vencimento)
print(prazoDeVencimento)


if prazoDeVencimento >= vencimento:
    print("O prazo esta vencido")