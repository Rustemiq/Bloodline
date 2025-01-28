import pygame
from modules.load_image import load_image

tile_images = {
        'wall': load_image('wall.png'),
        'empty': load_image('floor.png'),
}
tile_size = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)