import os

from modules.player import Player
from modules.weapon_item import WeaponItem
from modules.tile import Tile
from modules.enemy import Enemy
from modules.boss import Boss
from modules.paper_note import PaperNote


tile_size = 50


class Level:
    def __init__(self, map_name, enemies=None, paper_notes=None):
        self.map_name = map_name
        self.enemies = enemies
        self.paper_notes = paper_notes

    def load_sprites(
        self,
        all_sprites,
        weapons_group,
        walls_group,
        tiles_group,
        enemies_group,
        dead_enemies_group,
        bullets_group,
        player_group,
        trigger_tile_group,
        paper_notes_group,
        sound,
    ):
        for sprite in all_sprites:
            sprite.kill()
        fullname = os.path.join("maps", self.map_name)
        with open(fullname) as map_file:
            level_map = [line.strip() for line in map_file]
        player = None
        for y in range(len(level_map)):
            for x in range(len(level_map[0])):
                cell = level_map[y][x]
                if cell == "#":
                    Tile("wall", x, y, tiles_group, walls_group, all_sprites)
                else:
                    if cell != "T":
                        Tile("empty", x, y, tiles_group, all_sprites)
                    else:
                        Tile(
                            "empty",
                            x,
                            y,
                            tiles_group,
                            trigger_tile_group,
                            all_sprites,
                        )
                    if cell == "@":
                        player = Player(
                            "empty", x, y, player_group, all_sprites
                        )
                        player.add_internal_objects(
                            walls_group,
                            weapons_group,
                            enemies_group,
                            bullets_group,
                            trigger_tile_group,
                            all_sprites,
                            sound,
                        )
                    elif cell != "." and cell != "T":
                        # для клеток с оружием
                        if cell == "S":
                            weapon = WeaponItem(
                                "shotgun",
                                x * tile_size,
                                y * tile_size,
                                weapons_group,
                                all_sprites,
                            )
                        if cell == "U":
                            weapon = WeaponItem(
                                "uzi",
                                x * tile_size,
                                y * tile_size,
                                weapons_group,
                                all_sprites,
                            )
                        if cell == "K":
                            weapon = WeaponItem(
                                "knife",
                                x * tile_size,
                                y * tile_size,
                                weapons_group,
                                all_sprites,
                            )
                        weapon.add_internal_objects(walls_group, enemies_group)
        if self.enemies is not None:
            for enemy_data in self.enemies:
                enemy = Enemy(*enemy_data, enemies_group, all_sprites)
                if enemy.weapon.type != "knife":
                    enemy.weapon.add_internal_objects(
                        bullets_group,
                        walls_group,
                        player_group,
                        sound,
                        all_sprites,
                    )
                else:
                    enemy.weapon.add_internal_objects(player_group, sound, enemy)
                enemy.add_internal_objects(
                    dead_enemies_group,
                    walls_group,
                    player_group,
                    weapons_group,
                    player,
                    all_sprites,
                    sound,
                )
                enemy.level_map = level_map
        if self.paper_notes is not None:
            for paper_note_data in self.paper_notes:
                paper_note = PaperNote(
                    *paper_note_data, paper_notes_group, all_sprites
                )
                paper_note.add_internal_objects(player)
        return player


class FinalLevel(Level):
    def __init__(self, map_name, boss_pos):
        super().__init__(map_name)
        self.boss_pos = boss_pos[0] * tile_size, boss_pos[1] * tile_size
        self.enemies = []

    def load_boss(self, boss_group, all_sprites):
        boss = Boss(*self.boss_pos, boss_group, all_sprites)
        return boss




