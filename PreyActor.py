from ActorClass import Actor, CauseOfDeath
import random


class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)
        self.id = ide
        self.dead = self.dead
        self.start_hunger = 0
        self.start_food = 5
        self.min_hunger = self.start_hunger
        self.food = self.start_food
        self.turns_without_food = 0
        self.MaxTurnsWithoutFood = 6




    #     Actor.reset(self)

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
    
    def step(self):
        self.last_food = self.food
        Actor.step(self)
        if self.current_cell.food > 0:
            self.current_cell.food -= 1
            self.food += 1
        self.food_difference = self.last_food - self.food
