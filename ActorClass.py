import pygame
import random

class Actor:
    def __init__(self, sim_state, spawn_index):
        self.sim_state = sim_state  # Ensure sim_state is initialized first
        self.color = (255, 255, 255)
        self.current_cell = None
        self.spawn_cell = self.sim_state.grid_cells[spawn_index]
        self.spawn()
        self.moves = 0
        self.actions = []
        for i in range(1, self.sim_state.MaxActions):
            random_actions = random.randint(0, 3)        
            if random_actions == 0:
                self.actions.append("left")
            if random_actions == 1:
                self.actions.append("right")
            if random_actions == 2:
                self.actions.append("top")
            if random_actions == 3:
                self.actions.append("down")
    def preform_action(self):
        if self.moves < self.sim_state.MaxActions:
            self.step()
            self.moves += 1
        elif self.moves == self.sim_state.MaxActions:
            self.spawn()

    def step(self):

        if self.current_cell:
            self.current_cell = self.current_cell.check_neighbors(self.sim_state.grid_cells)
        else:
            self.spawn()
    # def step(self, moves):
    #     action = self.actions[moves % len(self.actions)]
    #     if action == 'top' and self.y > 0:
    #         self.y -= 1
    #     elif action == 'down' and self.y < self.rows - 1:
    #         self.y += 1
    #     elif action == 'left' and self.x > 0:
    #         self.x -= 1
    #     elif action == 'right' and self.x < self.cols - 1:
    #         self.x += 1
    #     return self

    def spawn(self):
        self.current_cell = self.spawn_cell
        self.moves = 0
    

class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index):
        super().__init__(sim_state, spawn_index)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)


class PredActor(Actor):
    def __init__(self, sim_state, spawn_index):
        super().__init__(sim_state, spawn_index)
        self.color = (255, 0, 0)
        self.spawn_color = (155, 0, 0)