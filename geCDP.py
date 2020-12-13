import os
import sqlite3

def criarBanco():
    arquivos = os.listdir()
    if 'bd_cdp.db' not in arquivos:
        sqlite3.connect('bd_cdp.db')
        criarTabelaContrato()
        criarTabelaFiscal()
        criarTabelaServidor()
        inserMassaDeDadosContrato()
        inserMassaDeDadosServidor()
        inserMassaDeDadosFiscal()

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
        numeroDeProcesso text, 
        dataAssinatura date, 
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


def criarTabelaFiscal():
    sql("""CREATE TABLE IF NOT EXISTS FISCAl(
        id INTEGER,
        idServidor, 
        idContrato INT, 
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
        VALUES("Bruno","555555-5")""")

def inserMassaDeDadosContrato():
    sql("""INSERT INTO CONTRATO (numeroDeProcesso, dataAssinatura, vencimento, idServidorGestor, status) 
        VALUES("E-17/0000/0000/0000","2020-3-5","2020-3-10", 1,"ATIVO")""")

def inserMassaDeDadosFiscal():
    sql("""INSERT INTO FISCAl (idServidor, idContrato) 
        VALUES(1,1)""")


if __name__ == "__main__":
    criarBanco()
    dado1 = queryTabela(tabela="SERVIDOR")
    dado2 = queryTabela(tabela="CONTRATO")
    dado3 = queryTabela(tabela="FISCAL")
    
    print(dado1,dado2,dado3)