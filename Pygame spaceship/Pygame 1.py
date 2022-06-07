import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1500, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slave 1 (Boba Fett) vs. Millennium Falcon (Han Solo)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (255, 0, 0)
GREEN = (250, 250, 0)

BORDER = pygame.Rect(0, HEIGHT//2, WIDTH, 8)

SOUND_FIRE = pygame.mixer.Sound(os.path.join("ASSETS", "Quadlaser turret fire.mp3")) 
SOUND_HIT = pygame.mixer.Sound(os.path.join("ASSETS", "XWing explode.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 50)

FPS = 60
VEL = 10
BULLET_VEL = 10
MAX_BULLETS = 10000000000
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 75

GREEN_HIT = pygame.USEREVENT + 1
GREY_HIT = pygame.USEREVENT + 2

Ship1_image = pygame.image.load(os.path.join("ASSETS", "Ship1.png"))
Ship1 = pygame.transform.rotate(pygame.transform.scale(Ship1_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

Ship2_image = pygame.image.load(os.path.join("ASSETS", "Ship2.png"))
Ship2 = pygame.transform.rotate(pygame.transform.scale(Ship2_image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "Space.webp")), (WIDTH, HEIGHT))


def draw_window(grey, green, grey_bullets, green_bullets, grey_health, green_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    grey_health_text = HEALTH_FONT.render("Health: " + str(grey_health), 1, WHITE)
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, WHITE)
    WIN.blit(grey_health_text, (WIDTH - grey_health_text.get_width() - 10, 10))
    WIN.blit(green_health_text, (10, 10))
    
    WIN.blit(Ship1, (grey.x, grey.y ))
    WIN.blit(Ship2, (green.x, green.y))
    pygame.display.update()

    for bullet in grey_bullets:
        pygame.draw.rect(WIN, GREY, bullet)

    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)
    
    pygame.display.update()

def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - VEL > 0: #left
        green.x -= VEL
    if keys_pressed[pygame.K_d] and green.x + VEL + green.height - 1000 < BORDER.y: #right
        green.x += VEL
    if keys_pressed[pygame.K_w] and green.y - VEL > 500: #up
        green.y -= VEL
    if keys_pressed[pygame.K_s] and green.y + VEL + green.width < HEIGHT: #down
        green.y += VEL

def grey_handle_movement(keys_pressed, grey):
    if keys_pressed[pygame.K_LEFT] and grey.x - VEL > 0: #left
        grey.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and grey.x + VEL + grey.width < WIDTH: #right
        grey.x += VEL
    if keys_pressed[pygame.K_UP] and grey.y - VEL > 0: #up
        grey.y -= VEL
    if keys_pressed[pygame.K_DOWN] and grey.y + VEL + grey.height < 480: #down
        grey.y += VEL

def handle_bullets(green_bullets, grey_bullets, green, grey):
    for bullet in green_bullets:
        bullet.y -= BULLET_VEL
        if grey.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREY_HIT))
            green_bullets.remove(bullet)

    for bullet in grey_bullets:
        bullet.y += BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            grey_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    
    grey = pygame.Rect(750, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(750, 900, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    grey_bullets = []
    green_bullets = []

    green_health = 15
    grey_health = 15

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x + green.width, green.y + green.height//2 - 2, 10, 5 )
                    green_bullets.append(bullet)
                    SOUND_FIRE.play()

                if event.key == pygame.K_RSHIFT and len(grey_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(grey.x, grey.y + grey.height//2 - 2, 10, 5 )
                    grey_bullets.append(bullet)
                    SOUND_FIRE.play()

            if event.type == GREY_HIT:
                grey_health -= 1
                SOUND_HIT.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                SOUND_HIT.play()

        winner_text = ""
        if grey_health <= 0:
            winner_text = "Slave 1 (Boba Fett) wins!"

        if green_health <= 0:
            winner_text = "The Millennium Falcon (Han Solo) wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        green_handle_movement(keys_pressed, green)
        grey_handle_movement(keys_pressed, grey)

        handle_bullets(green_bullets, grey_bullets, green, grey)

        draw_window(grey, green, grey_bullets, green_bullets, grey_health, green_health)
    
    main()

if __name__ == "__main__":
    main()
