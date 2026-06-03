import pygame

INTERACT_DIST = 120

class Computer:
    def __init__(self, data: dict):
        self.x          = data["x"]
        self.y          = data["y"]
        self.w          = data.get("w", 64)
        self.h          = data.get("h", 64)
        self.id         = data.get("id", 0)
        self.completed  = data.get("completed", False)
        self.rect       = pygame.Rect(self.x, self.y, self.w, self.h)

    def complete(self):
        self.completed = True

    def in_range(self, player_rect: pygame.Rect) -> bool:
        cx = self.x + self.w // 2
        cy = self.y + self.h // 2
        px = player_rect.centerx
        py = player_rect.centery
        return ((cx - px)**2 + (cy - py)**2) ** 0.5 <= INTERACT_DIST

    def to_dict(self):
        return {
            "x": self.x, "y": self.y,
            "w": self.w, "h": self.h,
            "id": self.id,
            "completed": self.completed,
        }