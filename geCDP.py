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
        
        inserMassaDeDadosContrato()
        inserMassaDeDadosServidor()
        inserMassaDeDadosFiscal()
        inserMassaDeDadosPagamento()

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
        for dado in linha:
            lista.append(dado)
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
    sql("""INSERT INTO CONTRATO (contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento, idServidorGestor, status) 
        VALUES("006/17","E-17/0000/0000/0000","Central telefonica","Ra telecom","2020-3-5","2021-3-5","2020-3-10", 1,"ATIVO")""")
    
    sql("""INSERT INTO CONTRATO (contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento, idServidorGestor, status) 
        VALUES("006/17","E-17/0000/0000/0000","Computadores","SIMPRESS","2020-3-5","2021-3-5","2020-3-10", 2,"ATIVO")""")

    sql("""INSERT INTO CONTRATO (contrato, numeroDeProcesso, objeto, empresa, dataAssinatura, dataTermino, vencimento, idServidorGestor, status) 
        VALUES("006/17","E-17/0000/0000/0000","Impressoras","CHADA","2020-3-5","2021-3-5","2020-3-10", 3,"ATIVO")""")

def inserMassaDeDadosFiscal():
    sql("""INSERT INTO FISCAl (idServidor, idContrato) 
        VALUES(1,1)""")
    sql("""INSERT INTO FISCAl (idServidor, idContrato) 
        VALUES(2,2)""")

def inserMassaDeDadosPagamento():
    sql("""INSERT INTO PAGAMENTO (idContrato, dataDePagamento, valor, status) 
        VALUES(1,"2020-12-13",500.10, "PAGO")""")


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

def queryTabelaGestorComContrato():
    c,connection = conectar()
    sql = '''SELECT CONTRATO.numeroDeProcesso, SERVIDOR.NOME  
    FROM FISCAL
    INNER JOIN SERVIDOR on FISCAL.idServidor = SERVIDOR.id
    INNER JOIN CONTRATO on CONTRATO.id = FISCAL.idContrato
    '''
    lista = []
    for linha in c.execute(sql):
        for dado in linha:
            lista.append(dado)
    connection.close()
    return lista

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

def excluirContrato(idContrato):
    sql("""DELETE FROM CONTRATO WHERE ID = {idContrato}""".format(idContrato=idContrato))
    sql("""DELETE FROM FISCAL WHERE FISCAL.idContrato = {idContrato}""".format(idContrato=idContrato))
    sql("""DELETE FROM PAGAMENTO WHERE PAGAMENTO.idContrato = {idContrato}""".format(idContrato=idContrato))

if __name__ == "__main__":
    criarBanco()
    # inserMassaDeDadosFiscal()
    # sql("""DELETE FROM fiscal WHERE fiscal.idContrato = 2""")
    # x = queryTabela(tabela="PAGAMENTO")
    # print(x)