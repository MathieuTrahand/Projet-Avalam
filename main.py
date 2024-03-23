import pygame

if __name__ == '__main__':
    pygame.init()
    from game import Game       # on le met ici car on a besoin du init() de pygame pour les fonts

    myGame = Game()
    myGame.run()

pygame.quit()







