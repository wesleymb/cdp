import datetime
import os
import geCDP
import modelContrato
import modelPagamento
import modelFiscal



def gerarRelatorio(idContrato):
    
    for queryContrato in geCDP.queryTabelaComWhere(tabela="CONTRATO",coluna="ID",dado=idContrato):
        Contrato = modelContrato.contrato(queryContrato)
            
        html1 ="""<!DOCTYPE html>
            <html>
            <head>
            <link rel="stylesheet" type="text/css" href="../estilos.css"/>
            </head>
            <body>

            <h1><img src="../icon.png" alt="Brasão" width="15%" height="15%"></h1>
            <h2>Relatório do Contrato</h2>"""

        html2 = """
        <h4>
            <tr>
                <td>Contrato:  {contrato}<br></td>
                <td>Número do processo: {numeroDeProcesso}<br></td>
                <td>Empresa: {empresa}</td>
            </tr>

        </h4>
        
        <h4>
            <hr>
            <td>Dados do contrato</td>
        </h4>

        <table>
        <tr>
            <th>Contrato</th>
            <th>Número de processo</th>
            <th>Objeto</th>
            <th>Assinatura</th>
            <th>Encerramento</th>
            <th>Vencimento</th>
            <th>Gestor</th>
            <th>Status</th>
            </tr>""".format(contrato=Contrato.contrato,numeroDeProcesso=Contrato.numeroDeProcesso,empresa=Contrato.empresa)
        
        nomeRelatorioHtml = 'relatorios\\{contrato}_{objeto}_{date}.html'.format(contrato=Contrato.empresa,objeto=Contrato.objeto,date=datetime.date.today())
        nomeRelatorioPdf = 'relatorios\\{contrato}_{objeto}_{date}.pdf'.format(contrato=Contrato.empresa,objeto=Contrato.objeto,date=datetime.date.today())

        with open(nomeRelatorioHtml, 'w+') as arqRelat:
            arqRelat.write(html1)
            arqRelat.write(html2)
            
            arqRelat.write('<tr>')
            arqRelat.write("<td>{contrato}</td>".format(contrato=Contrato.contrato))
            arqRelat.write("<td>{numeroDeProcesso}</td>".format(numeroDeProcesso=Contrato.numeroDeProcesso))   
            arqRelat.write("<td>{objeto}</td>".format(objeto=Contrato.objeto))   
            arqRelat.write("<td>{dataAssinatura}</td>".format(dataAssinatura=Contrato.dataAssinatura))     
            arqRelat.write("<td>{dataTermino}</td>".format(dataTermino= Contrato.dataTermino))    
            arqRelat.write("<td>{vencimento}</td>".format(vencimento= Contrato.vencimento))    
            arqRelat.write("<td>{gestor}</td>".format(gestor= Contrato.gestor))    
            arqRelat.write("<td>{status}</td>".format(status= Contrato.status))    
            arqRelat.write('</tr>')

            
            arqRelat.write("""
            </table>
            </br>
            
            
            <h4>
                <hr>
                <td>Fiscais</td>
            </h4>
            <table>
            <tr>
                <th>Nome</th>
                <th>Id funcional</th>
            </tr>""")

            for queryFiscal in geCDP.queryTabelaComWhere(tabela="FISCAL",coluna="idContrato",dado=idContrato):
                Fiscal = modelFiscal.fiscal(queryFiscal)
                arqRelat.write('<tr>')
                arqRelat.write("<td>{nome}</td>".format(nome=Fiscal.nomeFiscal))
                arqRelat.write("<td>{nome}</td>".format(nome=Fiscal.idFuncional))
                arqRelat.write('<tr>')

            
            arqRelat.write("""
            </table>
            </br>
            
            <h4>
                <hr>
                <td>Pagamentos</td>
            </h4>
            <table>
            <tr>
                <th>Data de pagamento</th>
                <th>Valor</th>
                <th>status</th>
                <th>Número de processo</th>
            </tr>""")

            
            total = 0
            for queryPagamento in geCDP.queryTabelaComWhere(tabela="PAGAMENTO",coluna="idContrato",dado=idContrato):
                
                Pagamento = modelPagamento.pagamento(queryPagamento)
                
                arqRelat.write('<tr>')
                arqRelat.write("<td>{dataDePagamento}</td>".format(dataDePagamento=Pagamento.dataDePagamento))
                arqRelat.write("<td>R$ {valor}</td>".format(valor=Pagamento.valor))
                arqRelat.write("<td>{status}</td>".format(status=Pagamento.status))
                arqRelat.write("<td>{numeroDeProcesso}</td>".format(numeroDeProcesso=Pagamento.numeroDeProcesso))
                arqRelat.write('<tr>')

                if Pagamento.valor != '':
                    total = Pagamento.valor + total

            arqRelat.write('''</table><h4>Total: R$ {total}</h4><hr>'''.format(total=total))
            arqRelat.write(
                '''<table>
                    <tr>
                        <th>Observação</th>
                    </tr>
                        <td>{observacao}</td>
                </table>'''.format(observacao=Contrato.observacao))

            arqRelat.write("""</br><h4>Data e hora: {horaEdata}</h4></body>
            </html>""".format(horaEdata=datetime.datetime.now().strftime("%c")))
            arqRelat.close()

        
        # self.dataDePagamento = self.listaDedados[2]
        # self.valor = self.listaDedados[3]
        # self.status = self.listaDedados[4]
        # self.numeroDeProcesso = self.listaDedados[5]



if __name__ == "__main__":
    gerarRelatorio(idContrato=1)