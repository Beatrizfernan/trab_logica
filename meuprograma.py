from lark import Lark, Transformer

# Tokens e gramática
TOKEN_OR = "|"
TOKEN_AND = "&"
TOKEN_IMPL = "->"
TOKEN_NEG = "¬"

grammar = f"""
    start: expr

    ?expr: "(" expr "{TOKEN_OR}" expr ")"  -> or_
          | "(" expr "{TOKEN_AND}" expr ")"  -> and_
          | "(" expr "{TOKEN_IMPL}" expr ")"  -> impl_
          | "{TOKEN_NEG}" expr  -> not_
          | VAR

    VAR: /[a-z]+[_0-9]*/
"""

parser = Lark(grammar, start='start')

class SubformulaExtractor(Transformer):
    def __init__(self):
        self.main_conective = None
        self.immediate_subformulas = None

    def or_(self, args):
        self.main_conective = TOKEN_OR
        self.immediate_subformulas = [args[0], args[1]]
        return f"({args[0]}{TOKEN_OR}{args[1]})"

    def and_(self, args):
        self.main_conective = TOKEN_AND
        self.immediate_subformulas = [args[0], args[1]]
        return f"({args[0]}{TOKEN_AND}{args[1]})"

    def impl_(self, args):
        self.main_conective = TOKEN_IMPL
        self.immediate_subformulas = [args[0], args[1]]
        return f"({args[0]}{TOKEN_IMPL}{args[1]})"

    def not_(self, args):
        self.main_conective = TOKEN_NEG
        self.immediate_subformulas = [args[0]]
        return f"{TOKEN_NEG}{args[0]}"

    def VAR(self, token):
        self.main_conective = "atom"
        self.immediate_subformulas = [token.value]
        return token.value

    def start(self, args):
        return args[0]

class PropositionalFormula:
    @staticmethod
    def _get_parsed_formula(formula):
        try:
            return parser.parse(formula)
        except Exception as e:
            print(f"Error parsing formula: {e}")
            return None

    @staticmethod
    def get_main_conective_and_immediate_subformulas(formula):
        parse_tree = PropositionalFormula._get_parsed_formula(formula)
        if parse_tree is None:
            return None, None
        extractor = SubformulaExtractor()
        extractor.transform(parse_tree)
        return extractor.main_conective, extractor.immediate_subformulas

# Variáveis globais modificadas
caminho = []
listas_beta = []
pilha_ramos = []
literais = []
interpretacoes = []

def processa_alfas():
    global caminho, listas_beta
    encontrou_alpha = True
    while encontrou_alpha:
        encontrou_alpha = False
        for elemento in caminho[:]:
            if not (eh_beta(elemento) or eh_literal(elemento)):
                marcador, formula = elemento
                operador, subformulas = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)
                primeira_expansao, segunda_expansao = subformulas[0], subformulas[1] if operador != TOKEN_NEG else None

                if marcador:
                    if operador == TOKEN_AND:
                        marcador_primeira = marcador_segunda = True
                    elif operador == TOKEN_NEG:
                        marcador_primeira = False
                else:
                    if operador == TOKEN_OR:
                        marcador_primeira = marcador_segunda = False
                    elif operador == TOKEN_IMPL:
                        marcador_primeira = True
                        marcador_segunda = False
                    elif operador == TOKEN_NEG:
                        marcador_primeira = True

                caminho.append([marcador_primeira, primeira_expansao])
                listas_beta.append(eh_beta([marcador_primeira, primeira_expansao]))

                if operador != TOKEN_NEG:
                    caminho.append([marcador_segunda, segunda_expansao])
                    listas_beta.append(eh_beta([marcador_segunda, segunda_expansao]))

                if not all(listas_beta):
                    encontrou_alpha = True

                caminho.remove(elemento)
                listas_beta.remove(eh_beta(elemento))

def processa_beta():
    global caminho, listas_beta, pilha_ramos
    for i in range(len(listas_beta)):
        if listas_beta[i]:
            marcador, formula = caminho[i]
            operador, [primeira_expansao, segunda_expansao] = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula)

            if not marcador and operador == TOKEN_AND:
                marcador_primeira = marcador_segunda = False
            elif marcador:
                if operador == TOKEN_OR:
                    marcador_primeira = marcador_segunda = True
                elif operador == TOKEN_IMPL:
                    marcador_primeira = False
                    marcador_segunda = True

            listas_beta[i] = False
            pilha_ramos.append([[marcador_segunda, segunda_expansao], len(caminho), listas_beta.copy()])

            caminho.append([marcador_primeira, primeira_expansao])
            listas_beta.append(eh_beta([marcador_primeira, primeira_expansao]))

            break

def verifica_fechamento():
    global caminho, literais
    for i in range(len(caminho)):
        marcador, formula = caminho[i]
        if eh_literal(caminho[i]):
            if [not marcador, formula] in literais:
                return True
            literais.append([marcador, formula])
    return False

def retorna_ultimo_ramo():
    global caminho, listas_beta, pilha_ramos
    segunda_expansao, tamanho_atual, lista_beta_antiga = pilha_ramos.pop()
    caminho = caminho[:tamanho_atual]
    listas_beta = lista_beta_antiga
    caminho.append(segunda_expansao)
    listas_beta.append(eh_beta(segunda_expansao))

def imprime_interpretacoes():
    global caminho, interpretacoes
    for elemento in caminho:
        if eh_literal(elemento) and elemento not in interpretacoes:
            interpretacoes.append(elemento)
    for valor in interpretacoes:
        print(f"{'V' if valor[0] else 'F'}{valor[1]}")

def eh_beta(formula):
    operador, _ = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula[1])
    return (formula[0] == True and operador in [TOKEN_OR, TOKEN_IMPL]) or (formula[0] == False and operador == TOKEN_AND)

def eh_literal(formula):
    operador, _ = PropositionalFormula.get_main_conective_and_immediate_subformulas(formula[1])
    return operador == "atom"

def ler_entrada():
    import io
    import sys
    entrada = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    quantidade_formulas = int(entrada.readline().strip())
    for i in range(quantidade_formulas - 1):
        caminho.append([True, entrada.readline().strip()])
        listas_beta.append(eh_beta(caminho[i]))
    caminho.append([False, entrada.readline().strip()])
    listas_beta.append(eh_beta(caminho[-1]))

# Início da leitura e execução do processamento
ler_entrada()

while True:
    processa_alfas()
    if verifica_fechamento():
        if pilha_ramos:
            retorna_ultimo_ramo()
        else:
            print("Sequente válido")
            break
    else:
        if any(listas_beta):
            processa_beta()
        else:
            imprime_interpretacoes()
            break
