from src.tipos import Programa, Transicao

 # Parsea as linhas da entrada, gerando um programa
def parseia_entrada(entrada: list[str]) -> Programa:
    programa = map(
        lambda linha: linha.split(),
        entrada
    )
    return list(programa)

def parseia_saida(programa: Programa):
    delimitador = ' '
    saida: list[str] = map(
        lambda transicao: delimitador.join(transicao) + '\n',
        programa
    )
    return list(saida)

def verifica_header(entrada: list[str]) -> tuple[list[str], str]:
    header = entrada[0]
    entrada_sem_header = entrada[1:]

    if header == ';S\n':
        tipo = 'sipser'

    elif header == ';I\n':
        tipo = 'infinita'

    else:
        tipo = 'desconhecido'
    
    return entrada_sem_header, tipo