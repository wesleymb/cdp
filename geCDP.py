import os
import sqlite3

def criarBanco():
    arquivos = os.listdir()
    if 'bd_cdp.db' not in arquivos:
        sqlite3.connect('bd_cdp.db')
        
        criarTabelaContrato()
        criarTabelaFiscal()
        criarTabelaServidor()
        criarTabelaPagamento()
        criarTabelaAditivo()

        
        inserMassaDeDadosContrato()
        inserMassaDeDadosServidor()
        inserMassaDeDadosFiscal()
        # inserMassaDeDadosPagamento()
        inserMassaDeDadosAditivo()

        print("Banco Criado com sucesso.")

def conectar():
    conecicao = sqlite3.connect('bd_cdp.db')
    cursor = conecicao.cursor()
    return conecicao,cursor

def sql(comando):
    conecicao,cursor = conectar()
    cursor.execute(comando)
    conecicao.commit()
    conecicao.close()

def criarTabelaContrato():
    sql("""CREATE TABLE IF NOT EXISTS CONTRATO(
        id INTEGER,
        contrato text,
        numeroDeProcesso text, 
        objeto text,
        empresa text,
        dataAssinatura date, 
        dataTermino date,
        vencimento date, 
        idServidorGestor int, 
        status text,
        observacao text,
        PRIMARY KEY (id),
        FOREIGN KEY (idServidorGestor) REFERENCES SERVIDOR(id)
        )""")

def criarTabelaServidor():
    sql("""CREATE TABLE IF NOT EXISTS SERVIDOR(
        id INTEGER,
        nome text, 
        idFuncional text,  
        PRIMARY KEY (id)
        )""")

def criarTabelaPagamento():
    sql("""CREATE TABLE IF NOT EXISTS PAGAMENTO(
        id INTEGER,
        idContrato INT, 
        dataDePagamento date,  
        valor NUMERIC,
        status text,
        numeroDeProcesso text, 
        PRIMARY KEY (id),
        FOREIGN KEY (idContrato) REFERENCES CONTRATO(id)
        )""")


def criarTabelaFiscal():
    sql("""CREATE TABLE IF NOT EXISTS FISCAl(
        id INTEGER,
        idContrato INT,
        idServidor INT, 
        PRIMARY KEY (id),
        FOREIGN KEY (idContrato) REFERENCES CONTRATO(id),
        FOREIGN KEY (idServidor) REFERENCES SERVIDOR(id)
        )""")

def criarTabelaAditivo():
    sql("""CREATE TABLE IF NOT EXISTS ADITIVO(
        id INTEGER,
        idContrato INT,
        valor NUMERIC, 
        dataAssinatura date, 
        dataTermino date,
        status text,
        PRIMARY KEY (id),
        FOREIGN KEY (idContrato) REFERENCES CONTRATO(id)
        )""")


def queryTabela(tabela):
    c,connection = conectar()
    sql = 'SELECT * FROM {tabela}'.format(tabela=tabela)
    lista = []
    for linha in c.execute(sql):
        lista.append(linha)
    connection.close()
    return lista

def queryTabelaComWhere(tabela,coluna,dado):
    c,connection = conectar()
    sql = """SELECT * FROM {tabela} WHERE {coluna} = '{dado}'""".format(tabela=tabela,coluna=coluna,dado=dado)
    lista = []
    for linha in c.execute(sql):
        lista.append(linha)
    connection.close()
    return lista

def queryTabelaComWhereLike(tabela,coluna,dado):
    c,connection = conectar()
    sql = """SELECT * FROM {tabela} WHERE {coluna} LIKE '{dado}%'""".format(tabela=tabela,coluna=coluna,dado=dado)
    lista = []
    for linha in c.execute(sql):
        lista.append(linha)
    connection.close()
    return lista    


def queryNomeServidores():
    c,connection = conectar()
    sql = 'SELECT SERVIDOR.NOME FROM SERVIDOR'
    lista = []
    for linha in c.execute(sql):
        for dado in linha:
            lista.append(dado)
    connection.close()
    return sorted(lista)



def inserMassaDeDadosServidor():
    sql("""INSERT INTO SERVIDOR (nome, idFuncional) 
        VALUES("Wesley","555555-5")""")
    sql("""INSERT INTO SERVIDOR (nome, idFuncional) 
        VALUES("Bruno","222222-2")""")
    sql("""INSERT INTO SERVIDOR (nome, idFuncional) 
        VALUES("Marco","333333-3")""")

