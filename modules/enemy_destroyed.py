import pygame
from modules.load_image import load_image
from random import choice, randint

dead_images = [
    load_image("enemy_dead1.png"),
    load_image("enemy_dead2.png"),
    load_image("enemy_dead3.png"),
]
knocked_out_image = load_image("enemy_knocked_out.png")


class EnemyDestroyed(pygame.sprite.Sprite):
    def __init__(self, enemy_rect, is_lethal, all_sprites, dead_enemies):
        super().__init__(all_sprites, dead_enemies)
        if is_lethal:
            self.image = choice(dead_images)
        else:
            self.image = knocked_out_image
        self.image = pygame.transform.rotate(self.image, randint(0, 360))
        self.rect = self.image.get_rect()
        self.rect.x = enemy_rect.centerx - self.rect.w // 2
        self.rect.y = enemy_rect.centery - self.rect.h // 2
