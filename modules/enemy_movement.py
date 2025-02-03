import pygame.transform
import math

from modules.rotate_on_pivot import rotate_on_pivot

tile_size = 50
enemy_center = 24, 25
neighbours = [
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]
rotations = {
    (1, 0): 0,
    (0, 1): -90,
    (0, -1): 90,
    (-1, 0): 180,
    (1, 1): -45,
    (-1, 1): -135,
    (1, -1): 45,
    (-1, -1): 135,
    (0, 0): -90,
}


class EnemyMovement:
    def __init__(self, pos, walk_around_pattern):
        self.start_pos = pos
        self.curr_pos = pos
        # будем измерять позицию в клеточках
        self.build_walk_around_path(walk_around_pattern)
        self.walk_around_iteration = 0
        self.run_to_player_iteration = 0
        self.distance = tile_size
        self.speed = 3
        self.aiming_timer = None

    def is_neighbour_availability(self, x, y, neighbour_offset, alg_map):
        n_x, n_y = x + neighbour_offset[0], y + neighbour_offset[1]
        if len(alg_map[0]) > n_x >= 0 and len(alg_map) > n_y >= 0:
            n_cell = alg_map[n_y][n_x]
            if neighbour_offset[0] != 0 and neighbour_offset[1] != 0:
                if not self.is_neighbour_availability(
                    x, y, (neighbour_offset[0], 0), alg_map
                ):
                    return False
                if not self.is_neighbour_availability(
                    x, y, (0, neighbour_offset[1]), alg_map
                ):
                    return False
            return n_cell != "#"
        return False

    def fill_neighbours(self, x, y, alg_map, deep):
        for neighbour in neighbours:
            if self.is_neighbour_availability(x, y, neighbour, alg_map):
                if (
                    type(alg_map[y + neighbour[1]][x + neighbour[0]])
                    is not int
                ):
                    alg_map[y + neighbour[1]][x + neighbour[0]] = deep + 1

    def fill_map(self, alg_map, deep, x_to, y_to):
        if type(alg_map[y_to][x_to]) is int:
            return alg_map
        neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for y in range(len(alg_map)):
            for x in range(len(alg_map[0])):
                cell = alg_map[y][x]
                if cell == deep:
                    self.fill_neighbours(x, y, alg_map, deep)
        return self.fill_map(alg_map, deep + 1, x_to, y_to)

    def restore_route(self, filled_map, x_from, y_from, x_to, y_to, route):
        curr_x, curr_y = x_to, y_to
        if (curr_x, curr_y) == (x_from, y_from):
            return route
        directions = {}
        for neighbour in neighbours:
            if self.is_neighbour_availability(
                curr_x, curr_y, neighbour, filled_map
            ):
                dist = filled_map[curr_y + neighbour[1]][curr_x + neighbour[0]]
                if type(dist) is int:
                    directions[dist] = neighbour
        direction = directions[min(directions.keys())]
        route.insert(0, (-direction[0], -direction[1]))
        curr_x += direction[0]
        curr_y += direction[1]
        return self.restore_route(
            filled_map, x_from, y_from, curr_x, curr_y, route
        )

    def build_route(self, x_to, y_to, level_map):
        algorithm_map = [list(row) for row in level_map]
        algorithm_map[self.curr_pos[1]][self.curr_pos[0]] = 0
        filled_map = self.fill_map(algorithm_map, 0, x_to, y_to)
        return self.restore_route(filled_map, *self.curr_pos, x_to, y_to, [])

    def build_walk_around_path(self, pattern):
        self.walk_around_path = []
        right_path = [(1, 0)] * abs(pattern[0])
        left_path = [(-1, 0)] * abs(pattern[0])
        up_path = [(0, -1)] * abs(pattern[1])
        down_path = [(0, 1)] * abs(pattern[1])
        if pattern[0] >= 0 and pattern[1] >= 0:
            self.walk_around_path = (
                right_path + down_path + left_path + up_path
            )
        if pattern[0] <= 0 and pattern[1] >= 0:
            self.walk_around_path = (
                left_path + down_path + right_path + up_path
            )
        if pattern[0] >= 0 and pattern[1] <= 0:
            self.walk_around_path = (
                right_path + up_path + left_path + down_path
            )
        if pattern[0] <= 0 and pattern[1] <= 0:
            self.walk_around_path = (
                left_path + up_path + right_path + down_path
            )

    def rotate(self, direction):
        self.image = pygame.transform.rotate(self.sample_image, direction)
        self.image_offset = rotate_on_pivot(
            enemy_center, 90 - direction, self.image, self.sample_image
        )

    def go_to_neighbour_tile(self, offset):
        self.direction = rotations[offset]
        self.rotate(self.direction)
        self.walk_direction = offset
        self.distance = tile_size

    def walk_around(self):
        if len(self.walk_around_path) > 0:
            if self.walk_around_iteration == len(self.walk_around_path):
                self.walk_around_iteration = 0
            offset = self.walk_around_path[self.walk_around_iteration]
            self.walk_around_iteration += 1
            self.go_to_neighbour_tile(offset)
        else:
            self.walk_direction = 0, 0
            self.rotate(rotations[self.walk_direction])

    def run_to_player(self, route_to_player):
        if route_to_player == []:
            return
        offset = route_to_player[self.run_to_player_iteration]
        self.run_to_player_iteration += 1
        self.go_to_neighbour_tile(offset)

    def shoot_to_player(self, rect, player_rect, weapon, aiming_timer, sound):
        x_rel = player_rect.centerx - rect.centerx
        y_rel = player_rect.centery - rect.centery
        self.direction = 180 / math.pi * -math.atan2(y_rel, x_rel)
        self.rotate(self.direction)
        if aiming_timer <= 0:
            weapon.shoot(rect.centerx, rect.centery, 90 - self.direction)
            weapon.charge()

    def use_knife(self, player, weapon):
        if player.weapon == "empty" or player.weapon.type != "knife":
            if player.hit_animation.curr_frame == 0:
                if player.is_alive:
                    weapon.use()

    def look_around(self, look_around_timer):
        if 110 >= look_around_timer >= 90 or look_around_timer < 10:
            self.direction -= 4
        elif 20 <= look_around_timer <= 40:
            self.direction += 4
        self.rotate(self.direction)

    def move(self, state, rect, route_to_player):
        if self.distance <= 0:
            if state == "walk_around":
                self.walk_around()
            elif state == "run_to_player":
                self.run_to_player(route_to_player)
        if self.distance != 0:
            self.distance -= self.speed
            rect.x += self.walk_direction[0] * self.speed
            rect.y += self.walk_direction[1] * self.speed
            if self.distance <= 0:
                rect.x += self.walk_direction[0] * self.distance
                rect.y += self.walk_direction[1] * self.distance
                self.curr_pos[0] += self.walk_direction[0]
                self.curr_pos[1] += self.walk_direction[1]
