import pygame
import math
from copy import copy

from modules.load_image import load_image
from modules.enemy_movement import EnemyMovement
from modules.enemy_destroyed import EnemyDestroyed
from modules.weapon_converter import convert_to_item

tile_size = 50
enemy_images = {
    "knife": load_image("enemy_knife.png"),
    "shotgun": load_image("enemy_shotgun.png"),
    "uzi": load_image("enemy_uzi.png"),
}
player_hearing_distance = 300


class Enemy(pygame.sprite.Sprite, EnemyMovement):
    def __init__(self, weapon, pos, walk_around_pattern, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        EnemyMovement.__init__(self, pos[:], walk_around_pattern)
        self.sample_image = self.image = enemy_images[weapon.type]
        self.rect = pygame.Rect(tile_size * pos[0], tile_size * pos[1], 45, 45)
        self.image_x, self.image_y = 0, 0
        self.weapon = copy(weapon)
        self.level_map = None
        self.state = "walk_around"
        self.walk_around()
        self.player_last_seen_in = -1, -1
        self.route_to_player = []
        self.is_player_heard = False
        self.is_player_alive = True

    def add_internal_objects(
        self,
        dead_enemies,
        walls_group,
        player_group,
        weapons_group,
        player,
        all_sprites,
        sound,
    ):
        self.all_sprites = all_sprites
        self.dead_enemies = dead_enemies
        self.walls_group = walls_group
        self.player_group = player_group
        self.weapons_group = weapons_group
        self.player = player
        self.sound = sound

    def is_player_visible(self):
        for wall in self.walls_group:
            if wall.rect.clipline(
                self.rect.centerx,
                self.rect.centery,
                self.player.rect.centerx,
                self.player.rect.centery,
            ):
                return False
        return True

    def destroy(self, is_lethal):
        EnemyDestroyed(
            self.rect, is_lethal, self.all_sprites, self.dead_enemies
        )
        convert_to_item(
            self.weapon, self.rect, self.weapons_group, self.all_sprites
        )
        self.kill()

    def draw(self, screen):
        hitbox_correction = 3
        # картинку необходимо сдвинуть относительно rect, дабы точка
        # вращения соответствовала голове врага
        x = self.rect.x + self.image_offset[0] - hitbox_correction
        y = self.rect.y + self.image_offset[1] - hitbox_correction
        screen.blit(self.image, (x, y))

    def start_shooting(self):
        if self.weapon.type != "knife":
            if (
                self.player.weapon != "empty"
                and self.player.weapon.type == "knife"
            ):
                self.aiming_timer = 25
            else:
                self.aiming_timer = 15
            self.state = "shoot"
        else:
            self.state = "use_knife"

    def start_run_to_player(self):
        self.state = "run_to_player"
        self.run_to_player_iteration = 0
        player_x = (
            round((self.player.rect.x - self.rect.x) / tile_size)
            + self.curr_pos[0]
        )
        player_y = (
            round((self.player.rect.y - self.rect.y) / tile_size)
            + self.curr_pos[1]
        )
        self.route_to_player = self.build_route(
            player_x, player_y, self.level_map
        )
        self.player_last_seen_in = player_x, player_y
        self.speed = 5

    def start_look_around(self):
        self.look_around_timer = 120
        self.state = "look_around"

    def player_shoots(self):
        dist_x = abs(self.player.rect.x - self.rect.x)
        dist_y = abs(self.player.rect.y - self.rect.y)
        distance = math.sqrt(dist_x**2 + dist_y**2)
        if distance <= player_hearing_distance:
            self.is_player_heard = True

    def player_died(self):
        self.is_player_alive = False

    def update(self):
        if self.state == "walk_around" or self.state == "run_to_player":
            self.move(self.state, self.rect, self.route_to_player)
        if self.state == "shoot" and self.is_player_alive:
            self.shoot_to_player(
                self.rect,
                self.player.rect,
                self.weapon,
                self.aiming_timer,
                self.sound,
            )
            if self.aiming_timer > 0:
                self.aiming_timer -= 1
        if self.state == "run_to_player" and self.weapon.type == "knife":
            self.use_knife(self.player, self.weapon)
        if self.state == "look_around":
            self.look_around_timer -= 1
            self.look_around(self.look_around_timer)
            if self.look_around_timer == 0:
                self.state = "keep_watch"
        if self.distance <= 0:
            if (
                self.is_player_alive
                and self.is_player_visible()
                and self.state != "shoot"
            ):
                self.start_shooting()
            if (
                (self.state == "shoot" and not self.is_player_visible())
                or self.state == "use_knife"
                or self.is_player_heard
            ):
                self.start_run_to_player()
                self.is_player_heard = False
            if (
                tuple(self.curr_pos) == self.player_last_seen_in
                and self.state == "run_to_player"
            ):
                self.start_look_around()
