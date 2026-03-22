class Interpreter:
    def __init__(self):
        self.memoria = {}

    def rodar(self, nos):
        for no in nos:
            if isinstance(no, NoAtribuicao):
                self.memoria[no.nome] = no.valor
            
            elif isinstance(no, NoSe):
                val_real = self.memoria.get(no.nome_var, 0)
                resultado = False
                if no.operador == '>': resultado = val_real > no.valor_comp
                if no.operador == '<': resultado = val_real < no.valor_comp
                if no.operador == '==': resultado = val_real == no.valor_comp
                
                if resultado:
                    print(f"Sintax diz: {no.mensagem}")

