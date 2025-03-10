import pygame
pygame.init()
from random import randint

#Cores
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (117, 117, 117)
BLACK = (0, 0, 0)

#Janela
screen = pygame.display.set_mode([960, 540])
pygame.display.set_caption("Space N")
logo_SpaceN = pygame.image.load("img/logo_space_n.png")
pygame.display.set_icon(logo_SpaceN)

#Imagens
bg_game = pygame.image.load("img/space bg game.png")
nave_jogador = pygame.image.load("img/sprite_nave_pequena.png")
nave_inimigo = pygame.image.load("img/nave_inimiga_pequena.png")
missil = pygame.image.load("img/missil_pequeno.png")

#sons
game_music = pygame.mixer.music.load("sound/AudioCoffee - Across the Stars.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

sound_missil = pygame.mixer.Sound("sound/smw_swimming.wav")
sound_missil.set_volume(0.1)

sound_collision = pygame.mixer.Sound("sound/medium-explosion-40472.wav")
sound_collision.set_volume(0.03)

#atributos personagens
pos_x_jogador = 435
pos_y_jogador = 440
vel_jogador = 5

pos_x_inimigo = randint(0, 870)
pos_y_inimigo = -74
vel_inimigo = 1

pos_x_missil = 0
pos_y_missil = -36
vel_missil = 5

#caixas de colisões
jogador_rect = nave_jogador.get_rect()
inimigo_rect = nave_inimigo.get_rect()
missil_rect = missil.get_rect()

#Relógio
clock = pygame.time.Clock()
fps = 60

def draw_rect():
    pygame.draw.rect(screen, RED, jogador_rect, 4)
    pygame.draw.rect(screen, RED, inimigo_rect, 4)
    pygame.draw.rect(screen, RED, missil_rect, 4)

def collision():
    global score, life
    global pos_x_inimigo
    global pos_y_inimigo
    global pos_x_missil

    if jogador_rect.colliderect(inimigo_rect):
        pos_x_inimigo = randint(0, 870)
        pos_y_inimigo = -74
        life -= 1
    if inimigo_rect.colliderect(missil_rect):
        sound_collision.play()
        pos_x_inimigo = randint(0, 870)
        pos_y_inimigo = -74
        pos_x_missil = -18
        score += 1

#texto
def text():
    global score, life

    font = pygame.font.SysFont(None, 50)

    text_score = font.render(f"Pontuação: {score}", True, WHITE)
    text_life = font.render(f"Vidas: {life}", True, WHITE)
    screen.blit(text_score, (0, 0))
    screen.blit(text_life, (0, 50))

#Dificuldade
def difficulty():
    global score, vel_inimigo

    if score == vel_inimigo*10:
        vel_inimigo += 1

def button(x, y):
    pygame.draw.rect(screen, GRAY, [x, y, 200, 40])
    pygame.draw.rect(screen, WHITE, [x-4, y-4, 208, 48], 4)

def button_screen_endgame():
    font = pygame.font.SysFont(None, 30)
    font_score = pygame.font.SysFont(None, 50)

    text_btn_play = font.render("Jogar novamente", True, BLACK)
    text_btn_back = font.render("Voltar para o menu", True, BLACK)
    text_score = font_score.render(f"Pontuação: {score}", True, WHITE)
    
    screen.blit(text_score, (360, 200))
    button(271, 300)
    screen.blit(text_btn_play, (285, 310))
    button(489, 300)
    screen.blit(text_btn_back, (496, 310))

def button_screen_home():
    font = pygame.font.SysFont(None, 30)
    font_title = pygame.font.SysFont(None, 60)

    text_btn_play = font.render("Jogar", True, BLACK)
    text_btn_howplay = font.render("Como jogar", True, BLACK)
    text_btn_credits = font.render("Créditos", True, BLACK)
    text_title = font_title.render("SPACE N", True, WHITE)

    screen.blit(text_title, (390, 100))
    button(380, 300)
    screen.blit(text_btn_play, (450, 310))
    button(380, 356)
    screen.blit(text_btn_howplay, (420, 366))
    button(380, 412)
    screen.blit(text_btn_credits, (435, 422))

def all_tips():
    font = pygame.font.SysFont(None, 30)

    text_tip_w = font.render("Aperte w para subir", True, WHITE)
    text_tip_s = font.render("Aperte s para descer", True, WHITE)
    text_tip_a = font.render("Aperte a para ir para a esquerda", True, WHITE)
    text_tip_d = font.render("Aperte d para ir para a esquerda", True, WHITE)
    text_tip_space = font.render("Aperte espaço para atirar", True, WHITE)
    text_tip_g = font.render("Aperte g para ver a colisão", True, WHITE)

    screen.blit(text_tip_w, (640, 0))
    screen.blit(text_tip_s, (640, 30))
    screen.blit(text_tip_a, (640, 60))
    screen.blit(text_tip_d, (640, 90))
    screen.blit(text_tip_space, (640, 120))
    screen.blit(text_tip_g, (640, 150))

def home():
    global playing, loop, time_mouse, tip, life, credit

    screen.blit(bg_game, (0, 0))
    button_screen_home()
    
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False
        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if mouse[0] > 376 and mouse[0] < 584 and mouse[1] > 296 and mouse[1] < 344:
                playing = True
                play_game()
            if time_mouse == 0 and mouse[0] > 376 and mouse[0] < 584 and mouse[1] > 352 and mouse[1] < 400:
                if tip == True:
                    tip = False
                    time_mouse = 20
                elif tip == False:
                    tip = True
                    time_mouse = 20
            if mouse[0] > 376 and mouse[0] < 584 and mouse[1] > 408 and mouse[1] < 456:
                credit = True

    if time_mouse > 0:
        time_mouse -= 1
    if tip:
        all_tips()

#Jogo
def game():
    global life, score, playing, key_g, time_g, endgame
    global pos_x_inimigo, pos_y_inimigo, vel_inimigo
    global pos_x_jogador, pos_y_jogador, vel_jogador
    global pos_x_missil, pos_y_missil, vel_missil

    #movimento do jogador
    command = pygame.key.get_pressed()
    if command[pygame.K_w] and pos_y_jogador > 0:
        pos_y_jogador -= vel_jogador
    if command[pygame.K_s] and pos_y_jogador < 440:
        pos_y_jogador += vel_jogador
    if command[pygame.K_a] and pos_x_jogador > 0:
        pos_x_jogador -= vel_jogador
    if command[pygame.K_d] and pos_x_jogador < 870:
        pos_x_jogador += vel_jogador

    #inimigo
    if pos_y_inimigo < 540:
        pos_y_inimigo += vel_inimigo
    if pos_y_inimigo >= 540:
        pos_x_inimigo = randint(0, 870)
        pos_y_inimigo = -74
        life -= 1

    #missil
    if command[pygame.K_SPACE]:
        pos_x_missil = pos_x_jogador + 37
        pos_y_missil = pos_y_jogador + 50
        sound_missil.play()
    if pos_y_missil > -36:
        pos_y_missil -= vel_missil
    if pos_y_missil <= 36:
        pos_x_missil = -18

    #Posição das caixas de colisões
    jogador_rect.x = pos_x_jogador
    jogador_rect.y = pos_y_jogador

    inimigo_rect.x = pos_x_inimigo
    inimigo_rect.y = pos_y_inimigo

    missil_rect.x = pos_x_missil
    missil_rect.y = pos_y_missil

    collision()

    #Desenhando a tela
    screen.blit(bg_game, (0, 0))
    screen.blit(missil, (pos_x_missil, pos_y_missil))
    screen.blit(nave_jogador, (pos_x_jogador, pos_y_jogador))
    screen.blit(nave_inimigo, (pos_x_inimigo, pos_y_inimigo))
    text()

    if command[pygame.K_g] and key_g == False and time_g == 0:
        key_g = True
        time_g = 20
    if command[pygame.K_g] and key_g == True and time_g == 0:
        key_g = False
        time_g = 20
    if time_g > 0:
        time_g -= 1
    if key_g:
        draw_rect()

    difficulty()
    if life < 1:
        playing = False
        endgame = True

def end_game():
    global score, playing, loop, endgame, life

    screen.blit(bg_game, (0, 0))
    button_screen_endgame()

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False
        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if mouse[0] > 267 and mouse[0] < 475 and mouse[1] > 296 and mouse[1] < 344:
                playing = True
                play_game()
                endgame = False
            if mouse[0] > 485 and mouse[0] < 693 and mouse[1] > 296 and mouse[1] < 344:
                endgame = False

def credits():
    global credit, pos_y_credits
    
    screen.blit(bg_game, (0, 0))

    command = pygame.key.get_pressed()
    if command[pygame.K_ESCAPE]:
        credit = False
        pos_y_credits = 520

    size_font = 30
    size_font_title = 40
    size_font_ESC = 60

    font = pygame.font.SysFont(None, size_font)
    font_title = pygame.font.SysFont(None, size_font_title)
    font_ESC = pygame.font.SysFont(None, size_font_ESC)

    text_sair = font_ESC.render("Aperte ESC para sair", True, WHITE)
    text_title_creator = font_title.render("Criadores", True, WHITE)
    text_credit_creator = font.render("Jonatas P. C. da Silva", True, WHITE)
    text_title_images = font_title.render("Imagens", True, WHITE)
    text_credit_images = font.render("Jonatas P. C. da Silva", True, WHITE)
    text_title_sounds = font_title.render("Sons", True, WHITE)
    text_credit_sounds = font.render("Jonatas P. C. da Silva", True, WHITE)
    text_credit_sounds2 = font.render('Music by AudioCoffee: https://www.audiocoffee.net/', True, WHITE)
    text_credit_final = font.render("Algumas imagens e sons foram tirados da internet", True, WHITE)
    text_title_instagram = font_title.render("Redes sociais", True, WHITE)
    text_credit_instagram = font.render("Instagram: @jonataspcs05", True, WHITE)
    text_credit_instagram2 = font.render("Instagram: @jonatas1603", True, WHITE)
    

    rect_text_sair = text_sair.get_rect()
    rect_text_title_creator = text_title_creator.get_rect()
    rect_text_credit_creator = text_credit_creator.get_rect()
    rect_text_title_images = text_title_images.get_rect()
    rect_text_credit_images = text_credit_images.get_rect()
    rect_text_title_sounds = text_title_sounds.get_rect()
    rect_text_credit_sounds = text_credit_sounds.get_rect()
    rect_text_credit_sounds2 = text_credit_sounds2.get_rect()
    rect_text_credit_final = text_credit_final.get_rect()
    rect_text_title_instagram = text_title_instagram.get_rect()
    rect_text_credit_instagram = text_credit_instagram.get_rect()
    rect_text_credit_instagram2 = text_credit_instagram2.get_rect()

    rect_text_sair.center = (screen.get_width() // 2, 30)
    rect_text_title_creator.center = (screen.get_width() // 2, pos_y_credits)
    rect_text_credit_creator.center = (screen.get_width() // 2, pos_y_credits + size_font_title)
    rect_text_title_images.center = (screen.get_width() // 2, pos_y_credits + (1*size_font_title) + (1*size_font) + (1*size_font_ESC))
    rect_text_credit_images.center = (screen.get_width() // 2, pos_y_credits + (2*size_font_title) + (1*size_font) + (1*size_font_ESC))
    rect_text_title_sounds.center = (screen.get_width() // 2, pos_y_credits + (2*size_font_title) + (2*size_font) + (2*size_font_ESC))
    rect_text_credit_sounds.center = (screen.get_width() // 2, pos_y_credits + (3*size_font_title) + (2*size_font) + (2*size_font_ESC))
    rect_text_credit_sounds2.center = (screen.get_width() // 2, pos_y_credits + (3*size_font_title) + (3*size_font) + (2*size_font_ESC))
    rect_text_credit_final.center = (screen.get_width() // 2, pos_y_credits + (3*size_font_title) + (4*size_font) + (3*size_font_ESC))
    rect_text_title_instagram.center = (screen.get_width() // 2, pos_y_credits + (3*size_font_title) + (5*size_font) + (4*size_font_ESC))
    rect_text_credit_instagram.center = (screen.get_width() // 2, pos_y_credits + (4*size_font_title) + (5*size_font) + (4*size_font_ESC))
    rect_text_credit_instagram2.center = (screen.get_width() // 2, pos_y_credits + (4*size_font_title) + (6*size_font) + (4*size_font_ESC))

    screen.blit(text_sair, rect_text_sair)
    screen.blit(text_title_creator, rect_text_title_creator)
    screen.blit(text_credit_creator, rect_text_credit_creator)
    screen.blit(text_title_images, rect_text_title_images)
    screen.blit(text_credit_images, rect_text_credit_images)
    screen.blit(text_title_sounds, rect_text_title_sounds)
    screen.blit(text_credit_sounds, rect_text_credit_sounds)
    screen.blit(text_credit_sounds2, rect_text_credit_sounds2)
    screen.blit(text_credit_final, rect_text_credit_final)
    screen.blit(text_title_instagram, rect_text_title_instagram )
    screen.blit(text_credit_instagram, rect_text_credit_instagram)
    screen.blit(text_credit_instagram2, rect_text_credit_instagram2)

    pos_y_credits -= vel_credits

    if pos_y_credits == -((4*size_font_title) + (6*size_font) + (4*size_font_ESC)):
        credit = False
        pos_y_credits = 520

def play_game():
    global life, score, key_g, vel_inimigo, pos_x_missil

    life = 5
    score = 0
    key_g = False
    vel_inimigo = 1
    pos_x_missil = -18

pos_y_credits = 520
vel_credits = 1

time_g = 0
time_mouse = 0
credit = False
tip = False
key_g = False
endgame = False
playing = False
loop = True
while loop:
    clock.tick(60)

    if not playing and not endgame and not credit:
        home()
    if playing:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                loop = False
        game()
    if endgame:
        end_game()
    if credit:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                loop = False
        credits()

    pygame.display.update()