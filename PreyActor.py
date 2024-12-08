from ActorClass import Actor, CauseOfDeath
import random


class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)
        self.id = ide
        self.dead = self.dead
        self.start_hunger = 30
        self.start_food = 40
        self.min_hunger = self.start_hunger
        self.food = self.start_food
        self.turns_without_food = 0
        self.sim_state.MaxTurnsWithoutFood = 6

    def kill(self, cause_of_death:CauseOfDeath=None):
        Actor.kill(self, cause_of_death)


    #     Actor.reset(self)

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
    
    def step(self):
        if self.current_cell.food > 0:

            self.current_cell.food -= 1
            self.food += 1

        Actor.step(self)
    

    def score_move(self, move, extra_score=0):
        current_move_stats = self.move_stack[move]
        extra_score = current_move_stats['food']/2 

        Actor.score_move(self, move, extra_score)