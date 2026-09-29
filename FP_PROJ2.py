'''
SCRABBLE2 - IST
Código escrito por: MARGARIDA MINEIRO IST1117883
LEIC-A Oct 2025
'''

ABC = ["A","B","C","Ç","D","E","F","G","H","I","J","L","M","N","O","P","Q","R","S","T","U","V","X","Z"]
PONTOS = {"A": 1,"B": 3,"C": 2,"Ç": 3,"D": 2,"E": 1,"F": 4,"G": 4,"H": 4,"I": 1,"J": 5,"L": 2,"M": 1,"N": 3,"O": 1,"P": 2,"Q": 6,"R": 1,"S": 1,"T": 1,"U": 1,"V": 4,"X": 8,"Z": 8}
OCC = {"A": 14,"B": 3,"C": 4,"Ç": 2,"D": 5,"E": 11,"F": 2,"G": 2,"H": 2,"I": 10,"J": 2,"L": 5,"M": 6,"N": 4,"O": 10,"P": 4,"Q": 1,"R": 6,"S": 8,"T": 5,"U": 7,"V": 2,"X": 1,"Z": 1}

#Lista de constantes: 
LINHAS, COLUNAS = 15, 15
TAM_MAX, TAM_MIN = 15, 2
HOR, VER = "H", "V"
LIVRE = "."

N1, N2, N3 = "FACIL", "MEDIO", "DIFICIL"
HUMAN, AGENT = "Humano", "Agente"
FINDER = "@"

LETRAS_POR_JOG = 7
NUM_DE_JOG_MIN, NUM_DE_JOG_MAX = 2, 4
INICIO = "Bem-vindo ao SCRABBLE2."
JOGA, PASSA, TROCA = "J", "P", "T"

#AUXILIARES:     
def joga_palavra(tab, palavra, casa, dir, letras, vocab):
    '''
    Tenta jogar uma palavra no tabuleiro e devolve as letras efetivamente usadas.

    Args:
        t (tabuleiro): Tabuleiro de Scrabble.
        p (str): Palavra a jogar.
        c (casa): Casa inicial.
        d (str): Direção ('H' horizontal, 'V' vertical).
        l (str): Letras disponíveis do jogador.
        vocab (dict): Vocabulário válido.

    Returns:
        tuple: Letras usadas do jogador na jogada; tuplo vazio se inválida.
    '''

    #Execução:
    if len(palavra) < 2: 
        return ()
    
    if dir == HOR: 
        if obtem_col(casa) + len(palavra) > COLUNAS + 1: 
            return ()
    if dir  == VER: 
        if obtem_lin(casa) + len(palavra) > LINHAS + 1: 
            return ()
    
    if dir == HOR:
        if obtem_col(casa) > 0 and (incrementa_casa(casa, dir, -1) != casa and obtem_letra(tab, incrementa_casa(casa, dir, -1)) != LIVRE): 
            return () 
        if obtem_col(casa) + len(palavra) < COLUNAS and (incrementa_casa(casa, dir, len(palavra)) != casa and obtem_letra(tab, incrementa_casa(casa, dir, len(palavra))) != LIVRE):
            return ()
    elif dir == VER:
        if obtem_lin(casa) > 0 and (incrementa_casa(casa, dir, -1) != casa and obtem_letra(tab, incrementa_casa(casa, dir, -1)) != LIVRE):
            return ()
        if obtem_lin(casa) + len(palavra) < LINHAS and (incrementa_casa(casa, dir, len(palavra)) != casa and obtem_letra(tab, incrementa_casa(casa, dir, len(palavra))) != LIVRE):
            return ()

    padrao = None
    
    if eh_tabuleiro_vazio(tab):
        if dir == HOR:
            casas = ()
            for idx in range(len(palavra)):
                if casa_val(obtem_lin(casa), obtem_col(casa) + idx):
                    casas += (cria_casa(obtem_lin(casa), obtem_col(casa) + idx),)
        elif dir == VER: 
            casas = ()
            for idx in range(len(palavra)):
                if casa_val(obtem_lin(casa) + idx, obtem_col(casa)):
                    casas += (cria_casa(obtem_lin(casa) + idx, obtem_col(casa)),)
            
        if cria_casa(8, 8) not in casas:
            return ()
        
        else: 
            inic = casa
            if dir == HOR: 
                if casa_val(obtem_lin(casa), obtem_col(casa) + len(palavra) - 1):
                    fin = cria_casa(obtem_lin(casa), obtem_col(casa) + len(palavra) - 1)
                    padrao = obtem_padrao(tab, inic, fin)
            elif dir == VER: 
                if casa_val(obtem_lin(casa) + len(palavra) - 1, obtem_col(casa)):
                    fin = cria_casa(obtem_lin(casa) + len(palavra) - 1, obtem_col(casa))
                    padrao = obtem_padrao(tab, inic, fin)

    else:   
        inic = casa
        if dir == HOR: 
            if casa_val(obtem_lin(casa), obtem_col(casa) + len(palavra) - 1):
                fin = cria_casa(obtem_lin(casa), obtem_col(casa) + len(palavra) - 1)
                padrao = obtem_padrao(tab, inic, fin)
        elif dir == VER: 
            if casa_val(obtem_lin(casa) + len(palavra) - 1, obtem_col(casa)):
                fin = cria_casa(obtem_lin(casa) + len(palavra) - 1, obtem_col(casa))
                padrao = obtem_padrao(tab, inic, fin)

    if padrao is None or not testa_palavra_padrao(vocab, palavra, padrao, letras):
        return ()
    else: 
        conj = ()

    for idx in range(len(palavra)): 
        if padrao[idx] == LIVRE: 
            conj += (palavra[idx],)
          
    tab = insere_palavra(tab, casa, dir, palavra) 
    return tuple(sorted(conj))

