import pygame
from random import seed, choice
import random
import ast

try:
    with open("data/pred.txt", "r") as file:
        file_contents = file.readlines()
except FileNotFoundError:
    file_contents = ["up\n", "down\n"]
print(f"Starting Maze Generator with seed value: {file_contents}")
predactions = [line.strip() for line in file_contents[1:]]

# Read prey.txt
try:
    with open("data/prey.txt", "r") as file:
        file_contents = file.readlines()
except FileNotFoundError:
    file_contents = ["up\n", "down\n"]
print(f"Starting Maze Generator with seed value: {file_contents}")
preyactions = [line.strip() for line in file_contents[1:]]

try:
    with open("data/config.txt", "r") as file:
        file_contents = file.readlines()
        MaxActions = int(file_contents[2].strip())
except (FileNotFoundError, ValueError, SyntaxError) as e:
    print(f"Error loading maze state: {e}")
    MaxActions = 50
try:
    with open("data/config.txt", "r") as file:
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
        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color(255, 255, 255), (x, y), (x + self.tile_size, y))
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color(255, 255, 255), (x + self.tile_size, y), (x + self.tile_size, y + self.tile_size))
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color(255, 255, 255), (x, y + self.tile_size), (x + self.tile_size, y + self.tile_size))
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color(255, 255, 255), (x, y), (x, y + self.tile_size))

    def check_cell(self, x, y, grid_cells):
        find_index = lambda x, y: x + y * self.cols
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return None
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, grid_cells, gen):
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

        if gen == True:
            return choice(neighbors) if neighbors else None
        else:
            return neighbors if neighbors else None

    def check_neighbors2(self, grid_cells):
        neighbors = []
        if self.x > 0:
            left = grid_cells[self.y * self.cols + (self.x - 1)]
            if not self.walls['left']:
                neighbors.append(left)
        if self.x < self.cols - 1:
            right = grid_cells[self.y * self.cols + (self.x + 1)]
            if not self.walls['right']:
                neighbors.append(right)
        if self.y > 0:
            top = grid_cells[(self.y - 1) * self.cols + self.x]
            if not self.walls['top']:
                neighbors.append(top)
        if self.y < self.rows - 1:
            bottom = grid_cells[(self.y + 1) * self.cols + self.x]
            if not self.walls['bottom']:
                neighbors.append(bottom)
        return neighbors


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

    def remove_walls2(self, next_cell):
        dx = self.x - next_cell.x
        dy = self.y - next_cell.y
        if dx == 1:  # next_cell is to the left
            self.walls['left'] = False
            next_cell.walls['right'] = False
        elif dx == -1:  # next_cell is to the right
            self.walls['right'] = False
            next_cell.walls['left'] = False
        if dy == 1:  # next_cell is above
            self.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif dy == -1:  # next_cell is below
            self.walls['bottom'] = False
            next_cell.walls['top'] = False


    def savegen(self, walls):
        for wall_name, wall_value in walls.items():
            self.walls[wall_name] = wall_value

    def preystep(self, screen, neighbors):
        """Moves the prey to a random valid neighboring cell."""
        if neighbors:
            next_cell = choice(neighbors)
            # Remove the wall between the current cell and the next cell
            self.remove_walls2(next_cell)
            # Update position
            self.x, self.y = next_cell.x, next_cell.y
        x, y = self.x * self.tile_size, self.y * self.tile_size
        pygame.draw.rect(screen, pygame.Color(0, 255, 0), (x + 2, y + 2, self.tile_size - 4, self.tile_size - 4))
        return self

    def predstep(self, screen, neighbors):
        """Moves the predator to a random valid neighboring cell."""
        if neighbors:
            next_cell = choice(neighbors)
            # Remove the wall between the current cell and the next cell
            self.remove_walls2(next_cell)
            # Update position
            self.x, self.y = next_cell.x, next_cell.y
        x, y = self.x * self.tile_size, self.y * self.tile_size
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), (x + 2, y + 2, self.tile_size - 4, self.tile_size - 4))
        return self
