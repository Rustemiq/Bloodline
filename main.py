import sys
import pygame
from modules.camera import Camera
from modules.load_image import load_image
from modules.level_iterator import LevelIterator
from modules.sound import Sound
from modules.score import Score

tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
weapons_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
dead_enemies_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
trigger_tile_group = pygame.sprite.Group()
paper_notes_group = pygame.sprite.Group()
player = None
boss = None


def shoot():
    if pygame.mouse.get_pressed(3)[0]:
        if player.weapon != "empty" and player.weapon.type != "knife":
            if player.weapon.ammo > 0:
                player.weapon.shoot(
                    player.rect.centerx, player.rect.centery, player.direction
                )
                for enemy in enemies_group:
                    enemy.player_shoots()


def use_knife():
    if player.weapon != "empty" and player.weapon.type == "knife":
        player.weapon.use()


def use_fists():
    if player.weapon == "empty":
        player.use_fists()


def recharge():
    if player.weapon != "empty" and player.weapon.type != "knife":
        player.weapon.charge()


def put_to_death_player():
    for enemy in enemies_group:
        enemy.player_died()


def draw_information():
    if player.weapon != "empty" and player.weapon.type != "knife":
        string = "Ammo: " + str(player.weapon.ammo)
        text = font1.render(string, True, (220, 20, 60))
        text_y = HEIGHT - text.get_height()
        screen.blit(text, (0, text_y))
    if not lvl_iterator.is_last_level:
        if not player.is_alive:
            string = "PRESS R TO RESTART"
            text = font1.render(string, True, (220, 20, 60))
            text_y = HEIGHT - text.get_height() - 50
            screen.blit(text, (0, text_y))
        elif is_level_cleared():
            string = "PRESS SPACE TO NEXT LEVEL"
            text = font2.render(string, True, (220, 20, 60))
            text_y = HEIGHT - text.get_height() - 40
            screen.blit(text, (0, text_y))
    score.draw_information(screen, font1, font2, font3)


def is_level_cleared():
    return len(enemies_group) == 0 and player.is_alive


def end_screen():
    alpha = 0
    curr_image = pygame.Surface((WIDTH, HEIGHT))
    curr_image.fill("black")
    curr_image.set_alpha(alpha)
    timer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if alpha <= 255:
            alpha = alpha + 5
            curr_image.set_alpha(alpha)
        else:
            timer += 1
        if timer >= 60:
            curr_image = load_image("end_screen.png")
        draw_all(screen)
        screen.blit(curr_image, (0, 0))
        if timer >= 120:
            score.draw_final_result(screen, font1)
        pygame.display.flip()
        clock.tick(fps)


def end_scene(player, boss):
    boss.is_scene_started = True
    timer = 0
    while True:
        screen.fill("gray")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if player.is_alive:
                    player.turn_to_mouse(event.pos)
        if timer == 60 and boss.is_alive:
            boss.shoot()
        if not boss.is_alive and timer < 60:
            timer = 60
        if timer == 180:
            end_screen()
        elif player.is_alive:
            shoot()
            recharge()
        update_all()
        draw_all(screen)
        pygame.display.flip()
        clock.tick(fps)
        timer += 1


def read_notes(screen):
    for paper_note in paper_notes_group:
        if pygame.sprite.collide_rect(player, paper_note):
            paper_note.read(screen)


def update_all():
    weapons_group.update()
    bullets_group.update()
    enemies_group.update()
    boss_group.update()
    paper_notes_group.update()
    player.update()
    score.update_combo_counter()
    camera.update(player)
    camera.apply()


def draw_all(screen):
    tiles_group.draw(screen)
    paper_notes_group.draw(screen)
    dead_enemies_group.draw(screen)
    weapons_group.draw(screen)
    for enemy in enemies_group:
        enemy.draw(screen)
    boss_group.draw(screen)
    player.draw(screen)
    bullets_group.draw(screen)
    draw_information()
    for paper_note in paper_notes_group:
        paper_note.show_text(screen, font2)
    sound.draw_icons(screen)


WIDTH, HEIGHT = 900, 600
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Bloodline")
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    font1 = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 35)
    font3 = pygame.font.Font(None, 70)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    sound = Sound(pygame.mixer)
    score = Score()
    lvl_iterator = LevelIterator()
    lvl_iterator.add_internal_objects(
        all_sprites,
        weapons_group,
        walls_group,
        tiles_group,
        enemies_group,
        dead_enemies_group,
        bullets_group,
        player_group,
        trigger_tile_group,
        paper_notes_group,
        boss_group,
        sound,
        score,
    )
    player, boss, score = lvl_iterator.__next__(player)
    camera = Camera(all_sprites)
    while running:
        screen.fill("gray")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if player.is_alive:
                    player.turn_to_mouse(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if player.is_alive:
                        player.weapon_interaction()
                elif event.button == 1:
                    sound.interaction(pygame.mouse.get_pos())
                    if not sound.is_icon_clicked:
                        if player.is_alive:
                            use_fists()
            if event.type == pygame.KEYDOWN:
                if player.is_alive:
                    if event.key == pygame.K_SPACE:
                        if (
                            is_level_cleared()
                            and not lvl_iterator.is_last_level
                        ):
                            player, boss, score = lvl_iterator.__next__(player)
                            # обновим камеру, чтобы игрок повернулся в правильную
                            # сторону
                            camera.update(player)
                            camera.apply()
                            player.turn_to_mouse(pygame.mouse.get_pos())
                    if event.key == pygame.K_e:
                        read_notes(screen)
                else:
                    if event.key == pygame.K_r:
                        player, boss, score = lvl_iterator.restart()
        if not player.is_alive:
            put_to_death_player()
        else:
            if not sound.is_icon_clicked:
                shoot()
            if not pygame.mouse.get_pressed(3)[0] and sound.is_icon_clicked:
                sound.is_icon_clicked = False
            use_knife()
            recharge()
            player.get_move(pygame.key.get_pressed())
        if player.is_trigger_touched():
            end_scene(player, boss)
            running = False
        if lvl_iterator.is_last_level:
            sound.fade_music()
        update_all()
        draw_all(screen)
        pygame.display.flip()
        clock.tick(fps)