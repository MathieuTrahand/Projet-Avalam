import pygame as pygame
from pygame.examples.moveit import WIDTH

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
VERT = (158, 253, 56)
ORANGE = (237, 127, 16)
ROUGE = (255, 0, 0)
# Définition de la taille de la fenêtre
WINDOW_TAILLE = (700, 700)

# Création de la fenêtre
screen = pygame.display.set_mode(WINDOW_TAILLE)
pygame.display.set_caption("AVALAM")

# Définition de la police d'écriture
font = pygame.font.SysFont("arialblack", int(0.04*WIDTH))
bb_font = pygame.font.SysFont("arialblack", int(0.025*WIDTH))
big_font = pygame.font.SysFont("arialblack", int(0.045*WIDTH))
error_font = pygame.font.SysFont("Consolas", int(0.03*WIDTH))



#définition des images
Fond_image=pygame.image.load("IMAGES/Fond_blanc.png").convert_alpha()
Fond_image=pygame.transform.scale(Fond_image,(700,700))
plateau_image=pygame.image.load("IMAGES/plateau_avalam.png").convert_alpha()
plateau_image=pygame.transform.scale(plateau_image,(550,550))
personnage_image=pygame.image.load("IMAGES/personnage.png").convert_alpha()
personnage_image=pygame.transform.scale(personnage_image,(70,70))
personnage2_image=pygame.image.load("IMAGES/personnage2.png").convert_alpha()
personnage2_image=pygame.transform.scale(personnage2_image,(70,70))



def draw_text(text:str, font, text_col:tuple, bg_col:tuple, x:float, y:float, screen) -> None:
    bg_rect = pygame.Rect(x, y, font.size(text)[0] + 5, font.size(text)[1] + 10)
    pygame.draw.rect(screen, bg_col, bg_rect)
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


running = True

while running:
    screen.blit(Fond_image, (0, 0))
    screen.blit(personnage_image, (10, 20))
    screen.blit(personnage2_image, (610, 20))
    pygame.draw.line(screen, NOIR, (WIDTH / 1000, WIDTH / 6.5), (WIDTH / 200 + WIDTH / 0.5, WIDTH / 6.5), 3)
    draw_text('PSEUDO 1', big_font, NOIR, BLANC, WIDTH / 7, WIDTH - WIDTH / 1.07, screen)
    draw_text('BOT', big_font, NOIR, BLANC, WIDTH / 1.2, WIDTH - WIDTH / 1.07, screen)
    screen.blit(plateau_image, (75, 120))
    pygame.display.flip()

    for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running=False

pygame.quit()