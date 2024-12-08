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
        self.min_hunger = 20



    def kill(self, cause_of_death:CauseOfDeath=None):

        Actor.kill(self, cause_of_death)


    def reset(self):
        self.food = 1
        self.min_hunger = 0
        
        Actor.reset(self)

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
    
    def move_reward(self):
        return 0

    def score_move(self, move):
  
        Actor.score_move(self, move)

    def score_move(self, move):
        self.move_stack

        current_move_stats = self.move_stack[move]
        if self.killed:
            self.current_move_score += 1
            self.killed = False   

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