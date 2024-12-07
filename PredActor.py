from ActorClass import Actor
from PreyActor import PreyActor
import random

class PredActor(Actor):
    def __init__(self, sim_state, spawn_index, ide, is_child, parent):
        super().__init__(sim_state, spawn_index, ide, is_child, parent)
        self.color = (255, 0, 0)
        self.spawn_color = (155, 0, 0)
        self.id = ide
        self.sim_state = sim_state
        self.food = 1
        self.min_hunger = 0
        self.killed = False
        self.dead = self.dead
        self.is_child = is_child
        self.parent = parent

    def reset(self):
        Actor.reset(self)
        self.food = 1
        self.min_hunger = 0

    def kill(self):
        self.sim_state.preds -= 1
        Actor.kill(self)

    def step(self):
        if self.food <= self.min_hunger:
            self.kill()
            print("Predator died of hunger:" + str(self.ide))
        
        for actor in self.sim_state.Actors:
            if actor.current_cell == self.current_cell and actor != self and isinstance(actor, PreyActor):
                self.food += 2
                self.killed = True
                actor.kill()

        Actor.step(self)
        if self.last_cell == self.current_cell:
            self.food -= 0.2

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
        current_move_stats = self.move_stack[move]
        if self.killed:
            self.current_move_score += 1
            self.killed = False

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

    def reset(self):
        if self.food >= self.min_hunger * 2:
            self.reproducing = True
        self.food = 1
        self.min_hunger = 0
        Actor.reset(self)

    def reproducing_actor(self):
        new_actor_location = Actor.reproducing_actor(self)
        if new_actor_location:
            self.sim_state.preds += 1
            for i, cell in enumerate(self.sim_state.grid_cells):
                if cell == new_actor_location:
                    new_spawn_index = i
                    break
            self.sim_state.Actors.append(PredActor(self.sim_state, new_spawn_index, len(self.sim_state.Actors), True, self))