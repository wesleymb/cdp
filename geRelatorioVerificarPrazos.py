import datetime
import os
import geCDP
import modelContrato

def gerarRelatorioContratosComFuturoVencimento():
    html1 ="""<!DOCTYPE html>
            <html>
            <head>
            <style>
            table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            }

            h4{
                font-family: arial,sans-serif;
            }

            td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
            }

            h1,h2{
                font-family: arial, sans-serif;
                text-align: center;
                
            }


            tr:nth-child(even) {
            background-color: #dddddd;
            }
            </style>
            </head>
            <body>

            <h1><img src="../icon.png" alt="Brasão" width="15%" height="15%"></h1>
            <h2>Relatório de contratos com prazos para vencer</h2>"""

    html2 = """
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
            </tr>"""
    
    nomeRelatorioHtml = "relatorios\\Relatorio prazos para vencer.html"

    with open(nomeRelatorioHtml, 'w+') as arqRelat:
        arqRelat.write(html1)
        arqRelat.write(html2)
        
        for queryContrato in geCDP.queryTabela(tabela="CONTRATO"):
            Contrato = modelContrato.contrato(queryContrato)
            if Contrato.verificarPrazoDeVencimentoDeContrato() == True:
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
        
        arqRelat.write("""</table>
            <h4>Data e hora: {horaEdata}</h4>
            </body>
            </html>""".format(horaEdata=datetime.datetime.now().strftime("%c")))
        
        arqRelat.close()
            



if __name__ == "__main__":
    consultarContratosComFuturoVencimento()