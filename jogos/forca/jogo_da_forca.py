import random
import os

# ASCII art for the hangman
HANGMAN_STAGES = ['''
    +---+
        |
        |
        |
       ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\\  |
        |
       ===''', '''
    +---+
    O   |
   /|\\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\\  |
   / \\  |
       ===''']

# Lista de palavras para o jogo
PALAVRAS = [
    'python', 'programacao', 'computador', 'teclado', 'mouse',
    'internet', 'software', 'hardware', 'dados', 'algoritmo',
    'desenvolvimento', 'interface', 'sistema', 'rede', 'seguranca'
]

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def escolher_palavra():
    """Escolhe uma palavra aleatória da lista"""
    return random.choice(PALAVRAS)

def mostrar_forca(palavra_secreta, letras_corretas, tentativas):
    """Mostra o estado atual do jogo"""
    print(HANGMAN_STAGES[tentativas])
    print('\nPalavra:', end=' ')
    for letra in palavra_secreta:
        if letra in letras_corretas:
            print(letra, end=' ')
        else:
            print('_', end=' ')
    print('\n')

def jogar():
    """Função principal do jogo"""
    palavra_secreta = escolher_palavra()
    letras_corretas = set()
    letras_erradas = set()
    tentativas = 0
    max_tentativas = len(HANGMAN_STAGES) - 1

    while True:
        limpar_tela()
        mostrar_forca(palavra_secreta, letras_corretas, tentativas)
        
        # Mostra letras já tentadas
        if letras_erradas:
            print('Letras erradas:', ' '.join(sorted(letras_erradas)))
        
        # Verifica se ganhou
        if all(letra in letras_corretas for letra in palavra_secreta):
            print('\nParabéns! Você venceu!')
            print(f'A palavra era: {palavra_secreta}')
            break
        
        # Verifica se perdeu
        if tentativas >= max_tentativas:
            print('\nGame Over! Você perdeu!')
            print(f'A palavra era: {palavra_secreta}')
            break
        
        # Pega a letra do jogador
        letra = input('\nDigite uma letra: ').lower().strip()
        
        if len(letra) != 1 or not letra.isalpha():
            print('Por favor, digite apenas uma letra válida!')
            input('Pressione Enter para continuar...')
            continue
        
        if letra in letras_corretas or letra in letras_erradas:
            print('Você já tentou essa letra!')
            input('Pressione Enter para continuar...')
            continue
        
        # Verifica se a letra está na palavra
        if letra in palavra_secreta:
            letras_corretas.add(letra)
        else:
            letras_erradas.add(letra)
            tentativas += 1

def main():
    """Função principal que controla o fluxo do jogo"""
    while True:
        limpar_tela()
        print('=' * 30)
        print('Bem-vindo ao Jogo da Forca!')
        print('=' * 30)
        print('\n1. Jogar')
        print('2. Sair')
        
        opcao = input('\nEscolha uma opção: ')
        
        if opcao == '1':
            jogar()
            input('\nPressione Enter para continuar...')
        elif opcao == '2':
            print('\nObrigado por jogar!')
            break
        else:
            print('\nOpção inválida!')
            input('Pressione Enter para continuar...')

if __name__ == '__main__':
    main() 