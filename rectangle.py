import pygame

# Define the size of the grid
GRID_SIZE = 20

# Define the dimensions of the grid
GRID_WIDTH = 30
GRID_HEIGHT = 20

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the obstacle value
OBSTACLE = 1

# Create a 2D array to represent the grid
grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

# Set the obstacles in the grid
grid[2][2] = OBSTACLE
grid[3][2] = OBSTACLE
grid[4][2] = OBSTACLE

# Initialize Pygame
pygame.init()

# Set the size of the window
WINDOW_SIZE = (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the title of the window
pygame.display.set_caption("Grid")

# Set the font
font = pygame.font.SysFont(None, 25)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if grid[y][x] == OBSTACLE:
                pygame.draw.rect(screen, RED, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw the text
    text = font.render("Click the window to quit", True, BLACK)
    screen.blit(text, (0, 0))

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
