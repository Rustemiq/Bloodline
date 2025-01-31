import pygame
from math import floor

from modules.load_image import load_image
from modules.weapon_in_hand import ShotgunInHand
from modules.animation import Animation


boss_center = 48, 25
class Boss(pygame.sprite.Sprite, Animation):
    def __init__(self, x, y, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        Animation.__init__(self, 'boss_sheet.png', 4, 2, 0.2, False)
        self.image = self.frames[self.curr_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.is_scene_started = False
        self.is_alive = True

    def add_inter_groups(self, bullets_group, walls_group, player_group,
                         all_sprites):
        self.bullets_group = bullets_group
        self.walls_group = walls_group
        self.player_group = player_group
        self.all_sprites = all_sprites

    def shoot(self):
        self.weapon = ShotgunInHand(target='player')
        self.weapon.add_inter_groups(self.bullets_group, self.walls_group,
                                     self.player_group, self.all_sprites)
        x = self.rect.x + boss_center[0]
        y = self.rect.y + boss_center[1]
        self.weapon.shoot(x, y, 90)

    def die(self):
        self.is_alive = False
        self.image = pygame.transform.rotate(load_image('boss_dead.png'), 90)

    def update(self):
        if self.is_scene_started and self.is_alive:
            self.image = self.animate()
            if pygame.sprite.spritecollideany(self, self.bullets_group):
                self.die()