def sorts(vocab): 
    '''
    Ordena o vocabulário por tamanho, letra inicial, pontos decrescentes e ordem alfabética.

    Args:
        vocab (dict): Vocabulário desorganizado.

    Returns:
        dict: Vocabulário organizado e ordenado.
    '''

    #Execução:
    new_vocab = {}
    for tamanho in sorted(vocab): 
        new_vocab[tamanho] = {}
        for letra in sorted(vocab[tamanho]):
            new_vocab[tamanho][letra] = sorted(vocab[tamanho][letra], key = lambda x : (-x[1], [ABC.index(let) for let in x[0]]))

    return new_vocab

def eh_conj(conj): 
    '''
    Verifica se o argumento é um dicionário de letras com ocorrências válidas.

    Args:
        conj (any): Objeto a testar.

    Returns:
        bool: True se for um dicionário válido de letras, False caso contrário.
    '''

    #Execução:
    return type(conj) == dict or all([key in ABC and type(value) == int and value >= 0 for key, value in conj.items()])

def casa_val(lin, col): 
    '''
    Verifica se uma linha e coluna representam uma casa válida no tabuleiro.

    Args:
        lin (int): Número da linha.
        col (int): Número da coluna.

    Returns:
        bool: True se a casa estiver dentro dos limites do tabuleiro, False caso contrário.
    '''

    #Execução:
    if int(col) > COLUNAS or int(col) <= 0 or int(lin) > LINHAS or int(lin) <= 0:
        return False
    
    else: 
        return True

#---------------------------#

#2.1. TADs

#---------------------------#

#2.1.1. TAD CASA: tuplo com dois elementos (linhas e colunas)

#CONSTRUTOR:
def cria_casa(lin, col):
    '''
        Cria uma casa do tabuleiro de Scrabble.

        Args:
            lin (int): número da linha (1-15)
            col (int): número da coluna (1-15)

        Returns:
            tuple: casa representada pelo par (linha, coluna)

        Raises:
            ValueError: se os argumentos não forem inteiros válidos dentro dos limites.
    '''

    #Verificação:
    if type(lin) != int or type(col) != int or col > COLUNAS or col <= 0 or lin > LINHAS or lin <= 0: 
        raise ValueError("cria_casa: argumentos inválidos")
    
    #Execução:
    return (lin,col)

#SELETORES:
def obtem_col(casa): 
    '''
    obtem_col: casa (tuplo) → int
    Devolve a coluna da casa.
    '''
    #Verificação:
    if not eh_casa(casa): 
        raise ValueError("obtem_col: argumentos inválidos")
    
    #Execução:
    return casa[1] 

def obtem_lin(casa): 
    '''
    obtem_lin: casa (tuplo) → int
    Devolve a linha da casa.
    '''
    #Verificação:
    if not eh_casa(casa): 
        raise ValueError("obtem_lin: argumentos inválidos")

    #Execução:
    return casa[0]

#RECONHECEDORES:
def eh_casa(casa): 
    '''
    eh_casa: universal → bool
    Verifica se o argumento é uma casa válida do tabuleiro.
    '''

    #Execução:
    return type(casa) == tuple and len(casa) == 2 and type(casa[1]) == int and type(casa[0]) == int and casa[0] <= COLUNAS \
          and casa[1] > 0 and casa[1] <= LINHAS and casa[0] > 0

def casas_iguais(casa1, casa2): 
    '''
    casas_iguais: arg x arg → bool
    Devolve True se ambas as casas forem válidas e iguais.
    '''

    #Verificação: 
    if not eh_casa(casa1) or not eh_casa(casa2): 
        raise ValueError("casas_iguas: argumentos inválidos")
    
    #Execução:
    return casa1 == casa2

#TRANSFORMADORES:
def casa_para_str(casa): 
    '''
    casa_para_str: casa (tuplo) → str
    Devolve a representação textual da casa, no formato '(linha,coluna)'.

    Raises:
        ValueError: se o argumento não for uma casa válida.
    '''

    #Verificação: 
    if not eh_casa(casa): 
        raise ValueError("casa_para_str: argumento inválido")
    
    #Execução: 
    return f"({obtem_lin(casa)},{obtem_col(casa)})"
    
def str_para_casa(scasa): 
    '''
    str_para_casa: str → casa (tuplo)
    Converte a cadeia '(linha,coluna)' numa casa.

    Raises:
        ValueError: se a string não representar uma casa válida.
    '''
    
    #Verificação: 
    if type(scasa) != str or len(scasa) > 7 or len(scasa) < 5: 
        raise ValueError("str_para_casa: argumento inválido")
    
    #Execução:
    nums = scasa.strip("()")
    lin, col = nums.split(",")

    if casa_val: 
        casa = cria_casa(int(lin), int(col))
    if not eh_casa(casa): 
        raise ValueError("str_para_casa: argumento inválido")
        
    return casa

#FUNÇÕES DE ALTO NÍVEL:
def incrementa_casa(casa, dir, dist): 
    '''
    incrementa_casa: casa x str x int → casa
    Devolve a casa obtida ao mover-se a partir de c
    na direção d ('H' ou 'V') uma distância s ( ≥ 0 ).

    Args:
        c (tuple): casa inicial
        d (str): direção ('H' ou 'V')
        s (int): deslocamento positivo

    Returns:
        tuple: nova casa, ou a própria c se sair dos limites.

    Raises:
        ValueError: se os argumentos não forem válidos.
    '''

    #Verificação: 
    if not (eh_casa(casa) and type(dir) == str and (dir == HOR or dir == VER) and type(dist) == int): 
        raise ValueError("incrementa_casa: argumentos inválidos")

    #Execução: 
    if dir == HOR and obtem_col(casa) + dist <= COLUNAS and casa_val(obtem_lin(casa), obtem_col(casa) + dist):
        return cria_casa(obtem_lin(casa), obtem_col(casa) + dist)
    
    if dir == VER and obtem_lin(casa) + dist <= LINHAS and casa_val(obtem_lin(casa) + dist, obtem_col(casa)): 
        return cria_casa(obtem_lin(casa) + dist, obtem_col(casa))
    
    else: 
        return casa

