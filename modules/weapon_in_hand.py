import math
from random import randint
from modules.bullet import Bullet

gun_len = 37
player_center = 450, 300

class WeaponInHand:
    def __init__(self, ammo, type, recharge):
        self.ammo = ammo
        self.type = type
        self.recharge = self.charge_level = recharge

    def add_inter_groups(self, bullets_group, all_spites):
        self.bullets_group = bullets_group
        self.all_spites = all_spites

    def get_gunpoint_coord(self, direction):
        x, y = player_center
        x += gun_len * math.cos((direction - 90) * math.pi / 180)
        y += gun_len * math.sin((direction - 90) * math.pi / 180)
        return x, y

    def charge(self):
        if self.charge_level < self.recharge:
            self.charge_level += 1


class ShotgunInHand(WeaponInHand):
    def __init__(self, ammo=None):
        if ammo == None:
            ammo = 6
        super().__init__(ammo, 'shotgun', 40)

    def shoot(self, direction):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord(direction)
            bullet_step = 3
            direction -= bullet_step * 4
            bullets = []
            for i in range(8):
                bullets.append(Bullet(x, y, direction + randint(-2, 2),
                                      self.bullets_group, self.all_spites))
                direction += bullet_step
            return bullets


class UziInHand(WeaponInHand):
    def __init__(self, ammo=None):
        if ammo == None:
            ammo = 30
        super().__init__(ammo, 'uzi', 3)

    def shoot(self, direction):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord(direction)
            bullets = [Bullet(x, y, direction + randint(-2, 2),
                                      self.bullets_group, self.all_spites)]
            return bullets


class KnifeInHand():
    def __init__(self):
        self.type = 'knife'