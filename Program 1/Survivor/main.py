import pygame.time

from settings_class import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from UI import *

from random import randint, choice


class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.window_size = settings.window_sizes[0]['size']
        self.display_surface = pygame.display.set_mode((settings.window_width, settings.window_height)) # tworzy okno
        pygame.display.set_caption("Survivor") # ustawia nazwę okna
        self.clock = pygame.time.Clock() # zegar
        self.running = True # czy postać biegnie
        self.fps = 60 # ilość klatek

        # game state
        self.game_state = 'playing'

        self.ui = None
        self.settings_menu = None

        self.initialize_game()

    '''Inicjlizuje obiekty i mechaniczmy potrzebne w grze '''
    def initialize_game(self):
        # groups
        self.all_sprites = AllSprites() # przechowuje wszystkie obiekty, słuzy do rysowania ich na ekranie
        self.collision_sprites = pygame.sprite.Group() # przechowuje pole kolizji
        self.bullet_sprites = pygame.sprite.Group() # obiekty kul
        self.enemy_sprites = pygame.sprite.Group() # obiekty przeciwników
        self.perk_sprites = pygame.sprite.Group()

        # gun timer
        self.can_shoot = True # do ograniczania częstotliwości strzału
        self.shoot_time = 0 # przechowuje czas oddania strzału

        # enemy timer
        self.enemy_event = pygame.event.custom_type() # event respienia przeciwników
        pygame.time.set_timer(self.enemy_event, 700)
        self.spawn_positions = [] # pozycje respienia


        # audio
        self.shoot_sound = pygame.mixer.Sound(join('Survivor', 'audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.4)
        self.impact_sound = pygame.mixer.Sound(join('Survivor', 'audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('Survivor', 'audio', 'music.wav'))
        self.music.set_volume(0.3)
        self.music.play(loops=-1)

        # setup
        self.load_images() # ładuje obrazy do gry
        self.setup()

        # UI
        self.ui = UI(self.player, self.enemy_sprites)

        # Setting Menu
        self.settings_menu = SettingsMenu(
            self.display_surface,
            self.apply_settings,
            self.return_to_game
        )

    def apply_settings(self):
        # Update audio volumes
        self.shoot_sound.set_volume(settings.current_settings['sfx_volume'])
        self.impact_sound.set_volume(settings.current_settings['sfx_volume'])
        self.music.set_volume(settings.current_settings['music_volume'])

        # Update window size and mode
        if settings.current_settings['fullscreen']:
            self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            settings.update_window_size(info.current_w, info.current_h)
        else:
            window_size = settings.window_sizes[settings.current_settings['window_size']]['size']
            settings.update_window_size(window_size[0], window_size[1])
            self.display_surface = pygame.display.set_mode(window_size)

        # Recreate UI with new dimensions
        self.ui = UI(self.player, self.enemy_sprites)

        # Recreate settings menu with new dimensions
        self.settings_menu = SettingsMenu(
            self.display_surface,
            self.apply_settings,
            self.return_to_game
        )

    def return_to_game(self):
        self.game_state = 'playing'

    '''Na nowo inicjalizuje grę po zakończeniu poprzedniej rozgrywki'''
    def restart_game(self):
        self.music.stop()
        # Reset game state
        self.game_state = 'playing'
        # Re-initialize the game
        pygame.time.set_timer(self.enemy_event, 0)  # Stop the enemy timer
        self.initialize_game()  # Reset everything

    '''Zmienia stan gry na False, jeśli zostanie wciśnięty przycisk QUIT'''
    def quit_game(self):
        self.running = False

    '''Ładuje obrazy do programu'''
    def load_images(self):
        # grafika kuli
        self.bullet_surf = pygame.image.load(join('Survivor', 'images', 'bullet', 'bullet.png')).convert_alpha()

        # grafiki przeciwników
        folders = list(walk(join('Survivor', 'images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('Survivor', 'images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    '''Obsługuje kliknięcię lewego przycisku myszy (strzelanie)'''
    def input(self):
        # jeśli lewy wcisnięty i można strzelać
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play() # dżwięk strzału
            # pozycja startowa pocisku
            pos = self.gun.rect.center + self.gun.player_direction * 50
            # tworzenie obiektu pocisku
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            # zablokowanie strzelania
            self.can_shoot = False
            # zapamiętanie czasu oddania strzału
            self.shoot_time = pygame.time.get_ticks()

    '''Kontroluje czas przeładowania broni'''
    def gun_timer(self):
        if not self.can_shoot: # jeśli broń jest zablokowana
            current_time = pygame.time.get_ticks() # pobiera aktualny czas
            # jeżeli czas od ostatniego wystrzału jest większy od cooldownu można strzelać
            if current_time - self.shoot_time >= self.gun.cooldown:
                self.can_shoot = True

    '''Ustawia mapę i obiekty'''
    def setup(self):
        # pobranie mapy
        map = load_pygame(join('Survivor', 'data', 'maps', 'world.tmx'))

        # ustawienie groundu
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * settings.tile_size, y * settings.tile_size), image, self.all_sprites)

        # ustawienie obiektów
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        # ustawienie kolizji
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        # ustawienie gracza, broni oraz miejsc spawnowania przeciwników
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    '''Obsługa kolizji pocisków z przeciwnikami'''
    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                # sprawdza czy pocisk koliduje z którymś z przeciwników
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites,
                                                                False, pygame.sprite.collide_mask)
                # jeśli jest kolizja
                if collision_sprites:
                    self.impact_sound.play() # dżwięk trafenia
                    for sprite in collision_sprites:
                        sprite.take_damage() # damage na przeciwniku
                        if sprite.health <= 0:
                            sprite.destroy()
                            # Wyrzuca perk z danym prawdopodobieństwem
                            if random.random() < 0.2:
                                # wybiera perka
                                perk_type = random.choice(['health', 'speed', 'shield'])
                                # dodaje perka do all_sprites
                                Perk(
                                    sprite.rect.center,
                                    perk_type,
                                    (self.all_sprites, self.perk_sprites),
                                    self.player,
                                    self.ui
                                )
                    bullet.kill() # usuwanie pocisku

    '''Obsługa kolizji gracza z przeciwnikami'''
    def player_collision(self):
        # ładuje kolizje gracza z przeciwnikami
        enemy_collisions = pygame.sprite.spritecollide(
            self.player,
            self.enemy_sprites,
            False,
            pygame.sprite.collide_mask
        )
        if enemy_collisions: # jeżeli są kolizje
            for enemy in enemy_collisions:
                self.player.take_damage(enemy.damage) # gracz odnosi obrażenia
                if self.player.health <= 0: # jesli zdrowie gracza poniżej 0
                    # Przełącza stan gry
                    self.game_state = 'game_over'
                    # tworzy okienko
                    self.game_over_screen = GameOverScreen(
                        self.display_surface,
                        self.restart_game,
                        self.quit_game,
                        self.player.level
                    )
                    # zatrzymuje respienie przeciwników
                    pygame.time.set_timer(self.enemy_event, 0)

    '''Nieskończona pętla aktualizująca grę'''
    def run(self):
        while self.running:
            # dt - czas trwania jednej klatki
            dt = self.clock.tick(self.fps) / 1000

            # pętla obsługi eventów
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # przycisk zamknięcia okna gry
                    self.running = False
                if event.type == self.enemy_event: # event respienia przeciwników
                    enemy_type = choice(list(self.enemy_frames.keys())) # wybór przeciwnika
                    Enemy(
                        choice(self.spawn_positions), # wybór losowej pozycji
                        self.enemy_frames[enemy_type],
                        enemy_type,
                        (self.all_sprites, self.enemy_sprites), # przekazania do grup spriteów
                        self.player,
                        self.collision_sprites,
                        self.ui
                    )
                if self.game_state == 'settings':
                    self.settings_menu.handle_event(event)

            # Obsługuje stany gry
            if self.game_state == 'playing': # jeśli gra trwa
                # Aktualizuje rozgrywkę
                self.gun_timer() # czas przeładowania
                self.input() # strzelanie
                self.all_sprites.update(dt) # aktualizowanie obiektów
                self.bullet_collision() # kolizja kul
                self.player_collision() # kolizja przeciwnika

                # Rysuje obiekty
                self.display_surface.fill('black')
                self.all_sprites.draw(self.player.rect.center) # wszystkie spritey

                # Rysuje UI i sprawdza czy kliknięto przycisk ustawień
                if self.ui.display(self.all_sprites.offset):
                    self.game_state = 'settings'

            elif self.game_state == 'game_over': # jeśli game over
                # Rysuje obiekty tak jak były podczas śmierci gracza
                self.display_surface.fill('black')
                self.all_sprites.draw(self.player.rect.center)
                # Wyświetla game over screen
                self.game_over_screen.update()

            elif self.game_state == 'settings':
                # Tło gry pozostaje widoczne
                self.display_surface.fill('black')
                self.all_sprites.draw(self.player.rect.center)
                # Wyświetla menu ustawień
                self.settings_menu.update()

            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
