import pygame, sys
pygame.init()
from graphic_interface import Image,fonts,windows_size

a=(700,700)
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode(a)
base_font=fonts['basic_font']
user_text='Pseudo Player 1'
user_text_2='Pseudo Player 2'
input="Entrez les noms d'utilisateur"
input_rect_1=pygame.Rect(0.37*a[0],0.49*a[1],100,50)
input_rect_2=pygame.Rect(0.37*a[0],0.675*a[1],100,50)
input_rect_3=pygame.Rect(120,120,80,32)
color_active=pygame.Color('lightskyblue3')
color_passive=pygame.Color('white')
color=color_passive

background=Image("Images\Interface_Login.png",(300,360),(1.25*a[0],1.25*a[1]))


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
    pygame.draw.rect(screen,color,input_rect_3,8)

    text_surface=base_font.render(user_text,True,(255,255,255))
    text_surface2 = base_font.render(user_text_2, True, (0, 0, 0))
    text_surface3=base_font.render(input, True, (255, 0, 0))

    background.draw(screen)




    screen.blit(text_surface,(input_rect_1.x+5,input_rect_1.y+5))
    screen.blit(text_surface2, (input_rect_2.x + 5, input_rect_2.y + 5))
    screen.blit(text_surface3,(input_rect_3.x + 5, input_rect_3.y + 5))
    input_rect_1.w=max(100,text_surface.get_width()+10)
    input_rect_2.w = max(100, text_surface2.get_width() + 10)


    pygame.display.flip()
    clock.tick(60)