import os

import pygame.mouse
from math import atan2, degrees

from settings_class import *


class Sprite(pygame.sprite.Sprite):
    # Sprite groundu
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    # Sprite pól kolizji
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class Gun(pygame.sprite.Sprite):
    # Sprite broni
    def __init__(self, player, groups):
        # połączenie z graczem
        self.player = player
        self.distance = 100 # dystans od gracza
        self.player_direction = pygame.Vector2() # kierunek gracza

        # ustawienie broni
        super().__init__(groups)
        self.guns = []
        self.load_images()
        self.current_gun_index = 0
        self.gun_surf = self.guns[self.current_gun_index]
        self.image = self.gun_surf
        self.rect = self.image.get_rect(center=self.player.rect.center + self.player_direction * self.distance)
        self.cooldown = 600

    def load_images(self):
        folder_path = join('Survivor', 'images', 'gun')
        for file in sorted(os.listdir(folder_path)):
            self.guns.append(pygame.image.load(join(folder_path, file)).convert_alpha())

    '''Ustawia kierunek broni'''
    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # pozycja myszy
        player_pos = pygame.Vector2(settings.window_width / 2, settings.window_height / 2) # pozycja gracza (środek)
        self.player_direction = (mouse_pos - player_pos).normalize()

    '''Obracanie broni'''
    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def set_gun(self):
        if self.player.level <= 2:
            new_index = 0
            self.cooldown = 600
        elif 2 < self.player.level <= 4:
            new_index = 1
            self.cooldown = 400
        elif 4 < self.player.level <= 6:
            new_index = 2
            self.cooldown = 200
        else:
            new_index = 3
            self.cooldown = 100

        # Zmiana broni tylko jeśli jest inna niż obecna
        if new_index != self.current_gun_index:
            self.current_gun_index = new_index
            self.gun_surf = self.guns[self.current_gun_index]
            self.rotate_gun()

    '''Aktualizuje broń'''
    def update(self, _):
        self.set_gun()

        self.get_direction() # ustawia kierunek
        self.rotate_gun() # obraca broń
        # aktualizuje pozycję broni
        self.rect.center = self.player.rect.center + self.player_direction * self.distance


class Bullet(pygame.sprite.Sprite): # Klasa pocisku
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks() # czasu spawnu
        self.lifetime = 1000 # czas po którym obiekt jest usuwany

        self.direction = direction # kierunek pocisku
        self.speed = 1200 # prędkość pocisku

    '''Aktualizowanie pocisku'''
    def update(self, dt):
        # aktualizowanie pozycji
        self.rect.center += self.direction * self.speed * dt

        # usuwanie po czasie
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()


class Enemy(pygame.sprite.Sprite): # klasa przeciwników
    def __init__(self, pos, frames, enemy_type, groups, player, collision_sprites, ui):
        super().__init__(groups)
        self.player = player
        self.ui = ui

        # image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.img = self.image
        self.animation_speed = 5

        # rect
        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()

        # enemy type
        self.enemy_type = enemy_type
        # speed
        self.speed = 0
        # health
        self.health = 0
        # damage
        self.damage = 0
        # exp
        self.exp = 0

        self.set_enemy_type()

        # timer
        self.damage_time = 0
        self.damage_duration = 400

    def set_enemy_type(self):
        if self.enemy_type == 'bat':
            self.speed = 200
            self.health = 1
            self.damage = 5
            self.exp = 2
        elif self.enemy_type == 'blob':
            self.speed = 50
            self.health = 3
            self.damage = 15
            self.exp = 4
        elif self.enemy_type == 'skeleton':
            self.speed = 100
            self.health = 2
            self.damage = 20
            self.exp = 6

    '''Animacje przeciwników'''
    def animate(self, dt):
        self.frame_index = self.frame_index + self.animation_speed * dt
        self.img = self.frames[int(self.frame_index) % len(self.frames)]

    '''Przemieszczanie przeciwników w stronę gracza'''
    def move(self, dt):
        # get direction
        player_pos = pygame.Vector2(self.player.rect.center) # pozycja gracza
        enemy_pos = pygame.Vector2(self.rect.center) # pozycja przeciwnika
        direction_vector = player_pos - enemy_pos # kierunek w stronę gracza
        if direction_vector.length() > 0:
            self.direction = direction_vector.normalize()
        else:
            self.direction = pygame.Vector2(0, 0)

        # aktualizuje pozycję przeciwnika i obsługuje kolizje
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    '''Obsługuje kolizje z obiektami nieprzechodzalnymi'''
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

    def take_damage(self):
        self.health -= 1
        # zmienia obraz na mask.from_surface
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    '''Obsługuje zabicie przeciwnika'''
    def destroy(self):
        # zapisuje czas śmierci
        self.damage_time = pygame.time.get_ticks()
        # dodaje doświadczenie
        self.player.get_experience(self.exp)

    '''Obsługuje timer uśmiercania przeciwnika'''
    def damage_timer(self):
        if pygame.time.get_ticks() - self.damage_time >= self.damage_duration:
            if self.health > 0:
                self.image = self.img
            else:
                self.kill()

    '''Aktualizuje przeciwnika'''
    def update(self, dt):
        if self.health > 0:
            self.move(dt) # przemieszcza
            self.animate(dt) # animuje
            self.damage_timer()
        else:   # jeśli nie żyje
            self.damage_timer() # odpala timer po którym zabija


class Perk(pygame.sprite.Sprite):
    def __init__(self, pos, perk_type, groups, player, ui):
        super().__init__(groups)
        self.ui = ui

        self.health_value = 20
        self.speed_value = 1.5
        self.perk_duration = 5000

        self.perk_type = perk_type
        self.player = player

        self.size = 24
        self.image = pygame.image.load(join('Survivor', 'images', 'perks', perk_type+'.png'))

        # setup pos and collision
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-6, -6)

        # lifespan and animation
        self.lifespan = 10000  # ms
        self.creation_time = pygame.time.get_ticks()
        self.apply_time = 0

    def apply_effect(self):
        if self.perk_type == 'health':
            self.player.health = min(self.player.health + self.health_value,
                                     self.player.max_health)
            self.kill()
        elif self.perk_type == 'speed':
            self.player.speed *= self.speed_value

        elif self.perk_type == 'shield':
            self.player.shielded = True
            self.ui.draw_health_bar()

        self.apply_time = pygame.time.get_ticks()

    def update(self, dt):
        # Check lifetime
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifespan:
            self.kill()

        # Check duration
        if current_time - self.apply_time > self.perk_duration:
            if self.perk_type == 'speed':
                self.player.speed = self.player.default_speed
            elif self.perk_type == 'shield':
                self.player.shielded = False
                self.ui.draw_health_bar()

        # Check collision with player
        if self.hitbox.colliderect(self.player.hitbox_rect):
            self.apply_effect()
            self.kill()

