import sys
import pygame
from modules.camera import Camera
from modules.load_image import load_image
from modules.level_iterator import LevelIterator
from modules.sound import Sound
from modules.score import Score


WIDTH, HEIGHT = 900, 600


class Game:
    def __init__(self):
        self.tiles_group = pygame.sprite.Group()
        self.walls_group = pygame.sprite.Group()
        self.weapons_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.dead_enemies_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.boss_group = pygame.sprite.Group()
        self.trigger_tile_group = pygame.sprite.Group()
        self.paper_notes_group = pygame.sprite.Group()
        self.player = None
        self.boss = None

    def shoot(self):
        if pygame.mouse.get_pressed(3)[0]:
            if (
                self.player.weapon != "empty"
                and self.player.weapon.type != "knife"
            ):
                if self.player.weapon.ammo > 0:
                    self.player.weapon.shoot(
                        self.player.rect.centerx,
                        self.player.rect.centery,
                        self.player.direction,
                    )
                    for enemy in self.enemies_group:
                        enemy.player_shoots()

    def use_knife(self):
        if (
            self.player.weapon != "empty"
            and self.player.weapon.type == "knife"
        ):
            self.player.weapon.use()

    def use_fists(self):
        if pygame.mouse.get_pressed(3)[0]:
            if self.player.weapon == "empty":
                self.player.use_fists()

    def recharge(self):
        if (
            self.player.weapon != "empty"
            and self.player.weapon.type != "knife"
        ):
            self.player.weapon.charge()

    def draw_information(self):
        if (
            self.player.weapon != "empty"
            and self.player.weapon.type != "knife"
        ):
            string = "Ammo: " + str(self.player.weapon.ammo)
            text = self.font1.render(string, True, (220, 20, 60))
            text_y = HEIGHT - text.get_height()
            self.screen.blit(text, (0, text_y))
        if not self.lvl_iterator.is_last_level:
            if not self.player.is_alive:
                string = "PRESS R TO RESTART"
                offset = 50
                text = self.font1.render(string, True, (220, 20, 60))
                text_y = HEIGHT - text.get_height() - offset
                self.screen.blit(text, (0, text_y))
            elif self.is_level_cleared():
                string = "PRESS SPACE TO NEXT LEVEL"
                offset = 40
                text = self.font2.render(string, True, (220, 20, 60))
                text_y = HEIGHT - text.get_height() - offset
                self.screen.blit(text, (0, text_y))
        self.score.draw_information(
            self.screen, self.font1, self.font2, self.font3
        )

    def is_level_cleared(self):
        return len(self.enemies_group) == 0 and self.player.is_alive

    def end_screen(self):
        alpha = 0
        curr_image = pygame.Surface((WIDTH, HEIGHT))
        curr_image.fill("black")
        curr_image.set_alpha(alpha)
        timer = 0
        alpha_change_step = 5
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if alpha <= 255:
                alpha += alpha_change_step
                curr_image.set_alpha(alpha)
            else:
                timer += 1
            if timer >= 60:
                curr_image = load_image("end_screen.png")
            self.draw_all()
            self.screen.blit(curr_image, (0, 0))
            if timer >= 120:
                self.score.draw_final_result(self.screen, self.font1)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def end_scene(self):
        self.boss.is_scene_started = True
        timer = 0
        while True:
            self.screen.fill("gray")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    if self.player.is_alive:
                        self.player.turn_to_mouse(event.pos)
            if timer == self.fps and self.boss.is_alive:
                self.boss.shoot()
            if not self.boss.is_alive and timer < self.fps:
                timer = self.fps
            if timer == self.fps * 3:
                self.end_screen()
            elif self.player.is_alive:
                self.shoot()
                self.recharge()
            self.update_all()
            self.draw_all()
            pygame.display.flip()
            self.clock.tick(self.fps)
            timer += 1

    def read_notes(self):
        for paper_note in self.paper_notes_group:
            if pygame.sprite.collide_rect(self.player, paper_note):
                paper_note.read(self.screen)

    def update_all(self):
        self.weapons_group.update()
        self.bullets_group.update()
        self.enemies_group.update()
        self.boss_group.update()
        self.paper_notes_group.update()
        self.player.update()
        self.score.update_combo_counter()
        self.camera.update(self.player)
        self.camera.apply()

    def draw_all(self):
        self.tiles_group.draw(self.screen)
        self.paper_notes_group.draw(self.screen)
        self.dead_enemies_group.draw(self.screen)
        self.weapons_group.draw(self.screen)
        for enemy in self.enemies_group:
            enemy.draw(self.screen)
        self.boss_group.draw(self.screen)
        self.player.draw(self.screen)
        self.bullets_group.draw(self.screen)
        self.draw_information()
        for paper_note in self.paper_notes_group:
            paper_note.show_text(self.screen, self.font2)
        self.sound.draw_icons(self.screen)

    def process_player_alive_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.player.turn_to_mouse(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.player.weapon_interaction()
            elif event.button == 1:
                self.sound.interaction(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if (
                    self.is_level_cleared()
                    and not self.lvl_iterator.is_last_level
                ):
                    self.player, self.boss, self.score = (
                        self.lvl_iterator.__next__(self.player)
                    )
                    # обновим камеру, чтобы игрок повернулся в правильную
                    # сторону
                    self.camera.update(self.player)
                    self.camera.apply()
                    self.player.turn_to_mouse(pygame.mouse.get_pos())
            if event.key == pygame.K_e:
                self.read_notes()
        if not pygame.mouse.get_pressed(3)[0] and self.sound.is_icon_clicked:
            self.sound.is_icon_clicked = False

    def process_player_dead_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.player, self.boss, self.score = (
                    self.lvl_iterator.restart()
                )

    def process_special_actions(self):
        if self.player.is_trigger_touched():
            self.end_scene()
            self.running = False
        if self.lvl_iterator.is_last_level:
            self.sound.fade_music()

    def player_control(self):
        if self.player.is_alive:
            self.use_knife()
            self.recharge()
            self.player.get_move(pygame.key.get_pressed())
            if not self.sound.is_icon_clicked:
                if self.player.is_alive:
                    self.use_fists()
                    self.shoot()

    def setup_game(self):
        pygame.init()
        pygame.display.set_caption("Bloodline")
        size = WIDTH, HEIGHT
        self.running = True
        self.screen = pygame.display.set_mode(size)
        self.font1 = pygame.font.Font(None, 50)
        self.font2 = pygame.font.Font(None, 35)
        self.font3 = pygame.font.Font(None, 70)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.sound = Sound(pygame.mixer)
        self.score = Score()
        self.lvl_iterator = LevelIterator()
        self.lvl_iterator.add_internal_objects(
            self.all_sprites,
            self.weapons_group,
            self.walls_group,
            self.tiles_group,
            self.enemies_group,
            self.dead_enemies_group,
            self.bullets_group,
            self.player_group,
            self.trigger_tile_group,
            self.paper_notes_group,
            self.boss_group,
            self.sound,
            self.score,
        )
        self.player, self.boss, self.score = self.lvl_iterator.__next__(
            self.player
        )
        self.camera = Camera(self.all_sprites)

    def game_cycle(self):
        while self.running:
            self.screen.fill("gray")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.player.is_alive:
                    self.process_player_alive_event(event)
                else:
                    self.process_player_dead_event(event)
            self.player_control()
            self.process_special_actions()
            self.update_all()
            self.draw_all()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def run(self):
        self.setup_game()
        self.game_cycle()
