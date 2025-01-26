import pygame.transform

from modules.rotate_on_pivot import rotate_on_pivot

tile_size = 50
enemy_center = 24, 25


class EnemyMovement:
    def __init__(self, pos, walk_around_pattern):
        self.start_pos = pos
        self.curr_pos = pos
        # будем измерять позицию в клеточках
        self.build_walk_around_path(walk_around_pattern)
        self.walk_around_iteration = 0
        self.distance = 0
        self.speed = 3
        self.aggressive = False

    def build_walk_around_path(self, pattern):
        self.walk_around_path = []
        right_path = [(1, 0)] * abs(pattern[0])
        left_path = [(-1, 0)] * abs(pattern[0])
        up_path = [(0, -1)] * abs(pattern[1])
        down_path = [(0, 1)] * abs(pattern[1])
        if pattern[0] > 0 and pattern[0] > 0:
            self.walk_around_path = right_path + down_path + left_path + up_path
        if pattern[0] < 0 and pattern[0] > 0:
            self.walk_around_path = left_path + down_path + right_path + up_path
        if pattern[0] > 0 and pattern[0] < 0:
            self.walk_around_path = right_path + up_path + left_path + down_path
        if pattern[0] < 0 and pattern[0] < 0:
            self.walk_around_path = left_path + up_path + right_path + down_path

    def rotate(self, direction):
        self.image = pygame.transform.rotate(self.sample_image, direction)
        self.image_offset = rotate_on_pivot(enemy_center, 90 - direction,
                                            self.image, self.sample_image)

    def go_to_neigbour_tile(self, offset):
        if offset == (1, 0):
            self.rotate(0)
        if offset == (0, 1):
            self.rotate(-90)
        if offset == (-1, 0):
            self.rotate(180)
        if offset == (0, -1):
            self.rotate(90)
        self.walk_direction = offset
        self.distance = tile_size

    def walk_around(self):
        if self.walk_around_iteration == len(self.walk_around_path):
            self.walk_around_iteration = 0
        offset = self.walk_around_path[self.walk_around_iteration]
        self.walk_around_iteration += 1
        self.go_to_neigbour_tile(offset)

    def move(self):
        if self.distance <= 0:
            if not self.aggressive:
                self.walk_around()
            self.curr_pos[0] += self.walk_direction[0]
            self.curr_pos[1] += self.walk_direction[1]
        if self.distance != 0:
            self.distance -= self.speed
            self.rect.x += self.walk_direction[0] * self.speed
            self.rect.y += self.walk_direction[1] * self.speed
            if self.distance < 0:
                self.rect.x += self.walk_direction[0] * self.distance
                self.rect.y += self.walk_direction[1] * self.distance


