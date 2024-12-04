import pygame
from CellClass import Cell
from ActorClass import Actor, PreyActor, PredActor
from inputs import Button, InputBox, text, Slider
import ast
import json
from random import seed

class SimState:
    def __init__(self):
        self.MaxActions = 100
        self.WIDTH, self.HEIGHT = 1202, 902
        self.TILE = 75
        self.cols, self.rows = self.WIDTH // self.TILE, self.HEIGHT // self.TILE        
        self.generation = 1
        self.pred_score = 0
        self.generation_actors = []
        self.killed_actors = []


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

    def save_walls(self):
        pass

    def create_grid(self):
            # Initialize grid cells
        self.grid_cells = [Cell(col, row, self) for row in range(self.rows) for col in range(self.cols)]
        # Load saved walls if available
        
        walls_data = self.load_walls()
        
        if walls_data:
            for cell, walls in zip(self.grid_cells, walls_data):
                cell.save_gen(walls)
    def create_actors(self):
        self.Actors = [ PreyActor(self, 10, 2), PreyActor(self, 30, 3), PreyActor(self, 40, 4), PredActor(self, 32, 1),PredActor(self, 43, 1),PredActor(self, 8, 1)]
        self.generation_actors = self.Actors

    def load(self):
        # Load the saved state
        with open("state.json", 'r') as f:
                state = json.load(f)
            
        self.MaxActions = state['max_actions']
        self.WIDTH = state['width']
        self.HEIGHT = state['height']
        self.TILE = state['tile']
        self.cols = state['cols']
        self.rows = state['rows']
        self.generation = state['generation']
        
        self.grid_cells = [Cell.from_dict(cell_data) for cell_data in state['grid_cells']]
        self.Actors = [Actor.from_dict(actor_data) for actor_data in state['actors']]
        pass
    def save(self):
        # Save the current state
        state = {
            'max_actions': self.MaxActions,
            'width': self.WIDTH,
            'height': self.HEIGHT,
            'tile': self.TILE,
            'cols': self.cols,
            'rows': self.rows,
            'generation': self.generation,
            'grid_cells': [cell.to_dict() for cell in self.grid_cells],
            'actors': [actor.to_dict() for actor in self.Actors]
        }
        with open("state.json", 'w') as f:
            json.dump(state, f, indent=4)
        pass

    def reset_generation(self):
        # Reset the generation
        for x in self.killed_actors:
            self.Actors.append(x)
            self.killed_actors.remove(x)
        self.generation += 1
        print(f"Generation: {self.generation}")        
        self.killed_actors = []
        pass

    def generate_sim(self):
        # Game loop
        seed(132)
        RES = self.WIDTH, self.HEIGHT
        FONT_SIZE = 32

        # Pygame setup
        pygame.init()
        sc = pygame.display.set_mode(RES)
        font = pygame.font.Font(None, FONT_SIZE)
        clock = pygame.time.Clock()

        sc.fill(pygame.Color(50, 50, 50))
        
        # Initialize the grid
        self.grid_cells = [Cell(col, row, self) for row in range(self.rows) for col in range(self.cols)]
        current_cell =  self.grid_cells[0]
        stack = []

        done = False

        # Main loop
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Draw all cells
            [cell.draw(sc) for cell in self.grid_cells]

            # Mark the current cell as visited and draw it
            current_cell.visited = True
            current_cell.draw_current_cell(sc)

            # Check for the next cell to move to
            next_cell = current_cell.check_neighbors(self.grid_cells)
            if next_cell:
                next_cell.visited = True
                stack.append(current_cell)
                Cell.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

            # Check if all cells are visited and if so, write to the file
            if all(cell.visited for cell in self.grid_cells):
                if not done:
                    print("All cells visited, writing to file...")
                    with open("lastmaze.txt", "w") as file:
                        file.write(str(self.TILE) + '\n')
                        for x in self.grid_cells:
                            file.write(str(x.walls) + '\n')
                    print("File written successfully.")
                    done = True
                    pygame.quit()
                    exit()

            # Update display
            pygame.display.flip()
            clock.tick(1000)  # Adjust the tick rate for smoother gameplay

    def start_sim(self):
        self.create_grid()
        self.create_actors()
        # Game loop
        RES = self.WIDTH, self.HEIGHT
        FONT_SIZE = 32
        font = pygame.font.Font(None, FONT_SIZE)
        
        settings_button = Button((1000, 50, 150, 50), "Settings", font, self.settings)
        pygame.init()
        sc = pygame.display.set_mode(RES)
        font = pygame.font.Font(None, FONT_SIZE)
        clock = pygame.time.Clock()
        
        while True:
            sc.fill((50, 50, 50))
            for a in self.Actors:
                a.preform_action()
            if self.Actors[0].moves == self.MaxActions:
                self.reset_generation()

                self.Actors = self.generation_actors


            # Draw all cells
            [cell.draw(sc) for cell in self.grid_cells]
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip()
            clock.tick(100)    
