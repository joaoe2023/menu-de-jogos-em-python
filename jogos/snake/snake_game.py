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
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
BACKGROUND = (25, 25, 35)
GRID_COLOR = (40, 40, 60)
SNAKE_HEAD = (100, 255, 100)
SNAKE_BODY = (50, 200, 50)
SNAKE_PATTERN = (70, 180, 70)
TONGUE_COLOR = (255, 100, 100)
GRASS_COLOR = (30, 100, 30)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 4)
        self.life = 1.0
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 0.02
        self.size *= 0.95

    def draw(self, surface):
        alpha = int(self.life * 255)
        color = (*self.color, alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction
        self.score = 0
        self.animation_time = 0
        self.movement_progress = 0
        self.last_move_time = 0
        self.move_speed = 0.15
        self.growing = False
        self.tongue_out = False
        self.tongue_progress = 0
        self.particles = []

    def get_head_position(self):
        return self.positions[0]

    def update(self, current_time):
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

        # Update tongue animation
        if self.tongue_out:
            self.tongue_progress += 0.1
            if self.tongue_progress >= 1:
                self.tongue_out = False
                self.tongue_progress = 0

        # Smooth movement
        if current_time - self.last_move_time >= self.move_speed:
            self.direction = self.next_direction
            cur = self.get_head_position()
            x, y = self.direction
            new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
            
            if new in self.positions[3:]:
                # Create death particles
                for _ in range(20):
                    self.particles.append(Particle(
                        cur[0] * GRID_SIZE + GRID_SIZE/2,
                        cur[1] * GRID_SIZE + GRID_SIZE/2,
                        SNAKE_HEAD
                    ))
                return False
                
            self.positions.insert(0, new)
            if not self.growing:
                self.positions.pop()
            else:
                self.growing = False
                
            self.last_move_time = current_time
            self.movement_progress = 0

            # Randomly flick tongue
            if random.random() < 0.1:
                self.tongue_out = True
                self.tongue_progress = 0
        else:
            self.movement_progress = (current_time - self.last_move_time) / self.move_speed
            
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = self.direction
        self.score = 0
        self.growing = False
        self.movement_progress = 0
        self.particles = []

    def render(self, surface):
        # Draw particles
        for p in self.particles:
            p.draw(surface)

        for i, p in enumerate(self.positions):
            # Calculate interpolated position for smooth movement
            if i == 0 and len(self.positions) > 1:
                next_pos = self.positions[1]
                dx = (next_pos[0] - p[0]) * self.movement_progress
                dy = (next_pos[1] - p[1]) * self.movement_progress
                x = p[0] - dx
                y = p[1] - dy
            else:
                x, y = p

            # Calculate color based on position in snake
            if i == 0:  # Head
                color = SNAKE_HEAD
                size = GRID_SIZE
            else:  # Body
                color = SNAKE_BODY
                size = GRID_SIZE * 0.9

            # Add pulsing effect to the snake
            pulse = math.sin(self.animation_time * 5 + i * 0.5) * 0.1 + 0.9
            color = tuple(int(c * pulse) for c in color)

            # Draw snake segment with rounded corners
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, size, size)
            pygame.draw.rect(surface, color, rect, border_radius=5)

            # Add snake pattern
            if i > 0:  # Only on body segments
                pattern_rect = pygame.Rect(x * GRID_SIZE + size * 0.2, 
                                        y * GRID_SIZE + size * 0.2,
                                        size * 0.6, size * 0.6)
                pygame.draw.rect(surface, SNAKE_PATTERN, pattern_rect, border_radius=3)

            # Add shine effect
            if i == 0:  # Only on head
                shine = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.rect(shine, (255, 255, 255, 30), 
                               (0, 0, size, size), border_radius=5)
                surface.blit(shine, rect)

                # Draw eyes
                eye_size = size * 0.2
                eye_offset = size * 0.2
                if self.direction == RIGHT:
                    left_eye = (rect.right - eye_offset, rect.top + eye_offset)
                    right_eye = (rect.right - eye_offset, rect.bottom - eye_offset)
                elif self.direction == LEFT:
                    left_eye = (rect.left + eye_offset, rect.top + eye_offset)
                    right_eye = (rect.left + eye_offset, rect.bottom - eye_offset)
                elif self.direction == UP:
                    left_eye = (rect.left + eye_offset, rect.top + eye_offset)
                    right_eye = (rect.right - eye_offset, rect.top + eye_offset)
                else:  # DOWN
                    left_eye = (rect.left + eye_offset, rect.bottom - eye_offset)
                    right_eye = (rect.right - eye_offset, rect.bottom - eye_offset)

                pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size)
                pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size)

                # Draw tongue
                if self.tongue_out:
                    tongue_length = size * (0.5 + self.tongue_progress)
                    tongue_points = []
                    if self.direction == RIGHT:
                        base = (rect.right, rect.centery)
                        tongue_points = [
                            base,
                            (base[0] + tongue_length, base[1] - 5),
                            (base[0] + tongue_length + 5, base[1]),
                            (base[0] + tongue_length, base[1] + 5)
                        ]
                    elif self.direction == LEFT:
                        base = (rect.left, rect.centery)
                        tongue_points = [
                            base,
                            (base[0] - tongue_length, base[1] - 5),
                            (base[0] - tongue_length - 5, base[1]),
                            (base[0] - tongue_length, base[1] + 5)
                        ]
                    elif self.direction == UP:
                        base = (rect.centerx, rect.top)
                        tongue_points = [
                            base,
                            (base[0] - 5, base[1] - tongue_length),
                            (base[0], base[1] - tongue_length - 5),
                            (base[0] + 5, base[1] - tongue_length)
                        ]
                    else:  # DOWN
                        base = (rect.centerx, rect.bottom)
                        tongue_points = [
                            base,
                            (base[0] - 5, base[1] + tongue_length),
                            (base[0], base[1] + tongue_length + 5),
                            (base[0] + 5, base[1] + tongue_length)
                        ]
                    pygame.draw.lines(surface, TONGUE_COLOR, False, tongue_points, 2)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        self.animation_time = 0
        self.size = GRID_SIZE
        self.particles = []

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

    def update(self):
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()

        # Add new particles occasionally
        if random.random() < 0.1:
            self.particles.append(Particle(
                self.position[0] * GRID_SIZE + GRID_SIZE/2,
                self.position[1] * GRID_SIZE + GRID_SIZE/2,
                self.color
            ))

    def render(self, surface):
        # Draw particles
        for p in self.particles:
            p.draw(surface)

        # Animate the food
        pulse = math.sin(self.animation_time * 5) * 0.2 + 0.8
        color = tuple(int(c * pulse) for c in self.color)
        
        # Draw food with a glowing effect
        rect = pygame.Rect(self.position[0] * GRID_SIZE, 
                         self.position[1] * GRID_SIZE, 
                         self.size, self.size)
        
        # Draw glow
        glow = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color, 50), (self.size, self.size), self.size)
        surface.blit(glow, (rect.centerx - self.size, rect.centery - self.size))
        
        # Draw food as a small mouse
        pygame.draw.ellipse(surface, color, rect)  # Body
        pygame.draw.ellipse(surface, color, (rect.x - 5, rect.y + 5, 10, 5))  # Tail
        pygame.draw.ellipse(surface, color, (rect.x + 5, rect.y - 5, 5, 5))  # Ear
        pygame.draw.ellipse(surface, color, (rect.x + 15, rect.y - 5, 5, 5))  # Ear

        # Draw eyes
        pygame.draw.circle(surface, (0, 0, 0), (rect.x + 8, rect.y + 8), 2)
        pygame.draw.circle(surface, (0, 0, 0), (rect.x + 16, rect.y + 8), 2)

