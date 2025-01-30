from copy import copy

from modules.level_list import level_list


class LevelIterator:
    def __init__(self):
        self.lvl_index = -1
        self.player_weapon = None
        self.boss = None
        self.is_last_level = False

    def restart(self):
        self.lvl_index -= 1
        return self.__next__()

    def add_inter_groups(self, all_sprites, weapons_group, walls_group,
                                    tiles_group, enemies_group,
                                    dead_enemies_group, bullets_group,
                                    player_group, trigger_tile_group,
                                    paper_notes_group, boss_group):
        self.all_sprites = all_sprites
        self.weapons_group = weapons_group
        self.walls_group = walls_group
        self.tiles_group = tiles_group
        self.enemies_group = enemies_group
        self.dead_enemies_group = dead_enemies_group
        self.bullets_group = bullets_group
        self.player_group = player_group
        self.trigger_tile_group = trigger_tile_group
        self.paper_notes_group = paper_notes_group
        self.boss_group = boss_group


    def __next__(self, player=None, *groups):
        self.lvl_index += 1
        if player is not None:
            self.player_weapon = copy(player.weapon)
        level = level_list[self.lvl_index]
        player = level.load_sprites(self.all_sprites, self.weapons_group,
                                    self.walls_group, self.tiles_group,
                                    self.enemies_group, self.dead_enemies_group,
                                    self.bullets_group, self.player_group,
                                    self.trigger_tile_group,
                                    self.paper_notes_group)
        if self.player_weapon is not None:
            player.set_weapon(self.player_weapon)
        if self.lvl_index == len(level_list) - 1 and self.boss is None:
            self.boss = level.load_boss(self.boss_group, self.all_sprites)
            self.boss.add_inter_groups(self.bullets_group, self.walls_group,
                                       self.player_group,
                                       self.all_sprites)
            self.is_last_level = True
        return player, self.boss
