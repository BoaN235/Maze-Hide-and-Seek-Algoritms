import pygame
from CellClass import Cell
from ActorClass import Actor
from PredActor import PredActor
from PreyActor import PreyActor
from inputs import Button, InputBox, Text, Slider, TransparentBox
import ast
import json
from random import seed
import random
from openpyxl import Workbook , load_workbook
import time

class SimState:
    def __init__(self):
        self.MaxActions = 50
        self.WIDTH, self.HEIGHT = 1202, 902
        self.TILE = 25
        self.cols, self.rows = self.WIDTH // self.TILE, self.HEIGHT // self.TILE        
        self.generation = 0
        self.pred_score = 0
        self.generation_actors = []
        self.killed_actors = []
        self.setting = False
        self.speed = 100
        self.preds = 20
        self.preys = 100       
        self.Actors = []
        self.max_generations = 1000 
        self.running = True
        self.path = "data/simdata.xlsx"
        self.workbook = self.create_workbook()
        self.current_row = 2
        self.sheet = self.create_sheet()
        self.start_time = time.time()
        self.end_time = time.time()
        self.time = time.time()
        self.time_in_ms = self.time * 1000


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
        total_actors = self.preds + self.preys
        spawn_indices = random.sample(range(len(self.grid_cells)), total_actors)

        for i in range(self.preds):
            spawn_index = spawn_indices.pop()
            self.Actors.append(PredActor(self, spawn_index, i))

        for i in range(self.preys):
            spawn_index = spawn_indices.pop()
            self.Actors.append(PreyActor(self, spawn_index, i))


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
        with open("state.json", 'a') as f:
            json.dump(state, f, indent=4)
        pass

    def save_gen_stats(self):
        # Save the current state
        for x in self.Actors:
            if x.dead:
                self.pred_score += 1


        if self.pred_score < self.preys:
            wins_data = "prey wins"
        if self.pred_score > self.preys:
            wins_data = "pred wins"

        self.sheet["A" + str(self.current_row)] = self.generation
        self.sheet["B" + str(self.current_row)] = wins_data
        self.sheet["C" + str(self.current_row)] = self.preys
        self.sheet["D" + str(self.current_row)] = self.preds
        self.sheet["E" + str(self.current_row)] = self.time_in_ms

        self.current_row += 1

        self.workbook.save(self.path)

    def create_workbook(self):
        workbook = Workbook()
        
        return workbook
    
    def create_sheet(self):
        sheet = self.workbook.active
        sheet.freeze_panes = "A1"
        headers = ["Generation", "Winner", "Prey", "Pred", "Time(ms)"]
        sheet["A1"] = headers[0]
        sheet["B1"] = headers[1]
        sheet["C1"] = headers[2]
        sheet["D1"] = headers[3]
        sheet.title = "Wins"
        self.workbook.save(self.path)
        return sheet

    def end_sim(self):
        self.running = False
        self.start_review()
        load_workbook(self.path)
        pass

    

    def reset_generation(self):
        # Reset the generation
        self.end_time = time.time()
        self.time = self.end_time - self.start_time
        
                # Convert time to milliseconds
        self.time_in_ms = self.time * 1000
        # Convert time to seconds
        time_in_s = self.time
        
        self.save_gen_stats()


        self.generation += 1
        print(f"Generation: {self.generation}  time: {time_in_s:.2f} seconds ({self.time_in_ms:.0f} milliseconds)")
        self.pred_score = 0

        if self.generation >= self.max_generations:
            self.end_sim()
        for x in self.Actors: # Respawn all dead actors
            x.reset()
        self.start_time = time.time()

        pass
    def settings(self):
        self.setting = not self.setting

    def draw_settings_screen(self, screen, settings_bar, font, slider, input_box):
        if self.setting:
            settings_bar.draw_box()
            slider.draw_slider()
            input_box.draw_input_box()

    def generate_sim(self):
        # Game loop
        seed(132)
        RES = self.WIDTH, self.HEIGHT
        FONT_SIZE = 32

        # Pygame setup
        pygame.init()
        sc = pygame.display.set_mode(RES)
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 32)

        sc.fill(pygame.Color(50, 50, 50))
        
        # Initialize the grid
        self.grid_cells = [Cell(col, row, self) for row in range(self.rows) for col in range(self.cols)]
        current_cell =  self.grid_cells[0]
        stack = []

        done = False

        # Main loop
        while self.running:

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
        FONT_SIZE = 24
        

        pygame.init()
        sc = pygame.display.set_mode(RES)
        font = pygame.font.Font(None, FONT_SIZE)
        clock = pygame.time.Clock()
        
        # Create settings bar
        settings_bar_rect = pygame.Rect(0, 0, 200, self.HEIGHT)
        settings_bar = TransparentBox(sc, settings_bar_rect, (0, 0, 0), 128)

        # Create settings button
        settings_button_rect = pygame.Rect(10, 10, 180, 40)
        settings_button = Button(sc, (0, 0, 255), "Settings", settings_button_rect, font, self.settings)

        # Create slider for speed control
        slider = Slider(sc, (10, 60), 180, 20, 1, 2000, self.speed)

        # Create input box for precise speed control
        input_data = {
            'color_active': (0, 255, 0),
            'color_passive': (255, 0, 0),
            'text': str(self.speed),
            'active': False
        }
        input_box_rect = pygame.Rect(10, 100, 180, 32)
        input_box = InputBox(sc, input_data, font, input_box_rect)

        while self.running:
            #sc.fill((30, 30, 30))
            sc.fill((0, 0, 0)) #cool mode
            #sc.fill((255, 255, 255)) #try it I DARE YOU
            
            for a in self.Actors:
                a.preform_action()
            if self.Actors[self.preds + self.preys - 1].moves >= self.MaxActions:
                self.reset_generation()

                self.Actors = self.generation_actors




            # Draw all cells
            [cell.draw(sc) for cell in self.grid_cells]
            
            
            settings_button.draw_button()

            # Draw the settings bar and its elements
            self.draw_settings_screen(sc, settings_bar, font, slider, input_box)

            
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                settings_button.handle_event(event)
                self.speed = int(input_box.handle_event(event))


            pygame.display.flip()
            clock.tick(self.speed)  # Adjust the tick rate for smoother gameplay    
    
    def start_review(self):
        # Game loop
        RES = self.WIDTH, self.HEIGHT
        FONT_SIZE = 24
        


        pygame.init()
        sc = pygame.display.set_mode(RES)
        font = pygame.font.Font(None, FONT_SIZE)
        clock = pygame.time.Clock()
        

        
        while True:
            #sc.fill((30, 30, 30))
            sc.fill((0, 0, 0)) #cool mode
            #sc.fill((255, 255, 255)) try it I DARE YOU


            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


            pygame.display.flip()
            clock.tick(self.speed)  # Adjust the tick rate for smoother gameplay  
