from src.tokens import *

class NoExpressao: # Para contas: pontos + 10
    def __init__(self, esq, op, dir):
        self.esq, self.op, self.dir = esq, op, dir

class NoAtribuicao:
    def __init__(self, nome, valor):
        self.nome, self.valor = nome, valor

class NoSe:
    def __init__(self, condicao, acao, senao_acao=None):
        self.condicao, self.acao, self.senao_acao = condicao, acao, senao_acao

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        instrucoes = []
        while self.tokens[self.pos].tipo != T_EOF:
            t = self.tokens[self.pos]
            
            if t.tipo == T_ID and self.tokens[self.pos+1].tipo == T_ATR:
                nome = t.valor
                self.pos += 2
                valor = self.tokens[self.pos].valor
                # Verifica se é uma conta (ex: x = x + 1)
                if self.tokens[self.pos+1].tipo in (T_SOMA, T_SUB):
                    op = self.tokens[self.pos+1].tipo
                    v2 = self.tokens[self.pos+2].valor
                    instrucoes.append(NoAtribuicao(nome, NoExpressao(valor, op, v2)))
                    self.pos += 3
                else:
                    instrucoes.append(NoAtribuicao(nome, valor))
                    self.pos += 1
            
            elif t.tipo == T_SE:
                cond = (self.tokens[self.pos+1].valor, self.tokens[self.pos+2].valor, self.tokens[self.pos+3].valor)
                acao = self.tokens[self.pos+4].valor
                self.pos += 5
                instrucoes.append(NoSe(cond, acao))
            else: self.pos += 1
        return instrucoes
                v_comp = int(self.tokens[self.pos+3].valor)
                msg = self.tokens[self.pos+4].valor 
                nos.append(NoSe(v_nome, op, v_comp, msg))
                self.pos += 5
            
            else:
                self.pos += 1
        return nos
