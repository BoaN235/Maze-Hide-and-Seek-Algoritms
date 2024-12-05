from ActorClass import Actor
from PreyActor import PreyActor

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

    def step(self):
        for actor in self.sim_state.Actors:
            if actor.current_cell == self.current_cell and actor != self and isinstance(actor, PreyActor):
                self.hunger += 0.1
                actor.kill()
        Actor.step(self)
        if self.last_cell == self.current_cell:
            self.min_hunger += 0.1