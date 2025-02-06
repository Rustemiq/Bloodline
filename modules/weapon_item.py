import pygame
from modules.load_image import load_image
import math

weapon_images = {
    "knife": load_image("knife.png"),
    "shotgun": load_image("shotgun.png"),
    "uzi": load_image("uzi.png"),
}
weapon_ammo = {"knife": 0, "shotgun": 4, "uzi": 20}


class WeaponItem(pygame.sprite.Sprite):
    def __init__(self, type, x, y, *groups, ammo=None):
        super().__init__(*groups)
        self.type = type
        self.image = weapon_images[self.type]
        self.rect = self.image.get_rect().move(x, y)
        if ammo is None:
            ammo = weapon_ammo[self.type]
        self.ammo = ammo
        self.thrown = False

    def add_internal_objects(self, walls_group, enemies_group):
        self.walls_group = walls_group
        self.enemies_group = enemies_group

    def throw(self, direction):
        self.thrown = True
        self.throw_speed = 20
        self.throw_direction = direction
        self.image = pygame.transform.rotate(self.image, 90 - direction)
        self.rect.w = self.image.get_rect().w
        self.rect.h = self.image.get_rect().h
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.thrown:
            self.rect.x += self.throw_speed * math.sin(
                self.throw_direction * math.pi / 180
            )
            self.rect.y -= self.throw_speed * math.cos(
                self.throw_direction * math.pi / 180
            )
            self.throw_speed -= 1
            for enemy in self.enemies_group:
                if pygame.sprite.collide_rect(self, enemy):
                    self.throw_speed = 0
                    enemy.destroy(is_lethal=False)
                    break
            for wall in self.walls_group:
                if pygame.sprite.collide_mask(self, wall):
                    self.throw_speed = 0
                    break
            if self.throw_speed == 0:
                self.thrown = False
