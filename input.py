import pygame, sys
pygame.init()
from graphic_interface import Image,fonts,windows_size

a=(600,600)
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode(a)
base_font=fonts['little_font']
user_text='Pseudo Player 1'
user_text_2='Pseudo Player 2'
coeff,coeff2=0.0006,0.0008
diff=a[0]-600
x1,x2,y1,y2=0.45,0.45,0.50,0.69

input_rect_1=pygame.Rect((x1-coeff*diff)*a[0],(y1-coeff*diff)*a[1],100,50)
input_rect_2=pygame.Rect((x2-coeff*diff)*a[0],(y2-coeff2*diff)*a[1],100,50)
input_rect_3=pygame.Rect(120,120,80,32)
#color_active=pygame.Color('lightskyblue3')
color_passive=pygame.Color('white')
color=color_passive

background=Image("Images\Interface_Login.png",(300,360),(1.25*a[0],1.25*a[1]))
login=Image("Images\LOGIN.png",(280,250),(400,400))


clic1, clic2=False,False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect_1.collidepoint(event.pos):
                  clic1=True
                  user_text=''
            else:
                  clic1=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect_2.collidepoint(event.pos):
                  clic2=True
                  user_text_2=''
            else:
                  clic2=False

        if event.type==pygame.KEYDOWN:
            if clic1==True:
                if event.key==pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text+=event.unicode
        if event.type==pygame.KEYDOWN:
            if clic2==True:
                if event.key==pygame.K_BACKSPACE:
                    user_text_2 = user_text_2[:-1]
                else:
                    user_text_2+=event.unicode


    #if active1:
       #color=color_active
    #else:
       #color=color_passive

    #if active2:
       #color=color_active
    #else:
       #color=color_passive


    #pygame.draw.rect(screen,color,input_rect_1,8)
    #pygame.draw.rect(screen, color, input_rect_2, 8)
    #pygame.draw.rect(screen,color,input_rect_3,8)

    text_surface=base_font.render(user_text,True,(135,135,135))
    text_surface2 = base_font.render(user_text_2, True, (135, 135, 135))


    background.draw(screen)
    login.draw(screen)




    screen.blit(text_surface,(input_rect_1.x+5,input_rect_1.y+5))
    screen.blit(text_surface2, (input_rect_2.x + 5, input_rect_2.y + 5))
    input_rect_1.w=max(100,text_surface.get_width()+10)
    input_rect_2.w = max(100, text_surface2.get_width() + 10)


    pygame.display.flip()
    clock.tick(60)