import pygame
from math import floor

from modules.load_image import load_image


class Animation:
    def __init__(self, sheet_name, columns, rows, animation_speed, cyclically):
        sheet = load_image(sheet_name)
        self.frames = self.cut_sheet(sheet, columns, rows)
        self.curr_frame = 0
        self.animation_speed = animation_speed
        self.cyclically = cyclically
        self.is_end = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        return frames

    def reset(self):
        self.is_end = False
        self.curr_frame = 0

    def animate(self):
        if floor(self.curr_frame + self.animation_speed) < len(self.frames):
            self.curr_frame += self.animation_speed
        elif self.cyclically:
            self.is_end = True
            return self.frames[0]
        return self.frames[floor(self.curr_frame)]