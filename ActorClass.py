import pygame
import random
from random import seed
import math
# from PredActor import PredActor
# from PreyActor import PreyActor


class Actor:
    def __init__(self, sim_state, spawn_index, ide):
        self.sim_state = sim_state  # Ensure sim_state is initialized first
        self.color = (255, 255, 255)
        self.current_cell = None
        self.spawn_index = spawn_index
        self.dead = False
        self.move_stack = []
        self.last_cell = None
        self.scored_list = []
        self.current_move_score = 0


        self.spawn()
        self.moves = 0
        self.actions = []
        self.ide = ide
        seed()
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
        self.dead = False
        self.current_cell = None
        self.move_stack = []
        self.last_cell = None
        self.spawn()
        self.moves = 0
        # self.generate_actions()

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
            move_reward = self.move_reward()

            self.move_stack.append({
                'action': self.actions[self.moves-1],
                'current_cell': self.current_cell,
                'last_cell': self.last_cell,
                'move_success': self.current_cell != self.last_cell,
                'neighboring_options': movable_cells,
                'move_reward': move_reward
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
        chosen_mutation_rate = random.randint(1, 5)  # Randomly choose a mutation rate between 1 and 5

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
        print(f"Actor {self.ide} has mutated")
    
    