#---------------------------#

#2.1.2. TAD JOGADOR: dicionário com três elementos (identidade(Humano ou Agente), pontos e letras) 

#CONSTRUTOR:
def cria_humano(nome):
    '''
    cria_humano: nome (str) → jogador (dict)
    Cria um jogador humano com o nome indicado.

    Args:
        nome (str): Nome do jogador humano.

    Returns:
        dict: jogador humano com campos "Humano", "Pontos" e "Letras".

    Raises:
        ValueError: se o nome for uma cadeia de caracteres vazia.
    '''

    #Verificação: 
    if type(nome) != str or nome == "" or nome[0] == '@': 
        raise ValueError("cria_humano: argumento inválido")
    
    #Execução: 
    return {HUMAN: nome, "Pontos": 0, "Letras": {}}

def cria_agente(nivel): 
    '''
    cria_agente: nivel (str) → jogador (dict)
    Cria um jogador agente (bot) com o nível de dificuldade especificado.

    Args:
        nivel (str): Nível do agente ('FACIL', 'MEDIO' ou 'DIFICIL').

    Returns:
        dict: jogador agente com campos "Agente", "Pontos" e "Letras".

    Raises:
        ValueError: se o nível não for um dos valores válidos.
    '''

    #Verificação: 
    if type(nivel) != str or (nivel != N1 and nivel != N2 and nivel != N3): 
        raise ValueError("cria_agente: argumento inválido")
    
    #Execução:
    return {AGENT: nivel, "Pontos": 0, "Letras": {}}

#SELETORES:
def jogador_identidade(jog): 
    '''
    jogador_identidade: jogador → str
    Devolve a identidade (nome ou nível) do jogador.
    '''

    #Verificação: 
    if not eh_jogador(jog):
        raise ValueError("jogador_identidade: argumento inválido")
    
    #Execução:
    if HUMAN in jog: 
        return jog[HUMAN]
    if AGENT in jog: 
        return jog[AGENT]
    
def jogador_pontos(jog): 
    '''
    jogador_pontos: jogador → int
    Devolve o número de pontos acumulados pelo jogador.
    '''

    #Verificação: 
    if not eh_jogador(jog):
        raise ValueError("jogador_pontos: argumento inválido")

    #Execução:
    return jog["Pontos"]

def jogador_letras(jog): 
    '''
    jogador_letras: jogador → str
    Devolve uma string contendo todas as letras que o jogador possui.
    '''

    #Verificação: 
    if not eh_jogador(jog):
        raise ValueError("jogador_letras: argumento inválido")
    
    #Execução:
    conj_lista = []
    for letras in ABC: 
        if letras in jog["Letras"]: 
            conj_lista += [letras,] * jog["Letras"][letras]

    return "".join(conj_lista)

#MODIFICADORES: 
def recebe_letra(jog, letra): 
    '''
    recebe_letra: jogador x dict → jogador
    Acrescenta a letra l ao conjunto de letras do jogador.
    '''

    #Verificação: 
    if not eh_jogador(jog) or letra not in ABC:
        raise ValueError("recebe_letra: argumentos inválidos")

    #Execução:
    if letra in jog["Letras"]: 
        jog["Letras"][letra] += 1
    else: 
        jog["Letras"][letra] = 1
    return jog

def usa_letra(jog, letra):
    '''
    usa_letra: jogador x dict → jogador
    Remove a letra l do conjunto de letras do jogador, se existir.
    '''

    #Verificação: 
    if not eh_jogador(jog) or letra not in ABC or letra not in jogador_letras(jog):
        raise ValueError("usa_letras: argumentos inválidos")

    #Execução: 
    if letra in jog["Letras"]: 
        jog["Letras"][letra] -= 1
    if jog["Letras"][letra] == 0: 
        del(jog["Letras"][letra])
    return jog

def soma_pontos(jog, pontos):
    '''
    soma_pontos: jogador x int → jogador
    Acrescenta p pontos ao total do jogador.
    '''

    #Verificação:
    if not eh_jogador(jog) or type(pontos) != int or pontos < 0:
        raise ValueError("soma_pontos: argumentos inválidos")
    
    #Execução: 
    jog["Pontos"] += pontos
    return jog

#RECONHECEDORES: 
def eh_jogador(arg): 
    '''
    eh_jogador: universal → bool
    Verifica se o argumento é um jogador válido.
    '''

    #Execução: 
    return type(arg) == dict and len(arg) == 3 and ((AGENT in arg and type(arg[AGENT]) == str) or (HUMAN in arg and type(arg[HUMAN]) == str))\
          and "Pontos" in arg and type(arg["Pontos"]) == int and arg["Pontos"] >= 0 and eh_conj(arg["Letras"]) and "Letras" in arg

def eh_humano(jog): 
    '''
    eh_humano: jogador (dict) → bool
    Verifica se o jogador é humano.
    '''

    #Execução:
    return eh_jogador(jog) and HUMAN in jog

def eh_agente(jog): 
    '''
    eh_agente: jogador (dict) → bool
    Verifica se o jogador é agente (bot).
    '''

    #Execução:
    return eh_jogador(jog) and AGENT in jog 

