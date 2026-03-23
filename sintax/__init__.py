"""
Sintax — Linguagem de programação em Português.

Uso como biblioteca:

    from sintax import Interpreter, executar

    # Executar código diretamente
    executar('print "Olá, Mundo!"')

    # Ou usar o interpreter diretamente
    interp = Interpreter()
    interp.rodar_codigo('x = 10\\nprint x')
"""

__version__  = "4.0.0"
__author__   = "Sintax Language"
__license__  = "MIT"

from sintax.interpreter import Interpreter
from sintax.lexer        import Lexer
from sintax.parser       import Parser


def executar(codigo: str, arquivo: str = "<string>") -> Interpreter:
    """
    Executa uma string de código Sintax.

    Args:
        codigo:  Código-fonte em Sintax (.stx)
        arquivo: Nome do arquivo (para mensagens de erro)

    Returns:
        O Interpreter após a execução (para inspecionar variáveis)

    Raises:
        SyntaxError: Erro léxico ou de sintaxe
        RuntimeError: Erro em tempo de execução
    """
    tokens = Lexer(codigo, arquivo).tokenizar()
    ast    = Parser(tokens).parse()
    interp = Interpreter()
    interp.rodar(ast)
    return interp


def executar_arquivo(caminho: str) -> Interpreter:
    """
    Executa um arquivo .stx.

    Args:
        caminho: Caminho para o arquivo .stx

    Returns:
        O Interpreter após a execução

    Raises:
        FileNotFoundError: Arquivo não encontrado
        SyntaxError: Erro léxico ou de sintaxe
        RuntimeError: Erro em tempo de execução
    """
    with open(caminho, encoding="utf-8") as f:
        codigo = f.read()
    return executar(codigo, caminho)


__all__ = [
    "Interpreter",
    "Lexer",
    "Parser",
    "executar",
    "executar_arquivo",
    "__version__",
]
