import pygame
from math import floor

from modules.load_image import load_image
from modules.weapon_in_hand import ShotgunInHand


boss_center = 48, 25
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        sheet = load_image('boss_sheet.png')
        columns, rows = 4, 2
        self.frames = self.cut_sheet(sheet, columns, rows)
        self.curr_frame = 0
        self.image = self.frames[self.curr_frame]
        self.rect = self.rect.move(x, y)
        self.is_scene_started = False
        self.is_alive = True

    def add_inter_groups(self, bullets_group, walls_group, player_group,
                         all_sprites):
        self.bullets_group = bullets_group
        self.walls_group = walls_group
        self.player_group = player_group
        self.all_sprites = all_sprites

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return frames

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
            if floor(self.curr_frame) < len(self.frames):
                self.image = self.frames[floor(self.curr_frame)]
                self.curr_frame += 0.2
            if pygame.sprite.spritecollideany(self, self.bullets_group):
                self.die()