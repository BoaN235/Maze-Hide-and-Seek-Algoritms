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
        self.current_cell.check_neighbors(self.sim_state.grid_cells)
        for actor in self.sim_state.Actors:
            if actor.ActorType() == ActorType.PREDATOR:
                if closest_actor is None:
                    closest_actor = actor
                elif self.current_cell.distance(actor.current_cell) < self.current_cell.distance(closest_actor.current_cell):
                    closest_actor = actor
        self.find_best_move_away_from_target(closest_actor)

    def search_for_food(self):
        closest_cell = None
        for cell in self.sim_state.grid_cells:
            if cell.food > 0:
                if closest_cell is None:
                    closest_cell = cell
                elif self.current_cell.distance(cell) < self.current_cell.distance(closest_cell) and cell.food > closest_cell.food:
                    closest_cell = cell
        self.find_best_move_to_target(closest_cell)
    #     Actor.reset(self)

    def find_best_move_to_target(self, target):
        moves = [self.current_cell.left, self.current_cell.right, self.current_cell.bottom, self.current_cell.top]
        moves = [move for move in moves if move is not None]  # Remove None values

        # Sort moves based on distance to target
        moves.sort(key=lambda move: move.distance(target))

        for cell in moves:
            if cell == self.current_cell.left and self.current_cell.can_move_left():
                self.current_cell = self.current_cell.left
                break
            if cell == self.current_cell.right and self.current_cell.can_move_right():
                self.current_cell = self.current_cell.right
                break
            if cell == self.current_cell.top and self.current_cell.can_move_top():
                self.current_cell = self.current_cell.top
                break
            if cell == self.current_cell.bottom and self.current_cell.can_move_bottom():
                self.current_cell = self.current_cell.bottom
                break



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
        if self.actions[self.sim_state.action_step] == Moves.SENSE_T:
            self.sense_threat()
        else:
            Actor.step(self)

        self.food_difference = self.last_food - self.food
        self.scoring_list_gen()

    def score_move(self, move, extra_score=0):
        current_move_stats = self.move_stack[move]
        extra_score = current_move_stats['food']/2 

        Actor.score_move(self, move, extra_score)