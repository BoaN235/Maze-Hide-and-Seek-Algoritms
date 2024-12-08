from ActorClass import Actor, CauseOfDeath
import random


class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)
        self.id = ide
        self.dead = self.dead
        self.min_hunger = 30
        
    def kill(self, cause_of_death:CauseOfDeath=None):
        Actor.kill(self, cause_of_death)

    def score_move(self, move):
        self.move_stack

        current_move_stats = self.move_stack[move]
        if current_move_stats['move_success']:
            self.current_move_score += 1

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


    # def reset(self):
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