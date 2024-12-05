import pygame
from random import seed, choice
import random
import ast


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
    def __init__(self, x, y, SimState):
        self.sim_state = SimState
        self.x, self.y = x, y
        self.tile_size = SimState.TILE
        self.cols = SimState.cols
        self.rows = SimState.rows
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.top = None
        self.right = None
        self.bottom = None
        self.left = None
    def draw_current_cell(self, screen):
        x, y = self.x * self.tile_size, self.y * self.tile_size
        pygame.draw.rect(screen, pygame.Color(0, 0, 0), (x + 2, y + 2, self.tile_size - 2, self.tile_size - 2))

    def draw(self, screen):
        x, y = self.x * self.tile_size, self.y * self.tile_size
        if self.visited:
            pygame.draw.rect(screen, pygame.Color(0, 0, 0), (x, y, self.tile_size, self.tile_size))
        if (hasattr(self.sim_state, 'Actors') and  self.sim_state.Actors != None):
            for a in self.sim_state.Actors:
                if a.dead == False:
                    if a.spawn_cell == self:
                        pygame.draw.circle(screen, a.spawn_color, (x + self.tile_size // 2 , y + self.tile_size // 2), self.tile_size // 4)
                    if a.current_cell == self:
                        pygame.draw.rect(screen, a.color, (x + self.tile_size / 4, y + self.tile_size / 4, self.tile_size/2, self.tile_size/2))


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
        self.top = self.check_cell(self.x, self.y - 1, grid_cells)
        self.right = self.check_cell(self.x + 1, self.y, grid_cells)
        self.bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        self.left = self.check_cell(self.x - 1, self.y, grid_cells)

        if self.top and not self.top.visited:
            neighbors.append(self.top)
        if self.right and not self.right.visited:
            neighbors.append(self.right)
        if self.bottom and not self.bottom.visited:
            neighbors.append(self.bottom)
        if self.left and not self.left.visited:
            neighbors.append(self.left)

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

    def save_gen(self, walls):
        for wall_name, wall_value in walls.items():
            self.walls[wall_name] = wall_value

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'walls': self.walls,
            'visited': self.visited
        }

    def from_dict(data, sim_state):
        cell = Cell(data['x'], data['y'], sim_state)
        cell.walls = data['walls']
        cell.visited = data['visited']
        return cell    
    
    def check_neighboring_options(self, grid_cells):
        movable_cells = []

        self.top = self.check_cell(self.x, self.y - 1, grid_cells)
        self.right = self.check_cell(self.x + 1, self.y, grid_cells)
        self.bottom = self.check_cell(self.x, self.y + 1, grid_cells)
        self.left = self.check_cell(self.x - 1, self.y, grid_cells)

        if self.top and not self.walls['top'] and not self.top.walls['bottom']:
            movable_cells.append(self.top)
        if self.right and not self.walls['right'] and not self.right.walls['left']:
            movable_cells.append(self.right)
        if self.bottom and not self.walls['bottom'] and not self.bottom.walls['top']:
            movable_cells.append(self.bottom)
        if self.left and not self.walls['left'] and not self.left.walls['right']:
            movable_cells.append(self.left)
        return movable_cells