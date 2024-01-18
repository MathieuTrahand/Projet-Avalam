import pygame

if __name__ == '__main__':
    pygame.init()
    from game import Game
    myGame = Game()
    myGame.run()

pygame.quit()







