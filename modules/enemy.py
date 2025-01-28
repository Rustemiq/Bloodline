import pygame
import math

from modules.load_image import load_image
from modules.enemy_movement import EnemyMovement
from modules.enemy_destroyed import EnemyDestroyed

tile_size = 50
enemy_images = {
    'knife': load_image('enemy_knife.png'),
    'shotgun': load_image('enemy_shotgun.png'),
    'uzi': load_image('enemy_uzi.png')
}
player_hearing_distance = 250


class Enemy(pygame.sprite.Sprite, EnemyMovement):
    def __init__(self, weapon, pos, walk_around_pattern, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
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
        self.is_player_heard = False

    def add_inter_groups(self, dead_enemies, walls_group,
                         player_group, player, all_sprites):
        self.all_sprites = all_sprites
        self.dead_enemies = dead_enemies
        self.walls_group = walls_group
        self.player_group = player_group
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

    def start_shooting(self):
        if self.weapon.type != 'knife':
            self.aiming_timer = 15
            self.state = 'shoot'
        else:
            self.state = 'use_knife'

    def start_run_to_player(self):
        self.state = 'run_to_player'
        self.run_to_player_iteration = 0
        player_x = (round((self.player.rect.x - self.rect.x)
                          / tile_size) + self.curr_pos[0])
        player_y = (round((self.player.rect.y - self.rect.y)
                          / tile_size) + self.curr_pos[1])
        self.route_to_player = self.build_route(
            player_x, player_y, self.level_map)
        self.player_last_seen_in = player_x, player_y
        self.speed = 5

    def start_look_around(self):
        self.look_around_timer = 120
        self.state = 'look_around'

    def look_around(self):
        self.look_around_timer -= 1
        if 110 >= self.look_around_timer >= 90 or self.look_around_timer < 10:
            self.direction -= 4
        elif 20 <= self.look_around_timer <= 40:
            self.direction += 4
        self.rotate(self.direction)

    def player_shoots(self):
        dist_x = abs(self.player.rect.x - self.rect.x)
        dist_y = abs(self.player.rect.y - self.rect.y)
        distance = math.sqrt(dist_x ** 2 + dist_y ** 2)
        if distance <= player_hearing_distance:
            self.is_player_heard = True

    def update(self):
        if self.state == 'walk_around' or self.state == 'run_to_player':
            self.move(self.state, self.rect, self.route_to_player)
        if self.state == 'shoot':
            if self.aiming_timer <= 0:
                self.shoot_to_player(self.rect, self.player.rect, self.weapon,
                                     self.player_group, self.walls_group)
            else:
                self.aiming_timer -= 1
        if self.state == 'look_around':
            self.look_around()
            if self.look_around_timer == 0:
                self.state = 'keep_watch'
        if self.distance <= 0:
            if self.is_player_visible() and self.state != 'shoot':
                self.start_shooting()
            if ((self.state == 'shoot' and not self.is_player_visible())
                    or self.state == 'use_knife' or self.is_player_heard):
                self.start_run_to_player()
                self.is_player_heard = False
            if (tuple(self.curr_pos) == self.player_last_seen_in
                    and self.state == 'run_to_player'):
                self.start_look_around()