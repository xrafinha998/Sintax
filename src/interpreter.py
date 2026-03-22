class Interpreter:
    def __init__(self):
        self.memoria = {}

    def resolver_valor(self, valor):
        if isinstance(valor, str) and valor in self.memoria:
            return self.memoria[valor]
        try:
            return int(valor)
        except:
            return valor

    def rodar(self, nos):
        for no in nos:

            # ATRIBUIÇÃO
            if isinstance(no, NoAtribuicao):
                if isinstance(no.valor, NoExpressao):
                    v1 = self.resolver_valor(no.valor.esq)
                    v2 = self.resolver_valor(no.valor.dir)

                    if no.valor.op == 'SOMA':
                        self.memoria[no.nome] = v1 + v2
                    elif no.valor.op == 'SUB':
                        self.memoria[no.nome] = v1 - v2
                    elif no.valor.op == 'MULT':
                        self.memoria[no.nome] = v1 * v2
                    elif no.valor.op == 'DIV':
                        self.memoria[no.nome] = v1 / v2
                else:
                    self.memoria[no.nome] = self.resolver_valor(no.valor)

            # CONDICIONAL
            elif isinstance(no, NoSe):
                v1 = self.resolver_valor(no.condicao[0])
                op = no.condicao[1]
                v2 = self.resolver_valor(no.condicao[2])

                res = False
                if op == '>': res = v1 > v2
                elif op == '<': res = v1 < v2
                elif op == '==': res = v1 == v2
                elif op == '!=': res = v1 != v2
                elif op == '>=': res = v1 >= v2
                elif op == '<=': res = v1 <= v2

                if res:
                    print(f"Sintax: {no.acao}")
