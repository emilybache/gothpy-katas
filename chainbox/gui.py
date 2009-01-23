##
## ChainBox GUI implementation using PyGame

import pygame
import sys

class ChainBox(object):
    def __init__(self, game, size = (400, 400), border = 10):
        pygame.init()

        pygame.display.set_mode(size)
        pygame.display.set_caption("ChainBox")

        self.size = size
        self.border = border

        self.surface_width, self.surface_height = self.size
        self.col_width = (self.surface_width - (self.border * 2)) // game.width
        self.col_height = (self.surface_height - (self.border * 2)) // game.height

    def render(self, game):
        surface = pygame.display.get_surface()

        surface.fill((161,113,32))
        line_color = (0,0,0)

        # grid
        a, xa, ya = self.border, self.surface_width - self.border, self.surface_height - self.border
        for x in range(game.width + 1):
            xx = x * self.col_width
            pygame.draw.line(surface, line_color, (xx + self.border, a), (xx + self.border, ya), 1)

        for y in range(game.height + 1):
            yy = y * self.col_height
            pygame.draw.line(surface, line_color, (a, yy + self.border), (xa, yy + self.border), 1)

        # markers
        for x in range(game.width):
            for y in range(game.height):
                self.place_marker(game.marker_at_position((x, y)), x, y)

        # chains
        for p in [1,2]:
            c = sorted(game._longest_chain(p), key = lambda t: t[0]*10 + t[1])
            if len(c) > 1:
                self.draw_longest_chain(p, c)

        pygame.display.update()

    def _translate(self, x, y):
        bx, by = self.border + (self.col_width // 2), self.border + (self.col_height // 2)
        return (self.col_width * x) + bx, (self.col_height * y) + by

    def place_marker(self, player, x, y):
        if player == 0:
            return

        surface = pygame.display.get_surface()
        colors = { 1: (255,255,255),
                   2: (0,0,0), }

        radius = self.col_width // 2 - 2
        if self.col_height < self.col_width:
            radius = self.col_height // 2 - 2

        px, py = self._translate(x, y)
        pygame.draw.circle(surface, colors[player], (px, py), radius)

    def draw_longest_chain(self, player, chain):
        surface = pygame.display.get_surface()
        colors = { 1: (255,255,255),
                   2: (0,0,0), }

        radius = self.col_width // 2 - 2
        if self.col_height < self.col_width:
            radius = self.col_height // 2 - 2
        line_width = radius // 2

        # The chain is sorted from left to right and top to bottom but there's
        # the additional constraint that no two markers may be further apart
        # than 1 distance unit.

        points = [self._translate(*p) for p in chain]
        pygame.draw.lines(surface, colors[player], False, points, line_width)
            
