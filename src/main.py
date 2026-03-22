#!/usr/bin/env python3
# ============================================================
#  SINTAX v4.0 — linguagem geral simples e poderosa
#  Uso:  python main.py arquivo.stx
#        python main.py             (modo interativo)
# ============================================================
import sys, os

BANNER = """\
  ╔═══════════════════════════════════════════╗
  ║   SINTAX v4.0 — linguagem em Português   ║
  ║   Mais simples que Python. Mais poderosa. ║
  ╚═══════════════════════════════════════════╝
  digite 'sair' para encerrar | 'ajuda' para dicas
"""


def _criar_interpreter():
    from src.interpreter import Interpreter
    return Interpreter()


def _rodar_codigo(codigo, interpreter, arquivo="<stdin>"):
    from src.lexer   import Lexer
    from src.parser  import Parser
    try:
        toks = Lexer(codigo, arquivo).tokenizar()
        ast  = Parser(toks).parse()
        interpreter.rodar(ast)
        return True
    except Exception as e:
        print(e)
        return False


def executar_arquivo(caminho):
    if not os.path.exists(caminho):
        print(f"\n╔══ ERRO ══════════════════════════════════\n"
              f"╚► Arquivo não encontrado: '{caminho}'\n")
        sys.exit(1)
    with open(caminho, encoding="utf-8") as f:
        codigo = f.read()
    interp = _criar_interpreter()
    _rodar_codigo(codigo, interp, caminho)


def modo_interativo():
    print(BANNER)
    interp  = _criar_interpreter()
    buffer  = []
    depth   = 0   # profundidade de blocos abertos

    DICAS = """\
  Exemplos rápidos:
    x = 10
    print x
    print "Olá {x}"
    para i 5 { print i }
    func dobrar(n) { return n * 2 }
    import math
    print math.pi
"""

    while True:
        try:
            prompt = "... " if buffer else ">>> "
            linha  = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print(); break

        if linha.strip() == "sair":   break
        if linha.strip() == "ajuda":  print(DICAS); continue
        if linha.strip() == "limpar": interp = _criar_interpreter(); continue

        # Conta blocos abertos
        depth += linha.count("{") - linha.count("}")

        if depth > 0 or (buffer and linha.strip()):
            buffer.append(linha)
            continue
        else:
            if buffer:
                buffer.append(linha)
                codigo = "\n".join(buffer)
                buffer = []
                depth  = 0
            else:
                if not linha.strip(): continue
                codigo = linha

        _rodar_codigo(codigo, interp)


def ajuda():
    print("""
SINTAX v4.0 — Linguagem de programação em Português

USO:
  python main.py arquivo.stx     Executa um arquivo
  python main.py                 Modo interativo (REPL)
  python main.py -h              Esta ajuda

SINTAXE RÁPIDA:
  Variáveis:    x = 10  |  nome = "Ana"  |  pi = 3.14
  Print:        print x  |  print "Olá {nome}"
  Input:        nome = input("Seu nome: ")
  Condição:     se x > 5 { ... } senao { ... }
  While:        enquanto x < 10 { x += 1 }
  Para (range): para i 10 { print i }
  Para (lista): para item em frutas { print item }
  Função:       func soma(a, b) { return a + b }
  Import:       import math  |  import random como r

MÓDULOS DISPONÍVEIS:
  math       pi, e, raiz, sen, cos, tan, log, ...
  random     número, inteiro, escolher, embaralhar, ...
  tempo      agora, dormir, formato
  arquivo    ler, escrever, existe, linhas
  json       parse, string, salvar, carregar
  os         listar, existe, criar_pasta, args

EXTENSÃO DOS ARQUIVOS: .stx
""")


def main():
    args = sys.argv[1:]

    if not args:
        modo_interativo()
        return

    if args[0] in ("-h", "--help", "ajuda"):
        ajuda()
        return

    executar_arquivo(args[0])


if __name__ == "__main__":
    main()
