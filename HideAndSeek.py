import pygame
from CellClass import Cell
import ast
import random
from random import seed
import numpy as np

try:
    with open("data/config.txt", "r") as file:
        file_contents = file.readlines()
        MaxActions = int(file_contents[2].strip())
        seedvalue = int(file_contents[3].strip())
except (FileNotFoundError, ValueError, SyntaxError) as e:
    print(f"Error loading maze state: {e}")
    MaxActions = 50
# Try to load TILE from the file, or use a default value
try:
    with open("data/lastmaze.txt", "r") as file:
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

# Initialize the actions
seed()
if setseed == True:
    seed(seedvalue)
preylist = []
for i in range(1, MaxActions + 1):
    random_actions = random.randint(0, 3)
    if random_actions == 0:
        preylist.append("left")
    if random_actions == 1:
        preylist.append("right")
    if random_actions == 2:
        preylist.append("top")
    if random_actions == 3:
        preylist.append("down")
with open("data/prey.txt", "w") as file:
    for x in preylist:
        file.write(str(x) + '\n')


predlist = []    
seed()
if setseed == True:
    seed(seedvalue)
for i in range(1, MaxActions):
    random_actions = random.randint(0, 3)        
    if random_actions == 0:
        predlist.append("left")
    if random_actions == 1:
        predlist.append("right")
    if random_actions == 2:
        predlist.append("top")
    if random_actions == 3:
        predlist.append("down")

with open("data/pred.txt", "w") as file:
    for x in predlist:
        file.write(str(x) + '\n')

# Load saved walls if available
if walls_data:
    for cell, walls in zip(grid_cells, walls_data):
        cell.savegen(walls)

movesleft = 0
initial_prey_pos = grid_cells[1]  # initial prey spawn
initial_pred_pos = grid_cells[5]  # initial pred spawn
nextprey = initial_prey_pos
nextpred = initial_pred_pos
gen_number = 0
gen = False

# Game loop
while True:
    sc.fill((50, 50, 50))

    if movesleft == 0:
        movesleft = MaxActions
        nextprey = initial_prey_pos
        nextpred = initial_pred_pos
        gen_number += 1
        print(f"Generation {gen_number}")
    else:
        prey_neighbors = nextprey.check_neighbors2(grid_cells)
        pred_neighbors = nextpred.check_neighbors2(grid_cells)

        # Move prey
        if prey_neighbors:
            nextprey = nextprey.preystep(sc, prey_neighbors)
        
        # Move predator
        if pred_neighbors:
            nextpred = nextpred.predstep(sc, pred_neighbors)
        
        movesleft -= 1

    # Draw all cells
    [cell.draw(sc) for cell in grid_cells]

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.flip()
    clock.tick(5)