def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

def draw_grass():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            if random.random() < 0.3:  # 30% chance of grass in each cell
                grass_height = random.randint(2, 5)
                pygame.draw.line(screen, GRASS_COLOR,
                               (x + random.randint(0, GRID_SIZE), y + GRID_SIZE),
                               (x + random.randint(0, GRID_SIZE), y + GRID_SIZE - grass_height))

def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Pontuação: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_instructions():
    font = pygame.font.Font(None, 24)
    instructions = font.render("Pressione ESC para voltar ao menu", True, WHITE)
    screen.blit(instructions, (WINDOW_WIDTH - 250, 10))

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    snake = Snake()
    food = Food()
    animation_time = 0
    start_time = pygame.time.get_ticks()

    while True:
        current_time = (pygame.time.get_ticks() - start_time) / 1000.0
        animation_time += 0.016
        snake.animation_time = animation_time
        food.animation_time = animation_time

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
                elif event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT

        # Update game objects
        if not snake.update(current_time):
            snake.reset()
            food.randomize_position()
        food.update()

        # Check if snake ate the food
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            snake.growing = True
            # Create eating particles
            for _ in range(10):
                snake.particles.append(Particle(
                    food.position[0] * GRID_SIZE + GRID_SIZE/2,
                    food.position[1] * GRID_SIZE + GRID_SIZE/2,
                    food.color
                ))
            food.randomize_position()
            # Increase speed slightly
            snake.move_speed = max(0.05, snake.move_speed - 0.001)

        # Draw everything
        screen.fill(BACKGROUND)
        draw_grid()
        draw_grass()
        snake.render(screen)
        food.render(screen)
        draw_score(snake.score)
        draw_instructions()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main() 