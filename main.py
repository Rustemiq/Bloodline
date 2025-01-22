import pygame
import os
import math

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
            if cell == '.':
                Tile('empty', x, y)
            if cell == '#':
                Tile('wall', x, y)
            if cell == '-':
                Tile('asphalt', x, y)
            if cell == '@':
                Tile('empty', x, y)
                player = Player('empty', x, y)
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
        self.angle = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, weapon, pos_x, pos_y):
        super().__init__(all_sprites)
        self.sample_image = self.image = player_images[weapon]
        self.rect = pygame.Rect(tile_size * pos_x + 16,
                                tile_size * pos_y + 18, 25, 25)
        self.image_x, self.image_y = self.rect.x, self.rect.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - self.image_x - self.rect.w // 2,
                                 self.rect.y - self.image_y - self.rect.h // 2))

    def get_head_coord(self):
        head_rel_x1 = self.sample_image.get_rect().w // 2 - player_center[0]
        head_rel_y1 = self.sample_image.get_rect().h // 2 - player_center[1]
        dist = math.sqrt(head_rel_x1 ** 2 + head_rel_y1 ** 2)
        head_ang = (-90 - (180 / math.pi *
                          -math.atan2(head_rel_y1, head_rel_x1))) % 360
        head_ang += self.corr_angle - 90
        head_ang %= 360
        real_center = self.image.get_rect().w // 2, self.image.get_rect().h // 2
        head_y = -(round(math.cos(head_ang * math.pi / 180) * dist))
        head_x = -(round(math.sin(-head_ang * math.pi / 180) * dist))
        head_x += real_center[0]
        head_y += real_center[1]
        return head_x, head_y

    def turn_to_mouse(self, mouse_pos):
        x_rel = mouse_pos[0] - screen_center[0]
        y_rel = mouse_pos[1] - screen_center[1]
        angle = (180 / math.pi * -math.atan2(y_rel, x_rel))
        self.corr_angle = (90 - angle) % 360
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
        if keys[pygame.constants.K_SPACE]:
            self.image = load_image('test.png', colorkey=False)
            self.image_x =- self.rect.w // 2
            self.image_y =- self.rect.w // 2
            self.draw(screen)

    def update(self, keys, mouse_pos):
        self.turn_to_mouse(mouse_pos)
        self.get_move(keys)


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
player_center = 24, 25
screen_center = WIDTH // 2, HEIGHT // 2
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
camera = Camera()
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Bloodline')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    player = generate_level('lvl1.txt')
    while running:
        screen.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        player.update(pygame.key.get_pressed(), pygame.mouse.get_pos())
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(fps)