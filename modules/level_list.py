from modules.level import Level, FinalLevel
from modules.weapon_in_hand import ShotgunInHand, UziInHand, KnifeInHand


enemies1 = [(ShotgunInHand(target='player'), [9, 4], (6, 3)),
            (UziInHand(target='player'), [4, 8], (3, 3)),
            (KnifeInHand(), [12, 9], (7, 0))]
enemies2 = [(ShotgunInHand(target='player'), [12, 5], (1, 1))]
paper_notes1 = [((3, 6), ['пример', 'подсказок', 'пример', 'подсказок'])]
level1 = Level('map1.txt', enemies1, paper_notes1)
level2 = Level('map2.txt', enemies2)
final_level = FinalLevel('final_map.txt', (5, 4))
level_list = [level1, level2, final_level]