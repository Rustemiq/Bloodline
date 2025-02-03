from modules.load_image import load_image

icons = {
    "music_on": load_image("music_on_icon.png"),
    "music_off": load_image("music_off_icon.png"),
    "sound_on": load_image("sound_on_icon.png"),
    "sound_off": load_image("sound_off_icon.png"),
}

sound_paths = {
    "music": "sounds//main_theme.mp3",
    "shotgun": "sounds//shotgun_shot.ogg",
    "uzi": "sounds//uzi_shot.wav",
    "knife_hit": "sounds//knife_hit.ogg",
    "fist_hit": "sounds//fist_hit.ogg",
    "throw": "sounds//throw.ogg",
}

icon_size = 35
WIDTH = 900


class Sound:
    def __init__(self, mixer):
        self.music_on = True
        self.sound_on = True
        self.mixer = mixer
        self.mixer.music.load(sound_paths["music"])
        self.mixer.music.play()
        self.shotgun_sound = self.mixer.Sound(sound_paths["shotgun"])
        self.uzi_sound = self.mixer.Sound(sound_paths["uzi"])
        self.knife_sound = self.mixer.Sound(sound_paths["knife_hit"])
        self.fist_sound = self.mixer.Sound(sound_paths["fist_hit"])
        self.is_icon_clicked = False
        self.throw_sound = self.mixer.Sound(sound_paths["throw"])
        self.volume = 1

    def off_on_music(self):
        self.music_on = not self.music_on
        if self.music_on:
            self.mixer.music.unpause()
        else:
            self.mixer.music.pause()

    def off_on_sound(self):
        self.sound_on = not self.sound_on

    def play_weapon_sound(self, weapon):
        if self.sound_on:
            if weapon == "empty":
                self.fist_sound.play()
            elif weapon.type == "knife":
                self.knife_sound.play()
            elif weapon.type == "shotgun":
                self.shotgun_sound.play()
            elif weapon.type == "uzi":
                self.uzi_sound.play()

    def play_throw_sound(self):
        if self.sound_on:
            self.throw_sound.play()

    def fade_music(self):
        if self.volume > 0:
            self.volume -= 0.01
            self.mixer.music.set_volume(self.volume)

    def interaction(self, mouse_pos):
        if icon_size > mouse_pos[1] > 0:
            if (
                    WIDTH - icon_size * 2 - 2 + icon_size
                    > mouse_pos[0]
                    > WIDTH - icon_size * 2 - 2
            ):
                self.off_on_music()
                self.is_icon_clicked = True
            if (
                    WIDTH - icon_size - 2 + icon_size
                    > mouse_pos[0]
                    > WIDTH - icon_size - 2
            ):
                self.off_on_sound()
                self.is_icon_clicked = True

    def draw_icons(self, screen):
        if self.music_on:
            screen.blit(icons["music_on"], (WIDTH - icon_size * 2 - 2, 0))
        else:
            screen.blit(icons["music_off"], (WIDTH - icon_size * 2 - 2, 0))
        if self.sound_on:
            screen.blit(icons["sound_on"], (WIDTH - icon_size, 0))
        else:
            screen.blit(icons["sound_off"], (WIDTH - icon_size, 0))
