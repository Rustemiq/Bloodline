import pygame
import math
from modules.load_image import load_image
from modules.weapon_converter import convert_to_hand, convert_to_item

HEIGHT = 600
player_images = {
        'empty': load_image('main_char_walk.png'),
        'knife': load_image('main_char_knife.png'),
        'shotgun': load_image('main_char_shotgun.png'),
        'uzi': load_image('main_char_uzi.png')
}
tile_size = 50
player_center = 24, 25


class Player(pygame.sprite.Sprite):
    def __init__(self, weapon, pos_x, pos_y):
        super().__init__()
        if weapon == 'empty':
            self.sample_image = self.image = player_images['empty']
        else:
            self.sample_image = self.image = player_images[weapon.type]
        self.rect = pygame.Rect(tile_size * pos_x,
                                tile_size * pos_y, 45, 45)
        self.image_x, self.image_y = 0, 0
        self.weapon = weapon

    def add_inter_groups(self, walls_group, weapons_group):
        self.walls_group = walls_group
        self.weapons_group = weapons_group

    def draw(self, screen, font):
        hitbox_correction = 20
        #картинку необходимо сдвинуть относительно rect, дабы точка
        #вращения соответствовала голове персонажа
        x = self.rect.x - self.image_x - self.rect.w // 2 + hitbox_correction
        y = self.rect.y - self.image_y - self.rect.h // 2 + hitbox_correction
        screen.blit(self.image, (x, y))
        if self.weapon != 'empty' and self.weapon.type != 'knife':
            string = "Ammo: " + str(self.weapon.ammo)
            text = font.render(string,
                               True, (220, 20, 60))
            text_y = HEIGHT - text.get_height()
            screen.blit(text, (0, text_y))

    def get_head_coord(self):
        head_rel_x1 = self.sample_image.get_rect().w // 2 - player_center[0]
        head_rel_y1 = self.sample_image.get_rect().h // 2 - player_center[1]
        dist = math.sqrt(head_rel_x1 ** 2 + head_rel_y1 ** 2)
        angle = (-90 - (180 / math.pi *
                          -math.atan2(head_rel_y1, head_rel_x1))) % 360
        angle += self.direction - 90
        angle %= 360
        real_center = self.image.get_rect().w // 2, self.image.get_rect().h // 2
        head_y = -(round(math.cos(angle * math.pi / 180) * dist))
        head_x = -(round(math.sin(-angle * math.pi / 180) * dist))
        head_x += real_center[0]
        head_y += real_center[1]
        return head_x, head_y

    def turn_to_mouse(self, mouse_pos):
        x_rel = mouse_pos[0] - self.rect.centerx
        y_rel = mouse_pos[1] - self.rect.centery
        angle = (180 / math.pi * -math.atan2(y_rel, x_rel))
        self.direction = (90 - angle) % 360
        self.image = pygame.transform.rotate(self.sample_image, angle)
        head_x, head_y = self.get_head_coord()
        self.image_x = head_x - player_center[0]
        self.image_y = head_y - player_center[1]

    def get_move(self, keys):
        if keys[pygame.constants.K_w]:
            self.rect.y -= 4
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.y += 4
        if keys[pygame.constants.K_a]:
            self.rect.x -= 4
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.x += 4
        if keys[pygame.constants.K_s]:
            self.rect.y += 4
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.y -= 4
        if keys[pygame.constants.K_d]:
            self.rect.x += 4
            if pygame.sprite.spritecollideany(self, self.walls_group):
                self.rect.x -= 4

    def throw_weapon(self):
        if self.weapon != 'empty':
            throwed_weapon = convert_to_item(self.weapon, self.rect)
            throwed_weapon.throw(self.direction)
            self.weapon = 'empty'
            self.sample_image = self.image = player_images['empty']
            self.turn_to_mouse(pygame.mouse.get_pos())
            return throwed_weapon

    def grab_weapon(self):
        weapons = pygame.sprite.spritecollide(self, self.weapons_group, False)
        weapons = list(filter(lambda wp: not wp.thrown, weapons))
        if weapons != []:
            self.weapon = convert_to_hand(weapons[0])
            self.sample_image = self.image = player_images[self.weapon.type]
            self.turn_to_mouse(pygame.mouse.get_pos())
            weapons[0].kill()

    def weapon_interaction(self):
        throwed_weapon = self.throw_weapon()
        self.grab_weapon()
        return throwed_weapon