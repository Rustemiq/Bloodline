import os
from modules.player import Player
from modules.weapon_item import WeaponItem
from modules.tile import Tile


tile_size = 50


def add_sprite(sprite, *groups):
    for group in groups:
        group.add(sprite)
    return sprite


class Level:
    def __init__(self, map_name, *enemies):
        self.map_name = map_name
        self.enemies = enemies

    def load_sprites(self, all_sprites, weapons_group,
                     walls_group, tiles_group, enemies_group):
        for sprite in all_sprites:
            sprite.kill()
        fullname = os.path.join('maps', self.map_name)
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
                        # для клеток с оружием
                        if cell == 'S':
                            weapon = WeaponItem('shotgun', x * tile_size,
                                                y * tile_size)
                        if cell == 'U':
                            weapon = WeaponItem('uzi', x * tile_size,
                                                y * tile_size)
                        if cell == 'K':
                            weapon = WeaponItem('knife', x * tile_size,
                                                y * tile_size)
                        add_sprite(weapon, all_sprites, weapons_group)
                        weapon.add_inter_groups(walls_group)
        return player


level1 = Level('map1.txt')
level2 = Level('map2.txt')
level_list = [level1, level2]



