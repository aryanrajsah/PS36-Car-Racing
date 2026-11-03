# Name: Aryan Raj
# Enrollment No.: RU-26-02977
# Admission No.: REF-2026-07307
# Email ID: aryan.raj4@rungta.org
# Section: BE-CSE-C-1-26-1-B2


import sys
import random
import pygame

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60

# Road specifications (spans x = 50 to 350)
ROAD_LEFT = 50
ROAD_RIGHT = 350
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT  # 300px

# Car specifications (40x80)
CAR_WIDTH = 40
CAR_HEIGHT = 80
PLAYER_START_X = 180
PLAYER_START_Y = 500
PLAYER_STEP = 10  # Moves 10px per keypress

# Boundary limits for player's top-left x coordinate
MIN_PLAYER_X = ROAD_LEFT                   # 50
MAX_PLAYER_X = ROAD_RIGHT - CAR_WIDTH      # 310

# Obstacle specifications
OBSTACLE_SPEED = 5
SPAWN_INTERVAL_FRAMES = 55

# Colors (R, G, B)
COLOR_GRASS = (34, 139, 34)
COLOR_ROAD = (50, 50, 50)
COLOR_LINE = (255, 255, 255)
COLOR_PLAYER = (0, 120, 255)
COLOR_OBSTACLE = (220, 40, 40)
COLOR_TEXT = (255, 255, 255)
COLOR_GAME_OVER = (255, 215, 0)


# ==========================================
# CORE LOGIC FUNCTIONS (Testable)
# ==========================================
def move_player(player_x: int, key: int) -> int:
    """
    Moves the player car 10px left or right within road boundaries (50 to 310).
    Ignores all keys other than LEFT and RIGHT arrows.
    """
    if key == pygame.K_LEFT:
        return max(MIN_PLAYER_X, player_x - PLAYER_STEP)
    elif key == pygame.K_RIGHT:
        return min(MAX_PLAYER_X, player_x + PLAYER_STEP)
    return player_x


def check_collision(player_rect: pygame.Rect, obstacle_rect: pygame.Rect) -> bool:
    """Detects collision between player car and obstacle car using Rect.colliderect()."""
    return player_rect.colliderect(obstacle_rect)


def spawn_obstacle() -> pygame.Rect:
    """Spawns a 40x80 obstacle car at the top of the screen within the road."""
    random_x = random.randint(MIN_PLAYER_X, MAX_PLAYER_X)
    return pygame.Rect(random_x, -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT)


# ==========================================
# MAIN GAME LOOP
# ==========================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("CarRacing Game - PS No. 36")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24, bold=True)
    game_over_font = pygame.font.SysFont("Arial", 32, bold=True)

    # Initial game state
    player_rect = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, CAR_WIDTH, CAR_HEIGHT)
    obstacles = []
    score = 0
    frame_count = 0
    game_over = False

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Restart game when 'R' is pressed
                if game_over and event.key == pygame.K_r:
                    player_rect.x = PLAYER_START_X
                    player_rect.y = PLAYER_START_Y
                    obstacles.clear()
                    score = 0
                    frame_count = 0
                    game_over = False

        # 2. Game State Updates
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x = move_player(player_rect.x, pygame.K_LEFT)
            if keys[pygame.K_RIGHT]:
                player_rect.x = move_player(player_rect.x, pygame.K_RIGHT)
            frame_count += 1
            if frame_count >= SPAWN_INTERVAL_FRAMES:
                obstacles.append(spawn_obstacle())
                frame_count = 0

            # Move obstacles downwards and check status
            for obs in obstacles[:]:
                obs.y += OBSTACLE_SPEED

                # Check collision with player car
                if check_collision(player_rect, obs):
                    game_over = True
                    break

                # Check if obstacle leaves the screen (y >= 600)
                if obs.y >= WINDOW_HEIGHT:
                    obstacles.remove(obs)
                    score += 1

        # 3. Rendering / Drawing
        screen.fill(COLOR_GRASS)

        # Draw road (x=50 to x=350) and boundary lines
        pygame.draw.rect(screen, COLOR_ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, WINDOW_HEIGHT))
        pygame.draw.line(screen, COLOR_LINE, (ROAD_LEFT, 0), (ROAD_LEFT, WINDOW_HEIGHT), 3)
        pygame.draw.line(screen, COLOR_LINE, (ROAD_RIGHT, 0), (ROAD_RIGHT, WINDOW_HEIGHT), 3)

        # Draw center dashed lane divider
        for y in range(0, WINDOW_HEIGHT, 40):
            pygame.draw.rect(screen, COLOR_LINE, (WINDOW_WIDTH // 2 - 2, y, 4, 20))

        # Draw player car and obstacles
        pygame.draw.rect(screen, COLOR_PLAYER, player_rect)
        for obs in obstacles:
            pygame.draw.rect(screen, COLOR_OBSTACLE, obs)

        # Draw live score
        score_surface = font.render(f"Score: {score}", True, COLOR_TEXT)
        screen.blit(score_surface, (60, 15))

        # Draw Game Over overlay
        if game_over:
            over_text = game_over_font.render("Game Over", True, COLOR_GAME_OVER)
            final_score_text = font.render(f"Final Score: {score}", True, COLOR_TEXT)
            restart_text = font.render("Press R to Restart", True, COLOR_TEXT)

            screen.blit(over_text, (WINDOW_WIDTH // 2 - over_text.get_width() // 2, 220))
            screen.blit(final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, 270))
            screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, 320))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()