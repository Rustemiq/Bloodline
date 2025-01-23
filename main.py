import pygame
import os
import math
from random import randint

WIDTH = 900
HEIGHT = 600
tile_size = 50


def load_image(name, colorkey=True):
    fullname = os.path.join('pictures', name)
    image = pygame.image.load(fullname)
    if colorkey:
        image.set_colorkey(image.get_at((0, 0)))
    return image


def generate_level(name):
    fullname = os.path.join('levels', name)
    with open(fullname) as map_file:
        level_map = [line.strip() for line in map_file]
    player = None
    for y in range(len(level_map)):
        for x in range(len(level_map[0]) - 1):
            cell = level_map[y][x]
            if cell == '#':
                Tile('wall', x, y)
            elif cell == '-':
                Tile('asphalt', x, y)
            else:
                Tile('empty', x, y)
                if cell == '@':
                    player = Player('empty', x, y)
                if cell == 'S':
                    WeaponItem('shotgun',
                               x * tile_size, y * tile_size)
                if cell == 'U':
                    WeaponItem('uzi', x * tile_size, y * tile_size)
                if cell == 'K':
                    WeaponItem('knife', x * tile_size, y * tile_size)
    return player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(all_sprites, tiles_group, walls_group)
        else:
            super().__init__(all_sprites, tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, weapon, pos_x, pos_y):
        super().__init__(all_sprites, player_group)
        if weapon == 'empty':
            self.sample_image = self.image = player_images['empty']
        else:
            self.sample_image = self.image = player_images[weapon.type]
        self.rect = pygame.Rect(tile_size * pos_x,
                                tile_size * pos_y, *player_size)
        self.image_x, self.image_y = 0, 0
        self.weapon = weapon

    def draw(self, screen):
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
        x_rel = mouse_pos[0] - screen_center[0]
        y_rel = mouse_pos[1] - screen_center[1]
        angle = (180 / math.pi * -math.atan2(y_rel, x_rel))
        self.direction = (90 - angle) % 360
        self.image = pygame.transform.rotate(self.sample_image, angle)
        head_x, head_y = self.get_head_coord()
        self.image_x = head_x - player_center[0]
        self.image_y = head_y - player_center[1]

    def get_move(self, keys):
        if keys[pygame.constants.K_w]:
            self.rect.y -= 4
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y += 4
        if keys[pygame.constants.K_a]:
            self.rect.x -= 4
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x += 4
        if keys[pygame.constants.K_s]:
            self.rect.y += 4
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.y -= 4
        if keys[pygame.constants.K_d]:
            self.rect.x += 4
            if pygame.sprite.spritecollideany(self, walls_group):
                self.rect.x -= 4

    def throw_weapon(self):
        if self.weapon != 'empty':
            throwed_weapon = self.weapon.convert_to_item()
            throwed_weapon.throw(self.direction)
            self.weapon = 'empty'
            self.sample_image = self.image = player_images['empty']
            self.turn_to_mouse(pygame.mouse.get_pos())

    def grab_weapon(self):
        weapons = pygame.sprite.spritecollide(self, weapons_group, False)
        weapons = list(filter(lambda wp: not wp.thrown, weapons))
        if weapons != []:
            self.weapon = weapons[0].convert_to_hand()
            self.sample_image = self.image = player_images[self.weapon.type]
            self.turn_to_mouse(pygame.mouse.get_pos())
            weapons[0].kill()

    def weapon_interaction(self):
        self.throw_weapon()
        self.grab_weapon()