#TESTE: 
def jogadores_iguais(j1, j2): 
    '''
    jogadores_iguais: jogador x jogador → bool
    Devolve True se os dois jogadores forem iguais (mesmo tipo, nome/nível,
    pontos e letras).
    '''

    #Verificação:
    if not eh_jogador(j1) or not eh_jogador(j2): 
        raise ValueError("jogadores_iguais: argumentos inválidos")

    #Execução:
    return j1 == j2

#TRANSFORMADOR: 
def jogador_para_str(jog): 
    '''
    jogador_para_str: jogador → str
    Devolve a representação textual do jogador, no formato:
        'Nome (###): L1 L2 ...'
        'BOT(NIVEL) (###): L1 L2 ...'

    Raises:
        ValueError: se o argumento não for um jogador válido.
    '''

    #Verificação:
    if not eh_jogador(jog): 
        raise ValueError("jogador_para_str: argumento inválido")
    
    #Execução: 
    if eh_humano(jog): 
        if jogador_letras(jog) != "":
            return f"{jog[HUMAN]} ({jog['Pontos']:>3}): {' '.join(jogador_letras(jog))}"
        else: 
            return f"{jog[HUMAN]} ({jog['Pontos']:>3}):"
    if eh_agente(jog): 
        if jogador_letras(jog) != "":
            return f"BOT({jog[AGENT]}) ({jog['Pontos']:>3}): {' '.join(jogador_letras(jog))}"
        else: 
            return f"BOT({jog[AGENT]}) ({jog['Pontos']:>3}):"

#FUNÇÕES DE ALTO NÍVEL: 
def distribui_letras(jog, saco, num): 
    '''
    distribui_letras: jogador x list x int → jogador
    Retira até num letras do saco e distribui-as ao jogador.

    Args:
        j (dict): jogador.
        saco (list): saco de letras (lista de caracteres).
        num (int): número máximo de letras a distribuir.

    Returns:
        dict: jogador atualizado com novas letras.
    '''

    #Verificação:
    if not eh_jogador(jog) or type(saco) != list or type(num) != int or num < 0: 
        raise ValueError("distribui_letras: argumentos inválidos")

    #Execução: 
    for _ in range(num):
        if saco: 
            recebe_letra(jog, saco.pop())
    return jog

#---------------------------#

#2.1.3. TAD VOCABULARIO: dicionário de dicionários (tamanho -> inicial -> tuplos (palavra, pontuação))

#CONSTRUTOR:
def cria_vocabulario(vocab):
    '''
    cria_vocabulario: tuplo → vocabulario (dict)
    Cria um vocabulário a partir de um tuplo de palavras válidas.

    Args:
        v (tuple): tuplo contendo palavras (str) válidas.

    Returns:
        dict: estrutura de vocabulário organizada por comprimento e letra inicial.

    Raises:
        ValueError: se o argumento não for um tuplo de palavras válidas,
                    ou se alguma palavra contiver caracteres inválidos
                    ou tiver comprimento fora dos limites [2,15].
    '''

    #Verificação: 
    if type(vocab) != tuple or vocab == (): 
        raise ValueError("cria_vocabulario: argumento inválido")
    
    #Execução: 
    vocabulario = {}

    vocabset = set(vocab)
    if not len(vocabset) == len(vocab): 
        raise ValueError("cria_vocabulario: argumento inválido")

    for palavra in vocab:

        #Verificação: 
        if type(palavra) != str or len(palavra) > TAM_MAX or len(palavra) < TAM_MIN: 
            raise ValueError("cria_vocabulario: argumento inválido")
        
        else:

            pontos = 0 
            inic = palavra[0]
            tamanho = len(palavra)

            for car in palavra: 
                #Verificação: 
                if car not in ABC: 
                    raise ValueError("cria_vocabulario: argumento inválido")
                else: 
                    pontos += PONTOS[car] 
                    
            if tamanho not in vocabulario: 
                vocabulario[tamanho] = {}

            if inic not in vocabulario[tamanho]: 
                vocabulario[tamanho][inic] = []
            
            if (palavra, pontos) not in vocabulario[tamanho][inic]:
                vocabulario[tamanho][inic].append((palavra, pontos))
                    
    return sorts(vocabulario)

#SELETORES: 
def obtem_pontos(vocabulario, palavra):
    '''
    obtem_pontos: vocabulario (dict) x palavra (str) → pontos (int)
    Devolve o número de pontos da palavra, se ela existir no vocabulário.
    '''

    #Execução:
    tamanho = len(palavra)
    inicial = palavra[0]
    if tamanho in vocabulario and inicial in vocabulario[tamanho]: 
        for (padrao, pontos) in vocabulario[tamanho][inicial]:
            if palavra == padrao: 
                return pontos
    return 0

def obtem_palavras(vocabulario, comp, letra): 
    '''
    obtem_palavras: vocabulario (dict) x int x str → tuplo
    Devolve um tuplo ordenado de pares (palavra, pontos)
    com todas as palavras de comprimento comp e inicial letra.

    Args:
        vocabulario (dict): vocabulário.
        comp (int): comprimento da palavra.
        letra (str): letra inicial.

    Returns:
        tuple: lista de pares (palavra, pontos), ordenada por
               pontos decrescentes e ordem alfabética.
    '''

    #Execução:
    if comp in vocabulario and letra in vocabulario[comp]: 
        return tuple(vocabulario[comp][letra])
    else: 
        return ()

