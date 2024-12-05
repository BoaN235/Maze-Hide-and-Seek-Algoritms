from ActorClass import Actor


class PreyActor(Actor):
    def __init__(self, sim_state, spawn_index, ide):
        super().__init__(sim_state, spawn_index, ide)
        self.color = (0, 255, 0)
        self.spawn_color = (0, 155, 0)
        self.id = ide
  
    def genetic_mutations(self):
        pass
     
    # def reset(self):
    #     Actor.reset(self)

