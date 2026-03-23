<div align="center">

# 🧠 Sintax

**Uma linguagem de programação em Português — mais simples que Python, mais rápida de aprender.**

![versão](https://img.shields.io/badge/versão-4.0-blue)
![python](https://img.shields.io/badge/requer-Python%203.7%2B-yellow)
![licença](https://img.shields.io/badge/licença-MIT-green)

</div>
![licença](https://img.shields.io/badge/licença-MIT-green)

## Licença

Este projeto está licenciado sob a Licença MIT — veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 📋 Índice

- [O que é Sintax?](#o-que-é-sintax)
- [Instalação](#instalação)
- [Olá, Mundo!](#olá-mundo)
- [Sintaxe completa](#sintaxe-completa)
  - [Variáveis e tipos](#variáveis-e-tipos)
  - [print — imprimir](#print--imprimir)
  - [input — ler do teclado](#input--ler-do-teclado)
  - [Aritmética](#aritmética)
  - [Comparação e lógica](#comparação-e-lógica)
  - [Condicionais — se / senao](#condicionais--se--senao)
  - [Loop enquanto](#loop-enquanto)
  - [Loop para — o mais simples do mundo](#loop-para--o-mais-simples-do-mundo)
  - [Funções](#funções)
  - [Listas](#listas)
  - [Dicionários](#dicionários)
  - [Strings avançadas](#strings-avançadas)
  - [Escopo e global](#escopo-e-global)
  - [Import — módulos](#import--módulos)
- [Funções da biblioteca padrão](#funções-da-biblioteca-padrão)
- [Módulos disponíveis](#módulos-disponíveis)
- [Exemplos completos](#exemplos-completos)
- [Comparação com Python](#comparação-com-python)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Erros e mensagens](#erros-e-mensagens)
- [Roadmap](#roadmap)

---

## O que é Sintax?

**Sintax** é uma linguagem de programação de uso geral, interpretada, com sintaxe em Português.

**Posicionamento:** *"Mais simples que Python. Feita para aprender e criar rápido."*

```
# Python
for i in range(10):
    print(i)

# Sintax
para i 10 {
    print i
}
```

**Com Sintax você pode criar:**
- Scripts de automação
- Ferramentas de linha de comando
- Processamento de arquivos e JSON
- Lógica de negócio
- Chatbots e scripts de IA simples
- Jogos de texto e protótipos

---

## Instalação

**Pré-requisito:** Python 3.7 ou superior.

```bash
git clone https://github.com/seu-usuario/Sintax.git
cd Sintax
python main.py                      # abre o modo interativo
python main.py examples/01_basico.stx   # executa um arquivo
```

Nenhuma dependência externa — funciona com Python puro.

---

## Olá, Mundo!

```
print "Olá, Mundo!"
```

```bash
python main.py ola.stx
# Olá, Mundo!
```

---

## Sintaxe completa

### Variáveis e tipos

Atribuição simples, sem `var`, sem `let`, sem `const`:

```
# Inteiro
pontos = 100

# Decimal
preco = 9.99

# Texto — aspas duplas OU simples
nome    = "Ana"
cidade  = 'São Paulo'

# Booleano
ativo   = true
pausado = false

# Nulo
resultado = nulo

# Interpolar variáveis numa string com { }
print "Olá, {nome}! Você mora em {cidade}."
print "1 + 1 = {1 + 1}"
```

**Tipos disponíveis:**

| Tipo | Exemplos | Verificar |
|------|----------|-----------|
| `inteiro` | `0`, `42`, `-10` | `é_inteiro(x)` |
| `decimal` | `3.14`, `-0.5` | `é_decimal(x)` |
| `texto` | `"oi"`, `'mundo'` | `é_texto(x)` |
| `booleano` | `true`, `false` | — |
| `lista` | `[1, 2, 3]` | `é_lista(x)` |
| `objeto` | `{"x": 1}` | — |
| `nulo` | `nulo` | `é_nulo(x)` |
| `func` | `func f() {...}` | `é_função(x)` |

---

### print — imprimir

```
print "Olá"
print 42
print true
print nome
print "Valor: " + texto(x)
print x, y, z          # imprime separado por espaço
print "Soma: {a + b}"  # interpolação direta
```

> **Interpolação:** use `{expr}` dentro de strings para inserir valores.  
> Qualquer expressão válida funciona: `{x * 2}`, `{lista[0]}`, `{nome.maiusculo()}`.

---

### input — ler do teclado

```
nome  = input("Seu nome: ")
idade = int(input("Sua idade: "))

print "Olá, {nome}! Você tem {idade} anos."

# Verificar tipo
se é_texto(nome) {
    print "Nome válido!"
}
```

---

### Aritmética

| Operador | Descrição | Exemplo | Resultado |
|----------|-----------|---------|-----------|
| `+` | Soma | `3 + 2` | `5` |
| `-` | Subtração | `10 - 4` | `6` |
| `*` | Multiplicação | `3 * 4` | `12` |
| `/` | Divisão | `10 / 3` | `3.333...` |
| `//` | Divisão inteira | `10 // 3` | `3` |
| `%` | Módulo (resto) | `10 % 3` | `1` |
| `**` | Potência | `2 ** 8` | `256` |

**Precedência correta** — `*` antes de `+`, parênteses mudam a ordem:

```
x = 2 + 3 * 4      # 14  (3*4 primeiro)
y = (2 + 3) * 4    # 20  (parênteses primeiro)
z = 2 ** 10        # 1024
r = 17 % 5         # 2
d = 17 // 5        # 3
```

**Atribuição composta:**

```
x = 10
x += 5    # x = 15
x -= 3    # x = 12
x *= 2    # x = 24
x /= 4    # x = 6.0
x %= 4    # x = 2.0
```

---

### Comparação e lógica

| Operador | Descrição |
|----------|-----------|
| `==` | Igual |
| `!=` | Diferente |
| `>` `<` | Maior / menor |
| `>=` `<=` | Maior ou igual / menor ou igual |
| `e` | E lógico (ambos verdadeiros) |
| `ou` | OU lógico (um ou outro) |
| `nao` | NÃO lógico (inverte) |

```
# Comparações
x = 10
print x > 5        # true
print x == 10      # true
print x != 7       # true

# Lógicos
idade = 20
cnh   = true

se idade >= 18 e cnh {
    print "Pode dirigir"
}

se nota < 5 ou faltou_muito {
    print "Reprovado"
}

se nao logado {
    print "Faça login primeiro"
}
```

---

### Condicionais — se / senao

```
se CONDIÇÃO {
    # bloco executado se verdadeiro
} senao se OUTRA_CONDIÇÃO {
    # bloco executado se a segunda for verdadeira
} senao {
    # bloco padrão
}
```

```
nota = 72

se nota >= 90 {
    print "A — Excelente"
} senao se nota >= 70 {
    print "B — Bom"
} senao se nota >= 50 {
    print "C — Recuperação"
} senao {
    print "F — Reprovado"
}
```

**Condicional em linha** (bloco de uma instrução):

```
se x > 0 { print "positivo" }
```

---

### Loop enquanto

```
enquanto CONDIÇÃO {
    # repete enquanto a condição for verdadeira
}
```

```
i = 1
enquanto i <= 10 {
    print i
    i += 1
}
```

**`pare`** — sai do loop  
**`continua`** — pula para a próxima iteração

```
i = 0
enquanto i < 100 {
    i += 1
    se i % 2 == 0 { continua }   # pula pares
    se i > 15     { pare }        # para em 15
    print i                        # imprime só ímpares até 15
}
```

---

### Loop `para` — o mais simples do mundo

O `para` do Sintax tem **quatro formas** — escolha a mais natural para cada situação:

#### Forma 1 — contar de 0 até N (mais simples)
```
para i 5 {
    print i    # imprime 0, 1, 2, 3, 4
}
```

#### Forma 2 — contar até N explícito
```
para i ate 10 {
    print i    # 0 até 9
}
```

#### Forma 3 — de A até B
```
para i de 1 ate 6 {
    print i    # 1, 2, 3, 4, 5
}
```

#### Forma 4 — de A até B com passo
```
# Pares de 0 a 10
para i de 0 ate 11 passo 2 {
    print i    # 0, 2, 4, 6, 8, 10
}

# Contagem regressiva
para i de 10 ate 0 passo -1 {
    print i    # 10, 9, 8, ... 1
}
```

#### Forma 5 — para cada item em iterável
```
frutas = ["maçã", "banana", "laranja"]
para fruta em frutas {
    print "- {fruta}"
}

# Funciona também com strings (letra a letra)
para letra em "sintax" {
    print letra
}

# E com dicionários (itera as chaves)
config = {"host": "localhost", "porta": 5432}
para chave em config {
    print "{chave} = {config[chave]}"
}
```

**Comparação com Python:**

| Situação | Python | Sintax |
|----------|--------|--------|
| 0 até N | `for i in range(N):` | `para i N {` |
| 1 até N | `for i in range(1, N+1):` | `para i de 1 ate N+1 {` |
| Com passo | `for i in range(0,10,2):` | `para i de 0 ate 10 passo 2 {` |
| Em lista | `for x in lista:` | `para x em lista {` |

---

### Funções

```
func NOME(param1, param2 = valorPadrao) {
    # corpo
    return valor
}
```

```
# Sem retorno
func saudar(nome) {
    print "Olá, {nome}!"
}

# Com retorno
func somar(a, b) {
    return a + b
}

# Com valor padrão
func potencia(base, exp = 2) {
    return base ** exp
}

# Recursão
func fatorial(n) {
    se n <= 1 { return 1 }
    return n * fatorial(n - 1)
}

# Closure — função que retorna função
func multiplicador(fator) {
    func aplicar(x) {
        return x * fator
    }
    return aplicar
}

# ── Usando ────────────────────────────────
saudar("Maria")

total = somar(10, 20)
print total

print potencia(3)       # 9  (usa padrão exp=2)
print potencia(2, 10)   # 1024

print fatorial(10)      # 3628800

triplicar = multiplicador(3)
print triplicar(7)      # 21
```

**Funções são valores** — podem ser passadas como argumentos:

```
func aplicar_em_lista(f, lista) {
    resultado = []
    para item em lista {
        resultado.adicionar(f(item))
    }
    return resultado
}

func dobro(x) { return x * 2 }

nums    = [1, 2, 3, 4, 5]
dobros  = aplicar_em_lista(dobro, nums)
print dobros    # [2, 4, 6, 8, 10]
```

---

### Listas

```
# Criar
nums   = [10, 20, 30, 40, 50]
nomes  = ["Ana", "Bruno", "Carla"]
mista  = [1, "dois", true, nulo]
vazia  = []

# Acessar (índice começa em 0)
print nums[0]          # 10
print nums[-1]         # 50  (negativo = de trás)

# Modificar
nums[2] = 99

# Tamanho
print len(nums)        # 5
```

**Métodos de lista:**

```
lista = [3, 1, 4, 1, 5]

lista.adicionar(9)          # adiciona ao final
lista.inserir(0, 0)         # insere no índice 0
lista.remover(1)            # remove o valor 1 (primeiro)
lista.pop()                 # remove e retorna o último
lista.pop(2)                # remove e retorna o índice 2

ord  = ordenar(lista)       # retorna nova lista ordenada
inv  = inverter(lista)      # retorna nova lista invertida
fat  = lista.fatiar(1, 3)   # retorna [1, 3]
tem  = lista.contem(5)      # true ou false
idx  = lista.indice(4)      # índice do valor 4
uni  = lista.unir(", ")     # "3, 4, 5, 9"
lista.limpar()              # esvazia a lista
cop  = lista.copiar()       # cria cópia

# Funções de ordem superior
func par(n)    { return n % 2 == 0 }
func quadrado(n) { return n * n }

pares     = filtrar(par, nums)
quadrados = mapear(quadrado, nums)
```

---

### Dicionários

```
# Criar
pessoa = {
    "nome":  "Carlos",
    "idade": 30,
    "ativo": true
}

# Acessar
print pessoa["nome"]
print pessoa["idade"]

# Adicionar / modificar
pessoa["email"] = "carlos@email.com"
pessoa["idade"] = 31

# Verificar existência
se pessoa.tem("email") {
    print "Email: " + pessoa["email"]
}

# Acesso com fallback
cidade = pessoa.get("cidade", "não informado")
print cidade

# Remover campo
pessoa.remover("ativo")

# Iterar
para chave em pessoa.chaves() {
    print "{chave}: {pessoa[chave]}"
}

# Tamanho
print len(pessoa)

# Dicionário aninhado
servidor = {
    "db": {
        "host": "localhost",
        "porta": 5432
    },
    "debug": true
}
print servidor["db"]["host"]
```

---

### Strings avançadas

```
s = "  Olá, Mundo!  "

# Propriedades e métodos
print s.tamanho            # 15  (propriedade, sem parênteses)
print s.maiusculo()        # "  OLÁ, MUNDO!  "
print s.minusculo()        # "  olá, mundo!  "
print s.capitalizar()      # "  olá, mundo!  " → "  Olá, mundo!  "
print s.strip()            # "Olá, Mundo!"
print s.lstrip()           # "Olá, Mundo!  "
print s.rstrip()           # "  Olá, Mundo!"
print s.contem("Mundo")    # true
print s.começa_com("  O")  # true
print s.termina_com("!  ") # true
print s.substituir("Mundo", "Sintax")   # "  Olá, Sintax!  "
print s.encontrar("Mundo") # 6  (índice)
print s.repetir(2)         # "  Olá, Mundo!    Olá, Mundo!  "

# Dividir
partes = "a,b,c,d".dividir(",")
print partes     # [a, b, c, d]

# Verificações
print "42".é_número()          # true
print "abc".é_alfanumérico()   # true

# Caracteres de escape
print "linha1\nlinha2"
print "col1\tcol2"

# Interpolação de expressões
x = 5
print "O dobro de {x} é {x * 2}"
print "Lista: {[1,2,3]}"
```

---

### Escopo e global

```
contador = 0

func incrementar() {
    global contador    # declara que 'contador' é a variável global
    contador += 1
}

func resetar() {
    global contador
    contador = 0
}

incrementar()
incrementar()
incrementar()
print contador    # 3

resetar()
print contador    # 0
```

**Regra:** dentro de uma função, variáveis são locais por padrão.  
Use `global nome` para acessar e modificar uma variável global.

---

### Import — módulos

```
import math
import random
import random como r    # alias
import tempo
import arquivo
import json
import os
```

```
# Usar funções do módulo com ponto
import math
print math.pi               # 3.141592653589793
print math.raiz(144)        # 12.0
print math.sen(math.rad(90))  # 1.0

# Com alias
import random como r
n = r.inteiro(1, 100)
print n
```

**Importar arquivos `.stx` como módulo:**

```
# meu_modulo.stx
PI = 3.14159

func area(r) {
    return PI * r * r
}
```

```
# main.stx
import meu_modulo como m
print m.PI
print m.area(5)
```

---

## Funções da biblioteca padrão

Disponíveis globalmente, sem precisar de `import`:

### Tipos e conversão

| Função | Descrição | Exemplo |
|--------|-----------|---------|
| `int(x)` / `inteiro(x)` | Converte para inteiro | `int("42")` → `42` |
| `float(x)` / `decimal(x)` | Converte para decimal | `float("3.14")` → `3.14` |
| `str(x)` / `texto(x)` | Converte para texto | `str(100)` → `"100"` |
| `bool(x)` | Converte para booleano | `bool(0)` → `false` |
| `tipo(x)` | Retorna o tipo como texto | `tipo(42)` → `"inteiro"` |
| `lista(x)` | Converte para lista | `lista("abc")` → `["a","b","c"]` |

### Tamanho e coleções

| Função | Descrição |
|--------|-----------|
| `len(x)` / `tam(x)` | Tamanho de lista, string ou dicionário |
| `range(n)` / `intervalo(n)` | Lista de 0 a n-1 |
| `range(a, b)` | Lista de a até b-1 |
| `range(a, b, passo)` | Lista com passo |
| `ordenar(lista)` | Lista ordenada (crescente) |
| `ordenar(lista, true)` | Lista ordenada (decrescente) |
| `inverter(lista)` | Lista invertida |
| `filtrar(func, lista)` | Filtra elementos |
| `mapear(func, lista)` | Transforma elementos |
| `zip(a, b)` | Combina duas listas |
| `enumerar(lista)` | Adiciona índices |
| `soma(lista)` | Soma todos os elementos |
| `max(a, b)` / `max(lista)` | Maior valor |
| `min(a, b)` / `min(lista)` | Menor valor |

### Matemática

| Função | Descrição |
|--------|-----------|
| `abs(x)` | Valor absoluto |
| `round(x)` / `arredondar(x)` | Arredonda |
| `round(x, n)` | Arredonda com n casas decimais |
| `sqrt(x)` / `raiz(x)` | Raiz quadrada |
| `piso(x)` | Arredonda para baixo (inteiro) |
| `teto(x)` | Arredonda para cima (inteiro) |
| `pot(x, n)` | Potência x^n |
| `log(x)` | Logaritmo natural |
| `sen(x)` / `cos(x)` / `tan(x)` | Trigonometria (radianos) |

### I/O e debug

| Função | Descrição |
|--------|-----------|
| `input("msg")` / `leia("msg")` | Lê entrada do usuário |
| `debug(x, ...)` | Imprime com `[DEBUG]` |
| `repr(x)` | Representação legível do valor |
| `assert(cond, "msg")` | Para se a condição for falsa |
| `sair(codigo)` / `exit(codigo)` | Encerra o programa |

### JSON embutido

| Função | Descrição |
|--------|-----------|
| `json_string(obj)` | Converte objeto para JSON string |
| `json_parse(str)` | Converte JSON string para objeto |

### Verificações de tipo

```
é_texto(x)        é_inteiro(x)     é_decimal(x)
é_lista(x)        é_nulo(x)        é_função(x)
```

---

## Módulos disponíveis

### `math` / `matematica`

```
import math

math.pi          # 3.14159...
math.e           # 2.71828...
math.raiz(x)     # raiz quadrada
math.abs(x)      # valor absoluto
math.piso(x)     # arredonda para baixo
math.teto(x)     # arredonda para cima
math.round(x, n) # arredonda com n casas
math.pot(x, n)   # potência
math.log(x)      # logaritmo natural
math.log10(x)    # log base 10
math.log2(x)     # log base 2
math.sen(x)      # seno (radianos)
math.cos(x)      # cosseno
math.tan(x)      # tangente
math.rad(graus)  # graus para radianos
math.graus(rad)  # radianos para graus
math.hipo(a, b)  # hipotenusa
math.inf         # infinito
```

### `random` / `aleatorio`

```
import random como r

r.número()           # float entre 0 e 1
r.inteiro(min, max)  # inteiro entre min e max
r.escolher(lista)    # item aleatório da lista
r.embaralhar(lista)  # embaralha a lista (in-place)
r.amostra(lista, n)  # n itens aleatórios
r.seed(n)            # define a semente
```

### `tempo` / `time`

```
import tempo

tempo.agora()          # timestamp atual (float)
tempo.dormir(n)        # pausa por n segundos
tempo.formato("%Y-%m-%d %H:%M:%S")  # data/hora formatada
```

### `arquivo` / `file`

```
import arquivo

arquivo.ler("arq.txt")              # lê todo o arquivo
arquivo.escrever("arq.txt", "...")  # escreve (sobrescreve)
arquivo.adicionar("arq.txt", "...")  # adiciona ao final
arquivo.existe("arq.txt")           # true/false
arquivo.linhas("arq.txt")           # lista de linhas
```

### `json`

```
import json

json.parse('{"x": 1}')           # string → objeto
json.string(obj)                  # objeto → string
json.string(obj, 2)               # com indentação
json.salvar("dados.json", obj)    # salva em arquivo
json.carregar("dados.json")       # carrega de arquivo
```

### `os` / `sistema`

```
import os

os.cwd()                   # pasta atual
os.listar(".")             # listar arquivos
os.existe("arq.txt")       # verificar existência
os.criar_pasta("nova/")    # criar pasta
os.remover("arq.txt")      # remover arquivo
os.env("PATH")             # variável de ambiente
os.args()                  # argumentos da linha de comando
```

---

## Exemplos completos

### Sequência de Fibonacci

```
func fib(n) {
    se n <= 1 { return n }
    a = 0
    b = 1
    para i de 2 ate n + 1 {
        temp = a + b
        a    = b
        b    = temp
    }
    return b
}

para i ate 11 {
    print "fib({i}) = {fib(i)}"
}
```

---

### Verificador de número primo

```
func primo(n) {
    se n < 2 { return false }
    para i de 2 ate int(sqrt(n)) + 1 {
        se n % i == 0 { return false }
    }
    return true
}

primos = []
para n de 2 ate 51 {
    se primo(n) {
        primos.adicionar(n)
    }
}
print "Primos até 50: {primos}"
```

---

### Ordenação por bolha (Bubble Sort)

```
func bubble_sort(lista) {
    n = len(lista)
    para i ate n {
        para j de 0 ate n - i - 1 {
            se lista[j] > lista[j + 1] {
                temp        = lista[j]
                lista[j]    = lista[j + 1]
                lista[j + 1] = temp
            }
        }
    }
    return lista
}

nums = [64, 34, 25, 12, 22, 11, 90]
print "Antes:  {nums}"
bubble_sort(nums)
print "Depois: {nums}"
```

---

### Calculadora interativa

```
func calcular(a, op, b) {
    se op == "+" { return a + b }
    se op == "-" { return a - b }
    se op == "*" { return a * b }
    se op == "/" {
        se b == 0 { return "Erro: divisão por zero" }
        return a / b
    }
    return "Operador inválido"
}

print "=== Calculadora Sintax ==="
enquanto true {
    entrada = input("\nDigite (ex: 10 + 5) ou 'sair': ")
    se entrada == "sair" { pare }

    partes = entrada.dividir(" ")
    se len(partes) != 3 {
        print "Formato inválido. Use: número operador número"
        continua
    }

    a  = float(partes[0])
    op = partes[1]
    b  = float(partes[2])

    resultado = calcular(a, op, b)
    print "= {resultado}"
}

print "Tchau!"
```

---

### Análise de dados simples

```
import math

dados = [78, 95, 42, 88, 63, 91, 55, 76, 84, 69]

# Estatísticas
total  = soma(dados)
media  = total / len(dados)
maximo = max(dados)
minimo = min(dados)

# Variância
variancias = mapear(func(x) {
    return (x - media) ** 2
}, dados)
variancia = soma(variancias) / len(variancias)
desvio    = math.raiz(variancia)

print "=== Análise dos Dados ==="
print "N:        {len(dados)}"
print "Total:    {total}"
print "Média:    {round(media, 2)}"
print "Máximo:   {maximo}"
print "Mínimo:   {minimo}"
print "Desvio:   {round(desvio, 2)}"

# Acima da média
acima = filtrar(func(x) { return x > media }, dados)
print "Acima da média: {acima}"
```

> **Nota:** funções anônimas inline `func(x) { return x * 2 }` são suportadas diretamente como argumentos.

---

## Comparação com Python

| Conceito | Python | Sintax |
|----------|--------|--------|
| Imprimir | `print(x)` | `print x` |
| Entrada | `input("msg")` | `input("msg")` |
| Se | `if x > 0:` | `se x > 0 {` |
| Senão | `else:` | `senao {` |
| Senão se | `elif x > 0:` | `senao se x > 0 {` |
| While | `while x < 10:` | `enquanto x < 10 {` |
| For range | `for i in range(10):` | `para i 10 {` |
| For lista | `for x in lista:` | `para x em lista {` |
| Função | `def f(x):` | `func f(x) {` |
| Retorno | `return x` | `return x` |
| Import | `import math` | `import math` |
| Comentário | `# comentário` | `# comentário` |
| Nulo | `None` | `nulo` |
| E lógico | `and` | `e` |
| Ou lógico | `or` | `ou` |
| Não lógico | `not` | `nao` |
| Verdadeiro | `True` | `true` |
| Falso | `False` | `false` |

**Vantagens do Sintax:**
- `para i 10 {` é mais curto que `for i in range(10):`
- Sem indentação obrigatória — usa `{ }` como blocos
- Sem parênteses no `print`
- Interpola strings diretamente com `{expr}`
- Sem `:` no final de `se`, `enquanto`, `func`
- Em Português — mais acessível para quem não fala inglês

---

## Estrutura do projeto

```
Sintax/
├── main.py                   # Ponto de entrada + modo interativo (REPL)
├── src/
│   ├── tokens.py             # Definição de todos os tokens
│   ├── lexer.py              # Análise léxica: texto → tokens
│   ├── parser.py             # Análise sintática: tokens → AST
│   └── interpreter.py        # Execução: percorre a AST
├── examples/
│   ├── 01_basico.stx         # Variáveis, tipos, interpolação
│   ├── 02_aritmetica.stx     # Operações matemáticas
│   ├── 03_condicionais.stx   # se / senao se / senao
│   ├── 04_loops.stx          # enquanto, para (5 formas), pare, continua
│   ├── 05_funcoes.stx        # Funções, recursão, closures
│   ├── 06_listas.stx         # Listas e métodos
│   ├── 07_dicionarios.stx    # Dicionários
│   ├── 08_strings.stx        # Strings e métodos
│   ├── 09_modulos.stx        # math, random, tempo
│   ├── 10_arquivo_json.stx   # arquivo e json
│   └── 11_completo.stx       # Programa completo (relatório de IMC)
└── README.md
```

---

## Erros e mensagens

A Sintax fornece mensagens de erro claras com localização exata:

```
╔══ ERRO LÉXICO ══════════════════════════
║  arquivo.stx:5:12
╚► Caractere inesperado: '@'

╔══ ERRO DE SINTAXE ══════════════════════
║  arquivo.stx:10:1
╚► Esperava '{', encontrei 'print'

╔══ ERRO DE EXECUÇÃO ══════════════════════
║  em 'calcular'  linha 8
║  em 'main'  linha 20
╚► Variável 'resultado' não definida
```

**Erros comuns:**

| Mensagem | Causa | Solução |
|----------|-------|---------|
| `Caractere inesperado: '@'` | Símbolo inválido | Use apenas os operadores suportados |
| `Esperava '{'` | Bloco sem `{` | Adicione `{` e `}` |
| `Variável 'x' não definida` | Usou antes de declarar | Declare a variável antes |
| `'x' não é uma função` | Chamou variável como função | Verifique o nome |
| `Divisão por zero` | Divisor é 0 | Verifique antes de dividir |
| `Índice 5 fora do alcance` | Índice inválido | Índices vão de 0 a `len-1` |
| `Loop infinito detectado` | Condição nunca muda | Garanta que a condição muda |
| `Módulo 'x' não encontrado` | Nome errado no `import` | Verifique os módulos disponíveis |

> **Palavras reservadas** (não use como nomes de variáveis):
> `se` `senao` `enquanto` `para` `em` `de` `ate` `passo`
> `func` `return` `retorne` `print` `imprima`
> `pare` `continua` `global` `delete`
> `import` `importar` `como`
> `true` `false` `verdadeiro` `falso` `nulo`
> `e` `ou` `nao`

---

## Roadmap

| Recurso | Status |
|---------|--------|
| Strings com aspas simples `'texto'` | ✅ Pronto |
| Interpolação `"Olá {nome}"` | ✅ Pronto |
| Comentários `# ...` e `/* ... */` | ✅ Pronto |
| Divisão inteira `//` | ✅ Pronto |
| Parâmetros com valor padrão | ✅ Pronto |
| Closures e funções anônimas inline | ✅ Pronto |
| Módulos com `import ... como` | ✅ Pronto |
| Dicionários aninhados | ✅ Pronto |
| `delete variavel` | ✅ Pronto |
| `global variavel` | ✅ Pronto |
| Desestruturação `a, b = lista` | 🔜 Em breve |
| `tente / capturar` — tratamento de erros | 🔜 Em breve |
| Tipos personalizados `tipo Nome { ... }` | 🔜 Planejado |
| Compilar para bytecode | 🔜 Planejado |
| `para i, v em enumerar(lista)` | 🔜 Em breve |
| Multiline strings com ` ``` ` | 🔜 Planejado |

---

<div align="center">

**Sintax — Programação em Português, do jeito mais simples.**

</div>
