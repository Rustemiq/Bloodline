from random import randint

import pygame
import math
from copy import copy

from modules.load_image import load_image
from modules.weapon_converter import convert_to_hand, convert_to_item
from modules.rotate_on_pivot import rotate_on_pivot
from modules.animation import Animation

HEIGHT = 600
player_images = {
        'empty': load_image('main_char_walk.png'),
        'knife': load_image('main_char_knife.png'),
        'shotgun': load_image('main_char_shotgun.png'),
        'uzi': load_image('main_char_uzi.png')
}
tile_size = 50
player_center = 24, 25
dead_player_center = 27, 47


class Player(pygame.sprite.Sprite):
    def __init__(self, weapon, pos_x, pos_y, *groups):
        super().__init__(*groups)
        if weapon == 'empty':
            self.sample_image = self.image = player_images['empty']
        else:
            self.sample_image = self.image = player_images[weapon.type]
        self.rect = pygame.Rect(tile_size * pos_x,
                                tile_size * pos_y, 45, 45)
        self.image_offset = 0, 0
        self.weapon = weapon
        self.speed = 4
        self.is_alive = True
        self.hit_animation = Animation('main_char_hit_sheet.png',
                                       5, 1, 0.34, True)

    def add_inter_groups(self, walls_group, weapons_group, enemies_group,
                         bullets_group, trigger_tile_group, all_sprites):
        self.walls_group = walls_group
        self.weapons_group = weapons_group
        self.enemies_group = enemies_group
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites
        self.trigger_tile_group = trigger_tile_group

    def draw(self, screen):
        hitbox_correction = 3
        dead_player_correction = -15
        #картинку необходимо сдвинуть относительно rect, дабы точка
        #вращения соответствовала голове персонажа
        x = (self.rect.x + self.image_offset[0] - hitbox_correction)
        y = (self.rect.y + self.image_offset[1] - hitbox_correction)
        if not self.is_alive:
            y += dead_player_correction
            #корректировка, связанная с разным размером картинки живого
            #и мертвого игрока
        screen.blit(self.image, (x, y))

    def turn_to_mouse(self, mouse_pos):
        x_rel = mouse_pos[0] - self.rect.centerx
        y_rel = mouse_pos[1] - self.rect.centery
        angle = (180 / math.pi * -math.atan2(y_rel, x_rel))
        self.direction = (90 - angle) % 360
        self.image = pygame.transform.rotate(self.sample_image, angle)
        self.image_offset = rotate_on_pivot(player_center, self.direction,
                                             self.image, self.sample_image)

    def get_move(self, keys):
        if self.weapon != 'empty' and self.weapon.type == 'knife':
            boost = 1
        else:
            boost = 0
        if keys[pygame.constants.K_w]:
            self.rect.y -= self.speed + boost
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.y += self.speed + boost
        if keys[pygame.constants.K_a]:
            self.rect.x -= self.speed + boost
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.x += self.speed + boost
        if keys[pygame.constants.K_s]:
            self.rect.y += self.speed + boost
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.y -= self.speed + boost
        if keys[pygame.constants.K_d]:
            self.rect.x += self.speed + boost
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.x -= self.speed + boost

    def set_weapon(self, weapon):
        if weapon == 'empty':
            self.sample_image = self.image = player_images['empty']
        else:
            self.sample_image = self.image = player_images[weapon.type]
        self.turn_to_mouse(pygame.mouse.get_pos())
        self.weapon = copy(weapon)

    def throw_weapon(self):
        if self.weapon != 'empty':
            throwed_weapon = convert_to_item(self.weapon, self.rect,
                                             self.weapons_group, self.all_sprites)
            throwed_weapon.add_inter_groups(self.walls_group,
                                            self.enemies_group)
            throwed_weapon.throw(self.direction)
            self.weapon = 'empty'
            self.sample_image = self.image = player_images['empty']
            self.turn_to_mouse(pygame.mouse.get_pos())
            return throwed_weapon

    def grab_weapon(self):
        weapons = pygame.sprite.spritecollide(self, self.weapons_group, False)
        weapons = list(filter(lambda wp: not wp.thrown, weapons))
        if weapons != []:
            weapon = convert_to_hand(weapons[0], self.bullets_group,
                                     self.walls_group, self.enemies_group,
                                     self.all_sprites)
            self.set_weapon(weapon)
            weapons[0].kill()

    def weapon_interaction(self):
        throwed_weapon = self.throw_weapon()
        self.grab_weapon()
        return throwed_weapon

    def use_knife(self):
        for enemy in self.enemies_group:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.destroy(is_lethal=True)

    def use_fists(self):
        if self.hit_animation.curr_frame == 0:
            self.image = self.sample_image = self.hit_animation.animate()

    def is_trigger_touched(self):
        return (pygame.sprite.spritecollideany(self, self.trigger_tile_group)
                is not None)

    def die(self):
        if self.is_alive:
            self.is_alive = False
            self.sample_image = load_image('player_dead.png')
            self.direction = randint(0, 360)
            self.image = pygame.transform.rotate(self.sample_image,
                                                 self.direction)
            self.image_offset = rotate_on_pivot(dead_player_center,
                                                90 - self.direction, self.image,
                                                self.sample_image)
    def update(self):
        if self.hit_animation.curr_frame > 0:
            if (self.weapon == 'empty'
                    and self.is_alive):
                self.image = self.sample_image = self.hit_animation.animate()
                self.turn_to_mouse(pygame.mouse.get_pos())
            else:
                self.hit_animation.reset()
            if self.hit_animation.is_end:
                self.hit_animation.reset()
            for enemy in self.enemies_group:
                if pygame.sprite.collide_rect(self, enemy):
                    enemy.destroy(False)