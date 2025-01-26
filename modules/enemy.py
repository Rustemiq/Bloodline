import pygame

from modules.load_image import load_image
from modules.enemy_movement import EnemyMovement
tile_size = 50
enemy_images = {
    'knife': load_image('enemy_knife.png'),
    'shotgun': load_image('enemy_shotgun.png'),
    'uzi': load_image('enemy_uzi.png')
}


class Enemy(pygame.sprite.Sprite, EnemyMovement):
    def __init__(self, weapon, pos, walk_around_pattern):
        pygame.sprite.Sprite.__init__(self)
        EnemyMovement.__init__(self, pos, walk_around_pattern)
        self.sample_image = self.image = enemy_images[weapon.type]
        self.rect = pygame.Rect(tile_size * pos[0],
                                tile_size * pos[1], 45, 45)
        self.image_x, self.image_y = 0, 0
        self.weapon = weapon

    def draw(self, screen):
        hitbox_correction = 3
        #картинку необходимо сдвинуть относительно rect, дабы точка
        #вращения соответствовала голове врага
        x = (self.rect.x + self.image_offset[0] - hitbox_correction)
        y = (self.rect.y + self.image_offset[1] - hitbox_correction)
        screen.blit(self.image, (x, y))

    def update(self):
        EnemyMovement.move(self)