import re
from src.tokens import *

class Lexer:
    def __init__(self, texto):
        self.texto = texto

    def gerar_tokens(self):
        padroes = [
            (r'senouse\b', T_S_OU), (r'senao\b', T_SENAO), (r'se\b', T_SE),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', T_ID), (r'\d+', T_INT),
            (r'==|>=|<=|<|>', T_OP), (r'\+', T_SOMA), (r'-', T_SUB),
            (r'=', T_ATR), (r'\".*?\"', T_STR),
        ]
        
        # Ajuste para não quebrar em parênteses
        tokens_encontrados = []
        palavras = re.findall(r'\".*?\"|[a-zA-Z_]\w*|==|>=|<=|[><=+\-]|\d+', self.texto)

        for p in palavras:
            for padrao, tipo in padroes:
                if re.fullmatch(padrao, p):
                    valor = p.replace('"', '') if tipo == T_STR else p
                    tokens_encontrados.append(Token(tipo, valor))
                    break
        
        tokens_encontrados.append(Token(T_EOF))
        return tokens_encontrados
