import pygame
import random
import sys
import time

WIDTH, HEIGHT = 600, 800
FPS = 60
MAX_LASERS = 6
ENEMY_SPEED = 3
ENEMY_SPAWN_INTERVAL = 40
FIRE_COOLDOWN = 0.2


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space invaders clone")
clock = pygame.time.Clock()

BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
NEON_BLUE = ( 50, 200, 255)
NEON_PINK = (255,  50, 200)
NEON_GREEN = ( 50, 255, 100)
font_small = pygame.font.SysFont("Consolas", 28)
font_large = pygame.font.SysFont("Consolas", 48) #i <3 consolas fuck you verdana


pygame.mixer.music.load("assets/fred3.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
laser_sound     = pygame.mixer.Sound("assets/explosion.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
laser_sound.set_volume(0.2)
explosion_sound.set_volume(0.3)

favicon = pygame.image.load('assets/supercoollogofr.png')
pygame.display.set_icon(favicon)

#yay much cool inits
player = pygame.Rect(WIDTH//2 - 20, HEIGHT - 80, 40, 40)
player_speed = 6
lasers = []
enemies = []
explosions = []
enemy_timer = 0
score = 0
high_score = 0
game_over = False
last_shot = 0


#do shit
def draw_starfield():
    for _ in range(2):
        x = random.randrange(0, WIDTH)
        y = random.randrange(-10, HEIGHT)
        color = random.choice([WHITE, NEON_BLUE, NEON_PINK])
        r = random.choice((1,2))
        pygame.draw.circle(screen, color, (x,y), r)

def draw_player():
    pts = [(player.centerx, player.top),
           (player.left, player.bottom),
           (player.right, player.bottom)]
    pygame.draw.polygon(screen, NEON_BLUE, pts)
    pygame.draw.polygon(screen, WHITE, pts, 2)

def draw_enemy(fr):
    pts = [(fr.centerx, fr.bottom),
           (fr.left, fr.top),
           (fr.right, fr.top)]
    pygame.draw.polygon(screen, NEON_PINK, pts)
    pygame.draw.polygon(screen, WHITE, pts, 2)

def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    return pygame.Rect(x, -40, 40, 40)

def draw_laser(skibidi):
    pygame.draw.rect(screen, NEON_GREEN, skibidi)
    pygame.draw.rect(screen, WHITE, skibidi, 1)

def draw_explosions():
    for exp in explosions[:]:
        x, y, r, max_r = exp
        if r < max_r:
            pygame.draw.circle(screen, NEON_PINK, (x,y), int(r), 2)
            exp[2] += 2
        else:
            explosions.remove(exp)

running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    draw_starfield()

    if not game_over:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and player.left  > 0:     player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH: player.x += player_speed
        if keys[pygame.K_SPACE] and len(lasers) < MAX_LASERS and time.time() - last_shot > FIRE_COOLDOWN:
            l = pygame.Rect(player.centerx - 3, player.top - 20, 6, 20)
            lasers.append(l)
            laser_sound.play()
            last_shot = time.time()

        for l in lasers[:]:
            l.y -= 10
            if l.bottom < 0:
                lasers.remove(l)

        enemy_timer += 1
        if enemy_timer > ENEMY_SPAWN_INTERVAL:
            enemy_timer = 0
            enemies.append(spawn_enemy())

        for e in enemies[:]:
            e.y += ENEMY_SPEED
            if e.top > HEIGHT:
                game_over = True
                #please work im begging
            
            for l in lasers[:]:
                if l.colliderect(e):
                    lasers.remove(l)
                    enemies.remove(e)
                    explosions.append([e.centerx, e.centery, 0, 30])
                    explosion_sound.play()
                    score += 1
                    if score > high_score:
                        high_score = score
                    break
                #i hate everything
        draw_player()
        for e in enemies:   draw_enemy(e)
        for l in lasers:    draw_laser(l)
        draw_explosions()

        score_surf      = font_small.render(f"Score: {score}", True, WHITE)
        high_score_surf = font_small.render(f"PB: {high_score}", True, WHITE)
        screen.blit(score_surf, (10, 10))
        screen.blit(high_score_surf, (WIDTH - high_score_surf.get_width() - 10, 10))

    else:
        over_surf  = font_large.render("GAME OVER", True, NEON_PINK)
        retry_surf = font_small.render("Press R to Retry", True, WHITE)
        screen.blit(over_surf,  (WIDTH//2 - over_surf.get_width()//2, HEIGHT//2 - 60))
        screen.blit(retry_surf, (WIDTH//2 - retry_surf.get_width()//2, HEIGHT//2 + 10))
        for thing in pygame.event.get():
            if thing.type == pygame.QUIT:
                running = False

        if pygame.key.get_pressed()[pygame.K_r]:
            enemies.clear(); lasers.clear(); explosions.clear()
            score = 0; game_over = False
            player.x = WIDTH//2 - player.width//2

    pygame.display.flip()

pygame.quit()
sys.exit()
