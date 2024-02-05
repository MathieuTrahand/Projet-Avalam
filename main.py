import pygame

if __name__ == '__main__':
    pygame.init()
    from game import Game, InputInterface        # on le met ici car on a besoin du init() de pygame pour les fonts
    inputInterface = InputInterface()

    inputInterface.run()

    if not inputInterface.quit:
        myGame = Game(inputInterface.get_players())
        myGame.run()

pygame.quit()







