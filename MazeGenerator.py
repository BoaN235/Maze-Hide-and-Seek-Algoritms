import pygame
from random import choice
from CellClass import Cell

done = False

try:
    with open("config.txt", "r") as file:
        lines = file.readlines()
        TILE = int(lines[0].strip())
except FileNotFoundError:
    TILE = 50
print(f"Starting Maze Generator with tile size: {TILE}")

# Constants
RES = WIDTH, HEIGHT = 1202, 902
cols, rows = WIDTH // TILE, HEIGHT // TILE

# Pygame setup
pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

# Initialize the grid
grid_cells = [Cell(col, row, TILE, cols, rows) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []

# Main loop
while True:
    sc.fill(pygame.Color(50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # Draw all cells
    [cell.draw(sc) for cell in grid_cells]

    # Mark the current cell as visited and draw it
    current_cell.visited = True
    current_cell.draw_current_cell(sc)

    # Check for the next cell to move to
    next_cell = current_cell.check_neighbors(grid_cells)
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        Cell.remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    # Check if all cells are visited and if so, write to the file
    if all(cell.visited for cell in grid_cells):
        if done == False:
            with open("lastmaze.txt", "w") as file:
                file.write(str(TILE) + '\n')
                for x in grid_cells:
                    file.write(str(x.walls) + '\n')
            done = True


    # Update display
    pygame.display.flip()
    clock.tick(1000)  # Adjust the tick rate for smoother gameplay
