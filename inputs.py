import pygame

class Button:
    
    def __init__(self, screen, button_color, button_text, button_rect, font, callback):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.button_color = button_color
        self.button_text = button_text
        self.button_rect = button_rect
        self.font = font
        self.callback = callback


    def draw_button(self):
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        text_surface = self.font.render(self.button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()

class InputBox:
    def __init__(self, screen, input_data, font ,input_rect):
        self.screen = screen
        self.input_data = input_data
        self.font = font
        self.input_rect = input_rect
    def draw_input_box(self):
        color = self.input_data['color_active'] if self.input_data['active'] else self.input_data['color_passive']
        pygame.draw.rect(self.screen, self.color, self.input_rect, 2)
        text_surface = self.font.render(self.input_data['text'], True, (255, 255, 255))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

class text:
    def __init__(self, screen, position, text, font, color):
        self.screen = screen
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.text_surface = text_surface = font.render(self.text, True, self.color)
        self.text_surface = text_surface.get_rect(center=self.position)  # Position the text


    def draw_text(self):
        self.screen.blit(self.text_surface, self.text_rect)  # Blit the text to the screen

class Slider:
    def __init__(self, screen, position, width, height, min_val, max_val, initial_val):
        self.screen = screen
        self.position = position
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.slider_rect = pygame.Rect(position[0], position[1], width, height)
        self.handle_rect = pygame.Rect(position[0] + (initial_val - min_val) / (max_val - min_val) * width - height // 2, position[1] - height // 2, height, height)
        self.dragging = False

    def draw_slider(self):
        pygame.draw.rect(self.screen, pygame.Color("gray"), self.slider_rect)
        pygame.draw.rect(self.screen, pygame.Color("white"), self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_x = max(self.slider_rect.x, min(event.pos[0], self.slider_rect.x + self.slider_rect.width))
                self.handle_rect.x = new_x - self.handle_rect.width // 2
                self.value = self.min_val + (new_x - self.slider_rect.x) / self.slider_rect.width * (self.max_val - self.min_val)

    def get_value(self):
        return self.value