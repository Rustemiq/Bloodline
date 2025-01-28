import math
from random import randint
from modules.bullet import Bullet

gun_len = 37

class WeaponInHand:
    def __init__(self, ammo, type, recharge, target):
        self.ammo = ammo
        self.type = type
        self.recharge = self.charge_level = recharge
        self.target = target

    def add_inter_groups(self, bullets_group, targets_group, all_sprites):
        self.bullets_group = bullets_group
        self.targets_group = targets_group
        self.all_sprites = all_sprites

    def get_gunpoint_coord(self, x, y, direction):
        x += gun_len * math.cos((direction - 90) * math.pi / 180)
        y += gun_len * math.sin((direction - 90) * math.pi / 180)
        return x, y

    def charge(self):
        if self.charge_level < self.recharge:
            self.charge_level += 1


class ShotgunInHand(WeaponInHand):
    def __init__(self, ammo=None, target='enemies'):
        if ammo == None:
            ammo = 6
        super().__init__(ammo, 'shotgun', 40, target)

    def shoot(self, x, y, direction):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord(x, y, direction)
            bullet_step = 3
            direction -= bullet_step * 4
            bullets = []
            for i in range(8):
                bullets.append(Bullet(x, y, direction + randint(-2, 2),
                                      self.target, self.bullets_group,
                                      self.all_sprites))
                direction += bullet_step
            return bullets


class UziInHand(WeaponInHand):
    def __init__(self, ammo=None, target='enemies'):
        if ammo == None:
            ammo = 30
        super().__init__(ammo, 'uzi', 3, target)

    def shoot(self, x, y, direction):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord(x, y, direction)
            bullets = [Bullet(x, y, direction + randint(-2, 2), self.target,
                                      self.bullets_group, self.all_sprites)]
            return bullets


class KnifeInHand():
    def __init__(self):
        self.type = 'knife'