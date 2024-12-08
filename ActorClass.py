import pygame
import random
from random import seed
import math
from enum import Enum
# from PredActor import PredActor
# from PreyActor import PreyActor

class CauseOfDeath(Enum):
    STARVATION = "starvation"
    KILLED = "killed"

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


        self.cause_of_death = None



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
        self.food = self.start_food
        self.min_hunger = self.start_hunger

        self.current_cell = None
        self.move_stack = []
        self.last_cell = None
        self.spawn()
        self.moves = 0
        # self.generate_actions()

    def step(self):
        if self.dead:
            return
        last_food = self.food
        if self.food <= self.min_hunger:
            if self.turns_without_food >= self.sim_state.MaxTurnsWithoutFood:
                self.kill(CauseOfDeath.STARVATION)
                self.turns_without_food = 0
            else:
                self.turns_without_food += 1

        
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
            if not self.last_cell == self.current_cell:
                self.food -= 0.1
                self.min_hunger += 1
            
            food_difference = last_food - self.food

            self.move_stack.append({
                'action': self.actions[self.moves-1],
                'current_cell': self.current_cell,
                'last_cell': self.last_cell,
                'move_success': self.current_cell != self.last_cell,
                'neighboring_options': movable_cells,
                'food': food_difference,
            })
            self.scored_list.append(self.score_move(self.moves-1))

        else:
            self.spawn()
        
    def kill(self, cause_of_death:CauseOfDeath=None):
        self.dead = True  # Set dead attribute to True
        self.cause_of_death = cause_of_death




        

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
            scores = [move['score'] for move in self.scored_list if move is not None]
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
    
    

    def score_move(self, move, extra_score=0):
        self.move_stack

        current_move_stats = self.move_stack[move] 

        current_move_stats = self.move_stack[move]
        if current_move_stats['move_success']:
            self.current_move_score += 1
        if self.dead:
            self.current_move_score = 0
            scored_move = { 
                'move_num': move,
                'score': self.current_move_score
            }   
            return scored_move  
        
        scored_move = { 
            'move_num': move,
            'score': self.current_move_score + int(extra_score)
          }   
        return scored_move
    