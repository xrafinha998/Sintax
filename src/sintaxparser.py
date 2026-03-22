# ============================================================
#  SINTAX — Parser v4.0
# ============================================================
from src.tokens import *

# ─────────────────────────────────────────────────────────────
#  NÓS DA AST
# ─────────────────────────────────────────────────────────────

class No:
    """Base para todos os nós."""
    linha = 0
    col   = 0

    def __init__(self, linha=0, col=0):
        self.linha = linha
        self.col   = col


# ── Literais ──────────────────────────────────────────────────
class NoInt(No):
    def __init__(self, v, l=0, c=0): super().__init__(l,c); self.valor=v
class NoFloat(No):
    def __init__(self, v, l=0, c=0): super().__init__(l,c); self.valor=v
class NoStr(No):
    def __init__(self, v, l=0, c=0): super().__init__(l,c); self.valor=v
class NoBool(No):
    def __init__(self, v, l=0, c=0): super().__init__(l,c); self.valor=v
class NoNulo(No):
    pass
class NoLista(No):
    def __init__(self, els, l=0, c=0): super().__init__(l,c); self.elementos=els
class NoDict(No):
    def __init__(self, pares, l=0, c=0): super().__init__(l,c); self.pares=pares

# ── Identificadores e acesso ──────────────────────────────────
class NoVar(No):
    def __init__(self, nome, l=0, c=0): super().__init__(l,c); self.nome=nome
class NoProp(No):
    def __init__(self, obj, prop, l=0, c=0):
        super().__init__(l,c); self.obj=obj; self.prop=prop
class NoIndice(No):
    def __init__(self, alvo, idx, l=0, c=0):
        super().__init__(l,c); self.alvo=alvo; self.idx=idx

# ── Operações ─────────────────────────────────────────────────
class NoBinOp(No):
    def __init__(self, esq, op, dir, l=0, c=0):
        super().__init__(l,c); self.esq=esq; self.op=op; self.dir=dir
class NoUnOp(No):
    def __init__(self, op, operando, l=0, c=0):
        super().__init__(l,c); self.op=op; self.operando=operando

# ── Chamadas ──────────────────────────────────────────────────
class NoChamada(No):
    def __init__(self, func, args, kwargs=None, l=0, c=0):
        super().__init__(l,c); self.func=func; self.args=args
        self.kwargs = kwargs or {}
class NoMetodo(No):
    def __init__(self, obj, metodo, args, l=0, c=0):
        super().__init__(l,c); self.obj=obj; self.metodo=metodo; self.args=args

# ── Atribuições ───────────────────────────────────────────────
class NoAtrib(No):
    def __init__(self, alvo, valor, op="=", l=0, c=0):
        super().__init__(l,c); self.alvo=alvo; self.valor=valor; self.op=op
# alvo pode ser NoVar, NoProp ou NoIndice

# ── Controle de fluxo ─────────────────────────────────────────
class NoPrint(No):
    def __init__(self, exprs, fim="\n", l=0, c=0):
        super().__init__(l,c); self.exprs=exprs; self.fim=fim
class NoSe(No):
    def __init__(self, ramos, senao, l=0, c=0):
        # ramos = [(condicao, bloco), ...]
        super().__init__(l,c); self.ramos=ramos; self.senao=senao
class NoEnquanto(No):
    def __init__(self, cond, bloco, l=0, c=0):
        super().__init__(l,c); self.cond=cond; self.bloco=bloco
class NoPara(No):
    """para var em iteravel"""
    def __init__(self, var, iteravel, bloco, l=0, c=0):
        super().__init__(l,c); self.var=var; self.iteravel=iteravel; self.bloco=bloco
class NoParaRange(No):
    """para var ate N  /  para var de A ate B  /  ...passo P"""
    def __init__(self, var, inicio, fim, passo, bloco, l=0, c=0):
        super().__init__(l,c)
        self.var=var; self.inicio=inicio; self.fim=fim
        self.passo=passo; self.bloco=bloco
