# Importa as definições de estrutura do Parser
from src.parser import NoAtribuicao, NoSe

class Interpreter:
    def __init__(self):
        self.memoria = {}

    def rodar(self, nos):
        for no in nos:
            # Agora ele vai reconhecer o que é NoAtribuicao
            if isinstance(no, NoAtribuicao):
                self.memoria[no.nome] = no.valor
                # Opcional: print(f"[LOG] {no.nome} = {no.valor}")
            
            # Agora ele vai reconhecer o que é NoSe
            elif isinstance(no, NoSe):
                val_real = self.memoria.get(no.nome_var, 0)
                resultado = False
                
                # Lógica de comparação
                if no.operador == '>': resultado = val_real > no.valor_comp
                if no.operador == '<': resultado = val_real < no.valor_comp
                if no.operador == '==': resultado = val_real == no.valor_comp
                
                if resultado:
                    print(f"Sintax diz: {no.mensagem}")
