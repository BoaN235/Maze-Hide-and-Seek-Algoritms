from ActorClass import Actor, CauseOfDeath, ActorType, Moves
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


    def ActorType(self):
        return ActorType.PREDATOR

    def search_for_food(self):
        closest_actor = None
        self.current_cell.check_neighbors(self.sim_state.grid_cells)
        for actor in self.sim_state.Actors:
            if actor.ActorType() == ActorType.PREDATOR:
                if closest_actor is None:
                    closest_actor = actor
                elif self.current_cell.distance(actor.current_cell) < self.current_cell.distance(closest_actor.current_cell):
                    closest_actor = actor
        self.find_best_move_to_target(closest_actor)



    def step(self):
        self.last_food = self.food
        for actor in self.sim_state.Actors:
            if actor.current_cell == self.current_cell and actor != self and actor.ActorType() == ActorType.PREY:
                self.food += actor.food 
                self.killed = True
                actor.kill(CauseOfDeath.KILLED)

        Actor.step(self)
        self.food_difference = self.last_food - self.food


    
    def generate_actions(self):
        for i in range(0, self.sim_state.MaxActions + 1):
            random_actions = random.randint(0, 3)        
            if random_actions == 0:
                self.actions.append(Moves.LEFT)
            if random_actions == 1:
                self.actions.append(Moves.RIGHT)
            if random_actions == 2:
                self.actions.append(Moves.TOP)
            if random_actions == 3:
                self.actions.append(Moves.BOTTOM)
            if random_actions == 5:
                self.actions.append(Moves.SENSE_F)

    def actor_type(self):
        return None