import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    ASTEROID_MIN_RADIUS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_LARGE_ASTEROID,
    SCORE_MEDIUM_ASTEROID,
    SCORE_SMALL_ASTEROID,
)
from explosion import Explosion, Particle
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    score = 0
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 72)
    game_over = False

    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    # Respawn: reset player position, velocity, score, and game_over flag
                    game_over = False
                    score = 0
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.velocity = pygame.Vector2(0, 0)

        if not game_over:
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_over = True

                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        shot.kill()
                        
                        # Create explosion effect
                        Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius, particles)
                        
                        # Calculate points based on asteroid size
                        if asteroid.radius == ASTEROID_MIN_RADIUS * 3:
                            score += SCORE_LARGE_ASTEROID
                        elif asteroid.radius == ASTEROID_MIN_RADIUS * 2:
                            score += SCORE_MEDIUM_ASTEROID
                        else:
                            score += SCORE_SMALL_ASTEROID
                        
                        asteroid.split()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))
        
        # Draw game over message if dead
        if game_over:
            game_over_text = large_font.render("GAME OVER", True, "red")
            respawn_text = font.render("Press SPACE to respawn", True, "white")
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
            respawn_rect = respawn_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
            
            screen.blit(game_over_text, game_over_rect)
            screen.blit(respawn_text, respawn_rect)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