#TESTE:     
def testa_palavra_padrao(vocabulario, palavra, padrao, letras): 
    '''
    testa_palavra_padrao: vocabulario (dict) x str x str x str → bool
    Verifica se a palavra é compatível com o padrão e com as letras disponíveis.

    Args:
        vocabulario (dict): vocabulário.
        palavra (str): palavra a testar.
        padrao (str): padrão retirado do tabuleiro ('.' para casas livres).
        letras (str): letras disponíveis do jogador.

    Returns:
        bool: True se a palavra for compatível, False caso contrário.
    '''

    #Execução:
    tamanho = len(palavra)
    inicial = palavra[0]
    letras_list = list(letras)

    if tamanho not in vocabulario or inicial not in vocabulario[tamanho]:
        return False
    elif len(padrao) != len(palavra) or obtem_pontos(vocabulario, palavra) == 0:
        return False
    
    idx = 0
    while idx < tamanho: 
        if padrao[idx] == palavra[idx]: 
            idx += 1
        elif padrao[idx] == LIVRE: 
            if palavra[idx] not in letras_list: 
                return False
            letras_list.remove(palavra[idx])
            idx += 1
        else: 
            return False
    return True
                        
#TRANSFORMADOR: 
def ficheiro_para_vocabulario(nome_fich): 
    '''
    ficheiro_para_vocabulario: str → vocabulario
    Lê um ficheiro de texto e cria o vocabulário correspondente.

    Args:
        nome_fich (str): nome do ficheiro a ler.

    Returns:
        dict: estrutura de vocabulário gerada.

    !!! Este código tem repetições por motivos de eficiência !!!
    '''

    #Execução:
    vocabulario = {}
    with open(nome_fich, "r") as vocabulario_file: 
        palavras = vocabulario_file.readlines()
        for PALAVRA in map(lambda palavra: palavra.strip().upper(), palavras):
            if all([letra in ABC for letra in PALAVRA]) and TAM_MIN <= len(PALAVRA) <= TAM_MAX:
                pontos = sum(PONTOS[car] for car in PALAVRA)
                inic = PALAVRA[0]
                tamanho = len(PALAVRA)
                    
                if tamanho not in vocabulario: 
                    vocabulario[tamanho] = {}

                if inic not in vocabulario[tamanho]: 
                    vocabulario[tamanho][inic] = []
            
                if (PALAVRA, pontos) not in vocabulario[tamanho][inic]:
                    vocabulario[tamanho][inic].append((PALAVRA, pontos))

    return sorts(vocabulario)

def vocabulario_para_str(vocabulario):
    '''
    vocabulario_para_str: vocabulario → str
    Devolve uma representação textual do vocabulário,
    contendo todas as palavras ordenadas linha a linha.
    '''

    #Execução:
    res = []
    vocab = sorts(vocabulario)
    for tamanho in vocab: 
        for letra in vocab[tamanho]:
            res += [pal[0] for pal in vocab[tamanho][letra]]
    return "\n".join(res)

#FUNÇÕES DE ALTO NÍVEL:
def procura_palavra_padrao(vocabulario, padrao, letras, min_pontos): 
    '''
    procura_palavra_padrao: vocabulario x str x str x int → tuplo
    Procura a melhor palavra (maior pontuação) que se ajusta
    a um determinado padrão e às letras disponíveis.

    Args:
        vocabulario (dict): vocabulário.
        padrao (str): padrão do tabuleiro.
        letras (str): letras disponíveis.
        min_pontos (int): pontuação mínima desejada.

    Returns:
        tuple: (palavra, pontos) da melhor opção, ou ("", 0) se nenhuma servir.
    '''

    #Execução:
    possibilidades = []
    if padrao[0] in ABC: 
        for possibilidade in obtem_palavras(vocabulario, len(padrao), padrao[0]): 
            if possibilidade[1] is not None:
                if testa_palavra_padrao(vocabulario, possibilidade[0], padrao, letras) and possibilidade[1] >= min_pontos: 
                    possibilidades += [possibilidade]
    else:
        for letra in letras: 
            for possibilidade in obtem_palavras(vocabulario, len(padrao), letra):
                if possibilidade[1] is not None: 
                    if testa_palavra_padrao(vocabulario, possibilidade[0], padrao, letras) and possibilidade[1] >= min_pontos: 
                        possibilidades += [possibilidade]

    melhor = ("", 0)
    for opçao, pont in possibilidades: 
        if pont > melhor[1]:
            melhor = (opçao, pont)
    return melhor
    
#---------------------------#

#2.1.4. TAD TABULEIRO: lista de listas com string livres (".") ou ocupados (com letras válidas)

#CONSTRUTOR: 
def cria_tabuleiro(): 
    '''
    cria_tabuleiro: {} → tabuleiro
    Cria um tabuleiro de Scrabble vazio (15x15),
    onde cada posição contém o símbolo '.' (LIVRE).

    Returns:
        list: lista de listas representando o tabuleiro vazio.
    '''

    #Execução:
    tab = []
    for _ in range(LINHAS):
        tab += [list(LIVRE * COLUNAS).copy()]
    return tab

#SELETORES: 
def obtem_letra(tab, casa): 
    '''
    obtem_letra: tabuleiro x casa → str
    Devolve a letra presente na casa c do tabuleiro.

    Args:
        tab (list): tabuleiro.
        casa (tuple): casa (linha, coluna).

    Returns:
        str: letra presente na casa.
    '''

    #Execução:
    return tab[obtem_lin(casa) - 1][obtem_col(casa) - 1]

#MODIFICADORES: 
def insere_letra(tab, casa, letra): 
    '''
    insere_letra: tabuleiro x casa x str → tabuleiro
    Coloca a letra l na casa c do tabuleiro.

    Args:
        tab (list): tabuleiro.
        casa (tuple): casa (linha, coluna).
        letra (str): letra a inserir (deve estar em ABC).

    Returns:
        list: tabuleiro atualizado.
    '''
    
    #Execução:
    tab[obtem_lin(casa) - 1][obtem_col(casa) - 1] = letra
    return tab

