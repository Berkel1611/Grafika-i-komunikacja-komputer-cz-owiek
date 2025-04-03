import pygame
from os.path import join
from os import walk
import math
import random


class GameSettings:
    def __init__(self):
        self._window_width = 1280
        self._window_height = 720
        self.tile_size = 64
        self.current_settings = {
            'sfx_volume': 0.4,
            'music_volume': 0.3,
            'window_size': 0,
            'fullscreen': False
        }
        self.window_sizes = [
            {'text': '1280 x 720', 'size': (1280, 720)},
            {'text': '1600 x 900', 'size': (1600, 900)},
            {'text': '1920 x 1080', 'size': (1920, 1080)}
        ]

    @property
    def window_width(self):
        return self._window_width

    @property
    def window_height(self):
        return self._window_height

    def update_window_size(self, width, height):
        self._window_width = width
        self._window_height = height


settings = GameSettings()
