import random
import math

import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = 12
        self.lumpiness = 0.3
        self.shape_offsets = [1 + (random.random() * 2 - 1) * self.lumpiness 
                              for _ in range(self.points)]

    def draw(self, screen):
        points_list = []
        for i in range(self.points):
            angle = (i / self.points) * 2 * math.pi
            r = self.radius * self.shape_offsets[i]
            px = self.position.x + r * math.cos(angle)
            py = self.position.y + r * math.sin(angle)
            points_list.append((px, py))
        pygame.draw.polygon(screen, "white", points_list, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2
