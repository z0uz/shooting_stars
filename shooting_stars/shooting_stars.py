import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Plane vs Stars")

# Load images
plane_img = pygame.image.load("plane.png")
star_img = pygame.image.load("star.png")

# Plane dimensions and starting position
plane_width = 50
plane_height = 50
plane_x = screen_width // 2 - plane_width // 2
plane_y = screen_height - plane_height - 10

# Bullet dimensions and speed
bullet_width = 3
bullet_height = 15
bullet_speed = 20

# Star dimensions and speed
star_width = 30
star_height = 30
star_speed = 2

font = pygame.font.Font(None, 36)


# Function to draw the plane on the screen
def draw_plane(x, y):
    screen.blit(plane_img, (x, y))


# Function to draw a bullet on the screen
def draw_bullet(x, y):
    pygame.draw.rect(screen, white, (x, y, bullet_width, bullet_height))


# Function to draw a star on the screen
def draw_star(x, y):
    screen.blit(star_img, (x, y))


# define score

def display_score(score):
    global font  # Declare font as a global variable
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (5, 5))


# Main game loop

def display_hit_screen(hit=None):
    hit_text = font.render(f"Hit: {hit}", True, white)
    screen.blit(hit_text, (screen_width // 2 - 40, hit_text.get_width() // 2 - 20))


def display_game_over_screen():
    game_over_text = font.render("Game Over", True, white)
    screen.blit(game_over_text, (screen_width // 2 - 40, game_over_text.get_width() // 2 - 20))

    restart_text = font.render("Press R to restart", True, white)
    screen.blit(restart_text, (screen_width // 2 - 40, restart_text.get_width() // 2 - 20))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_loop()

shooting_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("expl3.wav")
explosion1_sound = pygame.mixer.Sound("explosion.wav")
def show_explosion(screen, x, y, explosion_max_radius):
    explosion_radius = 20
    explosion_speed = 1
    explosion_sound.play()
    while explosion_radius < explosion_max_radius:
        pygame.draw.circle(screen, (255, 0, 0), (x, y), explosion_radius)
        pygame.display.update()
        pygame.time.delay(explosion_speed)
        explosion_radius += 1
    explosion_sound.stop()


def game_loop(coallision_counter=None):
    global plane_x  # Declare plane_x as a global variable
    collision_counter = 0
    plane_x_change = 0
    bullets = []
    score = 0
    stars = []
    coalitions_counter = 0
    hit_timer = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    plane_x_change = -5
                elif event.key == pygame.K_RIGHT:
                    plane_x_change = 5
                elif event.key == pygame.K_SPACE:
                    shooting_sound.play()
                    bullets.append([plane_x + plane_width // 2 - bullet_width // 2, plane_y])

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    plane_x_change = 0
        plane_x += plane_x_change

        for star in stars[:]:
            if (
                    plane_x < star[0] + star_width
                    and plane_x + plane_width > star[0]
                    and plane_y < star[1] + star_height
                    and plane_y + plane_height > star[1]
            ):
                stars.remove(star)
                collision_counter += 1
                explosion1_sound.play()
                show_explosion(screen, plane_x + plane_width // 2, plane_y + plane_height // 2,
                               100)
                
                hit_timer = 30  # Display the "hit" screen for 30 frames
                if collision_counter >= 5:
                    # Game over, reset the game
                    collision_counter = 0
                    score = 0
                    bullets.clear()
                    stars.clear()


        # Display the "hit" screen if the timer is greater than 0
        if hit_timer > 0:
            display_hit_screen()
            hit_timer -= 1

        # Boundary check for the plane
        if plane_x < 0:
            plane_x = 0
        elif plane_x > screen_width - plane_width:
            plane_x = screen_width - plane_width

        # Move bullets and remove if off the screen
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Generate stars randomly
        if random.randint(0, 100) < 2:
            star_x = random.randint(0, screen_width - star_width)
            star_y = -star_height
            stars.append([star_x, star_y])

        # Move stars and check for collision
        for star in stars[:]:
            star[1] += star_speed

            if star[1] > screen_height:
                stars.remove(star)

            for bullet in bullets[:]:
                if (
                        bullet[0] < star[0] + star_width
                        and bullet[0] + bullet_width > star[0]
                        and bullet[1] < star[1] + star_height
                        and bullet[1] + bullet_height > star[1]
                ):
                    bullets.remove(bullet)
                    stars.remove(star)
                    collision_counter += 1
                    explosion_sound.play()
                    score += 1  # Increase score when a star is shot down
                    hit_timer = 30  # Display the "hit" screen for 30 frames

        if hit_timer > 0:
            display_hit_screen()
            hit_timer -= 1

        if collision_counter >= 5:
            # Game over, reset the game
            collision_counter = 0
            score = 0
            bullets.clear()
            stars.clear()

        # Clear the screen
        screen.fill(black)

        # Draw the plane
        draw_plane(plane_x, plane_y)

        # Draw bullets
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])

        # Draw stars
        for star in stars:
            draw_star(star[0], star[1])

        # score

        display_score(score)

        # Update the display
        pygame.display.update()

        # Control the frame rate (60 frames per second)
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
