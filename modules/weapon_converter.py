from modules.weapon_item import WeaponItem
from modules.weapon_in_hand import ShotgunInHand, UziInHand, KnifeInHand


def convert_to_hand(weapon, bullets_group, walls_group, targets_group, sound,
                    player, all_sprites):
    if weapon.type == 'shotgun':
        weapon = ShotgunInHand(weapon.ammo)
        weapon.add_inter_groups(bullets_group, walls_group, targets_group,
                                sound, all_sprites)
    if weapon.type == 'uzi':
        weapon = UziInHand(weapon.ammo)
        weapon.add_inter_groups(bullets_group, walls_group, targets_group,
                                sound, all_sprites)
    if weapon.type == 'knife':
        weapon = KnifeInHand()
        weapon.add_inter_groups(targets_group, sound, player)
    return weapon


def convert_to_item(weapon, rect, weapons_group, all_sprites):
    if weapon.type != 'knife':
        return WeaponItem(weapon.type, rect.x, rect.y,
                          weapons_group, all_sprites, ammo=weapon.ammo)
    else:
        return WeaponItem(weapon.type, rect.x, rect.y,
                          weapons_group, all_sprites)