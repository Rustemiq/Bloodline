import pygame
import os

from modules.camera import Camera
from modules.tile import Tile
from modules.player import Player
from modules.weapon_item import WeaponItem

tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
weapons_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()


def add_sprite(sprite, *groups):
    for group in groups:
        group.add(sprite)
    return sprite


def generate_level(name):
    tile_size = 50
    fullname = os.path.join('levels', name)
    with open(fullname) as map_file:
        level_map = [line.strip() for line in map_file]
    player = None
    for y in range(len(level_map)):
        for x in range(len(level_map[0]) - 1):
            cell = level_map[y][x]
            if cell == '#':
                add_sprite(Tile('wall', x, y),
                           all_sprites, walls_group, tiles_group)
            else:
                add_sprite(Tile('empty', x, y), all_sprites, tiles_group)
                if cell == '@':
                    player = add_sprite(Player('empty', x, y), all_sprites)
                    player.add_inter_groups(walls_group, weapons_group)
                elif cell != '.':
                    #для клеток с оружием
                    if cell == 'S':
                        weapon = WeaponItem('shotgun', x * tile_size, y * tile_size)
                    if cell == 'U':
                        weapon = WeaponItem('uzi', x * tile_size, y * tile_size)
                    if cell == 'K':
                        weapon = WeaponItem('knife', x * tile_size, y * tile_size)
                    add_sprite(weapon, all_sprites, weapons_group)
                    weapon.add_inter_groups(walls_group)
    return player


def weapon_interaction():
    throwed_weapon = player.weapon_interaction()
    if throwed_weapon is not None:
        add_sprite(throwed_weapon, all_sprites, weapons_group)
        throwed_weapon.add_inter_groups(walls_group)


def shoot():
    if pygame.mouse.get_pressed(3)[0]:
        if player.weapon != 'empty' and player.weapon.type != 'knife':
            bullets = player.weapon.shoot(player.direction)
            if bullets is not None:
                for bullet in bullets:
                    add_sprite(bullet, all_sprites, bullets_group)
                    bullet.add_inter_groups(walls_group)


def recharge():
    if player.weapon != 'empty' and player.weapon.type != 'knife':
        player.weapon.charge()


def update_all():
    camera.update(player)
    camera.apply()
    weapons_group.update()
    bullets_group.update()


def draw_all(screen):
    tiles_group.draw(screen)
    weapons_group.draw(screen)
    player.draw(screen, font)
    bullets_group.draw(screen)


WIDTH, HEIGHT = 900, 600
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
    camera = Camera(all_sprites)
    while running:
        screen.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                player.turn_to_mouse(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    weapon_interaction()
        shoot()
        recharge()
        player.get_move(pygame.key.get_pressed())
        update_all()
        draw_all(screen)
        pygame.display.flip()
        clock.tick(fps)
