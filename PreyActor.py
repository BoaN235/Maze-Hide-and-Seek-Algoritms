from ActorClass import Actor
import random

class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index, ide, is_child, parent):
        super().__init__(sim_state, spawn_index, ide, is_child, parent)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)
        self.id = ide
        self.dead = self.dead
        self.is_child = is_child
        self.parent = parent
        self.Reproducing = True

    def score_move(self, move):
        current_move_stats = self.move_stack[move]
        if current_move_stats['move_success']:
            self.current_move_score += 1

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

    def kill(self):
        self.sim_state.preys -= 1
        Actor.kill(self)

    def generate_actions(self):
        for i in range(1, self.sim_state.MaxActions):
            random_actions = random.randint(0, 3)
            if random_actions == 0:
                self.actions.append("left")
            elif random_actions == 1:
                self.actions.append("right")
            elif random_actions == 2:
                self.actions.append("top")
            elif random_actions == 3:
                self.actions.append("bottom")

    def reproducing_actor(self):
        new_actor_location = Actor.reproducing_actor(self)
        if new_actor_location:
            self.sim_state.preys += 1
            for i, cell in enumerate(self.sim_state.grid_cells):
                if cell == new_actor_location:
                    new_spawn_index = i
                    break
            self.sim_state.Actors.append(PreyActor(self.sim_state, new_spawn_index, len(self.sim_state.Actors), True, self))