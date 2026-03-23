# ============================================================
#  SINTAX — Interpreter v4.0
# ============================================================
import os, sys, math as _math, random as _random, time as _time
import json as _json

from sintax.parser import (
    NoInt, NoFloat, NoStr, NoBool, NoNulo, NoLista, NoDict,
    NoVar, NoProp, NoIndice, NoBinOp, NoUnOp,
    NoChamada, NoMetodo, NoAtrib,
    NoPrint, NoSe, NoEnquanto, NoPara, NoParaRange,
    NoPare, NoContinua, NoReturn, NoDelete,
    NoFuncDef, NoImport, NoGlobal,
)

# ── Controle de fluxo ────────────────────────────────────────
class _Retorno(Exception):
    def __init__(self, v): self.valor = v
class _Pare(Exception):    pass
class _Continua(Exception):pass


# ── Erros de runtime ─────────────────────────────────────────
class SintaxRuntimeError(Exception):
    def __init__(self, msg, no=None, stack=None):
        self.msg   = msg
        self.no    = no
        self.stack = stack or []
        linhas = ["\n╔══ ERRO DE EXECUÇÃO ══════════════════════"]
        for frame in reversed(self.stack):
            linhas.append(f"║  em '{frame[0]}'  linha {frame[1]}")
        if no:
            linhas.append(f"║  linha {no.linha}")
        linhas.append(f"╚► {msg}")
        super().__init__("\n".join(linhas))


# ── Objeto Sintax (dicionário com acesso .campo) ─────────────
class SObj:
    """Objeto genérico — campos acessados por ponto."""
    def __init__(self, campos=None):
        object.__setattr__(self, "_d", campos or {})
    def __getitem__(self, k):
        d = object.__getattribute__(self, "_d")
        if k not in d: raise KeyError(f"Campo '{k}' não existe")
        return d[k]
    def __setitem__(self, k, v):
        object.__getattribute__(self, "_d")[k] = v
    def __contains__(self, k):
        return k in object.__getattribute__(self, "_d")
    def keys(self):
        return list(object.__getattribute__(self, "_d").keys())
    def values(self):
        return list(object.__getattribute__(self, "_d").values())
    def items(self):
        return list(object.__getattribute__(self, "_d").items())
    def get(self, k, p=None):
        return object.__getattribute__(self, "_d").get(k, p)
    def __repr__(self):
        d = object.__getattribute__(self, "_d")
        itens = ", ".join(f"{k!r}: {_repr(v)}" for k, v in d.items())
        return "{" + itens + "}"
    def __len__(self):
        return len(object.__getattribute__(self, "_d"))
    def _dict(self):
        return object.__getattribute__(self, "_d")


# ── Função Sintax ─────────────────────────────────────────────
class SFunc:
    def __init__(self, no_def, escopo_def):
        self.no    = no_def
        self.escopo = escopo_def    # closure scope
    def __repr__(self):
        return f"<func {self.no.nome}>"


# ── Função nativa ─────────────────────────────────────────────
class SNativa:
    def __init__(self, fn, nome="?"):
        self.fn = fn; self.nome = nome
    def __repr__(self): return f"<nativa {self.nome}>"


# ── Módulo ────────────────────────────────────────────────────
class SModulo:
    def __init__(self, nome, campos):
        self._nome   = nome
        self._campos = campos
    def __repr__(self): return f"<módulo {self._nome}>"


# ── Escopo léxico ─────────────────────────────────────────────
class Escopo:
    def __init__(self, pai=None, nome="<global>"):
        self._vars  = {}
        self._pai   = pai
        self._nome  = nome
        self._globais = set()   # nomes declarados global

    def ler(self, nome, linha=0):
        if nome in self._vars:   return self._vars[nome]
        if self._pai:            return self._pai.ler(nome, linha)
        raise NameError(f"Variável '{nome}' não definida")

    def escrever(self, nome, valor):
        if nome in self._globais:
            self._raiz()._vars[nome] = valor
            return
        if self._pai and nome in self._globais:
            self._raiz()._vars[nome] = valor
            return
        self._vars[nome] = valor

    def definir_global(self, nomes):
        self._globais.update(nomes)

    def _raiz(self):
        e = self
        while e._pai: e = e._pai
        return e

    def global_scope(self):
        return self._raiz()


# ── Representação legível ─────────────────────────────────────
def _repr(v, indent=0):
    if isinstance(v, bool):  return "true" if v else "false"
    if v is None:            return "nulo"
    if isinstance(v, float):
        return str(int(v)) if v == int(v) else str(v)
    if isinstance(v, list):
        if not v: return "[]"
        itens = ", ".join(_repr(x) for x in v)
        return f"[{itens}]"
    if isinstance(v, SObj):  return repr(v)
    if isinstance(v, SFunc): return repr(v)
    return str(v)


