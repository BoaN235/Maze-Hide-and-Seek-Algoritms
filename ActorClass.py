import pygame
import random

class Actor:
    def __init__(self, grid_cells, spawn_index, MaxActions):
        self.color = (255, 255, 255)
        self.current_cell = None
        self.grid_cells = grid_cells
        self.spawn = grid_cells[spawn_index]
        self.spawn()
        self.actions = []
        for i in range(1, MaxActions):
            random_actions = random.randint(0, 3)        
            if random_actions == 0:
                self.actions.append("left")
            if random_actions == 1:
                self.actions.append("right")
            if random_actions == 2:
                self.actions.append("top")
            if random_actions == 3:
                self.actions.append("down")
    
    def step(self):
        self.current_cell = self.current_cell.check_neighbors(self.grid_cells)
    def step(self, moves, actions):
        action = actions[moves % len(actions)]
        if action == 'top' and self.y > 0:
            self.y -= 1
        elif action == 'down' and self.y < self.rows - 1:
            self.y += 1
        elif action == 'left' and self.x > 0:
            self.x -= 1
        elif action == 'right' and self.x < self.cols - 1:
            self.x += 1
        return self

    def spawn(self):
        self.current_cell = self.spawn

class PreyActor(Actor):
    def __init__(self, grid_cells, spawn_index, MaxActions):
        super().__init__(grid_cells, spawn_index, MaxActions)
        self.color = (0, 255, 0)


class PredActor(Actor):
    def __init__(self, grid_cells, spawn_index, MaxActions):
        super().__init__(grid_cells, spawn_index, MaxActions)
        self.color = (255, 0, 0)