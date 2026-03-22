# TIPOS DE TOKEN

T_ID = "ID"
T_INT = "INT"
T_STR = "STR"

T_SE = "SE"
T_SENAO = "SENAO"
T_S_OU = "SENOUSE"

T_OP = "OP"

T_SOMA = "SOMA"
T_SUB = "SUB"
T_MULT = "MULT"
T_DIV = "DIV"

T_ATR = "ATR"

T_LPAREN = "LPAREN"
T_RPAREN = "RPAREN"

T_EOF = "EOF"


# CLASSE TOKEN
class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"{self.tipo}:{self.valor}"
