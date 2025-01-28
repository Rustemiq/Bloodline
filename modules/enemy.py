from sys import intern

import pygame

from modules.load_image import load_image
from modules.enemy_movement import EnemyMovement
from modules.enemy_destroyed import EnemyDestroyed
from copy import copy

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
        self.level_map = None
        self.state = 'walk_around'
        self.walk_around()
        self.player_last_seen_in = -1, -1
        self.route_to_player = []

    def add_inter_groups(self, all_sprites, dead_enemies, walls_group, player):
        self.all_sprites = all_sprites
        self.dead_enemies = dead_enemies
        self.walls_group = walls_group
        self.player = player

    def is_player_visible(self):
        for wall in self.walls_group:
            if wall.rect.clipline(self.rect.centerx, self.rect.centery,
                                  self.player.rect.centerx,
                                  self.player.rect.centery):
                return False
        return True

    def destroy(self, is_lethal):
        EnemyDestroyed(self.rect, is_lethal,
                       self.all_sprites, self.dead_enemies)
        self.kill()

    def draw(self, screen):
        hitbox_correction = 3
        #картинку необходимо сдвинуть относительно rect, дабы точка
        #вращения соответствовала голове врага
        x = (self.rect.x + self.image_offset[0] - hitbox_correction)
        y = (self.rect.y + self.image_offset[1] - hitbox_correction)
        screen.blit(self.image, (x, y))

    def update(self):
        self.move(self.state, self.rect, self.route_to_player)
        if self.distance <= 0:
            if self.is_player_visible():
                player_x = (round((self.player.rect.x - self.rect.x)
                                  / tile_size) + self.curr_pos[0])
                player_y = (round((self.player.rect.y - self.rect.y)
                                  / tile_size) + self.curr_pos[1])
                self.state = 'shoot'
                self.player_last_seen_in = player_x, player_y
            if self.player_last_seen_in != (-1, -1):
                if not self.is_player_visible() or self.weapon.type == 'knife':
                    self.state = 'run_to_player'
                    self.run_to_player_iteration = 0
                    self.route_to_player = self.build_route(
                        *self.player_last_seen_in, self.level_map)
                    self.speed = 5
            if tuple(self.curr_pos) == self.player_last_seen_in:
                self.state = 'look_around'