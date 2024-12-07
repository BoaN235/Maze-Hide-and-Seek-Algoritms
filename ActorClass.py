import pygame
import random
from random import seed
from numba import cuda
import numpy as np
import math
# from PredActor import PredActor
# from PreyActor import PreyActor


class Actor:
    def __init__(self, sim_state, spawn_index, ide, is_child, parent):
        self.sim_state = sim_state  # Ensure sim_state is initialized first
        self.color = (255, 255, 255)
        self.current_cell = None
        self.spawn_index = spawn_index
        self.dead = False
        self.move_stack = []
        self.last_cell = None
        self.scored_list = []
        self.current_move_score = 0
        self.reproducing = False
        self.is_child = is_child
        self.parent = parent


        self.spawn()
        self.moves = 0
        self.ide = ide
        seed()

        self.actions = []
        if self.is_child:
            self.actions = self.parent.actions
        else:
            self.generate_actions()
    
    def preform_action(self):
        if not self.dead:
            if self.moves < self.sim_state.MaxActions:
                self.step()
                self.moves += 1
            elif self.moves == self.sim_state.MaxActions:
                self.spawn()

    def reset(self):
        if self.dead:
            self.genetic_mutations()
        if self.reproducing == True:
            self.reproducing_actor()
        self.dead = False
        self.current_cell = None
        self.move_stack = []
        self.last_cell = None
        self.spawn()
        self.moves = 0
        # self.generate_actions()
    
    def reproducing_actor(self):
        if not self.current_cell:
            return None

        parent_cell = self.current_cell
        grid_cells = self.sim_state.grid_cells

        distances = np.zeros(len(grid_cells), dtype=np.float32)
        parent_cell_coords = np.array([parent_cell.x, parent_cell.y], dtype=np.float32)
        grid_cells_coords = np.array([[cell.x, cell.y] for cell in grid_cells], dtype=np.float32)

        threadsperblock = 32
        blockspergrid = (len(grid_cells) + (threadsperblock - 1)) // threadsperblock

        self.calculate_distances[blockspergrid, threadsperblock](parent_cell_coords, grid_cells_coords, distances)

        distances = distances.copy_to_host()
        total_distance = np.sum(distances)
        if total_distance > 0:
            weights = [1 / distance if distance > 0 else 1 for distance in distances]
        else:
            weights = [1] * len(grid_cells)  # Equal weights if total_distance is 0

        new_actor_location = random.choices(grid_cells, weights)[0]
        return new_actor_location

    @staticmethod
    @cuda.jit
    def calculate_distances(parent_cell_coords, grid_cells_coords, distances):
        idx = cuda.grid(1)
        if idx < len(grid_cells_coords):
            cell_coords = grid_cells_coords[idx]
            distances[idx] = math.sqrt((parent_cell_coords[0] - cell_coords[0]) ** 2 + (parent_cell_coords[1] - cell_coords[1]) ** 2)

    
    def step(self):
        if self.dead:
            return
        
        if self.current_cell:
            self.last_cell = self.current_cell      
            self.current_cell.check_neighbors(self.sim_state.grid_cells)
            movable_cells = self.current_cell.check_neighboring_options(self.sim_state.grid_cells)
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

            self.move_stack.append({
                'action': self.actions[self.moves-1],
                'current_cell': self.current_cell,
                'last_cell': self.last_cell,
                'move_success': self.current_cell != self.last_cell,
                'neighboring_options': movable_cells,
            })
            self.scored_list.append(self.score_move(self.moves-1))

        else:
            self.spawn()
        
    def kill(self):
        self.dead = True  # Set dead attribute to True

        

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

    def genetic_mutations(self):
        chosen_mutation_rate = random.randint(0, 2)  # Randomly choose a mutation rate between 1 and 2

        if self.scored_list and len(self.scored_list) == len(self.actions):
            scores = [move['score'] for move in self.scored_list]
            total_score = sum(scores)
            if total_score > 0:
                weights = [score / total_score for score in scores]
            else:
                weights = [1 / len(self.actions)] * len(self.actions)  # Equal weights if total_score is 0
        else:
            weights = [1 / len(self.actions)] * len(self.actions)  # Equal weights if no scores or mismatch

        # Select specific moves to change using weights
        for i in range(chosen_mutation_rate):
            chosen_action_index = random.choices(range(len(self.actions)), weights)[0]
            new_action = random.choice(["left", "right", "top", "bottom"])  # Randomly choose new action
            self.actions[chosen_action_index] = new_action

        # Regenerate the actions list randomly
        new_actions = []
        for i in range(self.sim_state.MaxActions):
            chosen_action = random.choice(self.actions)  # Randomly choose from the updated actions
            new_actions.append(chosen_action)

        self.actions = new_actions
        #print(f"Actor {self.ide} has mutated")
    
    