class WeaponItem(pygame.sprite.Sprite):
    def __init__(self, type, x, y, ammo=None):
        super().__init__(all_sprites, weapons_group)
        self.type = type
        self.image = weapon_images[self.type]
        self.rect = self.image.get_rect().move(x, y)
        if ammo is None:
            ammo = weapon_ammo[self.type]
        self.ammo = ammo
        self.thrown = False

    def convert_to_hand(self):
        if self.type == 'shotgun':
            return ShotgunInHand(self.ammo)
        if self.type == 'uzi':
            return UziInHand(self.ammo)
        if self.type == 'knife':
            return KnifeInHand()

    def throw(self, direction):
        self.thrown = True
        self.throw_speed = 15
        self.throw_direction = direction
        self.image = pygame.transform.rotate(self.image, 90 - direction)
        self.rect.w = self.image.get_rect().w
        self.rect.h = self.image.get_rect().h
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.thrown:
            self.rect.x += self.throw_speed * math.sin(
                self.throw_direction * math.pi / 180)
            self.rect.y -= self.throw_speed * math.cos(
                self.throw_direction * math.pi / 180)
            self.throw_speed -= 1
            for wall in walls_group:
                if pygame.sprite.collide_mask(self, wall):
                    self.throw_speed = 0
                    break
            if self.throw_speed == 0:
                self.thrown = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(all_sprites, bullets_group)
        self.image = pygame.Surface((4, 4))
        self.image.fill('yellow')
        self.rect = pygame.Rect(x, y, 4, 4)
        self.x, self.y = x, y
        self.speed = 15
        self.direction = direction

    def update(self):
        self.x += self.speed * math.cos((self.direction - 90) * math.pi / 180)
        self.y += self.speed * math.sin((self.direction - 90) * math.pi / 180)
        self.rect.x = self.x
        self.rect.y = self.y
        if pygame.sprite.spritecollideany(self, walls_group):
            self.kill()


class WeaponInHand:
    def __init__(self, ammo, type, recharge):
        self.ammo = ammo
        self.type = type
        self.recharge = self.charge_level = recharge

    def get_gunpoint_coord(self):
        x, y = player.rect.center
        x += gun_len * math.cos((player.direction - 90) * math.pi / 180)
        y += gun_len * math.sin((player.direction - 90) * math.pi / 180)
        return x, y

    def convert_to_item(self):
        return WeaponItem(self.type, player.rect.x,
                          player.rect.y, self.ammo)

    def charge(self):
        if self.charge_level < self.recharge:
            self.charge_level += 1


class ShotgunInHand(WeaponInHand):
    def __init__(self, ammo):
        super().__init__(ammo, 'shotgun', 40)

    def shoot(self):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord()
            bullet_step = 3
            direction = player.direction - 4 * bullet_step
            for i in range(8):
                Bullet(x, y, direction + randint(-2, 2))
                direction += bullet_step


class UziInHand(WeaponInHand):
    def __init__(self, ammo):
        super().__init__(ammo, 'uzi', 3)

    def shoot(self):
        if self.charge_level >= self.recharge and self.ammo > 0:
            self.charge_level = 0
            self.ammo -= 1
            x, y = self.get_gunpoint_coord()
            Bullet(x, y, player.direction + randint(-2, 2))


class KnifeInHand():
    def __init__(self):
        self.type = 'knife'

    def convert_to_item(self):
        return WeaponItem(self.type, player.rect.x,
                          player.rect.y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


tile_images = {
        'wall': load_image('wall.png', colorkey=False),
        'empty': load_image('floor.png', colorkey=False),
        'asphalt': load_image('asphalt.png', colorkey=False)
}
player_images = {
        'empty': load_image('main_char_walk.png'),
        'knife': load_image('main_char_knife.png'),
        'shotgun': load_image('main_char_shotgun.png'),
        'uzi': load_image('main_char_uzi.png')
}
weapon_images = {
        'knife': load_image('knife.png'),
        'shotgun': load_image('shotgun.png'),
        'uzi': load_image('uzi.png')
}
weapon_ammo = {
        'knife': 0,
        'shotgun': 6,
        'uzi': 30
}

player_center = 24, 25
player_size = 45, 45
gun_len = 37
screen_center = WIDTH // 2, HEIGHT // 2
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
weapons_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
camera = Camera()
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Bloodline')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    player = generate_level('lvl1.txt')
    while running:
        screen.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                player.turn_to_mouse(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    player.weapon_interaction()
        if pygame.mouse.get_pressed(3)[0]:
            if player.weapon != 'empty' and player.weapon.type != 'knife':
                player.weapon.shoot()
        player.get_move(pygame.key.get_pressed())
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        weapons_group.update()
        bullets_group.update()
        if player.weapon != 'empty' and player.weapon.type != 'knife':
            player.weapon.charge()
        tiles_group.draw(screen)
        weapons_group.draw(screen)
        player.draw(screen)
        bullets_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)