from settings_class import *

'''Klasa reprezentująca gracza'''


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.frames = None # klatki animacji gracza
        self.load_images() # ładuje obrazy
        self.state, self.frame_index = 'down', 0 # pozycja gracza, numer klatki
        # ładowanie pierwszej klatki
        self.image = pygame.image.load(join('Survivor', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos) # ładowanie rect gracza
        self.hitbox_rect = self.rect.inflate(-60, -90) # rect hitboxu

        # movement
        self.direction = pygame.Vector2() # wektor przechowujący kierunek, w którym porusza się gracz
        self.default_speed = 500
        self.speed = self.default_speed # prędkość gracza
        self.collision_sprites = collision_sprites # obiekty, przez które nie może przechodzić

        # health system
        self.max_health = 100 # maksmalne życie
        self.health = self.max_health # ustawia życie na maksymalne
        self.invincible = False # nietykalność
        self.invincibility_duration = 1000  # cooldown nietykalności
        self.hurt_time = 0 # czas zranienia
        self.shielded = False

        # experience system
        self.level = 1
        self.max_experience = 20
        self.experience = 0

    '''Ładuje obrazy'''
    def load_images(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('Survivor', 'images', 'player', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    '''Obsługa sterowania klawiaturą'''
    def input(self):
        keys = pygame.key.get_pressed() # wczytuje wciśnięte klawisze
        # ustawia kierunek poruszania postaci poziomo (ujemne w lewo, dodatnie w prawo)
        self.direction.x = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(keys[pygame.K_LEFT] or keys[pygame.K_a])
        # ustawia kierunek poruszania postaci pionowe (ujemne w górę, dodatnie w dół)
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])
        # normalizuje wektor, jeśli nie jest zerowy
        self.direction = self.direction.normalize() if self.direction else self.direction

    '''Obsługuje przemieszczanie postaci'''
    def move(self, dt):
        # modyfikuje rect hitbox i sprawdza kolizje
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    '''Obsługuje kolizje z obiektami nie do przejścia'''
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                # jeśli kierunek poruszania był poziomy
                if direction == 'horizontal':
                    # jeśli w prawo, przenosi gracza na lewo od obiektu
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    # jeśli w lewo, przenosi gracza na prawo od obiektu
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                # jeśli kierunek poruszania był pionowy
                else:
                    # jeśli w górę, przenosi gracza na dół od obiektu
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                    # jeśli w dół, przenosi gracza na górę od obiektu
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top

    '''Obsługuje animacje gracza'''
    def animate(self, dt):
        # ustawia stan postaci
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # animuje
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    '''Obsługuje obrażenia otrzymane przez gracza'''
    def take_damage(self, amount):
        if not self.invincible and not self.shielded: # jeżeli tykalny
            self.health -= amount # zmniejsza zdrowie
            self.health = max(0, self.health)  # jeżeli mniejsze niż 0 ustawia 0
            self.invincible = True # włącza nietykalność
            self.hurt_time = pygame.time.get_ticks() # zapisuje czas otrzymanych obrażeń

    '''Obsługuje timer nietykalności'''
    def invincibility_timer(self):
        if self.invincible: # jeżeli tykalny
            current_time = pygame.time.get_ticks() # pobiera aktualny czas
            # jeżeli ostatnie obrażenia były dawniej niż cooldown, wyłącza nietykalność
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def get_experience(self, exp):
        self.experience += exp
        if self.experience >= self.max_experience:
            excess = self.experience - self.max_experience
            self.level += 1
            self.set_max_experience()
            self.experience = excess

    def set_max_experience(self):
        self.max_experience += self.level * self.level * 5

    '''Aktualizuje postać gracza'''
    def update(self, dt):
        self.input() # obsługa klawiatury
        self.move(dt) # przemieszczanie postaci
        self.animate(dt) # animowanie
        self.invincibility_timer()  # timer nietykalności
