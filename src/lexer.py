import re
from src.tokens import *

class Lexer:
    def __init__(self, texto):
        self.texto = texto

    def gerar_tokens(self):
        padroes = [
            (r'senouse\b', T_S_OU),
            (r'senao\b', T_SENAO),
            (r'se\b', T_SE),

            (r'==|>=|<=|!=|<|>', T_OP),

            (r'\+', T_SOMA),
            (r'-', T_SUB),
            (r'\*', T_MULT),
            (r'/', T_DIV),

            (r'\(', T_LPAREN),
            (r'\)', T_RPAREN),

            (r'=', T_ATR),

            (r'\d+', T_INT),
            (r'"[^"]*"', T_STR),

            (r'[a-zA-Z_][a-zA-Z0-9_]*', T_ID),
        ]

        tokens = []

        palavras = re.findall(
            r'"[^"]*"|[a-zA-Z_]\w*|==|>=|<=|!=|[()><=+\-*/]|\d+',
            self.texto
        )

        for p in palavras:
            for padrao, tipo in padroes:
                if re.fullmatch(padrao, p):
                    valor = p.replace('"', '') if tipo == T_STR else p
                    tokens.append(Token(tipo, valor))
                    break
            else:
                raise Exception(f"Token inválido: {p}")

        tokens.append(Token(T_EOF))
        return tokens
