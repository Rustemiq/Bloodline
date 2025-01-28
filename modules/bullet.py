import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((4, 4))
        self.image.fill('yellow')
        self.rect = pygame.Rect(x, y, 4, 4)
        self.x, self.y = x, y
        self.speed = 15
        self.direction = direction

    def add_inter_groups(self, walls_group, enemies_group):
        self.walls_group = walls_group
        self.enemies_group = enemies_group

    def update(self):
        self.x += self.speed * math.cos((self.direction - 90) * math.pi / 180)
        self.y += self.speed * math.sin((self.direction - 90) * math.pi / 180)
        self.rect.x = self.x
        self.rect.y = self.y
        for enemy in self.enemies_group:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.destroy(is_lethal=True)
                self.kill()
        if pygame.sprite.spritecollideany(self, self.walls_group):
            self.kill()
