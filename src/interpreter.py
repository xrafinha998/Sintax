from src.parser import NoAtribuicao, NoSe, NoExpressao

class Interpreter:
    def __init__(self):
        self.memoria = {}

    def rodar(self, nos):
        for no in nos:
            if isinstance(no, NoAtribuicao):
                if isinstance(no.valor, NoExpressao):
                    v1 = int(self.memoria.get(no.valor.esq, no.valor.esq))
                    v2 = int(no.valor.dir)
                    if no.valor.op == 'SOMA': self.memoria[no.nome] = v1 + v2
                    if no.valor.op == 'SUB':  self.memoria[no.nome] = v1 - v2
                else:
                    self.memoria[no.nome] = int(no.valor)
            
            elif isinstance(no, NoSe):
                v1 = int(self.memoria.get(no.condicao[0], 0))
                op, v2 = no.condicao[1], int(no.condicao[2])
                res = (v1 > v2 if op == '>' else v1 < v2 if op == '<' else v1 == v2)
                if res: print(f"Sintax: {no.acao}")
