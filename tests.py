import pygame
import graphic_interface
import game_management


class Game:
    def __init__(self, surface, bg_color="white"):
        self.screen = surface
        self.running = True
        self.clock = pygame.time.Clock()
        self.bg_color = bg_color
        self.windows_size = self.screen.get_size()

        self.board = graphic_interface.Image(
            path="IMAGES/plateau_avalam.png",
            xy=(self.windows_size[0] // 2, self.windows_size[1] // 2 + 0.08 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.7, min(self.windows_size) * 0.7)
        )

        self.player1 = game_management.Player(name="Player 1")
        self.player2 = game_management.Player(name="Player 2")


    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        """if clique:
                fichier.clique() --> va gérer le clique dans un autre fichier
                                     sur colonne ? Maintenu ? => Gérer drag and drop
                                     sur bouton pause ? """

    def update(self):
        "timer update"
        "gestion drage and drop ??? Jsp si ça se fera là aussi ou pas à voir"

    def display(self):
        self.screen.fill(self.bg_color)
        self.board.draw(self.screen)

        pygame.draw.line(surface=screen,
                         color="black",
                         start_pos=(0, self.windows_size[1] * 0.2),
                         end_pos=(self.windows_size[0], self.windows_size[1] * 0.2),
                         width=3
                         )

        self.player1.text.draw(
            screen,
            position=(self.windows_size[0] * 0.14, self.windows_size[1] * 0.02)
        )

        self.player2.text.draw(
            screen,
            position=(self.windows_size[0] * 0.86, self.windows_size[1] * 0.02),
            anchor='topright'
        )



        """gestion des persos : noms et couleur"""
        "gestion de l'affichage du temps"
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)


screen = pygame.display.set_mode(graphic_interface.windows_size)
game = Game(screen)
game.run()

pygame.quit()
