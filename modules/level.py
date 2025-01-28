import os

from modules.player import Player
from modules.weapon_in_hand import ShotgunInHand, UziInHand, KnifeInHand
from modules.weapon_item import WeaponItem
from modules.tile import Tile
from modules.enemy import Enemy


tile_size = 50


class Level:
    def __init__(self, map_name, *enemies):
        self.map_name = map_name
        self.enemies = enemies

    def load_sprites(self, all_sprites, weapons_group, walls_group, tiles_group,
                     enemies_group, dead_enemies_group, bullets_group,
                     player_group):
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
                    Tile('wall', x, y, tiles_group, walls_group, all_sprites)
                else:
                    Tile('empty', x, y, tiles_group, all_sprites)
                    if cell == '@':
                        player = Player('empty', x, y, player_group,
                                        all_sprites)
                        player.add_inter_groups(walls_group, weapons_group,
                                                enemies_group, bullets_group,
                                                all_sprites)
                    elif cell != '.':
                        # для клеток с оружием
                        if cell == 'S':
                            weapon = WeaponItem('shotgun', x * tile_size,
                                                y * tile_size, weapons_group,
                                                all_sprites)
                        if cell == 'U':
                            weapon = WeaponItem('uzi', x * tile_size,
                                                y * tile_size, weapons_group,
                                                all_sprites)
                        if cell == 'K':
                            weapon = WeaponItem('knife', x * tile_size,
                                                y * tile_size, weapons_group,
                                                all_sprites)
                        weapon.add_inter_groups(walls_group, enemies_group)
        for enemy_data in self.enemies:
            enemy = Enemy(*enemy_data, enemies_group, all_sprites)
            if enemy.weapon.type != 'knife':
                enemy.weapon.add_inter_groups(bullets_group, player_group,
                                              all_sprites)
            enemy.add_inter_groups(dead_enemies_group, walls_group,
                         player_group, player, all_sprites)
            enemy.level_map = level_map
        return player


enemies1 = [(ShotgunInHand(), [9, 4], (6, 3)),
            (UziInHand(), [4, 8], (3, 3)),
            (KnifeInHand(), [12, 9], (7, 0))]
level1 = Level('map1.txt', *enemies1)
level2 = Level('map2.txt')
level_list = [level1, level2]