#RECONHECEDOR: 
def eh_tabuleiro(arg): 
    '''
    eh_tabuleiro: universal → bool
    Verifica se o argumento é um tabuleiro válido de Scrabble.

    Returns:
        bool: True se for um tabuleiro 15x15 válido, False caso contrário.
    '''

    #Execução:
    return type(arg) == list and len(arg) == LINHAS and all(type(col) == list and len(col) == COLUNAS for col in arg)\
          and all(all(type(car) == str for car in col) for col in arg)

def eh_tabuleiro_vazio(arg): 
    ''''
    eh_tabuleiro_vazio: universal → bool
    Verifica se o argumento é um tabuleiro válido e se todas as casas estão livres.
    '''

    #Execução:
    return arg == cria_tabuleiro()

#TESTE: 
def tabuleiros_iguais(t1, t2): 
    '''
    tabuleiros_iguais: tabuleiro x tabuleiro → bool
    Devolve True se os dois tabuleiros forem iguais.
    '''

    #EXecução
    return eh_tabuleiro(t1) and eh_tabuleiro(t2) and t1 == t2

#TRANSFORMADOR: 
def tabuleiro_para_str(tab): 
    '''
    tabuleiro_para_str: tabuleiro → str
    Devolve uma representação textual formatada do tabuleiro de Scrabble.
    '''

    #Execução:
    res = "    "
    for n in range(1, COLUNAS + 1): 
        if n // 10 == 0: 
            res += "  "
        else: 
            res += f" {n // 10}"
    res += "\n    "

    for n in range(1, COLUNAS + 1):
        res += f" {n % 10}"

    res += "\n   +" + ("-" *  (COLUNAS * 2 + 1)) + "+\n"

    for n in range(0, LINHAS): 
        res += f"{n + 1:>2} | {' '.join(tab[n])} |\n"

    res += "   +" + ("-" * (COLUNAS * 2 + 1)) + "+"

    return res

#FUNÇÕES DE ALTO NÍVEL: 
def obtem_padrao(tab, inic, fin):
    '''
    obtem_padrao: tabuleiro x casa x casa → str
    Devolve o padrão de letras (ou '.') entre as casas inic e fin.

    Args:
        tab (list): tabuleiro.
        inic (tuple): casa inicial.
        fin (tuple): casa final.

    Returns:
        str: sequência de letras (ou '.') entre as duas casas.
    '''

    #Execução:
    padrao = ""
    if obtem_lin(inic) == obtem_lin(fin) and eh_casa(inic) and eh_casa(fin): 
        inc = obtem_col(inic)
        while inc <= obtem_col(fin): 
            if casa_val(obtem_lin(inic), inc):
                padrao += f"{obtem_letra(tab, cria_casa(obtem_lin(inic), inc))}"
                inc += 1

    elif obtem_col(inic) == obtem_col(fin) and eh_casa(inic) and eh_casa(fin): 
        inc = obtem_lin(inic)
        while inc <=  obtem_lin(fin): 
            if casa_val(inc, obtem_col(inic)): 
                padrao += f"{obtem_letra(tab, cria_casa(inc, obtem_col(inic)))}"
                inc += 1

    return padrao 

def insere_palavra(tab, casa, dir, palavra):
    '''
    insere_palavra: tabuleiro x casa x str x str → tabuleiro
    Insere a palavra p no tabuleiro, a partir da casa c,
    na direção d ('H' ou 'V').

    Args:
        tab (list): tabuleiro.
        casa (tuple): casa inicial.
        dir (str): direção ('H' ou 'V').
        palavra (str): palavra.

    Returns:
        list: tabuleiro atualizado.
    '''

    #Execução:
    if dir == HOR: 
        if obtem_col(casa) + len(palavra) > COLUNAS + 1: 
            return tab 
    if dir == VER: 
        if obtem_lin(casa) + len(palavra) > LINHAS + 1: 
            return tab 
        
    for let in palavra: 
        insere_letra(tab, casa, let)
        casa = incrementa_casa(casa, dir, 1)
    return tab

def obtem_subpadroes(tab, inic, fin, liv_max): 
    '''
    Devolve os subpadrões possíveis entre duas casas do tabuleiro.

    Args:
        tab (tabuleiro): Tabuleiro de jogo.
        inic (casa): Casa inicial do intervalo.
        fin (casa): Casa final do intervalo.
        liv_max (int): Máximo de espaços livres permitidos.

    Returns:
        tuple: Tuplo com os subpadrões possíveis.
    '''

    #Execução:
    subpad = ()
    ci = ()
    padrao = obtem_padrao(tab, inic, fin)

    if eh_casa(inic) and eh_casa(fin) and obtem_lin(inic) <= obtem_lin(fin):
    #HORIZONTAL
        if obtem_lin(inic) == obtem_lin(fin): 
            for inicio in range(len(padrao)): 
                quant = len(padrao)
                while quant > 0 and quant > inicio: 
                    lin = obtem_lin(inic)
                    coli = obtem_col(inic) + inicio
                    colf = obtem_col(inic) + quant - 1
                    existe_anterior, existe_seguinte = False, False
                    if casa_val(lin, coli - 1): 
                        anterior = cria_casa(lin, coli - 1)
                        existe_anterior = eh_casa(anterior) and obtem_letra(tab, anterior) != LIVRE
                    if casa_val(lin, colf + 1):
                        seguinte = cria_casa(lin, colf + 1)
                        existe_seguinte = eh_casa(seguinte) and obtem_letra(tab, seguinte) != LIVRE
                    if not existe_anterior and not existe_seguinte:
                        subpad += (padrao[inicio:quant],) 
                        ci += (cria_casa(obtem_lin(inic), obtem_col(inic) + inicio),)
                    quant -= 1 

    #VERTICAL
        elif obtem_col(inic) == obtem_col(fin): 
            for inicio in range(len(padrao)): 
                quant = len(padrao)
                while quant > 0 and quant > inicio: 
                    col = obtem_col(inic)
                    lini = obtem_lin(inic) + inicio
                    linf = obtem_lin(inic) + quant - 1
                    existe_anterior, existe_seguinte = False, False
                    if casa_val(lini - 1, col):
                        anterior = cria_casa(lini - 1, col)
                        existe_anterior = eh_casa(anterior) and obtem_letra(tab, anterior) != LIVRE
                    if casa_val(linf + 1, col):
                        seguinte = cria_casa(linf + 1, col)
                        existe_seguinte = eh_casa(seguinte) and obtem_letra(tab, seguinte) != LIVRE
                    if not existe_anterior and not existe_seguinte:
                        subpad += (padrao[inicio:quant],)
                        ci += (cria_casa(obtem_lin(inic) + inicio, obtem_col(inic)),)
                    quant -= 1 

    idx = 0
    while idx < len(subpad): 
        cc = 0 
        for car in subpad[idx]: 
            if car == LIVRE: 
                cc += 1
        if cc > liv_max or all([car == LIVRE for car in subpad[idx]]) or all([car in ABC for car in subpad[idx]]): 
            subpad = subpad[:idx] + subpad[idx+1:]
            ci = ci[:idx] + ci[idx+1:]
        else:
            idx += 1
    return (subpad, ci)

