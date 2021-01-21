import datetime
import os

class relatorio:
    def __init__(self,nome,idFuncional,listaServidoresFiscal,listaServidoresGestor):
        self.nome = nome
        self.idFuncional = idFuncional

        self.listaServidoresFiscal = listaServidoresFiscal
        self.listaServidoresGestor = listaServidoresGestor
        
        

    def gerarRelatorio(self):
        
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

            <h1><img src="icon.png" alt="Brasão" width="15%" height="15%"></h1>
            <h2>Relatório do servidor</h2>"""

        html2 = """
        <h4>
            <tr>
                <td>Nome:  {nome}<br></td>
                <td>ID funcinal: {id}</td>
            </tr>

        </h4>

        <h4>
            <td>Perfíl: Fiscal</td>
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
            </tr>""".format(nome=self.nome,id=self.idFuncional)

        # with open(os.path.join(os.environ['USERPROFILE'], 'Desktop','{nome}_{id}.html'.format(nome=self.nome,id=self.idFuncional)), 'a+') as arqRelat:

        with open('{nome}_{id}.html'.format(nome=self.nome,id=self.idFuncional), 'w+') as arqRelat:
                arqRelat.write(html1)
                arqRelat.write(html2)
                for Fiscal in self.listaServidoresFiscal:
                    arqRelat.write('<tr>')
                    arqRelat.write("<td>{contrato}</td>".format(contrato=Fiscal.contrato))
                    arqRelat.write("<td>{numeroDeProcesso}</td>".format(numeroDeProcesso=Fiscal.numeroDeProcesso))   
                    arqRelat.write("<td>{objeto}</td>".format(objeto=Fiscal.objeto))   
                    arqRelat.write("<td>{dataAssinatura}</td>".format(dataAssinatura=Fiscal.dataAssinatura))     
                    arqRelat.write("<td>{dataTermino}</td>".format(dataTermino= Fiscal.dataTermino))    
                    arqRelat.write("<td>{vencimento}</td>".format(vencimento= Fiscal.vencimento))    
                    arqRelat.write("<td>{gestor}</td>".format(gestor= Fiscal.gestor))    
                    arqRelat.write("<td>{status}</td>".format(status= Fiscal.status))    
                    arqRelat.write('</tr>')

                arqRelat.write("""
</table>
</br>
<h4>
    <td>Perfíl: Gestor</td>
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
  </tr>""")
                for Gestor in self.listaServidoresGestor:
                    arqRelat.write('<tr>')
                    arqRelat.write("<td>{contrato}</td>".format(contrato=Gestor.contrato))
                    arqRelat.write("<td>{numeroDeProcesso}</td>".format(numeroDeProcesso=Gestor.numeroDeProcesso))   
                    arqRelat.write("<td>{objeto}</td>".format(objeto=Gestor.objeto))   
                    arqRelat.write("<td>{dataAssinatura}</td>".format(dataAssinatura=Gestor.dataAssinatura))     
                    arqRelat.write("<td>{dataTermino}</td>".format(dataTermino= Gestor.dataTermino))    
                    arqRelat.write("<td>{vencimento}</td>".format(vencimento= Gestor.vencimento))    
                    arqRelat.write("<td>{gestor}</td>".format(gestor= Gestor.gestor))    
                    arqRelat.write("<td>{status}</td>".format(status= Gestor.status))    
                    arqRelat.write('</tr>')

                arqRelat.write("""</table>
                <h4>Data e hora: {horaEdata}</h4>
                </body>
                </html>""".format(horaEdata=datetime.datetime.now().strftime("%c")))
                arqRelat.close()