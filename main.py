import pygame
import constants
from character import Character



pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
pygame.display.set_caption("Game Uniregminton")

clock = pygame.time.Clock()

#movimiento de jugador
moving_left = False
moving_right = False
moving_up = False
moving_down = False

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

mob_animations = []
mob_types = ["dog", "imp", "goblin","tiny_zombie"]

animation_types = ["idle", "run"]


for mob in mob_types:
    animation_list = []
    
    for animation in animation_types:
        temp_list = []
        for i in range(2):
            img = player_image = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            if mob != "dog":
                img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)


player = Character(100, 100, mob_animations, 0)

run = True
while run:
    #fps
    clock.tick(constants.FPS)

    screen.fill(constants.BG)
    #movimiento en plano carteciano
    dx = 0
    dy = 0
    
    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED

    #Moviento de jugador
    player.move(dx, dy)
    player.update()
    player.draw(screen)
    for event in pygame.event.get():
        #salir de la ventana
        if event.type == pygame.QUIT:
            run = False
        #evento de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()

pygame.quit()