# ── Interpreter ───────────────────────────────────────────────
class Interpreter:
    def __init__(self):
        self._global = Escopo(nome="<global>")
        self._escopo = self._global
        self._call_stack = []          # [(nome_func, linha)]
        self._modulos_cache = {}
        self._registrar_stdlib()

    # ── Execução ──────────────────────────────────────────────
    def rodar(self, nos):
        for no in nos:
            self._exec(no)

    def _exec(self, no):
        try:
            return self._exec_inner(no)
        except (_Retorno, _Pare, _Continua):
            raise
        except SintaxRuntimeError:
            raise
        except Exception as e:
            raise SintaxRuntimeError(str(e), no, self._call_stack[:])

    def _exec_inner(self, no):

        # ── print ─────────────────────────────────────────────
        if isinstance(no, NoPrint):
            partes = [_repr(self._eval(e)) for e in no.exprs]
            print(" ".join(partes), end=no.fim)
            return

        # ── Atribuição ────────────────────────────────────────
        if isinstance(no, NoAtrib):
            self._atribuir(no)
            return

        # ── delete ────────────────────────────────────────────
        if isinstance(no, NoDelete):
            alvo = no.alvo
            if isinstance(alvo, NoVar):
                self._escopo._vars.pop(alvo.nome, None)
            elif isinstance(alvo, NoProp):
                obj = self._eval(alvo.obj)
                if isinstance(obj, SObj): obj._dict().pop(alvo.prop, None)
            elif isinstance(alvo, NoIndice):
                obj = self._eval(alvo.alvo)
                idx = self._eval(alvo.idx)
                del obj[idx]
            return

        # ── global ────────────────────────────────────────────
        if isinstance(no, NoGlobal):
            self._escopo.definir_global(no.nomes)
            return

        # ── se ────────────────────────────────────────────────
        if isinstance(no, NoSe):
            for cond, bloco in no.ramos:
                if self._eval(cond):
                    self._exec_bloco(bloco); return
            if no.senao is not None:
                self._exec_bloco(no.senao)
            return

        # ── enquanto ──────────────────────────────────────────
        if isinstance(no, NoEnquanto):
            _lim = 10_000_000; _c = 0
            while self._eval(no.cond):
                try: self._exec_bloco(no.bloco)
                except _Pare: break
                except _Continua: pass
                _c += 1
                if _c >= _lim:
                    raise SintaxRuntimeError(
                        f"Loop infinito detectado ({_lim:,} iterações)", no
                    )
            return

        # ── para ... em ───────────────────────────────────────
        if isinstance(no, NoPara):
            iteravel = self._eval(no.iteravel)
            if isinstance(iteravel, str):
                iteravel = list(iteravel)
            elif isinstance(iteravel, SObj):
                iteravel = iteravel.keys()
            for item in iteravel:
                self._escopo.escrever(no.var, item)
                try: self._exec_bloco(no.bloco)
                except _Pare: break
                except _Continua: pass
            return

        # ── para ... range ────────────────────────────────────
        if isinstance(no, NoParaRange):
            ini   = int(self._eval(no.inicio)) if no.inicio else 0
            fim   = int(self._eval(no.fim))
            passo = int(self._eval(no.passo)) if no.passo else (1 if fim >= ini else -1)
            for i in range(ini, fim, passo):
                self._escopo.escrever(no.var, i)
                try: self._exec_bloco(no.bloco)
                except _Pare: break
                except _Continua: pass
            return

        if isinstance(no, NoPare):     raise _Pare()
        if isinstance(no, NoContinua): raise _Continua()

        # ── return ────────────────────────────────────────────
        if isinstance(no, NoReturn):
            v = self._eval(no.expr) if no.expr else None
            raise _Retorno(v)

        # ── definição de função ───────────────────────────────
        if isinstance(no, NoFuncDef):
            fn = SFunc(no, self._escopo)
            self._escopo.escrever(no.nome, fn)
            return

        # ── import ────────────────────────────────────────────
        if isinstance(no, NoImport):
            self._importar(no)
            return

        # Expressão como instrução (chamada de função etc.)
        self._eval(no)

    def _exec_bloco(self, bloco):
        for instrucao in bloco:
            self._exec(instrucao)

    # ── Atribuição ────────────────────────────────────────────
    def _atribuir(self, no):
        alvo  = no.alvo
        valor = self._eval(no.valor)

        if no.op != "=":
            atual = self._eval(alvo)
            OP = {
                "+=": lambda a,b: (a+b) if not (isinstance(a,str) or isinstance(b,str)) else str(a)+str(b),
                "-=": lambda a,b: a-b,
                "*=": lambda a,b: a*b,
                "/=": lambda a,b: a/b,
                "%=": lambda a,b: a%b,
            }
            valor = OP[no.op](atual, valor)

        if isinstance(alvo, NoVar):
            self._escopo.escrever(alvo.nome, valor)
        elif isinstance(alvo, NoProp):
            obj = self._eval(alvo.obj)
            if isinstance(obj, SObj):
                obj[alvo.prop] = valor
            else:
                raise SintaxRuntimeError(
                    f"Não é possível definir '{alvo.prop}' em {type(obj).__name__}", alvo
                )
        elif isinstance(alvo, NoIndice):
            obj = self._eval(alvo.alvo)
            idx = self._eval(alvo.idx)
            obj[idx] = valor
        else:
            raise SintaxRuntimeError("Alvo de atribuição inválido", no)

    # ── Avaliação de expressões ───────────────────────────────
    def _eval(self, no):
        if no is None: return None

        if isinstance(no, NoInt):   return no.valor
        if isinstance(no, NoFloat): return no.valor
        if isinstance(no, NoStr):   return self._interpolar(no.valor, no)
        if isinstance(no, NoBool):  return no.valor
        if isinstance(no, NoNulo):  return None

        if isinstance(no, NoLista):
            return [self._eval(e) for e in no.elementos]

        if isinstance(no, NoDict):
            d = {}
            for chave, valor in no.pares:
                k = self._eval(chave)
                v = self._eval(valor)
                d[k] = v
            return SObj(d)

        if isinstance(no, NoVar):
            try:
                return self._escopo.ler(no.nome, no.linha)
            except NameError as e:
                raise SintaxRuntimeError(str(e), no, self._call_stack[:])

        if isinstance(no, NoProp):
            obj = self._eval(no.obj)
            return self._get_prop(obj, no.prop, no)

        if isinstance(no, NoIndice):
            obj = self._eval(no.alvo)
            idx = self._eval(no.idx)
            return self._get_idx(obj, idx, no)

        if isinstance(no, NoBinOp):
            return self._bin_op(no)

        if isinstance(no, NoUnOp):
            v = self._eval(no.operando)
            if no.op == "-":   return -v
            if no.op == "nao": return not v

        if isinstance(no, NoChamada):
            return self._chamar(no)

        if isinstance(no, NoMetodo):
            return self._chamar_metodo(no)

        # Expressão que é instrução também (print como expr retorna None)
        if isinstance(no, NoPrint):
            self._exec(no); return None

        return None

    # ── Operações binárias ────────────────────────────────────
    def _bin_op(self, no):
        op = no.op
        # Short-circuit
        if op == "e":
            return bool(self._eval(no.esq)) and bool(self._eval(no.dir))
        if op == "ou":
            return bool(self._eval(no.esq)) or  bool(self._eval(no.dir))

        esq = self._eval(no.esq)
        dir = self._eval(no.dir)

        if op == "+":
            if isinstance(esq, (list,)) and isinstance(dir, list):
                return esq + dir
            if isinstance(esq, str) or isinstance(dir, str):
                return _repr(esq) + _repr(dir)
            return esq + dir
        if op == "-":  return esq - dir
        if op == "*":
            if isinstance(esq, str) and isinstance(dir, int): return esq * dir
            if isinstance(esq, list) and isinstance(dir, int): return esq * dir
            return esq * dir
        if op == "/":
            if dir == 0: raise SintaxRuntimeError("Divisão por zero", no)
            return esq / dir
        if op == "//":
            if dir == 0: raise SintaxRuntimeError("Divisão inteira por zero", no)
            return esq // dir
        if op == "%":
            if dir == 0: raise SintaxRuntimeError("Módulo por zero", no)
            return esq % dir
        if op == "**": return esq ** dir

        COMP = {"==":lambda a,b:a==b, "!=":lambda a,b:a!=b,
                ">":lambda a,b:a>b,   "<":lambda a,b:a<b,
                ">=":lambda a,b:a>=b, "<=":lambda a,b:a<=b}
        if op in COMP: return COMP[op](esq, dir)

        raise SintaxRuntimeError(f"Operador desconhecido: '{op}'", no)

    # ── Propriedades e índices ────────────────────────────────
    def _get_prop(self, obj, prop, no):
        if isinstance(obj, SObj):
            if prop in obj: return obj[prop]
            # Métodos embutidos de objeto
            return self._metodo_sobj(obj, prop, no)
        if isinstance(obj, list):
            return self._metodo_lista_prop(obj, prop, no)
        if isinstance(obj, str):
            return self._metodo_str_prop(obj, prop, no)
        if isinstance(obj, SModulo):
            if prop in obj._campos: return obj._campos[prop]
            raise SintaxRuntimeError(f"Módulo '{obj._nome}' não tem '{prop}'", no)
        raise SintaxRuntimeError(
            f"'{_repr(obj)}' (tipo {self._tipo(obj)}) não tem atributo '{prop}'", no
        )

    def _get_idx(self, obj, idx, no):
        try:
            if isinstance(obj, SObj): return obj[idx]
            return obj[idx]
        except (IndexError, KeyError, TypeError) as e:
            raise SintaxRuntimeError(str(e), no)

    # ── Chamadas ──────────────────────────────────────────────
    def _chamar(self, no):
        func = self._eval(no.func)
        args = [self._eval(a) for a in no.args]
        return self._aplicar(func, args, no)

    def _chamar_metodo(self, no):
        obj    = self._eval(no.obj)
        args   = [self._eval(a) for a in no.args]
        metodo = no.metodo
        return self._metodo_chamado(obj, metodo, args, no)

    def _aplicar(self, func, args, no):
        if isinstance(func, SNativa):
            try: return func.fn(args)
            except Exception as e:
                raise SintaxRuntimeError(str(e), no, self._call_stack[:])

        if isinstance(func, SFunc):
            return self._exec_func(func, args, no)

        if callable(func):
            return func(args)

        raise SintaxRuntimeError(
            f"'{_repr(func)}' não é uma função (tipo: {self._tipo(func)})", no
        )

    def _exec_func(self, sfunc, args, no):
        params  = sfunc.no.params
        # Validar aridade
        obrig   = sum(1 for _, d in params if d is None)
        if len(args) < obrig:
            raise SintaxRuntimeError(
                f"'{sfunc.no.nome}' espera ao menos {obrig} arg(s), "
                f"recebeu {len(args)}", no
            )

        self._call_stack.append((sfunc.no.nome, no.linha))
        escopo_ant  = self._escopo
        self._escopo = Escopo(sfunc.escopo, sfunc.no.nome)

        for i, (pnome, pdef) in enumerate(params):
            if i < len(args):
                self._escopo.escrever(pnome, args[i])
            elif pdef is not None:
                # default: avaliado no escopo corrente
                old = self._escopo; self._escopo = escopo_ant
                v   = self._eval(pdef)
                self._escopo = old
                self._escopo.escrever(pnome, v)
            else:
                self._escopo.escrever(pnome, None)

        resultado = None
        try:
            self._exec_bloco(sfunc.no.bloco)
        except _Retorno as r:
            resultado = r.valor
        finally:
            self._escopo = escopo_ant
            if self._call_stack: self._call_stack.pop()

        return resultado

    # ── Interpolação de strings "{var}" ──────────────────────
    def _interpolar(self, s, no):
        if "{" not in s: return s
        resultado = ""
        i = 0
        while i < len(s):
            if s[i] == "{" and i + 1 < len(s) and s[i+1] != "{":
                # Encontra o } balanceado (ignorando aninhamento)
                depth = 1; j = i + 1
                while j < len(s) and depth > 0:
                    if s[j] == "{": depth += 1
                    elif s[j] == "}": depth -= 1
                    j += 1
                if depth != 0: resultado += s[i]; i += 1; continue
                expr_str = s[i+1:j-1].strip()
                try:
                    from sintax.lexer  import Lexer
                    from sintax.parser import Parser
                    toks = Lexer(expr_str, "<interp>").tokenizar()
                    ast  = Parser(toks).parse()
                    v = self._eval(ast[0]) if ast else ""
                    resultado += _repr(v)
                except Exception:
                    resultado += "{" + expr_str + "}"
                i = j
            elif s[i:i+2] == "{{":
                resultado += "{"; i += 2
            elif s[i:i+2] == "}}":
                resultado += "}"; i += 2
            else:
                resultado += s[i]; i += 1
        return resultado

    # ── Métodos de lista e string (acesso como .prop) ─────────
    def _metodo_lista_prop(self, lista, prop, no):
        _a = lambda: SNativa(lambda args: lista.append(args[0]) or lista, "add")
        _props = {
            "tamanho":   len(lista),
            "length":    len(lista),
            "add":       SNativa(lambda a: lista.append(a[0]) or lista, "add"),
            "adicionar": SNativa(lambda a: lista.append(a[0]) or lista, "adicionar"),
            "remover":   SNativa(lambda a: lista.remove(a[0]) or lista, "remover"),
            "pop":       SNativa(lambda a: lista.pop(int(a[0])) if a else lista.pop(), "pop"),
            "inserir":   SNativa(lambda a: lista.insert(int(a[0]),a[1]) or lista, "inserir"),
            "ordenar":   SNativa(lambda a: lista.sort(reverse=bool(a[0]) if a else False) or lista, "ordenar"),
            "inverter":  SNativa(lambda a: lista.reverse() or lista, "inverter"),
            "contem":    SNativa(lambda a: a[0] in lista, "contem"),
            "indice":    SNativa(lambda a: lista.index(a[0]), "indice"),
            "fatiar":    SNativa(lambda a: lista[int(a[0]):int(a[1])], "fatiar"),
            "limpar":    SNativa(lambda a: lista.clear() or lista, "limpar"),
            "copiar":    SNativa(lambda a: lista[:], "copiar"),
            "unir":      SNativa(lambda a: (a[0] if a else ", ").join(_repr(x) for x in lista), "unir"),
            "filtrar":   SNativa(lambda a, _n=no: [x for x in lista if self._aplicar(a[0],[x],_n)], "filtrar"),
            "mapear":    SNativa(lambda a, _n=no: [self._aplicar(a[0],[x],_n) for x in lista], "mapear"),
        }
        if prop in _props: return _props[prop]
        raise SintaxRuntimeError(f"Lista não tem '{prop}'", no)

    def _metodo_str_prop(self, s, prop, no):
        _props = {
            "tamanho":        len(s),
            "length":         len(s),
            "maiusculo":      SNativa(lambda a: s.upper(), "maiusculo"),
            "upper":          SNativa(lambda a: s.upper(), "upper"),
            "minusculo":      SNativa(lambda a: s.lower(), "minusculo"),
            "lower":          SNativa(lambda a: s.lower(), "lower"),
            "capitalizar":    SNativa(lambda a: s.capitalize(), "capitalizar"),
            "dividir":        SNativa(lambda a: s.split(a[0] if a else None), "dividir"),
            "split":          SNativa(lambda a: s.split(a[0] if a else None), "split"),
            "substituir":     SNativa(lambda a: s.replace(a[0],a[1]), "substituir"),
            "replace":        SNativa(lambda a: s.replace(a[0],a[1]), "replace"),
            "contem":         SNativa(lambda a: a[0] in s, "contem"),
            "começa_com":     SNativa(lambda a: s.startswith(a[0]), "começa_com"),
            "termina_com":    SNativa(lambda a: s.endswith(a[0]), "termina_com"),
            "strip":          SNativa(lambda a: s.strip(), "strip"),
            "lstrip":         SNativa(lambda a: s.lstrip(), "lstrip"),
            "rstrip":         SNativa(lambda a: s.rstrip(), "rstrip"),
            "repetir":        SNativa(lambda a: s * int(a[0]), "repetir"),
            "encontrar":      SNativa(lambda a: s.find(a[0]), "encontrar"),
            "para_int":       SNativa(lambda a: int(s), "para_int"),
            "para_float":     SNativa(lambda a: float(s), "para_float"),
            "é_número":       SNativa(lambda a: s.replace(".","",1).lstrip("-").isdigit(), "é_número"),
            "é_alfanumérico": SNativa(lambda a: s.isalnum(), "é_alfanumérico"),
        }
        if prop in _props: return _props[prop]
        raise SintaxRuntimeError(f"Texto não tem '{prop}'", no)

    def _metodo_sobj(self, obj, prop, no):
        _d = object.__getattribute__(obj, "_d")
        _props = {
            "chaves":  SNativa(lambda a: list(_d.keys()), "chaves"),
            "keys":    SNativa(lambda a: list(_d.keys()), "keys"),
            "valores": SNativa(lambda a: list(_d.values()), "valores"),
            "values":  SNativa(lambda a: list(_d.values()), "values"),
            "itens":   SNativa(lambda a: [[k,v] for k,v in _d.items()], "itens"),
            "items":   SNativa(lambda a: [[k,v] for k,v in _d.items()], "items"),
            "tem":     SNativa(lambda a: a[0] in _d, "tem"),
            "has":     SNativa(lambda a: a[0] in _d, "has"),
            "get":     SNativa(lambda a: _d.get(a[0], a[1] if len(a)>1 else None), "get"),
            "remover": SNativa(lambda a: _d.pop(a[0], None), "remover"),
            "tamanho": SNativa(lambda a: len(_d), "tamanho"),
        }
        if prop in _props: return _props[prop]
        raise SintaxRuntimeError(f"Objeto não tem campo '{prop}'", no)

    def _metodo_chamado(self, obj, metodo, args, no):
        prop = self._get_prop(obj, metodo, no)
        if isinstance(prop, (SNativa, SFunc)):
            return self._aplicar(prop, args, no)
        if callable(prop):
            return prop(args)
        raise SintaxRuntimeError(
            f"'{metodo}' não é um método (valor: {_repr(prop)})", no
        )

    # ── Importação ────────────────────────────────────────────
    def _importar(self, no):
        nome = no.modulo

        # 1. Módulo nativo da stdlib
        modulo = self._stdlib_modulo(nome)
        if modulo:
            alias = no.alias or nome
            self._escopo.escrever(alias, modulo)
            return

        # 2. Arquivo .stx
        caminhos = [
            nome + ".stx",
            os.path.join("stdlib", nome + ".stx"),
        ]
        for caminho in caminhos:
            if os.path.exists(caminho):
                if caminho in self._modulos_cache:
                    mod = self._modulos_cache[caminho]
                else:
                    mod = self._importar_arquivo(caminho, nome)
                    self._modulos_cache[caminho] = mod
                alias = no.alias or nome
                self._escopo.escrever(alias, mod)
                return

        raise SintaxRuntimeError(f"Módulo '{nome}' não encontrado", no)

    def _importar_arquivo(self, caminho, nome):
        from sintax.lexer  import Lexer
        from sintax.parser import Parser
        with open(caminho, encoding="utf-8") as f:
            codigo = f.read()
        toks = Lexer(codigo, caminho).tokenizar()
        ast  = Parser(toks).parse()
        # Executa em escopo isolado
        escopo_ant   = self._escopo
        self._escopo = Escopo(nome=f"<módulo {nome}>")
        try:
            self._exec_bloco(ast)
        except Exception as e:
            self._escopo = escopo_ant
            raise
        vars_mod     = dict(self._escopo._vars)
        self._escopo = escopo_ant
        campos = {k: v for k, v in vars_mod.items() if not k.startswith("_")}
        return SModulo(nome, campos)

    # ── Tipos ─────────────────────────────────────────────────
    def _tipo(self, v):
        if isinstance(v, bool):  return "booleano"
        if isinstance(v, int):   return "inteiro"
        if isinstance(v, float): return "decimal"
        if isinstance(v, str):   return "texto"
        if isinstance(v, list):  return "lista"
        if v is None:            return "nulo"
        if isinstance(v, SObj):  return "objeto"
        if isinstance(v, SFunc): return "func"
        if isinstance(v, SNativa): return "func"
        if isinstance(v, SModulo): return "módulo"
        return type(v).__name__

    # ── Biblioteca padrão ─────────────────────────────────────
    def _registrar_stdlib(self):
        g = self._global

        def nativa(nome, fn):
            g.escrever(nome, SNativa(fn, nome))

        # ── I/O ──────────────────────────────────────────────
        nativa("input",   lambda a: input(a[0] if a else ""))
        nativa("leia",    lambda a: input(a[0] if a else ""))

        # ── Tipos ──────────────────────────────────────────────
        nativa("int",     lambda a: int(float(a[0])))
        nativa("inteiro", lambda a: int(float(a[0])))
        nativa("float",   lambda a: float(a[0]))
        nativa("decimal", lambda a: float(a[0]))
        nativa("str",     lambda a: _repr(a[0]))
        nativa("texto",   lambda a: _repr(a[0]))
        nativa("bool",    lambda a: bool(a[0]))
        nativa("tipo",    lambda a: self._tipo(a[0]))
        nativa("type",    lambda a: self._tipo(a[0]))
        nativa("lista",   lambda a: list(a[0]) if a else [])
        nativa("objeto",  lambda a: SObj(dict(a[0]._dict()) if a and isinstance(a[0], SObj) else {}))

        # ── Tamanho ────────────────────────────────────────────
        nativa("len",     lambda a: len(a[0]))
        nativa("tam",     lambda a: len(a[0]))

        # ── Matemática ─────────────────────────────────────────
        nativa("abs",        lambda a: abs(a[0]))
        nativa("round",      lambda a: round(a[0]) if len(a)==1 else round(a[0],int(a[1])))
        nativa("arredondar", lambda a: round(a[0]) if len(a)==1 else round(a[0],int(a[1])))
        nativa("max",        lambda a: max(a[0]) if (len(a)==1 and hasattr(a[0],"__iter__")) else max(a))
        nativa("min",        lambda a: min(a[0]) if (len(a)==1 and hasattr(a[0],"__iter__")) else min(a))
        nativa("soma",       lambda a: sum(a[0]) if (len(a)==1 and hasattr(a[0],"__iter__")) else sum(a))
        nativa("sqrt",       lambda a: _math.sqrt(a[0]))
        nativa("raiz",       lambda a: _math.sqrt(a[0]))
        nativa("piso",       lambda a: int(_math.floor(a[0])))
        nativa("teto",       lambda a: int(_math.ceil(a[0])))
        nativa("pot",        lambda a: a[0]**a[1])
        nativa("log",        lambda a: _math.log(a[0], a[1]) if len(a)>1 else _math.log(a[0]))
        nativa("sen",        lambda a: _math.sin(a[0]))
        nativa("cos",        lambda a: _math.cos(a[0]))
        nativa("tan",        lambda a: _math.tan(a[0]))

        # ── Strings ────────────────────────────────────────────
        nativa("maiusculo",  lambda a: str(a[0]).upper())
        nativa("minusculo",  lambda a: str(a[0]).lower())
        nativa("strip",      lambda a: str(a[0]).strip())
        nativa("dividir",    lambda a: str(a[0]).split(a[1]) if len(a)>1 else str(a[0]).split())
        nativa("unir",       lambda a: (a[1] if len(a)>1 else ", ").join(_repr(x) for x in a[0]))
        nativa("formatar",   lambda a: self._formatar(a))
        nativa("repr",       lambda a: _repr(a[0]))

        # ── Listas ─────────────────────────────────────────────
        nativa("range",   lambda a: list(range(int(a[0]), int(a[1]), int(a[2]) if len(a)>2 else 1)) if len(a)>1 else list(range(int(a[0]))))
        nativa("intervalo", lambda a: list(range(int(a[0]), int(a[1]), int(a[2]) if len(a)>2 else 1)) if len(a)>1 else list(range(int(a[0]))))
        nativa("ordenar",  lambda a: sorted(a[0], reverse=bool(a[1]) if len(a)>1 else False))
        nativa("inverter", lambda a: list(reversed(a[0])))
        _dummy = type("_No", (), {"linha": 0, "col": 0})()
        nativa("filtrar",  lambda a: [x for x in a[1] if self._aplicar(a[0],[x],_dummy)])
        nativa("mapear",   lambda a: [self._aplicar(a[0],[x],_dummy) for x in a[1]])
        nativa("zip",      lambda a: [list(x) for x in zip(*a)])
        nativa("enumerar", lambda a: [[i,v] for i,v in enumerate(a[0])])

        # ── Conversão / verificação ─────────────────────────────
        nativa("é_texto",     lambda a: isinstance(a[0], str))
        nativa("é_inteiro",   lambda a: isinstance(a[0], int) and not isinstance(a[0], bool))
        nativa("é_decimal",   lambda a: isinstance(a[0], float))
        nativa("é_lista",     lambda a: isinstance(a[0], list))
        nativa("é_nulo",      lambda a: a[0] is None)
        nativa("é_função",    lambda a: isinstance(a[0], (SFunc, SNativa)))

        # ── Debug ───────────────────────────────────────────────
        nativa("debug",    lambda a: (print("[DEBUG]", *[_repr(x) for x in a]) or None))
        nativa("assert",   lambda a: (None if (a[0]) else (_ for _ in ()).throw(
            AssertionError(a[1] if len(a)>1 else "Assertion falhou"))))
        nativa("sair",     lambda a: sys.exit(int(a[0]) if a else 0))
        nativa("exit",     lambda a: sys.exit(int(a[0]) if a else 0))

        # ── JSON ────────────────────────────────────────────────
        def _to_json(v):
            if isinstance(v, SObj): return {k: _to_json(x) for k,x in v.items()}
            if isinstance(v, list): return [_to_json(x) for x in v]
            if isinstance(v, bool): return v
            return v

        def _from_json(v):
            if isinstance(v, dict): return SObj({k: _from_json(x) for k,x in v.items()})
            if isinstance(v, list): return [_from_json(x) for x in v]
            return v

        nativa("json_string",  lambda a: _json.dumps(_to_json(a[0]), ensure_ascii=False))
        nativa("json_parse",   lambda a: _from_json(_json.loads(a[0])))

    def _formatar(self, args):
        if not args: return ""
        template = str(args[0])
        valores  = args[1:]
        i = 0
        res = ""
        for c in template:
            if c == "{":
                if i < len(valores):
                    res += _repr(valores[i]); i += 1
            elif c != "}":
                res += c
        return res

    # ── Módulos stdlib ────────────────────────────────────────
    def _stdlib_modulo(self, nome):
        if nome == "math" or nome == "matematica":
            return SModulo("math", {
                "pi":     _math.pi,
                "e":      _math.e,
                "inf":    float("inf"),
                "raiz":   SNativa(lambda a: _math.sqrt(a[0]), "raiz"),
                "sqrt":   SNativa(lambda a: _math.sqrt(a[0]), "sqrt"),
                "abs":    SNativa(lambda a: abs(a[0]), "abs"),
                "piso":   SNativa(lambda a: int(_math.floor(a[0])), "piso"),
                "teto":   SNativa(lambda a: int(_math.ceil(a[0])), "teto"),
                "round":  SNativa(lambda a: round(a[0]) if len(a)==1 else round(a[0],int(a[1])), "round"),
                "pot":    SNativa(lambda a: a[0]**a[1], "pot"),
                "log":    SNativa(lambda a: _math.log(a[0], a[1]) if len(a)>1 else _math.log(a[0]), "log"),
                "log10":  SNativa(lambda a: _math.log10(a[0]), "log10"),
                "log2":   SNativa(lambda a: _math.log2(a[0]), "log2"),
                "sen":    SNativa(lambda a: _math.sin(a[0]), "sen"),
                "cos":    SNativa(lambda a: _math.cos(a[0]), "cos"),
                "tan":    SNativa(lambda a: _math.tan(a[0]), "tan"),
                "graus":  SNativa(lambda a: _math.degrees(a[0]), "graus"),
                "rad":    SNativa(lambda a: _math.radians(a[0]), "rad"),
                "hipo":   SNativa(lambda a: _math.hypot(*a), "hipo"),
            })

        if nome == "random" or nome == "aleatorio":
            return SModulo("random", {
                "número":   SNativa(lambda a: _random.random(), "número"),
                "inteiro":  SNativa(lambda a: _random.randint(int(a[0]),int(a[1])), "inteiro"),
                "escolher": SNativa(lambda a: _random.choice(a[0]), "escolher"),
                "embaralhar": SNativa(lambda a: _random.shuffle(a[0]) or a[0], "embaralhar"),
                "amostra":  SNativa(lambda a: _random.sample(a[0],int(a[1])), "amostra"),
                "seed":     SNativa(lambda a: _random.seed(a[0]) or None, "seed"),
            })

        if nome == "tempo" or nome == "time":
            return SModulo("tempo", {
                "agora":    SNativa(lambda a: _time.time(), "agora"),
                "dormir":   SNativa(lambda a: _time.sleep(float(a[0])) or None, "dormir"),
                "sleep":    SNativa(lambda a: _time.sleep(float(a[0])) or None, "sleep"),
                "formato":  SNativa(lambda a: _time.strftime(a[0] if a else "%Y-%m-%d %H:%M:%S"), "formato"),
            })

        if nome == "arquivo" or nome == "file":
            def ler_arq(a):
                with open(str(a[0]), encoding="utf-8") as f: return f.read()
            def escrever_arq(a):
                with open(str(a[0]), "w", encoding="utf-8") as f: f.write(str(a[1]))
            def adicionar_arq(a):
                with open(str(a[0]), "a", encoding="utf-8") as f: f.write(str(a[1]))
            def existe_arq(a):
                return os.path.exists(str(a[0]))
            def linhas_arq(a):
                with open(str(a[0]), encoding="utf-8") as f:
                    return [l.rstrip("\n") for l in f.readlines()]
            return SModulo("arquivo", {
                "ler":       SNativa(ler_arq, "ler"),
                "escrever":  SNativa(escrever_arq, "escrever"),
                "adicionar": SNativa(adicionar_arq, "adicionar"),
                "existe":    SNativa(existe_arq, "existe"),
                "linhas":    SNativa(linhas_arq, "linhas"),
            })

        if nome == "os" or nome == "sistema":
            return SModulo("os", {
                "cwd":        SNativa(lambda a: os.getcwd(), "cwd"),
                "listar":     SNativa(lambda a: os.listdir(a[0] if a else "."), "listar"),
                "existe":     SNativa(lambda a: os.path.exists(a[0]), "existe"),
                "criar_pasta":SNativa(lambda a: os.makedirs(a[0], exist_ok=True) or None, "criar_pasta"),
                "remover":    SNativa(lambda a: os.remove(a[0]) or None, "remover"),
                "env":        SNativa(lambda a: os.environ.get(a[0], a[1] if len(a)>1 else None), "env"),
                "args":       SNativa(lambda a: sys.argv[1:], "args"),
            })

        if nome == "json":
            def _to_j(v):
                if isinstance(v, SObj): return {k:_to_j(x) for k,x in v.items()}
                if isinstance(v, list): return [_to_j(x) for x in v]
                return v
            def _from_j(v):
                if isinstance(v, dict): return SObj({k:_from_j(x) for k,x in v.items()})
                if isinstance(v, list): return [_from_j(x) for x in v]
                return v
            return SModulo("json", {
                "string":    SNativa(lambda a: _json.dumps(_to_j(a[0]), ensure_ascii=False, indent=int(a[1]) if len(a)>1 else None), "string"),
                "parse":     SNativa(lambda a: _from_j(_json.loads(str(a[0]))), "parse"),
                "salvar":    SNativa(lambda a: open(str(a[0]),"w",encoding="utf-8").write(_json.dumps(_to_j(a[1]),ensure_ascii=False,indent=2)) or None, "salvar"),
                "carregar":  SNativa(lambda a: _from_j(_json.load(open(str(a[0]),encoding="utf-8"))), "carregar"),
            })

        return None
