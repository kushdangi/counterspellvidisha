#firstGame


import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60
BIKE_WIDTH, BIKE_HEIGHT = 60, 80
OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH = 40, 100
OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT = 40, 80
OBSTACLE_SPEED = 5
OBSTACLE_ACCELERATION = 0.1  # Speed up the obstacles over time

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Bike Game")

# Bike settings
bike_x = WIDTH // 2
bike_y = HEIGHT - BIKE_HEIGHT - 20
bike_speed = 10

# Font for score
font = pygame.font.SysFont('Arial', 36)

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to generate random obstacles with random types
def generate_obstacle():
    width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
    x_pos = random.randint(0, WIDTH - width)  # Random horizontal position
    height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)

    # Randomly determine if obstacle is moving or stationary
    obstacle_type = random.choice(["moving", "stationary"])
    
    if obstacle_type == "moving":
        return {"rect": pygame.Rect(x_pos, -height, width, height), "type": "moving", "direction": random.choice(["left", "right"])}
    else:
        return {"rect": pygame.Rect(x_pos, -height, width, height), "type": "stationary"}

# Main game loop
def game_loop():
    global bike_x, OBSTACLE_SPEED, bike_speed
    score = 0
    clock = pygame.time.Clock()

    # List to hold obstacles
    obstacles = []
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get player input (move bike left and right)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bike_x > 0:
            bike_x -= bike_speed
        if keys[pygame.K_RIGHT] and bike_x < WIDTH - BIKE_WIDTH:
            bike_x += bike_speed

        # Increase difficulty over time:
        score += 1
        if score % 100 == 0:  # Every 100 points
            OBSTACLE_SPEED += OBSTACLE_ACCELERATION  # Gradual increase in obstacle speed
            bike_speed += 1  # Gradual increase in bike speed (making it harder to control)
            print(f"New obstacle speed: {OBSTACLE_SPEED}, New bike speed: {bike_speed}")

        # Generate obstacles (random chance)
        if random.randint(1, 40) == 1:  # More frequent obstacles
            obstacles.append(generate_obstacle())

        # Move obstacles down the screen
        for obstacle in obstacles:
            obstacle["rect"].y += OBSTACLE_SPEED
            
            # Handle moving obstacles
            if obstacle["type"] == "moving":
                if obstacle["direction"] == "left":
                    obstacle["rect"].x -= 2  # Move left
                    if obstacle["rect"].x <= 0:
                        obstacle["direction"] = "right"  # Change direction when hitting the screen edge
                else:
                    obstacle["rect"].x += 2  # Move right
                    if obstacle["rect"].x >= WIDTH - obstacle["rect"].width:
                        obstacle["direction"] = "left"  # Change direction when hitting the screen edge

        # Remove obstacles that have gone off-screen
        obstacles = [obstacle for obstacle in obstacles if obstacle["rect"].y < HEIGHT]

        # Check for collision with obstacles
        bike_rect = pygame.Rect(bike_x, bike_y, BIKE_WIDTH, BIKE_HEIGHT)
        for obstacle in obstacles:
            if bike_rect.colliderect(obstacle["rect"]):
                pygame.quit()
                sys.exit()  # End game on collision

        # Fill the screen with background color
        screen.fill(BLACK)

        # Draw the bike (green rectangle)
        pygame.draw.rect(screen, GREEN, (bike_x, bike_y, BIKE_WIDTH, BIKE_HEIGHT))

        # Draw obstacles (red rectangles)
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle["rect"])

        # Display score
        display_score(score)

        # Update the screen
        pygame.display.update()

        # Frame rate control
        clock.tick(FPS)

# Run the game
game_loop()
