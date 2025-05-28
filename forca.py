import random  # Importa o módulo random para escolher palavras aleatórias
import os      # Importa o módulo os para limpar a tela do terminal
from palavras import obter_todas_palavras, obter_palavras_categoria
from interface import (
    limpar_tela, mostrar_menu_principal, mostrar_categorias,
    mostrar_estado_jogo
)

# Lista de palavras para o jogo
palavras = ['python', 'programacao', 'computador', 'teclado', 'mouse', 'monitor', 'internet', 'software', 'hardware', 'dados']

def limpar_tela():
    # Função que limpa a tela do terminal
    # 'cls' para Windows, 'clear' para Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def desenhar_forca(erros):
    # Função que desenha a forca baseada no número de erros
    # Retorna uma string ASCII art representando o estado atual da forca
    forca = [
        '''
           -----
           |   |
               |
               |
               |
               |
        =========''',
        '''
           -----
           |   |
           O   |
               |
               |
               |
        =========''',
        '''
           -----
           |   |
           O   |
           |   |
               |
               |
        =========''',
        '''
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========''',
        '''
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========''',
        '''
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========''',
        '''
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        ========='''
    ]
    return forca[erros]

def jogar_forca(categoria=None):
    """Função principal do jogo"""
    # Escolhe a palavra baseada na categoria ou todas as palavras
    if categoria:
        palavras = obter_palavras_categoria(categoria)
    else:
        palavras = obter_todas_palavras()
    
    palavra = random.choice(palavras)
    letras_acertadas = ['_' for _ in palavra]
    letras_erradas = []
    tentativas = 6
    acertos = 0

    while True:
        limpar_tela()
        mostrar_estado_jogo(letras_acertadas, letras_erradas, tentativas)

        if acertos == len(palavra):
            print('\nParabéns! Você venceu!')
            break

        if tentativas == 0:
            print('\nGame Over! Você perdeu!')
            print(f'A palavra era: {palavra}')
            break

        letra = input('\nDigite uma letra: ').lower()

        if len(letra) != 1 or not letra.isalpha():
            print('\nPor favor, digite apenas uma letra válida!')
            continue

        if letra in letras_acertadas or letra in letras_erradas:
            print('\nVocê já tentou esta letra!')
            continue

        if letra in palavra:
            for i, char in enumerate(palavra):
                if char == letra:
                    letras_acertadas[i] = letra
                    acertos += 1
        else:
            letras_erradas.append(letra)
            tentativas -= 1

        input('\nPressione ENTER para continuar...')

def main():
    """Função principal que controla o menu do jogo"""
    while True:
        limpar_tela()
        mostrar_menu_principal()
        
        opcao = input('\nEscolha uma opção: ')
        
        if opcao == '1':
            jogar_forca()
            input('\nPressione ENTER para voltar ao menu...')
        elif opcao == '2':
            mostrar_categorias()
        elif opcao == '3':
            print('\nObrigado por jogar!')
            break
        else:
            print('\nOpção inválida!')
            input('\nPressione ENTER para continuar...')

if __name__ == '__main__':
    main()  # Inicia o jogo quando o arquivo é executado diretamente 