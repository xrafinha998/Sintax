import re
from src.tokens import *

class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.tokens = []

    def gerar_tokens(self):
        # Expressões regulares para identificar cada parte
        padroes = [
            (r'se\b', T_SE),
            (r'senouse\b', T_S_OU),
            (r'senao\b', T_SENAO),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', T_ID),
            (r'\d+', T_INT),
            (r'==|>=|<=|<|>', T_OP),
            (r'=', T_ATR),
            (r'\".*?\"', T_STR),
        ]

        # Limpeza e tokenização simples
        texto_limpo = self.texto.replace('(', ' ( ').replace(')', ' ) ')
        palavras = re.findall(r'\".*?\"|\S+', texto_limpo)

        for p in palavras:
            match_found = False
            for padrao, tipo in padroes:
                if re.fullmatch(padrao, p):
                    valor = p.replace('"', '') if tipo == T_STR else p
                    self.tokens.append(Token(tipo, valor))
                    match_found = True
                    break
        
        self.tokens.append(Token(T_EOF))
        return self.tokens

