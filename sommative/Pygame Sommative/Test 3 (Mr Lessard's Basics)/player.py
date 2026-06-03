import pygame

class Player:
    def __init__(self):
        self.x = 960
        self.y = 540
        self.speed = 6
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def update(self, keys, walls):
        old_x = self.x
        old_y = self.y

        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed

        self.rect.x = self.x
        self.rect.y = self.y

        for wall in walls:
            if self.rect.colliderect(wall):
                self.x = old_x
                self.y = old_y
                self.rect.x = self.x
                self.rect.y = self.y
                break

    def teleport(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect.x = self.x
        self.rect.y = self.y