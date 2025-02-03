import pygame

from modules.load_image import load_image

tile_size = 50
WIDTH, HEIGHT = 900, 600


class PaperNote(pygame.sprite.Sprite):
    def __init__(self, pos, text, *groups):
        super().__init__(*groups)
        self.image = self.default_image = load_image("paper_note.png")
        self.with_hint_image = load_image("paper_note_with_hint.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(
            pos[0] * tile_size + (tile_size - self.rect.w) // 2,
            pos[1] * tile_size + (tile_size - self.rect.h) // 2,
        )
        self.text = text
        self.is_player_reading = False

    def add_inter_groups(self, player):
        self.player = player

    def read(self, screen):
        self.is_player_reading = True

    def show_text(self, screen, font):
        if self.is_player_reading:
            window_height = 100
            pygame.draw.rect(
                screen,
                (250, 243, 237),
                (400, HEIGHT - window_height - 10, WIDTH - 410, window_height),
            )
            text_y = HEIGHT - 100
            text_x = 410
            for line in self.text:
                text = font.render(line, True, (0, 0, 0))
                screen.blit(text, (text_x, text_y))
                text_y += 20

    def update(self):
        if (
            pygame.sprite.collide_rect(self, self.player)
            and self.player.is_alive
        ):
            self.image = self.with_hint_image
        else:
            self.image = self.default_image
            self.is_player_reading = False
