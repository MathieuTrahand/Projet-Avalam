import pygame
import graphic_interface
import game_management


class InputInterface:
    def __init__(self, game):
        self.game = game

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False

    def update(self):
        pass

    def display(self):
        pass


class Game:
    def __init__(self, bg_color="white"):
        self.screen = pygame.display.set_mode(graphic_interface.windows_size)
        self.running = True
        self.clock = pygame.time.Clock()
        self.bg_color = bg_color
        self.windows_size = self.screen.get_size()
        self.window = "game"

        self.board = graphic_interface.Image(
            path="IMAGES/plateau_avalam.png",
            xy=(self.windows_size[0] // 2, self.windows_size[1] // 2 + 0.08 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.7, min(self.windows_size) * 0.7)
        )
        self.black_pawn = graphic_interface.Image(
            path="IMAGES/boule noir.png",
            xy=(self.windows_size[0] // 1.08, 0.07 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.1, min(self.windows_size) * 0.1)
        )
        self.white_pawn = graphic_interface.Image(
            path="IMAGES/boule blanche.png",
            xy=(self.windows_size[0] * 0.07, 0.07 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.1, min(self.windows_size) * 0.1)
        )

        self.timer = graphic_interface.Timer(
            position=(self.windows_size[0]/2, self.windows_size[1]*0.08),
            anchor='center'
        )

        self.all_piles = []
        self.create_piles()

        self.player1 = game_management.Player(name="Player 1", all_piles=self.all_piles, color="blanc")
        self.player2 = game_management.Player(name="Player 2", all_piles=self.all_piles, color="noir")

    def create_piles(self):
        couleur = "blanc"
        for i in range(6):
            self.all_piles.append(game_management.PileDePions(self.screen, self.all_piles, couleur,
                                                              (140 + 37 * i, 295), 1))
            if couleur == "blanc":
                couleur = "noir"
            else:
                couleur = "blanc"

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            for pile in self.all_piles:
                pile.handle_event(event)

        """if clique:
                fichier.clique() --> va gérer le clique dans un autre fichier
                                     sur colonne ? Maintenu ? => Gérer drag and drop
                                     sur bouton pause ? """

    def update(self):

        # Mettre à jour le minuteur toutes les secondes
        self.timer.update_timer += self.clock.get_time()  # Temps écoulé depuis la dernière frame
        if self.timer.update_timer >= 1000:  # 1000 millisecondes = 1 seconde
            self.timer.tick()
            self.timer.update_timer = 0  # Réinitialiser le compteur

        for pile in self.all_piles:
            pile.update()

        self.player1.update_score()
        self.player2.update_score()

        "gestion drage and drop ??? Jsp si ça se fera là aussi ou pas à voir"

    def display(self):
        self.screen.fill(self.bg_color)
        self.board.draw(self.screen)
        self.black_pawn.draw(self.screen)

        self.white_pawn.draw(self.screen),
        pygame.draw.line(surface=self.screen,
                         color="black",
                         start_pos=(0, self.windows_size[1] * 0.2),
                         end_pos=(self.windows_size[0], self.windows_size[1] * 0.2),
                         width=3
                         )

        self.player1.name_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.14, self.windows_size[1] * 0.04)
        )

        self.player1.score_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.14, self.windows_size[1] * 0.1)
        )

        self.player2.name_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.86, self.windows_size[1] * 0.04),
            anchor='topright'
        )

        self.player2.score_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.86, self.windows_size[1] * 0.1),
            anchor='topright'
        )

        self.timer.draw(self.screen)

        for pile in self.all_piles:
            pile.draw()

        pygame.display.flip()

    def run(self):
        while self.running:

            if self.window == "input interface":
                interface = InputInterface(self)

                interface.handling_events()
                interface.update()
                interface.display()
                self.clock.tick(60)

            elif self.window == "game":
                self.handling_events()
                self.update()
                self.display()
                self.clock.tick(60)
