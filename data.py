from datetime import date
from dateutil.relativedelta import relativedelta

# 31 de janeiro de 2016
d = date(2016, 1, 31)
# somar 1 mês = 29 de fevereiro de 2016
d = d + relativedelta(months=1)
print(d)
# somar 1 ano = 28 de fevereiro de 2017
d = d + relativedelta(years=1)
print(d)