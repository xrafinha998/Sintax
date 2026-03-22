from src.tokens import T_EOF, T_ID, T_ATR, T_SE, T_STR, T_OP

class NoAtribuicao:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

class NoSe:
    def __init__(self, nome_var, operador, valor_comp, mensagem):
        self.nome_var = nome_var
        self.operador = operador
        self.valor_comp = valor_comp
        self.mensagem = mensagem

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        nos = []
        # O loop continua enquanto não chegar no fim dos tokens
        while self.pos < len(self.tokens) and self.tokens[self.pos].tipo != T_EOF:
            token_atual = self.tokens[self.pos]
            
            # Caso 1: Atribuição (ex: pontos = 100)
            if token_atual.tipo == T_ID and (self.pos + 1) < len(self.tokens) and self.tokens[self.pos+1].tipo == T_ATR:
                nome = token_atual.valor
                valor = self.tokens[self.pos+2].valor
                nos.append(NoAtribuicao(nome, int(valor)))
                self.pos += 3
            
            # Caso 2: Estrutura SE (ex: se pontos > 50 "Ganhou")
            elif token_atual.tipo == T_SE:
                v_nome = self.tokens[self.pos+1].valor
                op = self.tokens[self.pos+2].valor
                v_comp = int(self.tokens[self.pos+3].valor)
                msg = self.tokens[self.pos+4].valor 
                nos.append(NoSe(v_nome, op, v_comp, msg))
                self.pos += 5
            
            else:
                self.pos += 1
        return nos
