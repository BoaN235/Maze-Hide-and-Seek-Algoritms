import pygame
import random
from random import seed

class Actor:
    def __init__(self, sim_state, spawn_index, ide):
        self.sim_state = sim_state  # Ensure sim_state is initialized first
        self.color = (255, 255, 255)
        self.current_cell = None
        self.spawn_index = spawn_index

        self.spawn()
        self.moves = 0
        self.actions = []
        self.ide = ide
        seed()
        for i in range(1, self.sim_state.MaxActions):
            random_actions = random.randint(0, 3)        
            if random_actions == 0:
                self.actions.append("left")
            if random_actions == 1:
                self.actions.append("right")
            if random_actions == 2:
                self.actions.append("top")
            if random_actions == 3:
                self.actions.append("bottom")
        print(self.actions)
    def preform_action(self):
        if self.moves < self.sim_state.MaxActions:
            self.step()
            self.moves += 1
        elif self.moves == self.sim_state.MaxActions:
            self.spawn()

    def step(self):

        if self.current_cell:
            self.current_cell.check_neighbors(self.sim_state.grid_cells)
            movable_cells = self.current_cell.check_neighboring_options(self.sim_state.grid_cells)
            print(str(movable_cells) + str(self.ide))
            if self.actions[self.moves-1] == 'top':
                for x in movable_cells:
                    if x == self.current_cell.top:
                        self.current_cell = self.current_cell.top
                        break
            if self.actions[self.moves-1] == 'left':
                for x in movable_cells:
                    if x == self.current_cell.left:
                        self.current_cell = self.current_cell.left
                        break
            if self.actions[self.moves-1] == 'right':
                for x in movable_cells:
                    if x == self.current_cell.right:
                        self.current_cell = self.current_cell.right
                        break
            if self.actions[self.moves-1] == 'bottom':
                for x in movable_cells:
                    if x == self.current_cell.bottom:
                        self.current_cell = self.current_cell.bottom
                        break
        else:
            self.spawn()

    def spawn(self):
        self.current_cell = self.spawn_cell = self.sim_state.grid_cells[self.spawn_index]
        self.moves = 0
    
    def to_dict(self):
        return {
            'color': self.color,
            'spawn_index': self.sim_state.grid_cells.index(self.spawn_cell),
            'moves': self.moves
        }
    
    def from_dict(data):
        actor = Actor(None, 0)
        actor.color = data['color']
        actor.spawn_index = data['spawn_index']
        actor.moves = data['moves']
        return actor

class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)
        self.id = ide
class PredActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (255, 0, 0)
        self.spawn_color = (155, 0, 0)
        self.id = ide