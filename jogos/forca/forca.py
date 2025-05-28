import pygame
import random
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
BACKGROUND = (25, 25, 35)
GALLOWS_COLOR = (139, 69, 19)  # Brown
ROPE_COLOR = (101, 67, 33)     # Dark Brown

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jogo da Forca')
clock = pygame.time.Clock()

# Lista de palavras em português
PALAVRAS = [
    "PYTHON", "PROGRAMACAO", "COMPUTADOR", "ALGORITMO", "INTERFACE",
    "DESENVOLVIMENTO", "APLICACAO", "SISTEMA", "DADOS", "INTERNET",
    "TECNOLOGIA", "SOFTWARE", "HARDWARE", "REDE", "SEGURANCA"
]

class Hangman:
    def __init__(self):
        self.palavra = random.choice(PALAVRAS)
        self.letras_adivinhadas = set()
        self.erros = 0
        self.max_erros = 6
        self.animation_time = 0
        self.game_over = False
        self.victory = False
        self.shake_offset = 0
        self.shake_time = 0

    def adivinhar_letra(self, letra):
        if letra in self.palavra:
            self.letras_adivinhadas.add(letra)
            if all(letra in self.letras_adivinhadas for letra in self.palavra):
                self.victory = True
            return True
        else:
            self.erros += 1
            self.shake_time = 0.5  # Start shake animation
            if self.erros >= self.max_erros:
                self.game_over = True
            return False

    def desenhar_forca(self, surface):
        # Base da forca
        pygame.draw.rect(surface, GALLOWS_COLOR, (100, 500, 200, 20))
        # Poste vertical
        pygame.draw.rect(surface, GALLOWS_COLOR, (150, 200, 20, 300))
        # Trave horizontal
        pygame.draw.rect(surface, GALLOWS_COLOR, (150, 200, 150, 20))
        # Rope
        pygame.draw.line(surface, ROPE_COLOR, (250, 200), (250, 250), 5)

        # Desenhar o boneco
        if self.erros >= 1:  # Cabeça
            pygame.draw.circle(surface, WHITE, (250, 270), 20)
        if self.erros >= 2:  # Corpo
            pygame.draw.line(surface, WHITE, (250, 290), (250, 350), 5)
        if self.erros >= 3:  # Braço esquerdo
            pygame.draw.line(surface, WHITE, (250, 310), (220, 340), 5)
        if self.erros >= 4:  # Braço direito
            pygame.draw.line(surface, WHITE, (250, 310), (280, 340), 5)
        if self.erros >= 5:  # Perna esquerda
            pygame.draw.line(surface, WHITE, (250, 350), (220, 400), 5)
        if self.erros >= 6:  # Perna direita
            pygame.draw.line(surface, WHITE, (250, 350), (280, 400), 5)

    def desenhar_palavra(self, surface):
        font = pygame.font.Font(None, 48)
        palavra_display = ""
        for letra in self.palavra:
            if letra in self.letras_adivinhadas:
                palavra_display += letra + " "
            else:
                palavra_display += "_ "
        
        # Apply shake effect if needed
        shake_x = 0
        if self.shake_time > 0:
            shake_x = math.sin(self.animation_time * 50) * 10
            self.shake_time -= 1/60  # Decrease shake time

        text = font.render(palavra_display, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2 + shake_x, 100))
        surface.blit(text, text_rect)

    def desenhar_teclado(self, surface):
        font = pygame.font.Font(None, 36)
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letra in enumerate(letras):
            x = 400 + (i % 7) * 50
            y = 200 + (i // 7) * 50
            
            # Determine button color
            if letra in self.letras_adivinhadas:
                if letra in self.palavra:
                    color = GREEN
                else:
                    color = RED
            else:
                color = WHITE

            # Draw button
            pygame.draw.rect(surface, color, (x, y, 40, 40), border_radius=5)
            text = font.render(letra, True, BLACK)
            text_rect = text.get_rect(center=(x + 20, y + 20))
            surface.blit(text, text_rect)

    def desenhar_mensagem(self, surface):
        if self.game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("GAME OVER!", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 50))
            surface.blit(text, text_rect)
            
            # Show the word
            font = pygame.font.Font(None, 36)
            text = font.render(f"A palavra era: {self.palavra}", True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 150))
            surface.blit(text, text_rect)
        elif self.victory:
            font = pygame.font.Font(None, 72)
            text = font.render("VITÓRIA!", True, GREEN)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, 50))
            surface.blit(text, text_rect)

def main():
    hangman = Hangman()
    running = True

    while running:
        hangman.animation_time += 1/60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.system('python menu.py')
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    os.system('python menu.py')
                    sys.exit()
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letra = chr(event.key).upper()
                    if not hangman.game_over and not hangman.victory:
                        hangman.adivinhar_letra(letra)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not hangman.game_over and not hangman.victory:
                    # Check keyboard clicks
                    mouse_pos = pygame.mouse.get_pos()
                    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    for i, letra in enumerate(letras):
                        x = 400 + (i % 7) * 50
                        y = 200 + (i // 7) * 50
                        if (x <= mouse_pos[0] <= x + 40 and 
                            y <= mouse_pos[1] <= y + 40):
                            hangman.adivinhar_letra(letra)

        # Draw everything
        screen.fill(BACKGROUND)
        hangman.desenhar_forca(screen)
        hangman.desenhar_palavra(screen)
        hangman.desenhar_teclado(screen)
        hangman.desenhar_mensagem(screen)

        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = font.render("Pressione ESC para voltar ao menu", True, WHITE)
        screen.blit(instructions, (WINDOW_WIDTH - 250, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main() 