def inserMassaDeDadosContrato():
    sql("""INSERT INTO CONTRATO (contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento, idServidorGestor, status,observacao) 
        VALUES("006/17","E-17/0000/0000/0000","Central telefonica","Ra telecom","2020-3-5","2021-3-5","2020-3-10", 1,"ATIVO","")""")
    
    sql("""INSERT INTO CONTRATO (contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento, idServidorGestor, status,observacao) 
        VALUES("006/17","E-17/0000/0000/0000","Computadores","SIMPRESS","2020-3-5","2021-3-5","2020-3-10", 2,"ATIVO","")""")

    sql("""INSERT INTO CONTRATO (contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento, idServidorGestor, status, observacao) 
        VALUES("006/17","E-17/0000/0000/0000","Impressoras","CHADA","2020-3-5","2021-3-5","2020-3-10", 3,"ATIVO","")""")

def inserMassaDeDadosFiscal():
    sql("""INSERT INTO FISCAl (idServidor, idContrato) 
        VALUES(2,1)""")
    
    sql("""INSERT INTO FISCAl (idServidor, idContrato) 
        VALUES(3,1)""")
    
    sql("""INSERT INTO FISCAl (idServidor, idContrato) 
        VALUES(1,2)""")

def inserMassaDeDadosPagamento():
    sql("""INSERT INTO PAGAMENTO (idContrato, dataDePagamento, valor, status, numeroDeProcesso) 
        VALUES(1,"2020-12-13",500.10, "PAGO", "SEI-170026/002148/2020")""")

def inserMassaDeDadosAditivo():
    sql("""INSERT INTO ADITIVO (idContrato, valor, dataAssinatura, dataTermino, status) 
        VALUES(1,500.10, "2020-12-13", "2021-12-13","ATIVO")""")


        # idContrato INT,
        # valor NUMERIC, 
        # dataAssinatura date, 
        # dataTermino date,
        # status text,

def queryTabelaServidorComContrato(servidor):
    c,connection = conectar()
    sql = '''SELECT SERVIDOR.NOME 
    FROM CONTRATO
    INNER JOIN SERVIDOR on CONTRATO.idServidorGestor = SERVIDOR.id
    WHERE SERVIDOR.id = {servidor}
    '''.format(servidor=servidor)
    lista = []
    for linha in c.execute(sql):
        for dado in linha:
            lista.append(dado)
    connection.close()
    return lista

def queryTabelaFiscalComContrato(idServidor):
    c,connection = conectar()
    sql = '''SELECT CONTRATO.id,contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento,  idServidorGestor,status,observacao
    FROM CONTRATO
    INNER JOIN FISCAL on FISCAL.idContrato = CONTRATO.id
    WHERE FISCAL.idServidor = {idServidor}
    '''.format(idServidor=idServidor)
    lista = []
    for linha in c.execute(sql):
        lista.append(linha)
    connection.close()
    return lista

def inserNovoAditivo(idContrato,valor,dataAssinatura,dataTermino,status):
    sql("""INSERT INTO ADITIVO (idContrato, valor, dataAssinatura, dataTermino, status) 
        VALUES({idContrato},{valor}, "{dataAssinatura}", "{dataTermino}","{status}")""".format(idContrato=idContrato,valor=valor,dataAssinatura=dataAssinatura,dataTermino=dataTermino,status=status))


def inserNovoContrato(contrato,numeroDeProcesso,objeto,empresa,dataAssinatura,dataTermino,vencimento,status):
    sql("""INSERT INTO CONTRATO (contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento, status)
        VALUES("{contrato}","{numeroDeProcesso}","{objeto}","{empresa}","{dataAssinatura}","{dataTermino}","{vencimento}","{status}")"""
        .format(contrato = contrato,
        numeroDeProcesso = numeroDeProcesso,
        objeto = objeto,
        empresa = empresa,
        dataAssinatura = dataAssinatura,
        dataTermino = dataTermino,
        vencimento = vencimento,
        status = status
        ))

def inserirNovoPagamentoAutomatico(idContrato,dataDePagamento):
    sql("""INSERT INTO PAGAMENTO (idContrato, dataDePagamento) 
        VALUES({idContrato},"{dataDePagamento}")""".format(idContrato=idContrato,dataDePagamento=dataDePagamento))

def inserirNovoPagamentoManual(idContrato,dataDePagamento,valor,status,numeroDeProcesso):
    sql("""INSERT INTO PAGAMENTO (idContrato, dataDePagamento,valor,status,numeroDeProcesso) 
        VALUES({idContrato},"{dataDePagamento}",{valor},"{status}","{numeroDeProcesso}")""".format(idContrato=idContrato,dataDePagamento=dataDePagamento,valor=valor,status=status,numeroDeProcesso=numeroDeProcesso))


        # idContrato INT, 
        # dataDePagamento date,  
        # valor NUMERIC,
        # status text,
        # numeroDeProcesso text, 



