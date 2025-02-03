from modules.level import Level, FinalLevel
from modules.weapon_in_hand import ShotgunInHand, UziInHand, KnifeInHand


enemies1 = [(ShotgunInHand(target='player'), [8, 3], (2, 2)),
            (KnifeInHand(target='player'), [15, 2], (3, 0)),
            (KnifeInHand(target='player'), [16, 3], (2, 0)),
            (ShotgunInHand(target='player'), [15, 4], (2, 0)),
            (ShotgunInHand(target='player'), [20, 5], (3, 3))
            ]

enemies2 = [(UziInHand(target='player'), [2, 2], (1, 1)),
            (ShotgunInHand(target='player'), [4, 2], (3, 1)),
            (KnifeInHand(target='player'), [2, 5], (3, 0)),
            (KnifeInHand(target='player'), [5, 5], (2, 0))
            ]

enemies3 = [(UziInHand(target='player'), [4, 6], (0, 0)),
            (ShotgunInHand(target='player'), [7, 3], (0, 0)),
            (KnifeInHand(target='player'), [8, 1], (7, 0)),
            (ShotgunInHand(target='player'), [15, 2], (0, 2)),
            (UziInHand(target='player'), [9, 3], (3, 0)),
            (UziInHand(target='player'), [13, 7], (0, 0))
            ]

enemies4 = [(ShotgunInHand(target='player'), [6, 7], (3, 2)),
            (KnifeInHand(target='player'), [5, 10], (2, 0)),
            (KnifeInHand(target='player'), [10, 10], (-2, 0)),
            (UziInHand(target='player'), [12, 7], (0, -2)),
            (ShotgunInHand(target='player'), [16, 7], (0, 0)),
            (UziInHand(target='player'), [12, 1], (1, 2)),
            (KnifeInHand(target='player'), [9, 2], (0, 0)),
            (UziInHand(target='player'), [21, 1], (2, 9)),
            (UziInHand(target='player'), [23, 10], (-2, -9))
            ]

enemies5 = [(ShotgunInHand(target='player'), [8, 3], (0, 0)),
            (UziInHand(target='player'), [1, 1], (3, 0)),
            (ShotgunInHand(target='player'), [2, 3], (0, 0)),
            (KnifeInHand(target='player'), [11, 9], (5, 0)),
            (UziInHand(target='player'), [11, 11], (5, 0)),
            (ShotgunInHand(target='player'), [16, 5], (2, 1)),
            (ShotgunInHand(target='player'), [18, 6], (-2, 1)),
            (UziInHand(target='player'), [12, 2], (0, 0)),
            (KnifeInHand(target='player'), [23, 4], (2, 2)),
            (KnifeInHand(target='player'), [22, 4], (2, 2)),
            (ShotgunInHand(target='player'), [23, 10], (0, -2)),
            (ShotgunInHand(target='player'), [25, 10], (0, -2)),
            (KnifeInHand(target='player'), [4, 2], (-3, 0))
            ]

enemies6 = [(UziInHand(target='player'), [4, 10], (0, 0)),
            (ShotgunInHand(target='player'), [1, 11], (0, 3)),
            (KnifeInHand(target='player'), [2, 14], (0, -3)),
            (ShotgunInHand(target='player'), [12, 5], (2, 0)),
            (UziInHand(target='player'), [12, 10], (2, 0)),
            (KnifeInHand(target='player'), [12, 3], (0, 0)),
            (KnifeInHand(target='player'), [14, 3], (0, 0)),
            (KnifeInHand(target='player'), [12, 12], (0, 0)),
            (KnifeInHand(target='player'), [14, 12], (0, 0)),
            (ShotgunInHand(target='player'), [19, 5], (-2, 9)),
            (ShotgunInHand(target='player'), [17, 14], (2, -9)),
            (UziInHand(target='player'), [13, 14], (4, 0)),
            (UziInHand(target='player'), [1, 1], (2, 2))
            ]

enemies7 = [(UziInHand(target='player'), [6, 18], (3, 0)),
            (ShotgunInHand(target='player'), [9, 11], (1, 2)),
            (KnifeInHand(target='player'), [15, 13], (0, 0)),
            (ShotgunInHand(target='player'), [18, 8], (0, 0)),
            (UziInHand(target='player'), [17, 18], (5, 0)),
            (KnifeInHand(target='player'), [22, 16], (-1, -5)),
            (KnifeInHand(target='player'), [21, 11], (1, 5)),
            (ShotgunInHand(target='player'), [8, 9], (-2, 0)),
            (ShotgunInHand(target='player'), [21, 5], (1, 1)),
            (UziInHand(target='player'), [15, 4], (0, 0)),
            (UziInHand(target='player'), [16, 5], (0, 0)),
            (ShotgunInHand(target='player'), [19, 4], (0, 0)),
            (ShotgunInHand(target='player'), [1, 1], (4, 2)),
            (KnifeInHand(target='player'), [2, 2], (2, 0)),
            (UziInHand(target='player'), [6, 1], (0, 2)),
            (UziInHand(target='player'), [1, 5], (2, 2)),
            (ShotgunInHand(target='player'), [3, 8], (-2, 2)),
            (ShotgunInHand(target='player'), [3, 11], (-2, 1)),
            (UziInHand(target='player'), [1, 14], (2, 2))
            ]


paper_notes1 = [((3, 3), ['Нажми ЛКМ для удара.',
                          'Чтобы подобрать оружие - ПКМ']),
                ((10, 7), ['Дробовик эффективен против',
                           'скучковавшихся врагов.',
                          '...и не только.',
                           'ЛКМ для стрельбы'])
                ]

paper_notes2 = [((14, 1), ['УЗИ имеет большой боезапас,',
                          'что поможет убить рассредоточенных',
                          'врагов']),
                ((15, 5), ['Звуки выстрелов',
                           'привлекает врагов.',
                           'Но это можно использовать',
                           'в свою пользу']),
                ]

paper_notes3 = [((17, 4), ['Чтобы метнуть нож или любое',
                          'другое оружие нажмите ПКМ']),
                ((1, 4), ['В тесных комнатах удобно',
                           ' использовать нож. Он даёт ускорение',
                           'и заставляет врагов дольше целиться.',
                          '(для удара - просто коснуться врага)'])
                ]


level1 = Level('map1.txt', enemies1, paper_notes1)
level2 = Level('map2.txt', enemies2, paper_notes2)
level3 = Level('map3.txt', enemies3, paper_notes3)
level4 = Level('map4.txt', enemies4)
level5 = Level('map5.txt', enemies5)
level6 = Level('map6.txt', enemies6)
level7 = Level('map7.txt', enemies7)

final_level = FinalLevel('final_map.txt', (5, 4))
level_list = [
     level1, level2, level3, level4, level5, level6, level7, final_level]