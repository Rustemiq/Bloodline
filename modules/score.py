from copy import deepcopy
import pygame

combo_hold_time = 240
death_points = -1000
level_timings = [13, 9, 14, 22, 22, 24, 44]
rank_table = {
    100000: 'F-',
    150000: 'F',
    200000: 'E-',
    250000: 'E',
    300000: 'E+',
    350000: 'D-',
    400000: 'D',
    450000: 'D+',
    400000: 'C-',
    450000: 'C',
    500000: 'C+',
    550000: 'B-',
    600000: 'B',
    650000: 'B+',
    800000: 'A',
    900000: 'A+',
    1000000: 'S',
    'S+': 'S+'
}
WIDTH = 900


class Score:
    def __init__(self):
        self.score = 0
        self.combo_counter = 0
        self.combo_timer = 0
        self.is_frozen = False
        self.scoring_message = None
        self.message_timer = 0
        self.level_start_tick = 0

    def draw_information(self, screen, font1, font2, font3):
        if self.combo_counter > 1:
            string = 'X' + str(self.combo_counter)
            text = font3.render(string, True, (220, 20, 60))
            text.set_alpha(self.combo_timer * 2)
            text_y = 40
            text_x = 10
            screen.blit(text, (text_x, text_y))
        string = str(self.score) + 'PTS'
        text = font1.render(string, True, (220, 20, 60))
        text_y = 10
        text_x = 10
        screen.blit(text, (text_x, text_y))
        if self.scoring_message is not None:
            self.message_timer -= 1
            text = font2.render(self.scoring_message, True, (220, 20, 60))
            text.set_alpha(self.message_timer * 5)
            text_y = 80
            text_x = 10
            screen.blit(text, (text_x, text_y))
            if self.message_timer <= 0:
                self.scoring_message = None

    def draw_final_result(self, screen, font):
        string = str(self.score) + 'PTS'
        text = font.render(string, True, (136, 0, 21))
        text_x = (WIDTH - text.get_rect().w) // 2
        text_y = 460
        screen.blit(text, (text_x, text_y))
        for points in rank_table.keys():
            if points == 'S+' or self.score < points:
                rank = rank_table[points]
                break
        string = 'GRADE ' + rank
        text = font.render(string, True, (136, 0, 21))
        text_x = (WIDTH - text.get_rect().w) // 2
        text_y = 490
        screen.blit(text, (text_x, text_y))


    def freeze(self):
        self.is_frozen = True
        self.combo_timer = 240

    def register_kill(self):
        self.combo_timer = combo_hold_time
        self.combo_counter += 1
        self.is_frozen = False

    def remember_score(self):
        self.level_start_tick = pygame.time.get_ticks()
        self.remembered_score = deepcopy(self)

    def register_time_bonus(self, lvl_index):
        at_level_time = (pygame.time.get_ticks() - self.level_start_tick) / 1000
        time_bonus = round((level_timings[lvl_index - 1    ] - at_level_time) * 1000)
        if time_bonus > 0:
            self.score += time_bonus
            self.scoring_message = 'TIME BONUS ' + str(time_bonus)
            self.message_timer = 60

    def reset(self):
        return self.remembered_score

    def register_combo(self):
        if self.combo_counter != 0:
            self.score += self.combo_counter * (self.combo_counter + 1) * 250
            self.combo_counter = 0
            self.combo_timer = combo_hold_time
            self.scoring_message = 'COMBO'
            self.message_timer = 60

    def register_death(self):
        self.score += death_points
        self.scoring_message = 'DEATH ' + str(death_points)
        self.message_timer = 60

    def update_combo_counter(self):
        if not self.is_frozen:
            if self.combo_timer >= 0:
                self.combo_timer -= 1
            else:
                self.register_combo()
