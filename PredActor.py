from ActorClass import Actor, CauseOfDeath
from PreyActor import PreyActor
import random
from enum import Enum



class PredActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (255, 0, 0)
        self.spawn_color = (155, 0, 0)
        self.id = ide
        self.sim_state = sim_state
        self.killed = False
        self.dead = self.dead
        self.start_hunger = 20
        self.start_food = 35
        self.min_hunger = self.start_hunger
        self.food = 35
        self.turns_without_food = 0
        self.sim_state.MaxTurnsWithoutFood = 10


    def kill(self, cause_of_death:CauseOfDeath=None):

        Actor.kill(self, cause_of_death)




    def step(self):
        for actor in self.sim_state.Actors:
            if actor.current_cell == self.current_cell and actor != self and isinstance(actor, PreyActor):
                self.food += actor.food 
                self.killed = True
                actor.kill(CauseOfDeath.KILLED)
        
        Actor.step(self)

    
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

    def score_move(self, move):
  
        Actor.score_move(self, move)
