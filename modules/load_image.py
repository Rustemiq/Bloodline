import pygame
import os


def load_image(name):
    fullname = os.path.join('pictures', name)
    image = pygame.image.load(fullname)
    return image