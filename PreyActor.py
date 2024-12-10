from ActorClass import Actor, CauseOfDeath, ActorType, Moves
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

    def ActorType(self):
        return ActorType.PREY


    def sense_threat(self):
        closest_actor = None
        for actor in self.sim_state.Actors:
            if actor.ActorType() == ActorType.PREDATOR:
                if closest_actor is None:
                    closest_actor = actor
                elif self.current_cell.distance(actor.current_cell) < self.current_cell.distance(closest_actor.current_cell):
                    closest_actor = actor

    #     Actor.reset(self)

    def generate_actions(self):
        for i in range(0, self.sim_state.MaxActions + 1):
            random_actions = random.randint(0, 5)        
            if random_actions == 0:
                self.actions.append(Moves.LEFT)
            if random_actions == 1:
                self.actions.append(Moves.RIGHT)
            if random_actions == 2:
                self.actions.append(Moves.TOP)
            if random_actions == 3:
                self.actions.append(Moves.BOTTOM)
            if random_actions == 4:
                self.actions.append(Moves.SENSE_T)
            if random_actions == 5:
                self.actions.append(Moves.SENSE_F)

    def step(self):
        self.last_food = self.food
        if self.current_cell.food > 0:
            self.current_cell.food -= 1
            self.food += 1
        if self.actions[self.sim_state.action_step] == "sense_t":
            self.sense_threat()
        else:
            Actor.step(self)

        self.food_difference = self.last_food - self.food
        self.scoring_list_gen()

    def score_move(self, move, extra_score=0):
        current_move_stats = self.move_stack[move]
        extra_score = current_move_stats['food']/2 

        Actor.score_move(self, move, extra_score)