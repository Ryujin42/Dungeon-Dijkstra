import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val, label="", is_float=False):
        self.rect = pygame.Rect(x, y, width, 20)
        self.min = min_val
        self.max = max_val
        self.val = start_val
        self.label = label
        self.dragging = False
        self.is_float = is_float
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            ratio = (event.pos[0] - self.rect.x) / self.rect.width
            ratio = max(0, min(1, ratio))
            self.val = self.min + (self.max - self.min) * ratio
            if not self.is_float:
                self.val = int(round(self.val))

    def draw(self, surface):
        pygame.draw.rect(surface, (180, 180, 180), self.rect)
        handle_x = self.rect.x + int((self.val - self.min) / (self.max - self.min) * self.rect.width)
        pygame.draw.circle(surface, (0, 120, 255), (handle_x, self.rect.centery), 8)
        label = f"{self.label}: {self.val:.2f}" if self.is_float else f"{self.label}: {int(self.val)}"
        text_surface = self.font.render(label, True, (255, 255, 255))
        surface.blit(text_surface, (self.rect.x, self.rect.y - 25))

