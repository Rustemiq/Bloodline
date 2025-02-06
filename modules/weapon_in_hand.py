import math
import pygame
from random import randint

from modules.bullet import Bullet

gun_len = 37


class WeaponInHand:
    def __init__(self, ammo, type, recharge, target):
        self.ammo = ammo
        self.type = type
        self.recharge = self.charge_level = recharge
        self.target = target

    def add_internal_objects(
        self, bullets_group, walls_group, targets_group, sound, all_sprites
    ):
        self.bullets_group = bullets_group
        self.targets_group = targets_group
        self.walls_group = walls_group
        self.sound = sound
        self.all_sprites = all_sprites

    def get_gunpoint_coord(self, x, y, direction):
        x += gun_len * math.cos((direction - 90) * math.pi / 180)
        y += gun_len * math.sin((direction - 90) * math.pi / 180)
        return x, y

    def charge(self):
        if self.charge_level < self.recharge:
            self.charge_level += 1


class ShotgunInHand(WeaponInHand):
    def __init__(self, ammo=None, target="enemies"):
        if ammo == None:
            ammo = 4
        super().__init__(ammo, "shotgun", 40, target)

    def shoot(self, x, y, direction):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord(x, y, direction)
            bullet_step = 1.5
            direction -= bullet_step * 5
            for i in range(10):
                bullet = Bullet(
                    x,
                    y,
                    direction + randint(-1, 1),
                    self.target,
                    self.bullets_group,
                    self.all_sprites,
                )
                bullet.add_internal_objects(self.walls_group, self.targets_group)
                direction += bullet_step
            self.sound.play_weapon_sound(self)


class UziInHand(WeaponInHand):
    def __init__(self, ammo=None, target="enemies"):
        if ammo == None:
            ammo = 20
        super().__init__(ammo, "uzi", 3, target)

    def shoot(self, x, y, direction):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord(x, y, direction)
            bullet = Bullet(
                x,
                y,
                direction + randint(-2, 2),
                self.target,
                self.bullets_group,
                self.all_sprites,
            )
            bullet.add_internal_objects(self.walls_group, self.targets_group)
            self.sound.play_weapon_sound(self)


class KnifeInHand:
    def __init__(self, target="enemy"):
        self.type = "knife"
        self.target_type = target

    def add_internal_objects(self, targets_group, sound, user):
        self.targets_group = targets_group
        self.sound = sound
        self.user = user

    def use(self):
        for target in self.targets_group:
            if pygame.sprite.collide_rect(self.user, target):
                if self.target_type == "enemy":
                    target.destroy(is_lethal=True)
                else:
                    target.die()
                self.sound.play_weapon_sound(self)
