# Tipos de Tokens
T_INT    = 'INT'
T_STR    = 'STRING'
T_ID     = 'ID'
T_OP     = 'OP'
T_ATR    = 'ATR'
T_SE     = 'SE'
T_SENAO  = 'SENAO'
T_S_OU   = 'SENOUSE'
T_EOF    = 'EOF'

class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"[{self.tipo}:{self.valor}]" if self.valor else f"[{self.tipo}]"
