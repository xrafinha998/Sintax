"""
sintax.cli — Entry point do comando `sintax` instalado via pip.

Após `pip install sintax-lang`:
    sintax arquivo.stx
    sintax                    # modo interativo
    sintax --help
    sintax --version
"""
import sys
import os


BANNER = """\
  ╔═══════════════════════════════════════════╗
  ║   SINTAX v4.0 — linguagem em Português   ║
  ║   Mais simples que Python. Aprenda já.   ║
  ╚═══════════════════════════════════════════╝
  'sair' para encerrar  |  'ajuda' para dicas
"""

AJUDA = """\
SINTAX v4.0 — Linguagem de programação em Português

USO:
  sintax arquivo.stx       Executa um arquivo
  sintax                   Modo interativo (REPL)
  sintax --version         Versão instalada
  sintax --help            Esta ajuda

SINTAXE RÁPIDA:
  x = 10                   Variável
  print x                  Imprimir
  print "Olá {x}"          Interpolação
  nome = input("Nome: ")   Ler do teclado

  se x > 5 {               Condicional
      print "grande"
  } senao {
      print "pequeno"
  }

  para i 10 { print i }    Loop simples (0 a 9)
  para x em lista { }      Loop em lista
  enquanto x < 10 { }      While

  func soma(a, b) {         Função
      return a + b
  }

  import math              Módulo matemático
  import random como r     Com alias

MÓDULOS: math, random, tempo, arquivo, json, os

EXTENSÃO: .stx
DOCS: https://github.com/seu-usuario/Sintax
"""


def _criar_interpreter():
    from sintax.interpreter import Interpreter
    return Interpreter()


def _rodar_codigo(codigo, interpreter, arquivo="<stdin>"):
    from sintax.lexer   import Lexer
    from sintax.parser  import Parser
    try:
        toks = Lexer(codigo, arquivo).tokenizar()
        ast  = Parser(toks).parse()
        interpreter.rodar(ast)
        return True
    except Exception as e:
        print(e, file=sys.stderr)
        return False


def executar_arquivo(caminho):
    if not os.path.exists(caminho):
        print(
            f"\n╔══ ERRO ══════════════════════════════════\n"
            f"╚► Arquivo não encontrado: '{caminho}'\n",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(caminho, encoding="utf-8") as f:
        codigo = f.read()

    interp = _criar_interpreter()
    ok     = _rodar_codigo(codigo, interp, caminho)
    sys.exit(0 if ok else 1)


def modo_interativo():
    print(BANNER)
    interp = _criar_interpreter()
    buffer = []
    depth  = 0

    while True:
        try:
            prompt = "... " if buffer else ">>> "
            linha  = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            break

        cmd = linha.strip()

        if cmd == "sair":
            break
        if cmd == "ajuda":
            print(AJUDA)
            continue
        if cmd == "limpar":
            interp = _criar_interpreter()
            print("Interpreter reiniciado.")
            continue
        if cmd == "versao":
            from sintax import __version__
            print(f"Sintax v{__version__}")
            continue

        # Rastrear profundidade de blocos abertos
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
                if not linha.strip():
                    continue
                codigo = linha

        _rodar_codigo(codigo, interp)


def main():
    args = sys.argv[1:]

    if not args:
        modo_interativo()
        return

    flag = args[0]

    if flag in ("-h", "--help", "ajuda", "help"):
        print(AJUDA)
        return

    if flag in ("-v", "--version", "--versao"):
        from sintax import __version__
        print(f"sintax {__version__}")
        return

    executar_arquivo(flag)


if __name__ == "__main__":
    main()
