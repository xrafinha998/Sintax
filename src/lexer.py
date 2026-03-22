# ============================================================
#  SINTAX — Lexer v4.0
# ============================================================
from src.tokens import *

# Palavras-chave aceitas em português e inglês
KEYWORDS = {
    # Controle de fluxo
    "se":       T_SE,
    "if":       T_SE,
    "senao":    T_SENAO,
    "else":     T_SENAO,
    "enquanto": T_ENQUANTO,
    "while":    T_ENQUANTO,
    "para":     T_PARA,
    "for":      T_PARA,
    "em":       T_EM,
    "in":       T_EM,
    "de":       T_DE,
    "ate":      T_ATE,
    "to":       T_ATE,
    "passo":    T_PASSO,
    "step":     T_PASSO,
    "pare":     T_PARE,
    "break":    T_PARE,
    "continua": T_CONTINUA,
    "continue": T_CONTINUA,

    # Funções
    "func":     T_FUNC,
    "def":      T_FUNC,
    "return":   T_RETURN,
    "retorne":  T_RETURN,

    # I/O
    "print":    T_PRINT,
    "imprima":  T_PRINT,

    # Módulos
    "import":   T_IMPORT,
    "importar": T_IMPORT,
    "como":     T_COMO,
    "as":       T_COMO,

    # Escopo
    "global":   T_GLOBAL,
    "delete":   T_DELETE,

    # Literais especiais
    "true":       (T_BOOL, True),
    "verdadeiro": (T_BOOL, True),
    "false":      (T_BOOL, False),
    "falso":      (T_BOOL, False),
    "nulo":       (T_NULO, None),
    "null":       (T_NULO, None),
    "none":       (T_NULO, None),

    # Lógicos
    "e":    T_E,
    "and":  T_E,
    "ou":   T_OU,
    "or":   T_OU,
    "nao":  T_NAO,
    "not":  T_NAO,

    # Condicional encadeada
    "senao se":   T_SENOUSE,   # tratado no lexer como dois tokens normalmente
}

# Tokens que fazem NEWLINE ser suprimido após eles
_SEM_NL_APOS = {
    T_COMMA, T_LBRACE, T_LPAREN, T_LBRACKET,
    T_ATR, T_ATR_SOMA, T_ATR_SUB, T_ATR_MULT, T_ATR_DIV, T_ATR_MOD,
    T_SOMA, T_SUB, T_MULT, T_DIV, T_DIVINT, T_MOD, T_POT,
    T_EQ, T_NEQ, T_GT, T_LT, T_GTE, T_LTE,
    T_E, T_OU, T_NAO, T_PONTO,
}


class LexError(Exception):
    def __init__(self, msg, arquivo, linha, col):
        self.msg     = msg
        self.arquivo = arquivo
        self.linha   = linha
        self.col     = col
        super().__init__(
            f"\n╔══ ERRO LÉXICO ══════════════════════════\n"
            f"║  {arquivo}:{linha}:{col}\n"
            f"╚► {msg}"
        )


