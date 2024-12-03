import pygame
from CellClass import Cell
from ActorClass import Actor, PreyActor, PredActor
import ast
import random

class SimState:
    def __init__(self):
        self.MaxActions = 10
        self.WIDTH, self.HEIGHT = 1202, 902
        self.TILE = 50
        self.cols, self.rows = self.WIDTH // self.TILE, self.HEIGHT // self.TILE        
        self.generation = 0
        self.ide = [1,2,3,4,5,6,7,8,9,10]



    def load_walls(self):
        try:
            with open("lastmaze.txt", "r") as file:
                file_contents = file.readlines()
                self.TILE = int(file_contents[0].strip())
                if len(file_contents) > 1:
                    # Process the remaining lines
                    walls_data = [ast.literal_eval(line.strip()) for line in file_contents[1:]]
        except (FileNotFoundError, ValueError, SyntaxError) as e:
            print(f"Error loading maze state: {e}")
            self.TILE = 100
            walls_data = []
        
        return walls_data


    def create_grid(self):
            # Initialize grid cells
        self.grid_cells = [Cell(col, row, self) for row in range(self.rows) for col in range(self.cols)]
        # Load saved walls if available
        
        walls_data = self.load_walls()
        
        if walls_data:
            for cell, walls in zip(self.grid_cells, walls_data):
                cell.save_gen(walls)
    def create_actors(self):
        self.Actors = [PredActor(self, 10, self.ide[0]), PreyActor(self, 20, self.ide[1]), PreyActor(self, 30, self.ide[2]), PreyActor(self, 40, self.ide[3])]


    def load():
        pass
    def save():
        pass

    def start_sim(self):
        self.create_grid()
        self.create_actors()
        # Game loop
        RES = self.WIDTH, self.HEIGHT
        FONT_SIZE = 32
        
        pygame.init()
        sc = pygame.display.set_mode(RES)
        font = pygame.font.Font(None, FONT_SIZE)
        clock = pygame.time.Clock()
        
        while True:
            sc.fill((50, 50, 50))
            for a in self.Actors:
                a.preform_action()
            
            self.generation += 1
            # Draw all cells
            [cell.draw(sc) for cell in self.grid_cells]
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()
            clock.tick(5)    


# Initialize Pygame

sim = SimState()
sim.start_sim()


