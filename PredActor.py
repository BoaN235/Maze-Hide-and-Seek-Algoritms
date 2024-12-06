from ActorClass import Actor
from PreyActor import PreyActor
import random

class PredActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (255, 0, 0)
        self.spawn_color = (155, 0, 0)
        self.id = ide
        self.sim_state = sim_state
        self.hunger = 0
        self.min_hunger = 0
        self.killed = False

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

    def step(self):
        for actor in self.sim_state.Actors:
            if actor.current_cell == self.current_cell and actor != self and isinstance(actor, PreyActor):
                self.hunger += 1
                self.killed = True
                actor.kill()
        
        Actor.step(self)
        if self.last_cell == self.current_cell:
            self.min_hunger += 0.1
    
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
    
    def move_reward(self):
        return 0

    def score_move(self, move):
        if self.killed:
            self.current_move_score += 1     
        Actor.score_move(self, move)