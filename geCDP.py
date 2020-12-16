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
        VALUES(2,1)""")

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
        lista.append(linha)
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
        lista.append(linha)
    connection.close()
    return lista
    

if __name__ == "__main__":
    criarBanco()
    # dado1 = queryTabela(tabela="SERVIDOR")
    dado2 = queryTabela(tabela="CONTRATO")
    # dado3 = queryTabela(tabela="FISCAL")
    # dado4 = queryTabela(tabela="PAGAMENTO")
    # dado5 = queryTabelaGestorComContrato()
    dado = queryTabelaServidorComContrato(servidor=1)
    print(dado)
    # print("Serivores:\n",dado1)
    print("Contratos:\n",dado2)
    # print("Fiscais:\n",dado3)
    # print("Pagamento:\n",dado4)
    # print(dado5)
