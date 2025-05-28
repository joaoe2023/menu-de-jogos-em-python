import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da janela
LARGURA = 800
ALTURA = 600
TITULO = "Jogo de Adivinhação de Palavras"

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Lista de palavras para adivinhar
palavras = ["PYTHON", "JOGO", "COMPUTADOR", "PROGRAMACAO", "JANELA", "TECLADO", "MOUSE", "INTERFACE"]

# Configuração da janela
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

# Fonte
fonte = pygame.font.SysFont('Arial', 32)
fonte_pequena = pygame.font.SysFont('Arial', 24)

class JogoAdivinhacao:
    def __init__(self):
        self.palavra_atual = random.choice(palavras)
        self.palavra_oculta = ['_' for _ in self.palavra_atual]
        self.letras_usadas = set()
        self.tentativas = 6
        self.jogando = True
        self.mensagem = ""
        self.input_texto = ""
        self.input_ativo = False

    def processar_letra(self, letra):
        if letra in self.letras_usadas:
            self.mensagem = "Letra já usada!"
            return

        self.letras_usadas.add(letra)
        acertou = False

        for i, char in enumerate(self.palavra_atual):
            if char == letra:
                self.palavra_oculta[i] = letra
                acertou = True

        if not acertou:
            self.tentativas -= 1
            self.mensagem = "Letra errada!"
        else:
            self.mensagem = "Acertou!"

        if '_' not in self.palavra_oculta:
            self.mensagem = "Parabéns! Você venceu!"
            self.jogando = False
        elif self.tentativas == 0:
            self.mensagem = f"Game Over! A palavra era {self.palavra_atual}"
            self.jogando = False

    def reiniciar(self):
        self.__init__()

def main():
    jogo = JogoAdivinhacao()
    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and jogo.input_ativo:
                    if len(jogo.input_texto) == 1:
                        jogo.processar_letra(jogo.input_texto.upper())
                    jogo.input_texto = ""
                elif evento.key == pygame.K_BACKSPACE:
                    jogo.input_texto = jogo.input_texto[:-1]
                elif evento.key == pygame.K_r and not jogo.jogando:
                    jogo.reiniciar()
                elif len(jogo.input_texto) < 1 and evento.unicode.isalpha():
                    jogo.input_texto += evento.unicode.upper()

        # Desenho
        janela.fill(BRANCO)
        
        # Desenha a palavra oculta
        palavra_texto = fonte.render(' '.join(jogo.palavra_oculta), True, PRETO)
        janela.blit(palavra_texto, (LARGURA//2 - palavra_texto.get_width()//2, 200))

        # Desenha as tentativas restantes
        tentativas_texto = fonte_pequena.render(f'Tentativas restantes: {jogo.tentativas}', True, PRETO)
        janela.blit(tentativas_texto, (20, 20))

        # Desenha as letras já usadas
        letras_usadas_texto = fonte_pequena.render(f'Letras usadas: {", ".join(sorted(jogo.letras_usadas))}', True, PRETO)
        janela.blit(letras_usadas_texto, (20, 60))

        # Desenha a mensagem
        if jogo.mensagem:
            mensagem_texto = fonte_pequena.render(jogo.mensagem, True, VERMELHO)
            janela.blit(mensagem_texto, (LARGURA//2 - mensagem_texto.get_width()//2, 300))

        # Desenha o input
        input_texto = fonte_pequena.render(f'Digite uma letra: {jogo.input_texto}', True, AZUL)
        janela.blit(input_texto, (LARGURA//2 - input_texto.get_width()//2, 400))

        # Instruções
        if not jogo.jogando:
            instrucoes = fonte_pequena.render('Pressione R para reiniciar', True, VERDE)
            janela.blit(instrucoes, (LARGURA//2 - instrucoes.get_width()//2, 500))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 