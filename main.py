import pygame
from copy import copy

from modules.camera import Camera
from modules.level import level_list

tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
weapons_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
dead_enemies_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None


def weapon_interaction():
    throwed_weapon = player.weapon_interaction()
    if throwed_weapon is not None:
        throwed_weapon.add_inter_groups(walls_group, enemies_group)


def shoot():
    if pygame.mouse.get_pressed(3)[0]:
        if player.weapon != 'empty' and player.weapon.type != 'knife':
            bullets = player.weapon.shoot(player.rect.centerx,
                                          player.rect.centery,
                                          player.direction)
            if bullets is not None:
                for bullet in bullets:
                    bullet.add_inter_groups(walls_group, enemies_group)
            for enemy in enemies_group:
                enemy.player_shoots()


def use_knife():
    if player.weapon != 'empty' and player.weapon.type == 'knife':
        player.use_knife()


def recharge():
    if player.weapon != 'empty' and player.weapon.type != 'knife':
        player.weapon.charge()


def put_to_death_player():
    for enemy in enemies_group:
        enemy.player_died()


def draw_information():
    if player.weapon != 'empty' and player.weapon.type != 'knife':
        string = "Ammo: " + str(player.weapon.ammo)
        text = font1.render(string,
                           True, (220, 20, 60))
        text_y = HEIGHT - text.get_height()
        screen.blit(text, (0, text_y))
    if not player.is_alive:
        string = "PRESS R TO RESTART"
        text = font1.render(string,
                           True, (220, 20, 60))
        text_y = HEIGHT - text.get_height() - 50
        screen.blit(text, (0, text_y))
    if is_level_cleared():
        string = "PRESS SPACE TO NEXT LEVEL"
        text = font2.render(string,
                           True, (220, 20, 60))
        text_y = HEIGHT - text.get_height() - 40
        screen.blit(text, (0, text_y))


def is_level_cleared():
    return len(enemies_group) == 0 and player.is_alive


def update_all():
    weapons_group.update()
    bullets_group.update()
    enemies_group.update()
    camera.update(player)
    camera.apply()


def draw_all(screen):
    tiles_group.draw(screen)
    dead_enemies_group.draw(screen)
    weapons_group.draw(screen)
    for enemy in enemies_group:
        enemy.draw(screen)
    player.draw(screen)
    bullets_group.draw(screen)
    draw_information()


class LevelIterator:
    def __init__(self):
        self.lvl_index = -1
        self.player_weapon = None

    def restart(self):
        self.lvl_index -= 1
        return self.__next__()

    def __next__(self, player=None):
        self.lvl_index += 1
        if self.lvl_index == len(level_list):
            pass #окончание игры
        if player is not None:
            self.player_weapon = copy(player.weapon)
        level = level_list[self.lvl_index]
        player = level.load_sprites(all_sprites, weapons_group, walls_group,
                                tiles_group, enemies_group, dead_enemies_group,
                                bullets_group, player_group)
        if self.player_weapon is not None:
            player.set_weapon(self.player_weapon)
        return player


WIDTH, HEIGHT = 900, 600
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Bloodline')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    font1 = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 35)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    lvl_iterator = LevelIterator()
    player = lvl_iterator.__next__(player)
    camera = Camera(all_sprites)

    while running:
        screen.fill('gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if player.is_alive:
                if event.type == pygame.MOUSEMOTION:
                    player.turn_to_mouse(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        weapon_interaction()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if is_level_cleared():
                            player = lvl_iterator.__next__(player)
                            #обновим камеру, чтобы игрок повернулся в правильную
                            #сторону
                            camera.update(player)
                            camera.apply()
                            player.turn_to_mouse(pygame.mouse.get_pos())

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        player = lvl_iterator.restart()
        if not player.is_alive:
            put_to_death_player()
        else:
            shoot()
            use_knife()
            recharge()
            player.get_move(pygame.key.get_pressed())
        update_all()
        draw_all(screen)
        pygame.display.flip()
        clock.tick(fps)
