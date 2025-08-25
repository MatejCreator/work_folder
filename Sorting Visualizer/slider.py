import pygame

from main import set_cursor, NEONGREEN

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.start_stop = (x - width / 2, x + width / 2)
        self.dragging = False
        self.dot_rect = pygame.Rect(0, 0, 12, height + 2)
        self.dot_rect.center = (self.start_stop[0] + self.value, y)

    def draw(self, screen):
        if self.dragging:
            set_cursor("drag")

        pygame.draw.rect(screen, NEONGREEN, self.rect)
        pygame.draw.rect(screen, "grey", self.dot_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.dot_rect.collidepoint(event.pos):
                self.dragging = True
                set_cursor("drag")
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            set_cursor("arrow")
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            set_cursor("drag")
            val_range = self.max_val - self.min_val
            pos_range = self.rect.width - self.dot_rect.width
            rel_x = min(max(event.pos[0] - self.rect.x, 0), pos_range)
            self.value = self.min_val + (rel_x * val_range) / pos_range

        self.dot_rect.center = (self.start_stop[0] + self.value * 2 - self.min_val * 2, self.y)

    @property
    def get_value(self):
        return int(self.value)
