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
        self.start_hunger = 0
        self.start_food = 10
        self.min_hunger = self.start_hunger
        self.food = self.start_food
        self.turns_without_food = 0
        self.MaxTurnsWithoutFood = 10







    def step(self):
        self.last_food = self.food
        for actor in self.sim_state.Actors:
            if actor.current_cell == self.current_cell and actor != self and isinstance(actor, PreyActor):
                self.food += actor.food 
                self.killed = True
                actor.kill(CauseOfDeath.KILLED)

        Actor.step(self)
        self.food_difference = self.last_food - self.food


    
    def generate_actions(self):
        for i in range(0, self.sim_state.MaxActions + 1):
            random_actions = random.randint(0, 3)        
            if random_actions == 0:
                self.actions.append("left")
            if random_actions == 1:
                self.actions.append("right")
            if random_actions == 2:
                self.actions.append("top")
            if random_actions == 3:
                self.actions.append("bottom")

