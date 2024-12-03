import pygame
from CellClass import Cell
from ActorClass import Actor, PreyActor, PredActor
import ast
import random


try:
    with open("config.txt", "r") as file:
        file_contents = file.readlines()
        MaxActions = int(file_contents[2].strip())
        seedvalue = int(file_contents[3].strip())
except (FileNotFoundError, ValueError, SyntaxError) as e:
    print(f"Error loading maze state: {e}")
    MaxActions = 50
# Try to load TILE from the file, or use a default value
try:
    with open("lastmaze.txt", "r") as file:
        file_contents = file.readlines()
        TILE = int(file_contents[0].strip())

        
        if len(file_contents) > 1:
            # Process the remaining lines
            walls_data = [ast.literal_eval(line.strip()) for line in file_contents[1:]]
except (FileNotFoundError, ValueError, SyntaxError) as e:
    print(f"Error loading maze state: {e}")
    TILE = 100
    seedvalue = None
    walls_data = []
print(TILE)
if seedvalue == None:
    setseed = False
else:
    setseed = True

# Setup display parameters
RES = WIDTH, HEIGHT = 1202, 902
cols, rows = WIDTH // TILE, HEIGHT // TILE
FONT_SIZE = 36

# Initialize Pygame
pygame.init()
sc = pygame.display.set_mode(RES)
font = pygame.font.Font(None, FONT_SIZE)
clock = pygame.time.Clock()

# Initialize grid cells
grid_cells = [Cell(col, row, TILE, cols, rows) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []


# Load saved walls if available
if walls_data:
    for cell, walls in zip(grid_cells, walls_data):
        cell.savegen(walls)

movesleft = 0
gen_number = 0
Actors = [PredActor(grid_cells, 2), PreyActor(grid_cells, 4)]

# Game loop
while True:
    sc.fill((50, 50, 50))

    if movesleft == MaxActions:
        movesleft = 0
        for a in Actors:
            a.spawn()
        gen_number += 1
        print(f"Generation {gen_number}")
    elif movesleft < MaxActions:
        for a in Actors:
            a.step(movesleft, )
        movesleft += 1

    # Draw all cells
    for cell in grid_cells:
        if cell != nextpred and cell != nextprey:
            cell.draw(sc)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()
    clock.tick(5)