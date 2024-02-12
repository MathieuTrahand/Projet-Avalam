import pygame
import graphic_interface
import game_management


#

class InputInterface:
    def __init__(self):
        self.screen = pygame.display.set_mode(graphic_interface.windows_size)
        self.running = True
        self.quit = False
        self.clock = pygame.time.Clock()

        self.background = graphic_interface.Image(
            "Images/Interface_Login.png",
            (0.5 * graphic_interface.windows_size[0], 0.6 * graphic_interface.windows_size[1]),
            (1.33 * graphic_interface.windows_size[0], 1.33 * graphic_interface.windows_size[1])
        )

        self.input1 = graphic_interface.Input(
            0.55 * graphic_interface.windows_size[0],
            0.52 * graphic_interface.windows_size[1],
            text='Player 1',
            second_color='white'
        )
        self.ask = graphic_interface.Input(
            0.5 * graphic_interface.windows_size[0],
            0.32 * graphic_interface.windows_size[1],
            text="Noms d'utilsateur",
            text_colour='black'
        )

        self.input2 = graphic_interface.Input(
            0.55 * graphic_interface.windows_size[0],
            0.72 * graphic_interface.windows_size[1],
            text='Player 2',
            second_color='black'
        )

        self.play = graphic_interface.Button(
            "Images/bouton_play.png",
            (0.5 * graphic_interface.windows_size[0], 0.9 * graphic_interface.windows_size[1]),
            (0.25 * graphic_interface.windows_size[0], 0.25 * graphic_interface.windows_size[1])
        )

    def handling_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.quit = True
                self.running = False

            self.input1.handling_events(event)
            self.input2.handling_events(event)
            self.ask.handling_events(event)

            self.play.handling_event(event)
            if self.play.action:
                self.running = False

    def display(self):
        self.background.draw(self.screen)
        self.input1.draw(self.screen)
        self.input2.draw(self.screen)
        self.ask.draw(self.screen)
        self.play.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.display()
            self.clock.tick(60)

    def get_players(self):
        return self.input1.text.text, self.input2.text.text


class Game:
    def __init__(self, players: (str, str) = ("Player 1", "Player 2")):
        self.screen = pygame.display.set_mode(graphic_interface.windows_size)
        self.running = True
        self.clock = pygame.time.Clock()
        self.windows_size = self.screen.get_size()

        self.bg = graphic_interface.Image(
            path='IMAGES/fond écran.png',
            xy=(self.windows_size[0] // 2, self.windows_size[1] // 2),
            size=(min(self.windows_size), min(self.windows_size))
        )

        self.resume = graphic_interface.Image(
            path="IMAGES/bouton_pause.png",
            xy=(self.windows_size[0] * 0.05, 0.05 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.07, min(self.windows_size) * 0.07)
        )

        self.black_pawn = graphic_interface.Image(
            path="IMAGES/boule noir.png",
            xy=(self.windows_size[0] * 0.05, 0.24 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.05, min(self.windows_size) * 0.05)
        )

        self.white_pawn = graphic_interface.Image(
            path="IMAGES/boule blanche.png",
            xy=(self.windows_size[0] * 0.05, 0.14 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.05, min(self.windows_size) * 0.05)
        )

        self.timer = graphic_interface.Timer(
            position=(self.windows_size[0] * 0.165, self.windows_size[1] * 0.05),
            anchor='center'
        )

        self.all_piles = []
        self.create_piles()

        self.player1 = game_management.Player(name=players[0], all_piles=self.all_piles, color="blanc")
        self.player2 = game_management.Player(name=players[1], all_piles=self.all_piles, color="noir")

    def create_piles(self):
        couleur = "blanc"
        x_start = self.windows_size[0] * 0.25
        y_start = self.windows_size[1] * 0.247
        x_increment = self.windows_size[0] * 0.0625
        y_increment = self.windows_size[1] * 0.063
        all_piles_append = self.all_piles.append

        # Liste des coordonnées qui ne peuvent pas avoir de pile
        no_pile = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 7), (0, 8), (1, 0), (1, 1), (1, 2), (1, 3), (1, 8),
                   (2, 0), (2, 1), (2, 8), (3, 8), (4, 4), (5, 0), (6, 0), (6, 7), (6, 8), (7, 0), (7, 5), (7, 6),
                   (7, 7), (7, 8), (8, 0), (8, 1), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]

        index = 0

        for i in range(9):
            ligne = []
            y_position = y_start + y_increment * i
            for j in range(9):
                x_position = x_start + x_increment * j

                if (i, j) == no_pile[index]:
                    index += 1
                    nb_pawns = 0
                else:
                    nb_pawns = 1

                ligne.append(
                    game_management.PawnsPile(
                        self.screen, self.all_piles, couleur,
                        position=(x_position, y_position),
                        nb_pawns=nb_pawns,
                        pawn_distance=(x_increment, y_increment)
                    )
                )

                couleur = "noir" if couleur == "blanc" else "blanc"

            all_piles_append(ligne)

    def handling_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            for ligne in self.all_piles:
                for pile in ligne:
                    pile.handle_event(event)

    def update(self):

        # Mettre à jour le minuteur toutes les secondes
        self.timer.update_timer += self.clock.get_time()  # Temps écoulé depuis la dernière frame
        if self.timer.update_timer >= 1000:  # 1000 millisecondes = 1 seconde
            self.timer.tick()
            self.timer.update_timer = 0  # Réinitialiser le compteur

        for ligne in self.all_piles:
            for pile in ligne:
                pile.update()

        self.player1.update_score()
        self.player2.update_score()

    def display(self):
        self.bg.draw(self.screen)
        self.black_pawn.draw(self.screen)
        self.resume.draw(self.screen)
        self.white_pawn.draw(self.screen),


        self.player1.name_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.08, self.windows_size[1] * 0.11)
        )


        self.player1.score_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.08, self.windows_size[1] * 0.155)
        )

        self.player2.name_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.08, self.windows_size[1] * 0.21),
        )

        self.player2.score_text.draw(
            self.screen,
            position=(self.windows_size[0] * 0.08, self.windows_size[1] * 0.255),
        )


        self.timer.draw(self.screen)

        pile_in_drag = None
        for ligne in self.all_piles:
            for pile in ligne:
                if pile.dragging:
                    pile_in_drag = pile
                else:
                    pile.draw()

        if pile_in_drag:
            pile_in_drag.draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)
