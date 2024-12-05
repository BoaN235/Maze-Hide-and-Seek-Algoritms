import pygame
import random
from random import seed

class Actor:
    def __init__(self, sim_state, spawn_index, ide):
        self.sim_state = sim_state  # Ensure sim_state is initialized first
        self.color = (255, 255, 255)
        self.current_cell = None
        self.spawn_index = spawn_index
        self.dead = False
        self.move_stack = []
        self.last_cell = None


        self.spawn()
        self.moves = 0
        self.actions = []
        self.ide = ide
        seed()
        self.generate_actions()



        #print(self.actions)
    def generate_actions(self):
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

        
        for actor in self.sim_state.Actors:
            if actor.current_cell == self.current_cell and actor != self and isinstance(actor, PredActor) and isinstance(self, PreyActor):
                actor.hunger += 0.1
                self.kill()


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
            if isinstance(self, PredActor):
                if self.last_cell == self.current_cell:
                    self.min_hunger += 0.1
            self.move_stack.append(self.current_cell)

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

class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)
        self.id = ide
  
    def genetic_mutations(self):
        pass
     
    # def reset(self):
    #     Actor.reset(self)



class PredActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (255, 0, 0)
        self.spawn_color = (155, 0, 0)
        self.id = ide
        self.sim_state = sim_state
        self.hunger = 0
        self.min_hunger = 0

    def check_if_hunger(self):
        if self.hunger <= self.min_hunger:
            self.kill()
        self.hunger = 0

    def genetic_mutations(self):
        pass

    def reset(self):
        Actor.reset(self)
        self.hunger = 0
        self.min_hunger = 0