def gera_todos_padroes(tab, liv_max):
    '''
    Gera todos os subpadrões possíveis no tabuleiro.

    Args:
        tab (tabuleiro): Tabuleiro de jogo.
        liv_max (int): Máximo de espaços livres permitidos.

    Returns:
        tuple: Tupla com todos os subpadrões gerados.
    '''

    #Execução:
    pad = ()
    casas = ()
    dir = ()
    for lin in range(1, LINHAS + 1): 
        if casa_val(lin , 1) and casa_val(lin, COLUNAS):
            sub_pad, ci = obtem_subpadroes(tab, cria_casa(lin , 1), cria_casa(lin, COLUNAS), liv_max)
        for subpadroes in range(len(sub_pad)): 
            dir += (HOR,)
            pad += (sub_pad[subpadroes],)
            casas += (ci[subpadroes],)

    for col in range(1, COLUNAS + 1): 
        if casa_val(1, col) and casa_val(LINHAS, col):
            sub_pad, ci = obtem_subpadroes(tab, cria_casa(1 , col), cria_casa(LINHAS, col), liv_max)
        for subpadroes in range(len(sub_pad)): 
            dir += (VER,)
            pad += (sub_pad[subpadroes],)
            casas += (ci[subpadroes],)

    return (pad, casas, dir)

#---------------------------#

#2.2. FUNÇÕES ADICIONAIS

#---------------------------#

#2.2.1. 
def baralha_saco(estado):
    '''
    baralha_saco: int → list
    Baralha o saco de letras (lista de todas as letras disponíveis),
    usando um gerador pseudoaleatório baseado no estado dado.

    Args:
        estado (int): semente para gerar aleatoriedade.

    Returns:
        list: lista baralhada de letras.
    '''

    #Execução: 
    def permuta_letras(letras, estado): 
        
        def gera_numero_aleatorio(estado): 
            estado ^= (estado<<13) & 0xFFFFFFFF
            estado ^= (estado>>17) & 0xFFFFFFFF
            estado ^= (estado<<5) & 0xFFFFFFFF
            return estado
        
        for idx in range(len(letras)-1, 0, -1):
            j = gera_numero_aleatorio(estado) % (idx + 1)
            letras[j], letras[idx] = letras[idx], letras[j]
            estado = gera_numero_aleatorio(estado)

    conj_lista = []
    for letras in ABC: 
        if letras in OCC: 
            conj_lista += [letras,] * OCC[letras]
    permuta_letras(conj_lista, estado)
    return conj_lista

#2.2.2.
def jogada_humano(tab, jog, vocab, pilha): 
    '''
    Processa a jogada de um jogador humano, podendo jogar, passar ou trocar letras.

    Args:
        tab (list[list[str]]): Tabuleiro atual.
        jog (dict): Jogador humano.
        vocab (dict): Vocabulário válido.
        pilha (list): Saco de letras disponível.

    Returns:
        bool: True se o jogador realizou uma ação (jogar ou trocar), False se passou a vez.
    '''

    #Execução:
    while True: 
        jogada = input(f"Jogada {jogador_identidade(jog)}: ")
        jogada = jogada.split()

        if len(jogada) == 0:
            continue

        #PASSAR A VEZ
        if jogada[0] == PASSA and len(jogada) == 1:
            return False
        
        #JOGAR
        if jogada[0] == JOGA and len(jogada) == 5 and (jogada[3] == HOR or jogada[3] == VER) and not (int(jogada[1]) > LINHAS \
                or int(jogada[2]) > COLUNAS or int(jogada[1]) < 1 or int(jogada[2]) < 1):
            
            valido = ()
            if casa_val(jogada[1], jogada[2]):
                valido = joga_palavra(tab,jogada[-1],cria_casa(int(jogada[1]),int(jogada[2])),jogada[3],jogador_letras(jog), vocab)

            if valido == ():
                continue

            for elm in valido:
                usa_letra(jog, elm)

                if len(pilha) > 0:
                    nova_let = pilha.pop()
                    recebe_letra(jog, nova_let)

            soma_pontos(jog, obtem_pontos(vocab, jogada[-1]))
            return True

        #TROCAR LETRAS
        if jogada[0] == TROCA and len(jogada) > 1 and len(pilha) >= LETRAS_POR_JOG:

            letras = jogador_letras(jog)
            check = False
            for letra in jogada[1:]: 
                if letra in letras:
                    letras = letras.replace(letra, "", 1)
                else: 
                    check = True

            if check: 
                continue
             
            for i in range(1, len(jogada)):
                if jogada[i] in jogador_letras(jog): 
                    nova_let = pilha.pop()
                    usa_letra(jog, jogada[i])
                    recebe_letra(jog, nova_let)
            return True
        
