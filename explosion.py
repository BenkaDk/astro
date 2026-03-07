import random

import pygame
from circleshape import CircleShape
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, lifetime=0.5, color="white"):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.radius = 3

    def draw(self, screen):
        # Fade out over time
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.kill()


class Explosion:
    def __init__(self, x, y, radius, particle_group):
        """
        Create an explosion at (x, y) with particles based on asteroid radius.
        
        Args:
            x: X position of explosion
            y: Y position of explosion
            radius: Radius of the asteroid (affects number of particles)
            particle_group: Sprite group to add particles to
        """
        # More particles for larger asteroids
        num_particles = int(radius / 10) * 3
        colors = ["white", "yellow", "orange", "red"]

        for _ in range(num_particles):
            # Random angle and speed
            angle = random.uniform(0, 360)
            speed = random.uniform(100, 400)
            vector = pygame.Vector2(0, 1).rotate(angle) * speed

            # Random lifetime for varied effect
            lifetime = random.uniform(0.3, 0.8)
            color = random.choice(colors)

            particle = Particle(x, y, vector, lifetime, color)
            particle.add(particle_group)
