import os

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def desenhar_forca(erros):
    """Retorna o desenho da forca baseado no número de erros"""
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

def mostrar_menu_principal():
    """Mostra o menu principal do jogo"""
    print('\n=== JOGO DA FORCA ===')
    print('\n1. Jogar')
    print('2. Ver Categorias')
    print('3. Sair')

def mostrar_categorias():
    """Mostra as categorias disponíveis"""
    from palavras import PALAVRAS
    print('\n=== CATEGORIAS DISPONÍVEIS ===')
    for categoria in PALAVRAS.keys():
        print(f'- {categoria.capitalize()}')
    input('\nPressione ENTER para voltar ao menu principal...')

def mostrar_estado_jogo(letras_acertadas, letras_erradas, tentativas):
    """Mostra o estado atual do jogo"""
    print('\nJOGO DA FORCA\n')
    print(desenhar_forca(len(letras_erradas)))
    print('\nPalavra:', ' '.join(letras_acertadas))
    print('\nLetras erradas:', ' '.join(letras_erradas))
    print(f'\nTentativas restantes: {tentativas}') 