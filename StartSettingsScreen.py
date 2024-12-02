import pygame
import subprocess
import numpy as np


# Constants
RES = WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
FONT_SIZE = 36

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Main Menu")
font = pygame.font.Font(None, FONT_SIZE)
clock = pygame.time.Clock()


# Stores text taken by the keyboard and input box properties
inputs = [
    {'text': '100', 'rect': pygame.Rect(0, 100, 240, 32), 'color_active': pygame.Color("lightskyblue"),
     'color_passive': pygame.Color("gray15"), 'active': False},
    {'text': '100', 'rect': pygame.Rect(0, 200, 240, 32), 'color_active': pygame.Color("lightskyblue"),
     'color_passive': pygame.Color("gray15"), 'active': False}, {'text': '100', 'rect': pygame.Rect(0, 300, 240, 32), 'color_active': pygame.Color("lightskyblue"),
     'color_passive': pygame.Color("gray15"), 'active': False}
]
buttons = [
    {'rect': pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 50, BUTTON_WIDTH, 50), 'color_active': pygame.Color("lightskyblue"),
     'text': 'generate'},
    {'rect': pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 50, BUTTON_WIDTH, 50), 'color_active': pygame.Color("lightskyblue"),
     'text': 'load last generated'}
]

# To add text at a specific location (e.g., above the start button)
def draw_text(screen, text, position, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)  # Create a text surface
    text_rect = text_surface.get_rect(center=position)  # Position the text
    screen.blit(text_surface, text_rect)  # Blit the text to the screen

def draw_button(screen, button_data):
    button_rect = button_data['rect']
    button_color = button_data['color_active']
    button_text = button_data['text']
    pygame.draw.rect(screen, button_color, button_rect)
    text_surface = font.render(button_text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def draw_input_box(screen, input_data):
    input_rect = input_data['rect']
    color = input_data['color_active'] if input_data['active'] else input_data['color_passive']
    pygame.draw.rect(screen, color, input_rect, 2)
    text_surface = font.render(input_data['text'], True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

start_button = buttons[0]['rect']
load_button = buttons[1]['rect']


while True:
    sc.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_button.collidepoint(event.pos):
                    # Write data to a temporary file
                    with open("data/config.txt", "w") as file:
                        file.write(inputs[0]['text'] + '\n')
                        file.write(inputs[1]['text'] + '\n')
                        file.write(inputs[2]['text'] + '\n')
                    # Launch the MazeGenerator
                    subprocess.Popen(["python", "MazeGenerator.py"])
                    pygame.quit()
                    exit()
                if load_button.collidepoint(event.pos):
                    subprocess.Popen(["python", "HideAndSeek.py"])
                    pygame.quit()
                    exit()


                # Check if the mouse clicked on any input box
                for input_data in inputs:
                    if input_data['rect'].collidepoint(event.pos):
                        input_data['active'] = True
                    else:
                        input_data['active'] = False

        if event.type == pygame.KEYDOWN:
            for input_data in inputs:
                if input_data['active']:
                    if event.key == pygame.K_RETURN:  # User presses enter
                        input_data['text'] = ''  # Reset text after pressing enter
                    elif event.key == pygame.K_BACKSPACE:  # User presses backspace
                        input_data['text'] = input_data['text'][:-1]
                    else:
                        input_data['text'] += event.unicode  # Append the typed character

        # Displaying title text
    draw_text(sc, "Tiles", (70, 65), font, (255, 255, 255))
    draw_text(sc, "Seed", (70, 165), font, (255, 255, 255))
    draw_text(sc, "Max Actions", (70, 265), font, (255, 255, 255))
    
    for button_data in buttons:
        draw_button(sc, button_data)

    # Draw all input boxes
    for input_data in inputs:
        draw_input_box(sc, input_data)

    pygame.display.flip()
    clock.tick(60)