class Lexer:
    def __init__(self, texto, arquivo="<stdin>"):
        self.texto   = texto
        self.arquivo = arquivo
        self.pos     = 0
        self.linha   = 1
        self.col     = 1
        # profundidade de ( ) [ ] — dentro deles, newlines são ignoradas
        self._profundidade = 0

    # ── Navegação ─────────────────────────────────────────────
    def _c(self, offset=0):
        i = self.pos + offset
        return self.texto[i] if i < len(self.texto) else ""

    def _avanca(self):
        c = self.texto[self.pos] if self.pos < len(self.texto) else ""
        self.pos += 1
        if c == "\n":
            self.linha += 1
            self.col    = 1
        else:
            self.col += 1
        return c

    def _tok(self, tipo, valor=None):
        return Token(tipo, valor, self.linha, self.col, self.arquivo)

    def _erro(self, msg):
        raise LexError(msg, self.arquivo, self.linha, self.col)

    # ── Leitores especializados ───────────────────────────────
    def _string(self):
        linha, col = self.linha, self.col
        self._avanca()   # pula "
        resultado = ""
        while self.pos < len(self.texto) and self._c() != '"':
            if self._c() == "\\":
                self._avanca()
                ESC = {"n": "\n", "t": "\t", '"': '"',
                       "\\": "\\", "r": "\r", "0": "\0"}
                resultado += ESC.get(self._c(), self._c())
                self._avanca()
            else:
                resultado += self._avanca()
        if self.pos >= len(self.texto):
            raise LexError("String não fechada", self.arquivo, linha, col)
        self._avanca()   # pula "
        return Token(T_STR, resultado, linha, col, self.arquivo)

    def _numero(self):
        linha, col = self.linha, self.col
        num = ""
        while self.pos < len(self.texto) and self._c().isdigit():
            num += self._avanca()
        # ponto decimal
        if self._c() == "." and self._c(1).isdigit():
            num += self._avanca()   # ponto
            while self.pos < len(self.texto) and self._c().isdigit():
                num += self._avanca()
            return Token(T_FLOAT, float(num), linha, col, self.arquivo)
        return Token(T_INT, int(num), linha, col, self.arquivo)

    def _identificador(self):
        linha, col = self.linha, self.col
        ident = ""
        while self.pos < len(self.texto) and (self._c().isalnum() or self._c() == "_"):
            ident += self._avanca()

        kw = KEYWORDS.get(ident)
        if kw is None:
            return Token(T_ID, ident, linha, col, self.arquivo)
        if isinstance(kw, tuple):
            tipo, val = kw
            return Token(tipo, val, linha, col, self.arquivo)
        return Token(kw, ident, linha, col, self.arquivo)

    # ── Principal ─────────────────────────────────────────────
    def tokenizar(self):
        tokens  = []
        ultimo  = lambda: tokens[-1].tipo if tokens else None

        def emit(tok):
            tokens.append(tok)

        def emit_nl():
            if self._profundidade == 0 and ultimo() not in (
                _SEM_NL_APOS | {T_NEWLINE, None}
            ):
                tokens.append(self._tok(T_NEWLINE, "\n"))

        while self.pos < len(self.texto):
            c = self._c()

            # Espaços / tabs
            if c in " \t\r":
                self._avanca(); continue

            # Quebra de linha
            if c == "\n":
                emit_nl()
                self._avanca(); continue

            # Comentário de linha (#)
            if c == "#":
                while self.pos < len(self.texto) and self._c() != "\n":
                    self._avanca()
                continue

            # Comentário de bloco /* ... */
            if c == "/" and self._c(1) == "*":
                self._avanca(); self._avanca()
                while self.pos < len(self.texto) - 1:
                    if self._c() == "*" and self._c(1) == "/":
                        self._avanca(); self._avanca(); break
                    self._avanca()
                continue

            # String
            if c == '"':
                emit(self._string()); continue

            # String com aspas simples
            if c == "'":
                self._avanca()
                s = ""
                while self.pos < len(self.texto) and self._c() != "'":
                    if self._c() == "\\":
                        self._avanca()
                        ESC = {"n": "\n", "t": "\t", "'": "'", "\\": "\\"}
                        s += ESC.get(self._c(), self._c())
                        self._avanca()
                    else:
                        s += self._avanca()
                if self.pos >= len(self.texto):
                    self._erro("String (aspas simples) não fechada")
                self._avanca()
                emit(self._tok(T_STR, s)); continue

            # Número
            if c.isdigit():
                emit(self._numero()); continue

            # Identificador / palavra-chave
            if c.isalpha() or c == "_":
                emit(self._identificador()); continue

            # ── Operadores multi-char (ordem importa!) ────────
            dois = c + self._c(1)

            if dois == "**": emit(self._tok(T_POT,     "**")); self._avanca(); self._avanca(); continue
            if dois == "//": emit(self._tok(T_DIVINT,  "//")); self._avanca(); self._avanca(); continue
            if dois == "==": emit(self._tok(T_EQ,      "==")); self._avanca(); self._avanca(); continue
            if dois == "!=": emit(self._tok(T_NEQ,     "!=")); self._avanca(); self._avanca(); continue
            if dois == "<=": emit(self._tok(T_LTE,     "<=")); self._avanca(); self._avanca(); continue
            if dois == ">=": emit(self._tok(T_GTE,     ">=")); self._avanca(); self._avanca(); continue
            if dois == "+=": emit(self._tok(T_ATR_SOMA,"+=")); self._avanca(); self._avanca(); continue
            if dois == "-=": emit(self._tok(T_ATR_SUB, "-=")); self._avanca(); self._avanca(); continue
            if dois == "*=": emit(self._tok(T_ATR_MULT,"*=")); self._avanca(); self._avanca(); continue
            if dois == "/=": emit(self._tok(T_ATR_DIV, "/=")); self._avanca(); self._avanca(); continue
            if dois == "%=": emit(self._tok(T_ATR_MOD, "%=")); self._avanca(); self._avanca(); continue

            # ── Char único ────────────────────────────────────
            SIMPLES = {
                "+": T_SOMA,  "-": T_SUB,  "*": T_MULT,
                "/": T_DIV,   "%": T_MOD,
                "<": T_LT,    ">": T_GT,   "=": T_ATR,
                ",": T_COMMA, ":": T_COLON, ".": T_PONTO,
            }
            if c in SIMPLES:
                emit(self._tok(SIMPLES[c], c)); self._avanca(); continue

            # Delimitadores com rastreamento de profundidade
            if c == "(":
                self._profundidade += 1
                emit(self._tok(T_LPAREN,   "(")); self._avanca(); continue
            if c == ")":
                self._profundidade = max(0, self._profundidade - 1)
                emit(self._tok(T_RPAREN,   ")")); self._avanca(); continue
            if c == "[":
                self._profundidade += 1
                emit(self._tok(T_LBRACKET, "[")); self._avanca(); continue
            if c == "]":
                self._profundidade = max(0, self._profundidade - 1)
                emit(self._tok(T_RBRACKET, "]")); self._avanca(); continue
            if c == "{":
                emit(self._tok(T_LBRACE,   "{")); self._avanca(); continue
            if c == "}":
                # Fecha bloco → emite NEWLINE antes se necessário
                if self._profundidade == 0 and ultimo() not in (T_NEWLINE, T_LBRACE, None):
                    tokens.append(self._tok(T_NEWLINE, "\n"))
                emit(self._tok(T_RBRACE,   "}")); self._avanca(); continue

            self._erro(f"Caractere inesperado: '{c}'")

        # EOF
        emit_nl()
        emit(self._tok(T_EOF))
        return tokens
