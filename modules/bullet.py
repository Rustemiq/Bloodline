import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, target_type, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((4, 4))
        self.image.fill("yellow")
        self.rect = pygame.Rect(x, y, 4, 4)
        self.x, self.y = x, y
        self.speed = 15
        self.direction = direction
        self.target_type = target_type

    def add_internal_objects(self, walls_group, targets_group):
        self.walls_group = walls_group
        self.targets_group = targets_group

    def update(self):
        self.x += self.speed * math.cos((self.direction - 90) * math.pi / 180)
        self.y += self.speed * math.sin((self.direction - 90) * math.pi / 180)
        self.rect.x = self.x
        self.rect.y = self.y
        for target in self.targets_group:
            if pygame.sprite.collide_rect(self, target):
                if self.target_type == "enemies":
                    target.destroy(is_lethal=True)
                else:
                    target.die()
                self.kill()
                return
        if pygame.sprite.spritecollideany(self, self.walls_group):
            self.kill()
