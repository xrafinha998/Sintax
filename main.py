from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
import sys

def iniciar():
    if len(sys.argv) < 2:
        print("Uso: python main.py arquivo.stx")
        return

    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            codigo = f.read()

        # LEXER
        lexer = Lexer(codigo)
        tokens = lexer.gerar_tokens()
        # print("TOKENS:", tokens)  # debug opcional

        # PARSER
        parser = Parser(tokens)
        ast = parser.parse()
        # print("AST:", ast)  # debug opcional

        # INTERPRETER
        interpretador = Interpreter()
        interpretador.rodar(ast)

    except Exception as e:
        print(f"[ERRO SINTAX] {e}")

if __name__ == "__main__":
    iniciar()
