class servidor:
    def __init__(self,listaDedadosServidor):
        self.listaDedadosServidor = listaDedadosServidor
        self.ajustarDados()

    def ajustarDados(self):
        self.id = self.listaDedadosServidor[0]
        self.nome = self.listaDedadosServidor[1]
        self.idFuncional = self.listaDedadosServidor[2]

