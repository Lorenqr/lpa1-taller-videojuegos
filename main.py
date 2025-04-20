import pygame
import csv
import constants 
from character import Character
from weapon import Weapon
from items import Item
from world import World

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
pygame.display.set_caption("Game Uniregminton")

clock = pygame.time.Clock()

#movimiento de jugador
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#crear niveles


#fuente de letras
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 14)

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

#guardado de corazones
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.SCALE_ITEM)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.SCALE_ITEM)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.SCALE_ITEM)
#inicio de monedas
coin_image = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.SCALE_ITEM)
    coin_image.append(img)

#cargar punto
red_point = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POINT_SCALE)

#armas
bow_image = pygame.image.load("assets/images/weapons/bol2.png")
arrow_image = pygame.image.load("assets/images/weapons/bol2.png")

#imagenes de plataforma
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

#personajes
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

#informacion general
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#heart info
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    #corazones
    heart_half_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full,(10 + i * 50, 0))
        elif (player.health % 20 > 0) and heart_half_drawn == False:
            screen.blit(heart_half, (10 +i * 50, 0))
            heart_half_drawn = True
        else: 
            screen.blit(heart_empty, (10 +i * 50, 0))
    draw_text(f"Score: {player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 130, 15)

#mundo vacio
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
with open("levels/level1_data.csv", newline="") as csvFile:
    reader = csv.reader(csvFile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list)

def draw_grid():
    for x in range(100):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))

#visa visual
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

#jugador
player = Character(100, 100, 30, mob_animations, 0)

#enemigo
enemy = Character(200, 300, 100, mob_animations, 1)

#arma
bow = Weapon(bow_image, arrow_image)

#lista de enemigos
enemy_list = []
enemy_list.append(enemy)

#group
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 145, 23, 0, coin_image)
item_group.add(score_coin)

point = Item(200, 200, 1, [red_point])
item_group.add(point)
coin = Item(400, 400, 0, coin_image)
item_group.add(coin)

#motor de juego
run = True
while run:
    #fps
    clock.tick(constants.FPS)

    screen.fill(constants.BG)
    
    draw_grid()
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

    for enemy in enemy_list:
        enemy.update()

    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(player)

    #dibujar mundo
    world.draw(screen)
    #dibujar enemigo
    for enemy in enemy_list:
        enemy.draw(screen)

    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)





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