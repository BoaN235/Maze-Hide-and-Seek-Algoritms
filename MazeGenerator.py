import pygame
from CellClass import Cell

# Constants
try:
    with open("data/config.txt", "r") as file:
        file_contents = file.readlines()
        TILE = int(file_contents[0].strip())
except (FileNotFoundError, ValueError, SyntaxError) as e:
    print(f"Error loading maze state: {TILE}")
    TILE = 50
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

# Initialize the done variable
done = False

# Main loop
while True:
    sc.fill(pygame.Color(50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Draw all cells
    [cell.draw(sc) for cell in grid_cells]

    # Mark the current cell as visited and draw it
    current_cell.visited = True
    current_cell.draw_current_cell(sc)
    gen = True
    # Check for the next cell to move to
    next_cell = current_cell.check_neighbors(grid_cells, gen)
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        Cell.remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    # Check if all cells are visited and if so, write to the file
    if all(cell.visited for cell in grid_cells):
        if not done:
            
            with open("data/lastmaze.txt", "w") as file:
                file.write(str(TILE) + '\n')
                for x in grid_cells:
                    file.write(str(x.walls) + '\n')
            print("File written successfully.")
            done = True

    # Update display
    pygame.display.flip()
    clock.tick(1000)  # Adjust the tick rate for smoother gameplay