import pygame
from random import seed, choice
import random
import ast

try:
    with open("pred.txt", "r") as file:
        predactionsstring = file.readlines()
except FileNotFoundError:
    predactionsstring = ["up\n","down\n"]
print(f"Starting Maze Generator with seed value: {predactionsstring}")
predactions = [ast.literal_eval(predactionsstring.strip()) for line in predactionsstring[1:]]
try:
    with open("prey.txt", "r") as file:
        preyactionsstring = file.readlines()
except FileNotFoundError:
    preyactionsstring = ["up\n","down\n"]
print(f"Starting Maze Generator with seed value: {preyactionsstring}")
preyactions = [ast.literal_eval(preyactionsstring.strip()) for line in preyactionsstring[1:]]

try:
    with open("config.txt", "r") as file:
        file_contents = file.readlines()
        MaxActions = int(file_contents[2].strip())
except (FileNotFoundError, ValueError, SyntaxError) as e:
    print(f"Error loading maze state: {e}")
    MaxActions = 50
try:
    with open("config.txt", "r") as file:
        lines = file.readlines()
        seedvalue = int(lines[1].strip())
except FileNotFoundError:
    seedvalue = 50
print(f"Starting Maze Generator with seed value: {seedvalue}")

seed(seedvalue)




class Cell:
    def __init__(self, x, y, tile_size, cols, rows):
        self.x, self.y = x, y
        self.tile_size = tile_size
        self.cols = cols
        self.rows = rows
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    def draw_current_cell(self, screen):
        x, y = self.x * self.tile_size, self.y * self.tile_size
        pygame.draw.rect(screen, pygame.Color(0, 0, 0), (x + 2, y + 2, self.tile_size - 2, self.tile_size - 2))

    def draw(self, screen):
        x, y = self.x * self.tile_size, self.y * self.tile_size
        if self.visited:
            pygame.draw.rect(screen, pygame.Color(0, 0, 0), (x, y, self.tile_size, self.tile_size))

        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color(150, 100, 0), (x, y), (x + self.tile_size, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color(150, 100, 0), (x + self.tile_size, y), (x + self.tile_size, y + self.tile_size), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color(150, 100, 0), (x + self.tile_size, y + self.tile_size), (x, y + self.tile_size), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color(150, 100, 0), (x, y + self.tile_size), (x, y), 2)

    def check_cell(self, x, y, grid_cells):
        find_index = lambda x, y: x + y * self.cols
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return None
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, grid_cells)
        right = self.check_cell(self.x + 1, self.y, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        left = self.check_cell(self.x - 1, self.y, grid_cells)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else None

    @staticmethod
    def remove_walls(current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False

    def savegen(self, walls):
        for wall_name, wall_value in walls.items():
            self.walls[wall_name] = wall_value

    def predstep(self, next, screen, moves):
        predactions[moves] 
        x, y = self.x * self.tile_size, self.y * self.tile_size
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), (x + 2, y + 2, self.tile_size - 2, self.tile_size - 2))        
        
        return next
    def preystep(self, next, screen, moves):
        preyactions[moves]        
        x, y = self.x * self.tile_size, self.y * self.tile_size
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), (x + 2, y + 2, self.tile_size - 2, self.tile_size - 2))        

        return next