class NoPare(No): pass
class NoContinua(No): pass
class NoReturn(No):
    def __init__(self, expr, l=0, c=0):
        super().__init__(l,c); self.expr=expr
class NoDelete(No):
    def __init__(self, alvo, l=0, c=0):
        super().__init__(l,c); self.alvo=alvo

# ── Definições ────────────────────────────────────────────────
class NoFuncDef(No):
    def __init__(self, nome, params, bloco, l=0, c=0):
        # params = [(nome, default_ou_None), ...]
        super().__init__(l,c)
        self.nome=nome; self.params=params; self.bloco=bloco
class NoImport(No):
    def __init__(self, modulo, alias, l=0, c=0):
        super().__init__(l,c); self.modulo=modulo; self.alias=alias
class NoGlobal(No):
    def __init__(self, nomes, l=0, c=0):
        super().__init__(l,c); self.nomes=nomes


# ─────────────────────────────────────────────────────────────
#  PARSER
# ─────────────────────────────────────────────────────────────

class ParseError(Exception):
    def __init__(self, msg, tok):
        self.msg = msg
        self.tok = tok
        super().__init__(
            f"\n╔══ ERRO DE SINTAXE ══════════════════════\n"
            f"║  {tok.pos}\n"
            f"╚► {msg}"
        )


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t.tipo != T_NEWLINE or True]
        self._tokens_filtrados = tokens
        self.pos    = 0

    # ── Navegação ─────────────────────────────────────────────
    def _at(self, offset=0):
        i = self.pos + offset
        return self.tokens[i] if i < len(self.tokens) else self.tokens[-1]

    def _avancar(self):
        t = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return t

    def _consumir(self, tipo, msg=None):
        t = self._at()
        if t.tipo != tipo:
            raise ParseError(
                msg or f"Esperava '{tipo}', encontrei '{t.tipo}' ('{t.valor}')", t
            )
        return self._avancar()

    def _pular_nl(self):
        while self._at().tipo == T_NEWLINE:
            self._avancar()

    def _consumir_nl(self):
        if self._at().tipo in (T_NEWLINE, T_EOF):
            if self._at().tipo == T_NEWLINE:
                self._avancar()

    def _espiar(self, skip_nl=True):
        """Olha para o próximo token não-newline."""
        i = self.pos
        while i < len(self.tokens):
            t = self.tokens[i]
            if t.tipo == T_NEWLINE and skip_nl:
                i += 1
            else:
                return t
        return self.tokens[-1]

    # ── Entrada ───────────────────────────────────────────────
    def parse(self):
        nos = []
        self._pular_nl()
        while self._at().tipo != T_EOF:
            nos.append(self._instrucao())
            self._pular_nl()
        return nos

    # ── Instrução ─────────────────────────────────────────────
    def _instrucao(self):
        t = self._at()

        if t.tipo == T_PRINT:   return self._print()
        if t.tipo == T_IMPORT:  return self._import()
        if t.tipo == T_FUNC:    return self._func_def()
        if t.tipo == T_RETURN:  return self._return()
        if t.tipo == T_SE:      return self._se()
        if t.tipo == T_ENQUANTO:return self._enquanto()
        if t.tipo == T_PARA:    return self._para()
        if t.tipo == T_GLOBAL:  return self._global()
        if t.tipo == T_DELETE:  return self._delete()

        if t.tipo == T_PARE:
            self._avancar(); self._consumir_nl()
            return NoPare(t.linha, t.col)
        if t.tipo == T_CONTINUA:
            self._avancar(); self._consumir_nl()
            return NoContinua(t.linha, t.col)

        # Atribuição ou expressão-instrução
        return self._atrib_ou_expr()

    def _print(self):
        t = self._avancar()   # consome 'print'
        exprs = []
        if self._at().tipo not in (T_NEWLINE, T_EOF):
            exprs.append(self._expr())
            while self._at().tipo == T_COMMA:
                self._avancar()
                exprs.append(self._expr())
        self._consumir_nl()
        return NoPrint(exprs, "\n", t.linha, t.col)

    def _import(self):
        t = self._avancar()
        nome = self._consumir(T_ID, "Esperava nome do módulo após 'import'").valor
        alias = None
        if self._at().tipo == T_COMO:
            self._avancar()
            alias = self._consumir(T_ID).valor
        self._consumir_nl()
        return NoImport(nome, alias, t.linha, t.col)

    def _func_def(self):
        t = self._avancar()   # func
        nome = self._consumir(T_ID, "Esperava nome da função").valor
        self._consumir(T_LPAREN)
        params = []
        if self._at().tipo != T_RPAREN:
            params.append(self._param())
            while self._at().tipo == T_COMMA:
                self._avancar()
                params.append(self._param())
        self._consumir(T_RPAREN)
        self._pular_nl()
        bloco = self._bloco()
        return NoFuncDef(nome, params, bloco, t.linha, t.col)

    def _param(self):
        nome = self._consumir(T_ID).valor
        default = None
        if self._at().tipo == T_ATR:
            self._avancar()
            default = self._expr()
        return (nome, default)

    def _return(self):
        t = self._avancar()
        expr = None
        if self._at().tipo not in (T_NEWLINE, T_EOF, T_RBRACE):
            expr = self._expr()
        self._consumir_nl()
        return NoReturn(expr, t.linha, t.col)

    def _se(self):
        t   = self._avancar()   # se
        ramos = []
        cond  = self._expr()
        self._pular_nl()
        bloco = self._bloco()
        ramos.append((cond, bloco))

        senao = None
        while True:
            self._pular_nl()
            # "senao se" ou "else if"
            if self._at().tipo == T_SENAO:
                prox = self._at(1)
                if prox.tipo == T_SE:
                    self._avancar(); self._avancar()   # consome senao se
                    c2 = self._expr()
                    self._pular_nl()
                    b2 = self._bloco()
                    ramos.append((c2, b2))
                    continue
                else:
                    self._avancar()   # consome senao
                    self._pular_nl()
                    senao = self._bloco()
            break

        return NoSe(ramos, senao, t.linha, t.col)

    def _enquanto(self):
        t = self._avancar()
        cond = self._expr()
        self._pular_nl()
        bloco = self._bloco()
        return NoEnquanto(cond, bloco, t.linha, t.col)

    def _para(self):
        t   = self._avancar()   # para
        var = self._consumir(T_ID, "Esperava nome de variável após 'para'").valor

        # para var em iteravel { }
        if self._at().tipo == T_EM:
            self._avancar()
            iteravel = self._expr()
            self._pular_nl()
            bloco = self._bloco()
            return NoPara(var, iteravel, bloco, t.linha, t.col)

        # para var ate N { }
        if self._at().tipo == T_ATE:
            self._avancar()
            fim   = self._expr()
            passo = None
            if self._at().tipo == T_PASSO:
                self._avancar(); passo = self._expr()
            self._pular_nl()
            bloco = self._bloco()
            return NoParaRange(var, None, fim, passo, bloco, t.linha, t.col)

        # para var N { }  (atalho: para i 10 == para i ate 10)
        if self._at().tipo in (T_INT, T_FLOAT, T_ID, T_LPAREN):
            fim   = self._expr()
            passo = None
            if self._at().tipo == T_PASSO:
                self._avancar(); passo = self._expr()
            self._pular_nl()
            bloco = self._bloco()
            return NoParaRange(var, None, fim, passo, bloco, t.linha, t.col)

        # para var de A ate B [passo P] { }
        if self._at().tipo == T_DE:
            self._avancar()
            inicio = self._expr()
            self._consumir(T_ATE, "Esperava 'ate' após valor inicial")
            fim    = self._expr()
            passo  = None
            if self._at().tipo == T_PASSO:
                self._avancar(); passo = self._expr()
            self._pular_nl()
            bloco = self._bloco()
            return NoParaRange(var, inicio, fim, passo, bloco, t.linha, t.col)

        raise ParseError(
            "Esperava 'em', 'ate', 'de' ou número após variável do 'para'",
            self._at()
        )

    def _global(self):
        t = self._avancar()
        nomes = [self._consumir(T_ID).valor]
        while self._at().tipo == T_COMMA:
            self._avancar()
            nomes.append(self._consumir(T_ID).valor)
        self._consumir_nl()
        return NoGlobal(nomes, t.linha, t.col)

    def _delete(self):
        t = self._avancar()
        alvo = self._sufixo(self._primario())
        self._consumir_nl()
        return NoDelete(alvo, t.linha, t.col)

    def _atrib_ou_expr(self):
        """Atribuição (simples ou composta) ou expressão-instrução."""
        t = self._at()
        expr = self._expr()
        OPS = {
            T_ATR: "=", T_ATR_SOMA: "+=", T_ATR_SUB: "-=",
            T_ATR_MULT: "*=", T_ATR_DIV: "/=", T_ATR_MOD: "%=",
        }
        if self._at().tipo in OPS:
            op  = OPS[self._avancar().tipo]
            val = self._expr()
            self._consumir_nl()
            return NoAtrib(expr, val, op, t.linha, t.col)
        self._consumir_nl()
        return expr   # expressão como instrução (ex: chamada de função)

    # ── Bloco { } ─────────────────────────────────────────────
    def _bloco(self):
        self._consumir(T_LBRACE, "Esperava '{' para abrir bloco")
        self._pular_nl()
        nos = []
        while self._at().tipo not in (T_RBRACE, T_EOF):
            nos.append(self._instrucao())
            self._pular_nl()
        self._consumir(T_RBRACE, "Esperava '}' para fechar bloco")
        self._pular_nl()
        return nos

    # ── Expressões (precedência Pratt-style) ──────────────────
    def _expr(self):          return self._ou()
    def _ou(self):
        esq = self._e()
        while self._at().tipo == T_OU:
            op=self._avancar(); esq=NoBinOp(esq,"ou",self._e(),op.linha,op.col)
        return esq
    def _e(self):
        esq = self._nao()
        while self._at().tipo == T_E:
            op=self._avancar(); esq=NoBinOp(esq,"e",self._nao(),op.linha,op.col)
        return esq
    def _nao(self):
        if self._at().tipo == T_NAO:
            t=self._avancar(); return NoUnOp("nao",self._nao(),t.linha,t.col)
        return self._comp()
    def _comp(self):
        esq = self._soma()
        OPS = {T_EQ:"==", T_NEQ:"!=", T_GT:">", T_LT:"<", T_GTE:">=", T_LTE:"<="}
        if self._at().tipo in OPS:
            t=self._avancar(); op=OPS[t.tipo]
            return NoBinOp(esq, op, self._soma(), t.linha, t.col)
        return esq
    def _soma(self):
        esq = self._mult()
        while self._at().tipo in (T_SOMA, T_SUB):
            t=self._avancar()
            esq=NoBinOp(esq, t.valor, self._mult(), t.linha, t.col)
        return esq
    def _mult(self):
        esq = self._pot()
        while self._at().tipo in (T_MULT, T_DIV, T_DIVINT, T_MOD):
            t=self._avancar()
            esq=NoBinOp(esq, t.valor, self._pot(), t.linha, t.col)
        return esq
    def _pot(self):
        base = self._unario()
        if self._at().tipo == T_POT:
            t=self._avancar()
            return NoBinOp(base, "**", self._pot(), t.linha, t.col)  # dir-assoc
        return base
    def _unario(self):
        if self._at().tipo == T_SUB:
            t=self._avancar(); return NoUnOp("-", self._unario(), t.linha, t.col)
        if self._at().tipo == T_NAO:
            t=self._avancar(); return NoUnOp("nao", self._unario(), t.linha, t.col)
        return self._sufixo(self._primario())

    def _sufixo(self, no):
        """Índice, propriedade, chamada."""
        while True:
            t = self._at()
            if t.tipo == T_LBRACKET:
                self._avancar()
                idx = self._expr()
                self._consumir(T_RBRACKET)
                no = NoIndice(no, idx, t.linha, t.col)
            elif t.tipo == T_PONTO:
                self._avancar()
                prop = self._consumir(T_ID).valor
                if self._at().tipo == T_LPAREN:
                    self._avancar()
                    args = self._args()
                    self._consumir(T_RPAREN)
                    no = NoMetodo(no, prop, args, t.linha, t.col)
                else:
                    no = NoProp(no, prop, t.linha, t.col)
            elif t.tipo == T_LPAREN:
                if isinstance(no, NoVar):
                    self._avancar()
                    args = self._args()
                    self._consumir(T_RPAREN)
                    no = NoChamada(no, args, {}, t.linha, t.col)
                else:
                    break
            else:
                break
        return no

    def _primario(self):
        t = self._at()
        if t.tipo == T_INT:    self._avancar(); return NoInt(t.valor,   t.linha, t.col)
        if t.tipo == T_FLOAT:  self._avancar(); return NoFloat(t.valor, t.linha, t.col)
        if t.tipo == T_STR:    self._avancar(); return NoStr(t.valor,   t.linha, t.col)
        if t.tipo == T_BOOL:   self._avancar(); return NoBool(t.valor,  t.linha, t.col)
        if t.tipo == T_NULO:   self._avancar(); return NoNulo(t.linha, t.col)
        if t.tipo == T_ID:     self._avancar(); return NoVar(t.valor,   t.linha, t.col)

        # Lista [ ... ]
        if t.tipo == T_LBRACKET:
            self._avancar()
            self._pular_nl()
            els = []
            if self._at().tipo != T_RBRACKET:
                els.append(self._expr())
                while self._at().tipo == T_COMMA:
                    self._avancar()
                    self._pular_nl()
                    if self._at().tipo == T_RBRACKET: break
                    els.append(self._expr())
            self._pular_nl()
            self._consumir(T_RBRACKET)
            return NoLista(els, t.linha, t.col)

        # Dict { chave: valor, ... }
        if t.tipo == T_LBRACE:
            return self._dict_literal()

        # Parênteses
        if t.tipo == T_LPAREN:
            self._avancar()
            expr = self._expr()
            self._consumir(T_RPAREN)
            return expr

        raise ParseError(f"Expressão inesperada: '{t.valor}' (tipo {t.tipo})", t)

    def _dict_literal(self):
        t = self._avancar()   # {
        self._pular_nl()
        pares = []
        if self._at().tipo != T_RBRACE:
            pares.append(self._par_dict())
            while self._at().tipo == T_COMMA:
                self._avancar()
                self._pular_nl()
                if self._at().tipo == T_RBRACE: break
                pares.append(self._par_dict())
        self._pular_nl()
        self._consumir(T_RBRACE)
        return NoDict(pares, t.linha, t.col)

    def _par_dict(self):
        chave = self._expr()
        self._consumir(T_COLON, "Esperava ':' após chave do dicionário")
        valor = self._expr()
        return (chave, valor)

    def _args(self):
        args = []
        self._pular_nl()
        if self._at().tipo == T_RPAREN:
            return args
        args.append(self._expr())
        while self._at().tipo == T_COMMA:
            self._avancar()
            self._pular_nl()
            if self._at().tipo == T_RPAREN: break
            args.append(self._expr())
        return args