def inserirNovoServidor(nome,idFuncional):
    sql("""INSERT INTO SERVIDOR (nome, idFuncional) 
    VALUES("{nome}","{idFuncional}")""".format(nome=nome,idFuncional=idFuncional))

def inserNovoFiscal(idServidor,idContrato):
    sql("""INSERT INTO FISCAl (idServidor, idContrato) VALUES({idServidor},{idContrato})""".format(idServidor=idServidor,idContrato=idContrato))
        
def excluirFiscal(idContrato,idServidor):
    sql("""DELETE FROM FISCAL WHERE FISCAL.idContrato = {idContrato} AND FISCAL.idServidor = {idServidor}"""
    .format(idContrato=idContrato,idServidor=idServidor))

def excluirServidor(idServidor):
    sql("""DELETE FROM SERVIDOR WHERE id = {idServidor}"""
    .format(idServidor=idServidor))

def excluirPagamento(idPagamento):
    sql("""DELETE FROM PAGAMENTO WHERE id = {idPagamento}"""
    .format(idPagamento=idPagamento))

def excluirAditivo(idAditivo):
    sql("""DELETE FROM ADITIVO WHERE id = {idAditivo}"""
    .format(idAditivo=idAditivo))

def excluirContrato(idContrato):
    sql("""DELETE FROM CONTRATO WHERE ID = {idContrato}""".format(idContrato=idContrato))
    sql("""DELETE FROM FISCAL WHERE FISCAL.idContrato = {idContrato}""".format(idContrato=idContrato))
    sql("""DELETE FROM PAGAMENTO WHERE PAGAMENTO.idContrato = {idContrato}""".format(idContrato=idContrato))

def ataulizarContrato(contrato,numeroDeProcesso,objeto,empresa,dataAssinatura,dataTermino,vencimento,idServidorGestor,status, observacao, idContrato):
        sql("""UPDATE CONTRATO SET  
        contrato = "{contrato}", numeroDeProcesso = "{numeroDeProcesso}", objeto = "{objeto}", empresa = "{empresa}", dataAssinatura = "{dataAssinatura}", dataTermino = "{dataTermino}", vencimento = "{vencimento}", idServidorGestor = {idServidorGestor},status = "{status}", observacao = "{observacao}" WHERE id = {idContrato}"""
        .format(contrato = contrato,
        numeroDeProcesso = numeroDeProcesso,
        objeto = objeto,
        empresa = empresa,
        dataAssinatura = dataAssinatura,
        dataTermino = dataTermino,
        vencimento = vencimento,
        idServidorGestor=idServidorGestor,
        status = status,
        observacao = observacao,
        idContrato=idContrato
        ))
def ataulizarServidor(nome,idFuncional,idServidor):
    sql("""UPDATE SERVIDOR SET nome = "{nome}", idFuncional = "{idFuncional}" WHERE id = {idServidor}""".format(nome=nome,idFuncional=idFuncional,idServidor=idServidor))

def ataulizarPagamento(dataDePagamento,valor,status,numeroDeProcesso,idPagamento):
    sql("""UPDATE PAGAMENTO SET 
    dataDePagamento = "{dataDePagamento}", valor = {valor}, numeroDeProcesso = "{numeroDeProcesso}", status = "{status}" WHERE id = {idPagamento}""".format(dataDePagamento=dataDePagamento,valor=valor,numeroDeProcesso=numeroDeProcesso,status=status,idPagamento=idPagamento))

def ataulizarAditivo(valor,dataAssinatura,dataTermino,status,idAditivo):
    sql("""UPDATE ADITIVO SET valor = "{valor}", dataAssinatura = "{dataAssinatura}" , dataTermino = "{dataTermino}", status = "{status}" WHERE id = {idAditivo}""".format(valor=valor,dataAssinatura=dataAssinatura,dataTermino=dataTermino,status=status,idAditivo=idAditivo))


        # id INTEGER,
        # idContrato INT,
        # valor NUMERIC, 
        # dataAssinatura date, 
        # dataTermino date,
        # status text,    



if __name__ == "__main__":
    criarBanco()
    # sql("""UPDATE CONTRATO SET observacao = ''""")
    # excluirPagamento(idPagamento=1)
    # # # inserMassaDeDadosFiscal()
    # # # x = queryTabelaComWhereLike(tabela='CONTRATO',coluna='OBJETO',dado='CENT')
    # inserMassaDeDadosAditivo()
    x = queryTabela(tabela="ADITIVO")
    # # # # # x = queryTabelaServidorComContrato(servidor =  2)
    # # # # x = queryTabelaFiscalComContrato(idServidor=3)
    for i in x:
        print(i)