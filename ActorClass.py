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
        self.genetic_mutations()
        self.dead = False
        self.current_cell = None
        self.move_stack = []
        self.last_cell = None
        self.spawn()
        self.moves = 0
        self.generate_actions()
        self.hunger = 0
        self.min_hunger = 0

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
        print("killing:", self.ide)
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
        pass
    
    
    def score_move(self, move):
        self.move_stack

        current_move_stats = self.move_stack[move]
        if current_move_stats['move_success']:
            self.current_move_score += 1

        self.current_move_score += current_move_stats['move_reward'] / 10
        
        if self.dead:
            self.current_move_score = 0
            scored_move = { 
                'move_num': move,
                'score': self.current_move_score
            }   
            return scored_move  
        
        scored_move = { 
            'move_num': move,
            'score': self.current_move_score
          }   
        return scored_move