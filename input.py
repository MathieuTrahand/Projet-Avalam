import pygame, sys
from graphic_interface import Image

pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode([600,600])
base_font=pygame.font.Font(None,28)
user_text='Pseudo Player 1'
user_text_2='Pseudo Player 2'
input_rect_1=pygame.Rect(280,225,140,32)
input_rect_2=pygame.Rect(280,385,140,32)
color_active=pygame.Color('lightskyblue3')
color_passive=pygame.Color('white')
color=color_passive

background=Image("")
background=pygame.image.load("INTERFAACE.png").convert()
white=pygame.image.load("pion_blanc_1.png").convert()
black=pygame.image.load("pion_noir_2.png").convert()

active1, active2=False,False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect_1.collidepoint(event.pos):
                  active1=True
                  user_text=''
            else:
                  active1=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect_2.collidepoint(event.pos):
                  active2=True
                  user_text_2=''
            else:
                  active2=False

        if event.type==pygame.KEYDOWN:
            if active1==True:
                if event.key==pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text+=event.unicode
        if event.type==pygame.KEYDOWN:
            if active2==True:
                if event.key==pygame.K_BACKSPACE:
                    user_text_2 = user_text_2[:-1]
                else:
                    user_text_2+=event.unicode

    screen.fill((0,0,0))
    if active1:
       color=color_active
    else:
       color=color_passive

    if active2:
       color=color_active
    else:
       color=color_passive

    pygame.draw.rect(screen,color,input_rect_1,8)
    pygame.draw.rect(screen, color, input_rect_2, 8)

    text_surface=base_font.render(user_text,True,(0,0,0))
    text_surface2 = base_font.render(user_text_2, True, (255, 255, 255))

    screen.blit(background, (-700, -100))
    white = pygame.transform.scale(white, (70,70))
    black=pygame.transform.scale(black,(70,70))

    screen.blit(white, (200, 200))
    screen.blit(black,(200,400))



    screen.blit(text_surface,(input_rect_1.x+5,input_rect_1.y+5))
    screen.blit(text_surface2, (input_rect_2.x + 5, input_rect_2.y + 5))
    input_rect_1.w=max(100,text_surface.get_width()+10)
    input_rect_2.w = max(100, text_surface2.get_width() + 10)


    pygame.display.flip()
    clock.tick(60)