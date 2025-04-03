from settings_class import *


class AllSprites(pygame.sprite.Group): # grupa wszystkich sprite'ów, służy do rysowania ich
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - settings.window_width / 2)
        self.offset.y = -(target_pos[1] - settings.window_height / 2)

        # ground
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        # inne obiekty
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