#2.2.3.
def jogada_agente(tab, jog, vocab, pilha):  
    '''
    Decide e executa a jogada de um agente (bot), podendo jogar, passar ou trocar letras.

    Args:
        tab (list[list[str]]): Tabuleiro atual.
        jog (dict): Jogador agente.
        vocab (dict): Vocabulário válido.
        pilha (list): Saco de letras disponível.

    Returns:
        bool: True se o agente realizou uma ação (jogar ou trocar), False se passou a vez.
    '''

    #Execução:
    if eh_tabuleiro_vazio(tab): 
        print(f"Jogada {jogador_identidade(jog)}: P")
        return False 
    if len(jogador_letras(jog)) == 0: 
        print(f"Jogada {jogador_identidade(jog)}: P")
        return False 
    
    def jog_possivel(tab, jog): 
        padroes = gera_todos_padroes(tab, len(jogador_letras(jog)))
        if jogador_identidade(jog) == N1: 
            N = 100
        elif jogador_identidade(jog) == N2: 
            N = 50
        elif jogador_identidade(jog) == N3: 
            N = 10

        pad_c_d = [padroes[0][::N], padroes[1][::N], padroes[2][::N]]
        padroes_sel = pad_c_d[0]
        casas_sel = pad_c_d[1]
        dir_sel = pad_c_d[2]
        possivel = ("", 0)

        if padroes_sel == (): 
            return False
        
        melhor_c = None
        melhor_d = None
        for padrao, casa, dir in zip(padroes_sel, casas_sel, dir_sel): 
            pal, pont = procura_palavra_padrao(vocab, padrao, jogador_letras(jog), possivel[1] + 1) 
            if pont > possivel[1]: 
                possivel = pal, pont
                melhor_c = casa
                melhor_d = dir
        
        palavra = possivel[0]

        if melhor_c == None and melhor_d == None: 
            return False
        
        valido = joga_palavra(tab, palavra, melhor_c, melhor_d, jogador_letras(jog), vocab)

        if valido == ():     
            return False

        for elm in valido: 
            jog = usa_letra(jog, elm)
        jog = distribui_letras(jog, pilha, len(valido))

        jog = soma_pontos(jog, possivel[1])
        print(f"Jogada {jogador_identidade(jog)}: J {obtem_lin(melhor_c)} {obtem_col(melhor_c)} {melhor_d} {palavra}")
        return True
    
    jogada = jog_possivel(tab, jog)
    if jogada: 
        return jogada

    def troc_possivel(jog, pilha): 
        if len(pilha) >= LETRAS_POR_JOG: 
            print(f"Jogada {jogador_identidade(jog)}: T {' '.join(jogador_letras(jog))}")
            for letra in jogador_letras(jog): 
                jog = usa_letra(jog, letra)
            distribui_letras(jog, pilha, LETRAS_POR_JOG)
            return True
        else:
            return False
      
    c = troc_possivel(jog, pilha)
    if c: 
        return c
    else: 
        print(f"Jogada {jogador_identidade(jog)}: P")
        return c

#2.2.4.
def scrabble2(jogadores, nome_fich, estado): 
    '''
    scrabble2: tuplo x str x int → tuplo
    Função principal do jogo Scrabble2. Inicializa o jogo com os jogadores
    fornecidos, o ficheiro de vocabulário e o estado aleatório.

    Args:
        jogadores (tuple): nomes dos jogadores (com '@' para bots).
        nome_fich (str): nome do ficheiro de vocabulário.
        estado (int): estado inicial para baralhar o saco.

    Returns:
        tuple: pontuações finais de cada jogador.

    Raises:
        ValueError: se os argumentos forem inválidos.
    '''
    # tuplo de str letras do saco < letra max
    #Verificação: 
    if type(jogadores) != tuple or any([type(jog) != str for jog in jogadores]) \
        or type(nome_fich) != str or  2 > len(jogadores) or len(jogadores) > 4 or type(estado) != int or estado < 0: 
        raise ValueError("scrabble2: argumentos inválidos")

    #Execução:
    vocab = ficheiro_para_vocabulario(nome_fich)
    saco = baralha_saco(estado)
    jogs = []
    tab = cria_tabuleiro()
    for nome in jogadores: 
        if nome[0] == FINDER: 
            if (nome[1::] == N1 or nome[1::] == N2 or nome[1::] == N3):
                jogs += [cria_agente(nome[1::])]
            else: 
                raise ValueError("scrabble2: argumentos inválidos")
        else: 
            jogs += [cria_humano(nome)]
        
    if len(saco) < LETRAS_POR_JOG * len(jogs): 
        raise ValueError("scrabble2: argumentos inválidos")

    for jog in jogs: 
        jog = distribui_letras(jog, saco, 7)

    print(INICIO)
    ordem = 0
    num_jog = len(jogs)
    passa_cont = [True,] * num_jog
    while all([len(jogador_letras(jog)) != 0 for jog in jogs]) and saco != {}: 

        for jog in jogs:
            if any(passa_cont): 
                print(tabuleiro_para_str(tab))
                for jogador in jogs: 
                    print(jogador_para_str(jogador))

                if eh_humano(jog): 
                    jogada = jogada_humano(tab, jog, vocab, saco)
                if eh_agente(jog): 
                    jogada = jogada_agente(tab, jog, vocab, saco)

                passa_cont[ordem] = jogada
                ordem += 1
            else: 
                return tuple([jogador_pontos(jog) for jog in jogs])

        if ordem == num_jog:
            ordem = 0

    return tuple([jogador_pontos(jog) for jog in jogs])
