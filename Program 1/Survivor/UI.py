from settings_class import *


class UI:  # obsługuje interfejsy użytkownika
    def __init__(self, player, enemy_sprites):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.enemy_sprites = enemy_sprites

        # Health bar
        self.health_bar_rect = pygame.Rect(20, 20, 300, 30)
        self.health_bar_border_width = 3
        self.health_color = (0, 230, 0)

        # Level
        self.font = pygame.font.Font(None, 36)

        # Experience
        self.exp_bar_rect = pygame.Rect(settings.window_width / 2 - 300, settings.window_height - 40, 600, 20)
        self.exp_bar_border_width = 3

        # Minimap
        self.minimap_size = 200
        self.minimap_rect = pygame.Rect(
            settings.window_width - self.minimap_size - 20,
            20,
            self.minimap_size,
            self.minimap_size
        )
        self.minimap_scale = 0.15
        self.minimap_player_size = 8
        self.minimap_enemy_size = 5

        # Settings button
        self.settings_button_rect = pygame.Rect(
            settings.window_width - 50,
            settings.window_height - 50,
            40,
            40
        )
        self.settings_icon = self.create_settings_icon()
        self.settings_button_hovered = False

    def create_settings_icon(self):
        # Ikonka koła zębatego
        icon_size = 40
        icon_surf = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)

        # Parametry koła zębatego
        outer_radius = 18
        inner_radius = 10
        teeth = 8

        center = (icon_size // 2, icon_size // 2)

        # Rysujemy zęby koła
        for i in range(teeth * 2):
            angle1 = i * math.pi / teeth
            angle2 = (i + 0.5) * math.pi / teeth
            radius = outer_radius if i % 2 == 0 else inner_radius

            x1 = center[0] + radius * math.cos(angle1)
            y1 = center[1] + radius * math.sin(angle1)
            x2 = center[0] + radius * math.cos(angle2)
            y2 = center[1] + radius * math.sin(angle2)

            if i == 0:
                points = [(x1, y1)]
            points.append((x2, y2))

        # Rysujemy wypełnione koło zębate
        pygame.draw.polygon(icon_surf, (200, 200, 200), points)

        # Rysujemy wewnętrzny okrąg
        pygame.draw.circle(icon_surf, (50, 50, 60), center, inner_radius - 2)

        return icon_surf

    def draw_settings_button(self):
        # Sprawdzamy, czy kursor jest nad przyciskiem
        mouse_pos = pygame.mouse.get_pos()
        self.settings_button_hovered = self.settings_button_rect.collidepoint(mouse_pos)

        # Zmiana koloru tła przy najechaniu
        if self.settings_button_hovered:
            pygame.draw.circle(self.display_surface, (100, 100, 120), self.settings_button_rect.center, 22)
        else:
            pygame.draw.circle(self.display_surface, (70, 70, 80), self.settings_button_rect.center, 20)

        # Rysujemy ikonkę
        icon_rect = self.settings_icon.get_rect(center=self.settings_button_rect.center)
        self.display_surface.blit(self.settings_icon, icon_rect)

        return self.settings_button_hovered and pygame.mouse.get_pressed()[0]

    '''Rysuje pasek zdrowia'''

    def draw_health_bar(self):
        # Border
        pygame.draw.rect(
            self.display_surface,
            'white',
            self.health_bar_rect.inflate(self.health_bar_border_width, self.health_bar_border_width),
            self.health_bar_border_width
        )

        # Health fill
        # oblicza jaką część paska wypełnić
        health_ratio = self.player.health / self.player.max_health
        current_health_width = self.health_bar_rect.width * health_ratio
        current_health_rect = pygame.Rect(
            self.health_bar_rect.left,
            self.health_bar_rect.top,
            current_health_width,
            self.health_bar_rect.height
        )

        # Zmienia kolor na bazie ilości zdrowia
        if self.player.shielded:
            self.health_color = (0, 0, 0)  # Black
        elif health_ratio > 0.6:
            self.health_color = (0, 230, 0)  # Green
        elif health_ratio > 0.3:
            self.health_color = (230, 230, 0)  # Yellow
        else:
            self.health_color = (230, 0, 0)  # Red

        pygame.draw.rect(
            self.display_surface,
            self.health_color,
            current_health_rect,
            border_radius=5
        )

        # Napis na pasku
        health_text = f"{int(self.player.health)}/{self.player.max_health}"
        health_text_surf = self.font.render(health_text, True, 'white')
        health_text_rect = health_text_surf.get_rect(center=self.health_bar_rect.center)
        self.display_surface.blit(health_text_surf, health_text_rect)

    def draw_exp_bar(self):
        # Border
        pygame.draw.rect(
            self.display_surface,
            'white',
            self.exp_bar_rect.inflate(self.exp_bar_border_width, self.exp_bar_border_width),
            self.exp_bar_border_width
        )

        # Exp fill
        # oblicza jaką część paska wypełnić
        exp_ratio = self.player.experience / self.player.max_experience
        current_exp_width = self.exp_bar_rect.width * exp_ratio
        current_exp_rect = pygame.Rect(
            self.exp_bar_rect.left,
            self.exp_bar_rect.top,
            current_exp_width,
            self.exp_bar_rect.height
        )

        pygame.draw.rect(
            self.display_surface,
            (255, 132, 19),
            current_exp_rect,
            border_radius=5
        )

        # Napis na pasku
        exp_text = f"{int(self.player.experience)}/{self.player.max_experience}"
        exp_text_surf = self.font.render(exp_text, True, 'black')
        exp_text_rect = exp_text_surf.get_rect(center=self.exp_bar_rect.center)
        self.display_surface.blit(exp_text_surf, exp_text_rect)

    '''Wypisuje level'''

    def draw_level(self):
        level_text = f"Level: {self.player.level}"
        level_surf = self.font.render(level_text, True, 'white')
        level_rect = level_surf.get_rect(midtop=(settings.window_width // 2, 20))

        # Border dla lepszej czytelności
        padding = 10
        border_rect = level_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(self.display_surface, 'black', border_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, 'white', border_rect, 2, border_radius=5)

        self.display_surface.blit(level_surf, level_rect)

    '''Rysuje minimapę'''

    def draw_minimap(self, world_offset):
        # tło minimapy
        pygame.draw.rect(self.display_surface, (0, 0, 0, 180), self.minimap_rect)
        pygame.draw.rect(self.display_surface, 'white', self.minimap_rect, 2)

        # definiuje centrum minimapy
        minimap_center = pygame.Vector2(
            self.minimap_rect.centerx,
            self.minimap_rect.centery
        )

        # rysuje gracza na minimapie
        pygame.draw.circle(
            self.display_surface,
            'green',
            minimap_center,
            self.minimap_player_size
        )

        # rysuje przeciwników
        for enemy in self.enemy_sprites:
            # oblicza pozycję przeciwnika
            rel_x = (enemy.rect.centerx - self.player.rect.centerx) * self.minimap_scale
            rel_y = (enemy.rect.centery - self.player.rect.centery) * self.minimap_scale

            # sprawdza czy przeciwnik jest poza minimapą
            if abs(rel_x) < self.minimap_size // 2 and abs(rel_y) < self.minimap_size // 2:
                enemy_pos = (
                    minimap_center.x + rel_x,
                    minimap_center.y + rel_y
                )

                # rysuje przeciwnika
                pygame.draw.circle(
                    self.display_surface,
                    'red',
                    enemy_pos,
                    self.minimap_enemy_size
                )

    '''Rysuje wszystko'''

    def display(self, world_offset):
        self.draw_health_bar()  # pasek zdrowia
        self.draw_exp_bar()
        self.draw_level()  # wynik
        self.draw_minimap(world_offset)  # minimapa

        return self.draw_settings_button()


class GameOverScreen:  # odpowiada za ekran game over
    def __init__(self, display_surface, restart_game, quit_game, level):
        self.display_surface = display_surface  # okno gry
        self.restart_game = restart_game
        self.quit_game = quit_game
        self.level = level  # wynik końcowy

        # Font
        self.title_font = pygame.font.Font(None, 80)
        self.normal_font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 36)

        # Colors
        self.text_color = 'white'
        self.button_color = (70, 70, 80)
        self.button_hover_color = (100, 100, 120)
        self.button_text_color = 'white'

        # Game over text
        self.title_surf = self.title_font.render("GAME OVER", True, 'red')
        self.title_rect = self.title_surf.get_rect(center=(settings.window_width // 2, settings.window_height // 3))

        # Level text
        self.level_surf = self.normal_font.render(f"Final level: {self.level}", True, self.text_color)
        self.level_rect = self.level_surf.get_rect(center=(settings.window_width // 2, settings.window_height // 2))

        # Buttons
        button_width, button_height = 200, 60
        button_y_pos = settings.window_height * 2 // 3
        button_spacing = 50

        # Restart button
        self.restart_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.restart_button_rect.centerx = settings.window_width // 2 - button_width // 2 - button_spacing // 2
        self.restart_button_rect.centery = button_y_pos
        self.restart_text_surf = self.normal_font.render("Restart", True, self.button_text_color)
        self.restart_text_rect = self.restart_text_surf.get_rect(center=self.restart_button_rect.center)

        # Quit button
        self.quit_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.quit_button_rect.centerx = settings.window_width // 2 + button_width // 2 + button_spacing // 2
        self.quit_button_rect.centery = button_y_pos
        self.quit_text_surf = self.normal_font.render("Quit", True, self.button_text_color)
        self.quit_text_rect = self.quit_text_surf.get_rect(center=self.quit_button_rect.center)

        # Button states
        self.restart_hovered = False
        self.quit_hovered = False

    '''Obsługuje kliknięcie w przyciski'''

    def check_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        # Check restart button
        self.restart_hovered = self.restart_button_rect.collidepoint(mouse_pos)
        if self.restart_hovered and mouse_buttons[0]:
            self.restart_game()

        # Check quit button
        self.quit_hovered = self.quit_button_rect.collidepoint(mouse_pos)
        if self.quit_hovered and mouse_buttons[0]:
            self.quit_game()

    '''Rysuje całe okienko'''

    def draw(self):
        # Draw semi-transparent background
        overlay = pygame.Surface((settings.window_width, settings.window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Semi-transparent black
        self.display_surface.blit(overlay, (0, 0))

        # Draw title and level
        self.display_surface.blit(self.title_surf, self.title_rect)
        self.display_surface.blit(self.level_surf, self.level_rect)

        # Draw restart button
        self.drawButton(
            self.restart_button_rect,
            self.restart_text_rect,
            self.restart_text_surf,
            self.restart_hovered
        )
        # Draw quit button
        self.drawButton(
            self.quit_button_rect,
            self.quit_text_rect,
            self.quit_text_surf,
            self.quit_hovered
        )

    '''Rysuje przycisk'''

    def drawButton(self, button_rect, text_rect, text_surf, hovered):
        button_color = self.button_hover_color if hovered else self.button_color
        pygame.draw.rect(self.display_surface, button_color, button_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, self.text_color, button_rect, 3, border_radius=10)
        self.display_surface.blit(text_surf, text_rect)

    '''Aktualizuje okno game over'''

    def update(self):
        self.check_input()
        self.draw()


class SettingsMenu:
    def __init__(self, display_surface, apply_settings, return_to_game):
        self.display_surface = display_surface
        self.apply_settings = apply_settings  # funkcja do zastosowania ustawień
        self.return_to_game = return_to_game  # funkcja powrotu do gry

        # Fonts
        self.title_font = pygame.font.Font(None, 60)
        self.normal_font = pygame.font.Font(None, 30)

        # Colors
        self.text_color = 'white'
        self.bg_color = (20, 20, 20)
        self.slider_bg_color = (70, 70, 70)
        self.slider_fg_color = (100, 100, 100)
        self.button_color = (70, 70, 70)
        self.button_hover_color = (100, 100, 100)

        # Button states
        self.button_states = {
            'apply': False,
            'back': False,
            'window_left': False,
            'window_right': False,
            'fullscreen': False
        }

        self.active_slider = None

        self._setup_ui()

    def _setup_ui(self):
        # Title
        self.title_surf = self.title_font.render("Settings", True, self.text_color)
        self.title_rect = self.title_surf.get_rect(midtop=(settings.window_width // 2, 50))

        # Position for settings
        self.settings_y = {
            'sfx': 180,
            'music': 280,
            'window': 380,
            'fullscreen': 480,
            'buttons': 580
        }

        # Sliders
        slider_width, slider_height = 400, 20
        slider_x = settings.window_width // 2

        # SFX Volume slider
        self.sfx_label_surf = self.normal_font.render("Sound Effects Volume", True, self.text_color)
        self.sfx_label_rect = self.sfx_label_surf.get_rect(midtop=(slider_x, self.settings_y['sfx']))
        self.sfx_slider_rect = pygame.Rect(0, 0, slider_width, slider_height)
        self.sfx_slider_rect.midtop = (slider_x, self.settings_y['sfx'] + 40)

        # Music Volume slider
        self.music_label_surf = self.normal_font.render("Music Volume", True, self.text_color)
        self.music_label_rect = self.music_label_surf.get_rect(midtop=(slider_x, self.settings_y['music']))
        self.music_slider_rect = pygame.Rect(0, 0, slider_width, slider_height)
        self.music_slider_rect.midtop = (slider_x, self.settings_y['music'] + 40)

        # Window Size selector
        self.window_label_surf = self.normal_font.render("Window Size", True, self.text_color)
        self.window_label_rect = self.window_label_surf.get_rect(midtop=(slider_x, self.settings_y['window']))

        arrow_width, arrow_height = 30, 30
        option_width = 200

        self.window_left_rect = pygame.Rect(0, 0, arrow_width, arrow_height)
        self.window_left_rect.midright = (slider_x - option_width // 2 - 10, self.settings_y['window'] + 50)

        self.window_option_rect = pygame.Rect(0, 0, option_width, arrow_height)
        self.window_option_rect.midtop = (slider_x, self.settings_y['window'] + 40)

        self.window_right_rect = pygame.Rect(0, 0, arrow_width, arrow_height)
        self.window_right_rect.midleft = (slider_x + option_width // 2 + 10, self.settings_y['window'] + 50)

        # Fullscreen toggle
        self.fullscreen_label_surf = self.normal_font.render("Fullscreen", True, self.text_color)
        self.fullscreen_label_rect = self.fullscreen_label_surf.get_rect(
            midtop=(slider_x - 60, self.settings_y['fullscreen']))

        self.fullscreen_rect = pygame.Rect(0, 0, 40, 40)
        self.fullscreen_rect.midleft = (slider_x + 60, self.settings_y['fullscreen'] + 20)

        # Buttons
        button_width, button_height = 180, 50
        button_spacing = 60

        self.apply_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.apply_button_rect.centerx = settings.window_width // 2 - button_width // 2 - button_spacing // 2
        self.apply_button_rect.centery = self.settings_y['buttons']

        self.back_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.back_button_rect.centerx = settings.window_width // 2 + button_width // 2 + button_spacing // 2
        self.back_button_rect.centery = self.settings_y['buttons']

        self.apply_text_surf = self.normal_font.render("Apply", True, self.text_color)
        self.apply_text_rect = self.apply_text_surf.get_rect(center=self.apply_button_rect.center)

        self.back_text_surf = self.normal_font.render("Back", True, self.text_color)
        self.back_text_rect = self.back_text_surf.get_rect(center=self.back_button_rect.center)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check sliders
                if self.sfx_slider_rect.collidepoint(mouse_pos):
                    self.active_slider = 'sfx'
                elif self.music_slider_rect.collidepoint(mouse_pos):
                    self.active_slider = 'music'
                # Check buttons
                elif self.apply_button_rect.collidepoint(mouse_pos):
                    self.apply_settings()
                elif self.back_button_rect.collidepoint(mouse_pos):
                    self.return_to_game()
                # Check window size controls
                elif self.window_left_rect.collidepoint(mouse_pos):
                    settings.current_settings['window_size'] = max(0, settings.current_settings['window_size'] - 1)
                elif self.window_right_rect.collidepoint(mouse_pos):
                    settings.current_settings['window_size'] = min(len(settings.window_sizes) - 1,
                                                                   settings.current_settings['window_size'] + 1)
                # Check fullscreen toggle
                elif self.fullscreen_rect.collidepoint(mouse_pos):
                    settings.current_settings['fullscreen'] = not settings.current_settings['fullscreen']

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left button released
                self.active_slider = None

        elif event.type == pygame.MOUSEMOTION:
            if self.active_slider:
                slider_rect = getattr(self, f"{self.active_slider}_slider_rect")
                # Calculate volume based on x position
                rel_x = max(0, min(1, (mouse_pos[0] - slider_rect.left) / slider_rect.width))
                settings.current_settings[f'{self.active_slider}_volume'] = rel_x

    def update_button_states(self):
        mouse_pos = pygame.mouse.get_pos()

        # Update button hover states
        self.button_states['apply'] = self.apply_button_rect.collidepoint(mouse_pos)
        self.button_states['back'] = self.back_button_rect.collidepoint(mouse_pos)
        self.button_states['window_left'] = self.window_left_rect.collidepoint(mouse_pos)
        self.button_states['window_right'] = self.window_right_rect.collidepoint(mouse_pos)
        self.button_states['fullscreen'] = self.fullscreen_rect.collidepoint(mouse_pos)

    def draw(self):
        # Draw background
        overlay = pygame.Surface((settings.window_width, settings.window_height))
        overlay.fill(self.bg_color)
        overlay.set_alpha(230)
        self.display_surface.blit(overlay, (0, 0))

        # Draw title
        self.display_surface.blit(self.title_surf, self.title_rect)

        # Draw SFX slider
        self.display_surface.blit(self.sfx_label_surf, self.sfx_label_rect)
        pygame.draw.rect(self.display_surface, self.slider_bg_color, self.sfx_slider_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, self.text_color, self.sfx_slider_rect, 2, border_radius=5)

        # Draw SFX level
        sfx_level_width = int(self.sfx_slider_rect.width * settings.current_settings['sfx_volume'])
        sfx_level_rect = pygame.Rect(self.sfx_slider_rect.left, self.sfx_slider_rect.top,
                                     sfx_level_width, self.sfx_slider_rect.height)
        pygame.draw.rect(self.display_surface, self.slider_fg_color, sfx_level_rect, border_radius=5)

        # Draw music slider
        self.display_surface.blit(self.music_label_surf, self.music_label_rect)
        pygame.draw.rect(self.display_surface, self.slider_bg_color, self.music_slider_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, self.text_color, self.music_slider_rect, 2, border_radius=5)

        # Draw music level
        music_level_width = int(self.music_slider_rect.width * settings.current_settings['music_volume'])
        music_level_rect = pygame.Rect(self.music_slider_rect.left, self.music_slider_rect.top,
                                       music_level_width, self.music_slider_rect.height)
        pygame.draw.rect(self.display_surface, self.slider_fg_color, music_level_rect, border_radius=5)

        # Draw window size selector
        self.display_surface.blit(self.window_label_surf, self.window_label_rect)

        # Left arrow
        arrow_color = self.button_hover_color if self.button_states['window_left'] else self.button_color
        pygame.draw.rect(self.display_surface, arrow_color, self.window_left_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, self.text_color, self.window_left_rect, 2, border_radius=5)
        # Drawing left arrow triangle
        pygame.draw.polygon(self.display_surface, self.text_color, [
            (self.window_left_rect.right - 10, self.window_left_rect.top + 5),
            (self.window_left_rect.right - 10, self.window_left_rect.bottom - 5),
            (self.window_left_rect.left + 5, self.window_left_rect.centery)
        ])

        # Window size option
        pygame.draw.rect(self.display_surface, self.slider_bg_color, self.window_option_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, self.text_color, self.window_option_rect, 2, border_radius=5)

        size_text = settings.window_sizes[settings.current_settings['window_size']]['text']
        size_surf = self.normal_font.render(size_text, True, self.text_color)
        size_rect = size_surf.get_rect(center=self.window_option_rect.center)
        self.display_surface.blit(size_surf, size_rect)

        # Right arrow
        arrow_color = self.button_hover_color if self.button_states['window_right'] else self.button_color
        pygame.draw.rect(self.display_surface, arrow_color, self.window_right_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, self.text_color, self.window_right_rect, 2, border_radius=5)
        # Drawing right arrow triangle
        pygame.draw.polygon(self.display_surface, self.text_color, [
            (self.window_right_rect.left + 10, self.window_right_rect.top + 5),
            (self.window_right_rect.left + 10, self.window_right_rect.bottom - 5),
            (self.window_right_rect.right - 5, self.window_right_rect.centery)
        ])

        # Draw fullscreen checkbox
        self.display_surface.blit(self.fullscreen_label_surf, self.fullscreen_label_rect)

        # Checkbox
        checkbox_color = self.button_hover_color if self.button_states['fullscreen'] else self.button_color
        pygame.draw.rect(self.display_surface, checkbox_color, self.fullscreen_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, self.text_color, self.fullscreen_rect, 2, border_radius=5)

        # Draw check mark if fullscreen is enabled
        if settings.current_settings['fullscreen']:
            pygame.draw.line(self.display_surface, self.text_color,
                             (self.fullscreen_rect.left + 10, self.fullscreen_rect.centery),
                             (self.fullscreen_rect.centerx - 5, self.fullscreen_rect.bottom - 10), 3)
            pygame.draw.line(self.display_surface, self.text_color,
                             (self.fullscreen_rect.centerx - 5, self.fullscreen_rect.bottom - 10),
                             (self.fullscreen_rect.right - 10, self.fullscreen_rect.top + 10), 3)

        # Draw buttons
        # Apply button
        apply_color = self.button_hover_color if self.button_states['apply'] else self.button_color
        pygame.draw.rect(self.display_surface, apply_color, self.apply_button_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, self.text_color, self.apply_button_rect, 2, border_radius=10)
        self.display_surface.blit(self.apply_text_surf, self.apply_text_rect)

        # Back button
        back_color = self.button_hover_color if self.button_states['back'] else self.button_color
        pygame.draw.rect(self.display_surface, back_color, self.back_button_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, self.text_color, self.back_button_rect, 2, border_radius=10)
        self.display_surface.blit(self.back_text_surf, self.back_text_rect)

    def update(self):
        self.update_button_states()
        self.draw()
