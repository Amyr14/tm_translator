from src.traducao import simula_sipser, simula_infinita
from src.parsing import parseia_entrada, parseia_saida, verifica_header
from src.tipos import Programa
from os.path import join, splitext
from os import getcwd, listdir

entrada_dir = join(getcwd(), 'dados/entrada')
saida_dir = join(getcwd(), 'dados/saida')

if __name__ == '__main__':
    for idx, arquivo in enumerate(listdir(entrada_dir)):

        if splitext(arquivo)[1] != '.in':
            print(f'{idx} - {arquivo}: Extensão desconhecida')
            continue

        with open(join(entrada_dir, arquivo), 'r') as buffer_entrada:
            
            entrada: list[str] = buffer_entrada.readlines()
            
            # Verifica o header de tipo e o retira
            entrada_sem_header, tipo_entrada = verifica_header(entrada)

            # Parseia a entrada, gerando um programa
            programa: Programa = parseia_entrada(entrada_sem_header)

            # Realiza a traducao
            if tipo_entrada == 'sipser':
                programa_traduzido = simula_sipser(programa)
            
            elif tipo_entrada == 'infinita':
                programa_traduzido = simula_infinita(programa)

            else:
                print(f'{idx} - {arquivo}: Header desconhecido')

            # Parseia o programa traduzido, gerando um iterador de strings
            saida = parseia_saida(programa_traduzido)

            # Persiste a saida na pasta de saidas
            with open(join(saida_dir, splitext(arquivo)[0] + '.out'), 'w') as buffer_saida:
                buffer_saida.writelines(saida)
                print(f'{idx} - {arquivo}: Traduzido com sucesso!')
            
    print('Tradução finalizada')
