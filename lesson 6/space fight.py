import pygame
import os
 
pygame.font.init()
pygame.mixer.init()

WIDTH=900
HEIGHT=500

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space game")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

RED_HIT = pygame.USEREVENT+1
YELLOW_HIT = pygame.USEREVENT+2

BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT) # x, y, width, length

HEALTH_FONT=pygame.font.SysFont("Comicsans",40)
WINNER_FONT=pygame.font.SysFont("Georgia",100)

MAX_BULLETS=3
FPS=60 #frame per second
VEL=5 #speed of the spaceship movement
BULLET_VEL=7 #speed of bullets
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40

YELLOW_SPACESHIP_IMAGE = pygame.image.load("spaceship_yellow.png")
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)

RED_SPACESHIP_IMAGE = pygame.image.load("Spaceship_red.png")
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

SPACE = pygame.transform.scale(pygame.image.load("space.png"), (WIDTH,HEIGHT))

def draw_window(red,yellow,red_bullets,yellow_bullets,yellow_health,red_health):
    screen.blit(SPACE,(0,0))
    pygame.draw.rect(screen,BLACK,BORDER)

    red_health_text=HEALTH_FONT.render("HEALTH:" +str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("HEALTH:" +str(yellow_health),1,WHITE)

    screen.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    screen.blit(yellow_health_text,(10,10))

    screen.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    screen.blit(RED_SPACESHIP,(red.x,red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(screen,YELLOW,bullet)

    for bullet in red_bullets:
        pygame.draw.rect(screen,RED,bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x -VEL > 0: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x : #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y >0 : #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT-15: #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x -VEL > BORDER.x+BORDER.width: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH : #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y >0 : #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT-15: #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    screen.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) #5000 miliseconds which is 5 seconds


def main():
    red=pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    red_bullets=[]
    yellow_bullets=[]

    red_health=10
    yellow_health=10

    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():


            if event.type==pygame.QUIT:
                run = False
                pygame.quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 - 2, 10,5)
                    yellow_bullets.append(bullet)

                if event.key==pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet=pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10,5)
                    red_bullets.append(bullet)
            
            if event.type==RED_HIT:
                red_health -= 1

            if event.type==YELLOW_HIT:
                yellow_health -= 1

        winner_text= ""
        if red_health <= 0 :
            winner_text="Yellow Wins"

        if yellow_health <= 0 :
            winner_text="Red Wins"

        if winner_text != "":
            draw_window(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,yellow_health,red_health)

    main()

if __name__=="__main__":
    main()