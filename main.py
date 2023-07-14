import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Dots")

# Define colors
BACKGROUND_COLOR = (10,10, 30)
DOT_COLOR = (255, 100, 100)

# Dot class
class Dot:
    def __init__(self, position, radius):
        self.position = pygame.Vector2(position)
        self.radius = radius
        self.mass = radius
        self.velocity = pygame.Vector2(0, 0)

    def draw(self):
        pygame.draw.circle(screen, DOT_COLOR, self.position, self.radius)

    def apply_force(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration

    def update(self):
        self.position += self.velocity

    def check_collision(self, other_dot):
        distance = other_dot.position - self.position
        radius_sum = self.radius + other_dot.radius
        if distance.length_squared() < radius_sum ** 2:
            return True
        return False

    def resolve_collision(self, other_dot):
        distance = self.position - other_dot.position
        distance.normalize_ip()
        relative_velocity = self.velocity - other_dot.velocity
        velocity_along_normal = relative_velocity.dot(distance)
        if velocity_along_normal > 0:
            return
        impulse_scalar = -(1 + 1) * velocity_along_normal / (self.mass + other_dot.mass)
        impulse = distance * impulse_scalar
        self.velocity += impulse / self.mass
        other_dot.velocity -= impulse / other_dot.mass

dots = []

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                position = pygame.mouse.get_pos()
                dot = Dot(position, 1)  # Start with a small radius
                dots.append(dot)
                start_time = pygame.time.get_ticks()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                end_time = pygame.time.get_ticks()
                duration = end_time - start_time
                dot = dots[-1]
                dot.radius = int(math.sqrt(duration))

    # Update the dots
    for dot in dots:
        force = pygame.Vector2(0, 0)
        for other_dot in dots:
            if dot is not other_dot:
                distance = pygame.Vector2(other_dot.position) - pygame.Vector2(dot.position)
                distance_squared = distance.length_squared()
                force += distance.normalize() * (other_dot.mass / distance_squared)
                if dot.check_collision(other_dot):
                    dot.resolve_collision(other_dot)
        dot.apply_force(force)
        dot.update()

    # Render the scene
    screen.fill(BACKGROUND_COLOR)
    for dot in dots:
        dot.draw()
    pygame.display.flip()

# Quit the game
pygame.quit()
