import pygame

if __name__ == '__main__':
    pygame.init()
    from game import Game, InputInterface        # on le met ici car on a besoin du init() de pygame pour les fonts
    inputInterface = InputInterface()
    myGame = Game()

    inputInterface.run()
    myGame.run()

pygame.quit()







