import pygame
import sys
import os
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TITLE_FONT_SIZE = 72
MENU_FONT_SIZE = 42

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
HIGHLIGHT = (255, 215, 0)  # Gold color for selected item
BACKGROUND_COLOR = (25, 25, 35)  # Dark blue-gray
TITLE_COLOR = (100, 200, 255)    # Light blue
MENU_BG_COLOR = (40, 40, 60)     # Slightly lighter blue-gray
PARTICLE_COLOR = (100, 200, 255, 128)  # Semi-transparent blue

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Menu de Jogos')
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 4)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)
        self.life = 1.0
        self.color = PARTICLE_COLOR

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 0.02
        self.size *= 0.95

    def draw(self, surface):
        alpha = int(self.life * 255)
        color = (*self.color[:3], alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))

class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
        self.selected_index = 0
        self.games = [
            {"name": "Snake", "path": "snake/snake_game.py", "color": (50, 255, 50)},
            {"name": "Forca", "path": "forca/forca.py", "color": (255, 50, 50)},
            {"name": "Adivinhação", "path": "adivinhacao/adivinhacao.py", "color": (50, 50, 255)}
        ]
        self.animation_time = 0
        self.particles = []
        self.menu_items = []
        self.initialize_menu_items()

    def initialize_menu_items(self):
        for i, game in enumerate(self.games):
            self.menu_items.append({
                "rect": pygame.Rect(WINDOW_WIDTH//2 - 200, 250 + i * 80, 400, 60),
                "hover": False,
                "glow": 0
            })

    def draw_gradient_background(self):
        for y in range(WINDOW_HEIGHT):
            # Create a subtle gradient from top to bottom
            color_value = int(25 + (y / WINDOW_HEIGHT) * 10)
            pygame.draw.line(screen, (color_value, color_value, color_value + 10), 
                           (0, y), (WINDOW_WIDTH, y))

    def draw_menu_item(self, text, pos, is_selected, animation_offset, color):
        # Draw menu item background
        bg_rect = pygame.Rect(WINDOW_WIDTH//2 - 200, pos - 30, 400, 60)
        if is_selected:
            # Animate the selected item
            pulse = math.sin(self.animation_time * 5) * 5
            bg_rect.inflate_ip(pulse, pulse)
            
            # Draw glow effect
            glow_surface = pygame.Surface((bg_rect.width + 20, bg_rect.height + 20), pygame.SRCALPHA)
            glow_color = (*color, 50)  # Semi-transparent color
            pygame.draw.rect(glow_surface, glow_color, (10, 10, bg_rect.width, bg_rect.height), border_radius=15)
            screen.blit(glow_surface, (bg_rect.x - 10, bg_rect.y - 10))
            
            # Draw main button
            pygame.draw.rect(screen, MENU_BG_COLOR, bg_rect, border_radius=15)
            pygame.draw.rect(screen, color, bg_rect, 3, border_radius=15)
        else:
            pygame.draw.rect(screen, MENU_BG_COLOR, bg_rect, border_radius=15)

        # Draw text with shadow
        text_color = color if is_selected else WHITE
        text_surface = self.menu_font.render(text, True, text_color)
        text_shadow = self.menu_font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2 + 2, pos + 2))
        text_shadow_rect = text_shadow.get_rect(center=(WINDOW_WIDTH//2, pos))
        screen.blit(text_shadow, text_shadow_rect)
        screen.blit(text_surface, text_rect)

    def update_particles(self):
        # Update existing particles
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

        # Add new particles
        if random.random() < 0.1:
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.particles.append(Particle(x, y))

    def draw(self):
        self.draw_gradient_background()
        
        # Draw particles
        for p in self.particles:
            p.draw(screen)
        
        # Draw title with shadow and glow
        title = self.title_font.render("Menu de Jogos", True, TITLE_COLOR)
        title_shadow = self.title_font.render("Menu de Jogos", True, (0, 0, 0))
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2 + 2, 102))
        title_shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH//2, 100))
        
        # Draw title glow
        glow_surface = pygame.Surface((title_rect.width + 40, title_rect.height + 40), pygame.SRCALPHA)
        glow_color = (*TITLE_COLOR, 30)  # Semi-transparent
        pygame.draw.rect(glow_surface, glow_color, (20, 20, title_rect.width, title_rect.height), border_radius=10)
        screen.blit(glow_surface, (title_rect.x - 20, title_rect.y - 20))
        
        screen.blit(title_shadow, title_shadow_rect)
        screen.blit(title, title_rect)

        # Draw menu items
        for i, game in enumerate(self.games):
            is_selected = i == self.selected_index
            animation_offset = math.sin(self.animation_time + i) * 5
            self.draw_menu_item(game["name"], 250 + i * 80, is_selected, animation_offset, game["color"])

        # Draw instructions with a semi-transparent background
        instructions_bg = pygame.Surface((600, 50), pygame.SRCALPHA)
        instructions_bg.fill((0, 0, 0, 128))
        screen.blit(instructions_bg, (WINDOW_WIDTH//2 - 300, WINDOW_HEIGHT - 70))
        
        instructions = self.menu_font.render("Use ↑↓ para navegar e ENTER para selecionar", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 45))
        screen.blit(instructions, instructions_rect)

    def run(self):
        running = True
        while running:
            self.animation_time += 0.016  # Approximately 60 FPS
            self.update_particles()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.games)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.games)
                    elif event.key == pygame.K_RETURN:
                        selected_game = self.games[self.selected_index]
                        pygame.quit()
                        os.system(f'python {selected_game["path"]}')
                        pygame.init()
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                        pygame.display.set_caption('Menu de Jogos')

            self.draw()
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    menu = Menu()
    menu.run() 