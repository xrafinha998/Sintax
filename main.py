from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
import sys

def iniciar():
    if len(sys.argv) < 2:
        print("Uso: python main.py arquivo.stx")
        return

    with open(sys.argv[1], 'r') as f:
        codigo = f.read()

    lexer = Lexer(codigo)
    tokens = lexer.gerar_tokens()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpretador = Interpreter()
    interpretador.rodar(ast)

if __name__ == "__main__":
    iniciar()
