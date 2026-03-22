# ============================================================
#  SINTAX — Tokens v4.0  (linguagem geral)
# ============================================================

# ── Literais ─────────────────────────────────────────────────
T_INT    = "INT"
T_FLOAT  = "FLOAT"
T_STR    = "STR"
T_BOOL   = "BOOL"
T_NULO   = "NULO"

# ── Identificador ─────────────────────────────────────────────
T_ID     = "ID"

# ── Palavras-chave ────────────────────────────────────────────
T_SE        = "SE"           # se
T_SENAO     = "SENAO"        # senao
T_SENOUSE   = "SENOUSE"      # senao se
T_ENQUANTO  = "ENQUANTO"     # enquanto
T_PARA      = "PARA"         # para
T_EM        = "EM"           # em          (for-each)
T_DE        = "DE"           # de          (range start)
T_ATE       = "ATE"          # ate         (range end)
T_PASSO     = "PASSO"        # passo       (range step)
T_FUNC      = "FUNC"         # func
T_RETURN    = "RETURN"       # return / retorne
T_PRINT     = "PRINT"        # print
T_IMPORT    = "IMPORT"       # import
T_COMO      = "COMO"         # como        (import ... como alias)
T_GLOBAL    = "GLOBAL"       # global
T_PARE      = "PARE"         # pare
T_CONTINUA  = "CONTINUA"     # continua
T_DELETE    = "DELETE"       # delete

# ── Operadores aritméticos ────────────────────────────────────
T_SOMA   = "SOMA"    # +
T_SUB    = "SUB"     # -
T_MULT   = "MULT"    # *
T_DIV    = "DIV"     # /
T_DIVINT = "DIVINT"  # //
T_MOD    = "MOD"     # %
T_POT    = "POT"     # **

# ── Comparação ────────────────────────────────────────────────
T_EQ  = "EQ"    # ==
T_NEQ = "NEQ"   # !=
T_GT  = "GT"    # >
T_LT  = "LT"    # <
T_GTE = "GTE"   # >=
T_LTE = "LTE"   # <=

# ── Lógicos ───────────────────────────────────────────────────
T_E   = "E"     # e / and
T_OU  = "OU"    # ou / or
T_NAO = "NAO"   # nao / not

# ── Atribuição ────────────────────────────────────────────────
T_ATR      = "ATR"       # =
T_ATR_SOMA = "ATR_SOMA"  # +=
T_ATR_SUB  = "ATR_SUB"   # -=
T_ATR_MULT = "ATR_MULT"  # *=
T_ATR_DIV  = "ATR_DIV"   # /=
T_ATR_MOD  = "ATR_MOD"   # %=

# ── Delimitadores ─────────────────────────────────────────────
T_LPAREN   = "LPAREN"    # (
T_RPAREN   = "RPAREN"    # )
T_LBRACE   = "LBRACE"    # {
T_RBRACE   = "RBRACE"    # }
T_LBRACKET = "LBRACKET"  # [
T_RBRACKET = "RBRACKET"  # ]
T_COMMA    = "COMMA"     # ,
T_COLON    = "COLON"     # :
T_PONTO    = "PONTO"     # .
T_PONTO2   = "PONTO2"    # ..   (range inclusivo futuro)

# ── Controle ──────────────────────────────────────────────────
T_NEWLINE  = "NEWLINE"
T_EOF      = "EOF"


# ── Classe Token ──────────────────────────────────────────────
class Token:
    __slots__ = ("tipo", "valor", "linha", "col", "arquivo")

    def __init__(self, tipo, valor=None, linha=1, col=0, arquivo="<stdin>"):
        self.tipo    = tipo
        self.valor   = valor
        self.linha   = linha
        self.col     = col
        self.arquivo = arquivo

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r}, L{self.linha}:{self.col})"

    @property
    def pos(self):
        return f"{self.arquivo}:{self.linha}:{self.col}"
