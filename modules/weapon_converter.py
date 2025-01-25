from modules.weapon_item import WeaponItem
from modules.weapon_in_hand import ShotgunInHand, UziInHand, KnifeInHand


def convert_to_hand(weapon):
    if weapon.type == 'shotgun':
        return ShotgunInHand(weapon.ammo)
    if weapon.type == 'uzi':
        return UziInHand(weapon.ammo)
    if weapon.type == 'knife':
        return KnifeInHand()


def convert_to_item(weapon, player_rect):
    if weapon.type != 'knife':
        return WeaponItem(weapon.type, player_rect.x, player_rect.y,
                          weapon.ammo)
    else:
        return WeaponItem(weapon.type, player_rect.x, player_rect.y)
