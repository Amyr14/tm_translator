from src.tipos import Transicao, Programa


def get_transicoes_inicializacao(simbolos: list[str], marcador_final: bool) -> Programa:
    simbolo_final = '$' if marcador_final else '_'

    transicoes_init = [ 
        ['init-reset', '#', '*', 'r', 'comeco'],
        ['init-push-final', '*', simbolo_final, 'l', 'init-reset']
    ]

    # TODO: Verificar se isso nao quebra com o simbolo branco e/ou fita vazia
    for x in simbolos:
        if x != '_':
            transicoes_x = [
                ['0', x, '#', 'r', f'init-push-{x}'],
                [f'init-push-{x}', '_', x, 'r', 'init-push-final'],
                ['init-reset', x, '*', 'l', '*'],
                *[[f'init-push-{x}', y, x, 'r', f'init-push-{y}'] for y in simbolos if y != '_'] # fecho y
            ]

            transicoes_init.extend(transicoes_x)

    return transicoes_init


def get_simbolos(programa: Programa) -> tuple[list[str], list[str]]:
    simbolos: list[str] = []

    for transicao in programa:
        if transicao[1] not in simbolos:
            simbolos.append(transicao[1])
        
        if transicao[2] not in simbolos:
            simbolos.append(transicao[2])

    return simbolos

def get_estados(programa: Programa) -> tuple[list[str], list[str]]:
    estados: list[str] = []

    for transicao in programa:
        if transicao[0] not in estados:
            estados.append(transicao[0])

        if transicao[4] not in estados:
            estados.append(transicao[4])

    return estados


def get_estados_de_simulacao(programa: Programa) -> tuple[Programa, list[str]]:
    tabela_estados = {}
    contador = 1

    # Identifica os estados presentes na funcao programa
    estados = get_estados(programa)

    # Popula a tabela de estados de simulacao para futuro mapeamento
    for estado in estados:
        if estado == '0':
            tabela_estados[estado] = 'comeco'
        
        elif estado[0:4] == 'halt':
            tabela_estados[estado] = estado
        
        else:
            tabela_estados[estado] = str(contador)
            contador += 1
    
    # Mapeia os estados antigos para os novos, construindo uma nova funcao programa
    novo_programa = map(
        lambda transicao: [tabela_estados[transicao[0]], *transicao[1:4], tabela_estados[transicao[4]]],
        programa
    )
    
    return list(novo_programa), tabela_estados.values()


def simula_infinita(programa: Programa) -> Programa:
    
    '''
        Adiciona todas as transicoes necessarias para simular
        uma maquina de Turing no modelo de fita infinita
    '''

    simbolos = get_simbolos(programa)
    if '_' not in simbolos:
        simbolos.append('_')

    # Mapeia as labels de estado para um novo conjunto
    novo_programa, estados_simulacao = get_estados_de_simulacao(programa)

    # Gera as transicoes que inserem o simbolo inicial e final na fita
    transicoes_inicializacao = get_transicoes_inicializacao(simbolos, marcador_final=True)

    '''
        Se o simbolo lido for o marcador de inicio de fita:
            1 - Se a maquina estiver no estado X
                2 - Repetir ate encontrar o marcador de fim de fita
                    3 - Com estado atual X-leu-y e o simbolo lido for z
                        4 - Escrever y na fita, movimentar a cabeca para a direita
                            e ir para o estado X-leu-z
                5 - Ir para o estado X-leu-final, movimentar a cabeca para a esquerda
                6 - Movimentar a cabeca para a esquerda ate encontrar o simbolo inicial
                7 - Movimentar a cabeca para a direita e retornar ao estado X
    '''

    # Transicoes que empurram um branco no extremo direito da fita
    empurra_branco_dir = []
    for estado in estados_simulacao:
        empurra_branco_dir.extend([
            [estado, '$', '_', 'r', f'{estado}-push-$-dir'],
            [f'{estado}-push-$-dir', '*', '$', 'l', estado]
        ])

    # Transicoes que empurram um branco no extremo esquerdo da fita
    empurra_branco_esq = []
    for estado in estados_simulacao:
        empurra_branco_esq.extend([
            # Essa transicao comeca empurrar os simbolos da fita para a direita, guardando o estado
            [estado, '#', '*', 'r', f'{estado}-push-_-esq'], 
            # Essas transicoes finalizam o processo de empurrar os simbolos da fita para a direita, comecando o reset
            [f'{estado}-push-$-esq', '*', '$', 'l', f'{estado}-reset'],
            [f'{estado}-reset', '#', '*', 'r', estado]
        ])
        for x in simbolos:
            empurra_branco_esq.extend([
                [f'{estado}-push-{x}-esq', '$', x, 'r', f'{estado}-push-$-esq'],
                [f'{estado}-reset', x, '*', 'l', '*'],
                # Fecho da transicao do simbolo x com todos os outros simbolos (incluindo ele mesmo)
                *[[f'{estado}-push-{x}-esq', y, x, 'r', f'{estado}-push-{y}-esq'] for y in simbolos]
            ])

    novo_programa.extend(transicoes_inicializacao)
    novo_programa.extend(empurra_branco_dir)
    novo_programa.extend(empurra_branco_esq)            
    
    return novo_programa


def simula_sipser(programa: Programa):

    '''
        Adiciona todas as transicoes necessarias para simular
        uma maquina de Turing no modelo de Sipser
    '''

    # Identifica os simbolos presentes na funcao programa
    simbolos = get_simbolos(programa)

    # Gera as transicoes que inserem o marcador de inicio na fita
    transicoes_inicializacao = get_transicoes_inicializacao(simbolos, marcador_final=False)
    
    # Mapeia o conjunto de estados para um novo conjunto
    novo_programa, estados_simulacao = get_estados_de_simulacao(programa)
    
    # Adiciona as transicoes de inicializacao
    novo_programa.extend(transicoes_inicializacao)

    # Adiciona as transicoes de movimento a esquerda da fita
    for estado in estados_simulacao:
        novo_programa.append(
            [estado, '#', '*', 'r', '*']
        )
    
    return novo_programa