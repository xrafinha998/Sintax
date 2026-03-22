from src.tokens import *

class NoExpressao:
    def __init__(self, esq, op, dir):
        self.esq = esq
        self.op = op
        self.dir = dir

class NoAtribuicao:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

class NoSe:
    def __init__(self, condicao, acao):
        self.condicao = condicao
        self.acao = acao

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        return self.tokens[self.pos]

    def avancar(self):
        self.pos += 1

    def parse(self):
        instrucoes = []

        while self.atual().tipo != T_EOF:
            if self.atual().tipo == T_ID:
                instrucoes.append(self.parse_atr())
            elif self.atual().tipo == T_SE:
                instrucoes.append(self.parse_se())
            else:
                self.avancar()

        return instrucoes

    def parse_atr(self):
        nome = self.atual().valor
        self.avancar()  # ID

        self.avancar()  # =

        valor = self.parse_expr()

        return NoAtribuicao(nome, valor)

    def parse_expr(self):
        esq = self.atual().valor
        self.avancar()

        if self.atual().tipo in (T_SOMA, T_SUB, T_MULT, T_DIV):
            op = self.atual().tipo
            self.avancar()

            dir = self.atual().valor
            self.avancar()

            return NoExpressao(esq, op, dir)

        return esq

    def parse_se(self):
        self.avancar()  # se

        v1 = self.atual().valor
        self.avancar()

        op = self.atual().valor
        self.avancar()

        v2 = self.atual().valor
        self.avancar()

        acao = self.atual().valor
        self.avancar()

        return NoSe((v1, op, v2), acao)
