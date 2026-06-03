import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self):
        self.x    = 0.0
        self.y    = 0.0
        self.zoom = 1.0

    def world_to_screen(self, x, y):
        return (x - self.x)*self.zoom, (y - self.y)*self.zoom

    def screen_to_world(self, sx, sy):
        return sx/self.zoom + self.x, sy/self.zoom + self.y

    def apply_rect(self, rect):
        sx, sy = self.world_to_screen(rect.x, rect.y)
        return pygame.Rect(int(sx), int(sy),
                           max(1, int(rect.width*self.zoom)),
                           max(1, int(rect.height*self.zoom)))

    def visible_world_rect(self):
        wx0, wy0 = self.screen_to_world(0, 0)
        wx1, wy1 = self.screen_to_world(SCREEN_WIDTH, SCREEN_HEIGHT)
        return pygame.Rect(int(wx0), int(wy0), int(wx1-wx0)+1, int(wy1-wy0)+1)

    def follow(self, target_rect):
        tcx = target_rect.centerx - SCREEN_WIDTH  / 2 / self.zoom
        tcy = target_rect.centery - SCREEN_HEIGHT / 2 / self.zoom
        self.x += (tcx - self.x) * 0.12
        self.y += (tcy - self.y) * 0.12