import pygame
import os

from modules.camera import Camera
from modules.level import level_list

tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
weapons_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


def add_sprite(sprite, *groups):
    for group in groups:
        group.add(sprite)
    return sprite


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


class LevelIterator:
    def __init__(self):
        self.lvl_index = -1

    def __next__(self):
        self.lvl_index += 1
        if self.lvl_index == len(level_list):
            pass #окончание игры
        level = level_list[self.lvl_index]
        player = level.load_sprites(all_sprites, weapons_group,
                                 walls_group, tiles_group, enemies_group)
        return player


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
    lvl_iterator = LevelIterator()
    player = lvl_iterator.__next__()
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
