import pygame
import graphic_interface
import game_management
import bot
import tests

import tests


class InputInterface:
    def __init__(self):
        self.screen = pygame.display.set_mode(graphic_interface.windows_size)
        self.running = True
        self.quit = False
        self.clock = pygame.time.Clock()
        self.ask = graphic_interface.Input(
            0.5 * graphic_interface.windows_size[0],
            0.3 * graphic_interface.windows_size[1],
            text="Noms d'utilisateur",
            text_colour='Black'
        )

        self.background = graphic_interface.Image(
            "Images/Interface_Login.png",
            (0.5 * graphic_interface.windows_size[0], 0.6 * graphic_interface.windows_size[1]),
            (1.33 * graphic_interface.windows_size[0], 1.33 * graphic_interface.windows_size[1])
        )
        self.parchemin_button = graphic_interface.Button(
            'IMAGES/parchemin.png',
            (0.92 * graphic_interface.windows_size[0], 0.06 * graphic_interface.windows_size[1]),
            (0.1 * graphic_interface.windows_size[0], 0.1 * graphic_interface.windows_size[1])
        )

        self.input1 = graphic_interface.Input(
            0.55 * graphic_interface.windows_size[0],
            0.52 * graphic_interface.windows_size[1],
            text='Player 1',
            second_color='white'
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
        self.parchemin_button.draw(self.screen)
        self.input1.draw(self.screen)
        self.input2.draw(self.screen)
        self.play.draw(self.screen)
        self.ask.draw(self.screen)
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
        self.is_paused = False
        self.is_rules = False
        self.is_over = False

        self.bg = graphic_interface.Image(
            path='IMAGES/fond écran.png',
            xy=(self.windows_size[0] // 2, self.windows_size[1] // 2),
            size=(min(self.windows_size), min(self.windows_size))
        )
        self.parchemin_button = graphic_interface.Button(
            path='IMAGES/parchemin.png',
            xy=(self.windows_size[0]*0.92, self.windows_size[1]*0.06),
            size=(min(self.windows_size)*0.1, min(self.windows_size)*0.1)
        )

        self.pause_button = graphic_interface.Button(
            path="IMAGES/bouton_pause.png",
            xy=(self.windows_size[0] * 0.05, 0.05 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.07, min(self.windows_size) * 0.07)
        )

        self.black_pawn = graphic_interface.Image(
            path="IMAGES/boule noir.png",
            xy=(self.windows_size[0] * 0.05, 0.14 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.05, min(self.windows_size) * 0.05)
        )

        self.white_pawn = graphic_interface.Image(
            path="IMAGES/boule blanche.png",
            xy=(self.windows_size[0] * 0.05, 0.24 * self.windows_size[1]),
            size=(min(self.windows_size) * 0.05, min(self.windows_size) * 0.05)
        )

        self.timer = graphic_interface.Timer(
            position=(self.windows_size[0] * 0.165, self.windows_size[1] * 0.05),
            anchor='center'
        )

        self.all_piles = []
        self.possible_moves = {}

        self.player1 = game_management.Player(name=players[0], possible_moves=self.possible_moves, color="noir")
        self.player2 = game_management.Player(name=players[1], possible_moves=self.possible_moves, color="blanc")

        self.pawn_distance = (self.windows_size[0] * 0.0625, self.windows_size[1] * 0.063)
        self.create_piles()

        self.bot = bot.Bot(self.player2, self.player1, self.possible_moves)





    def create_piles(self):
        self.display()

        couleur = "blanc"
        x_start = self.windows_size[0] * 0.25
        y_start = self.windows_size[1] * 0.247
        x_increment, y_increment = self.pawn_distance
        #all_piles_append = self.all_piles.append

        all_piles = [[None for _ in range(9)] for i in range(9)]

        # Liste des coordonnées qui ne peuvent pas avoir de pile
        no_pile = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 7), (0, 8), (1, 0), (1, 1), (1, 2), (1, 3), (1, 8),
                   (2, 0), (2, 1), (2, 8), (3, 8), (4, 4), (5, 0), (6, 0), (6, 7), (6, 8), (7, 0), (7, 5), (7, 6),
                   (7, 7), (7, 8), (8, 0), (8, 1), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]

        index = 0

        for i in range(9):
            y_position = y_start + y_increment * i
            for j in range(9):
                x_position = x_start + x_increment * j

                if (i, j) == no_pile[index]:
                    index += 1
                    nb_pawns = 0
                else:
                    nb_pawns = 1

                pawn_pile = game_management.PawnsPile(
                        game=self,
                        color=couleur,
                        initial_position=(x_position, y_position),
                        nb_pawns=nb_pawns,
                        matrix_position=(i, j)
                    )

                all_piles[i][j] = pawn_pile

                self.possible_moves[pawn_pile] = []

                self.add_edges(pawn_pile, all_piles)

                self.display()

                couleur = "noir" if couleur == "blanc" else "blanc"

    def add_edges(self, actual_pile, all_piles):
        i, j = actual_pile.matrix_position

        if j > 0:  # si on est pas tout à gauche de la matrice
            pile = all_piles[i][j - 1]     # on ajoute celui à gauche
            if 0 < pile.nb_pawns:               # si il y a des pions dedans
                self.possible_moves[actual_pile].append(pile)  # on l'ajoute à la liste des piles où on peut déposer des pions
                self.possible_moves[pile].append(actual_pile)  # et on ajoute la pile actuelle à la liste de l'autre piles

            if i > 0:  # si en plus on est pas tout en haut
                pile = all_piles[i - 1][j - 1]  # on s'occupe de la diagonale haut gauche
                if 0 < pile.nb_pawns:
                    self.possible_moves[actual_pile].append(pile)
                    self.possible_moves[pile].append(actual_pile)

        if i > 0:  # si on est pas tout en haut
            pile = all_piles[i - 1][j]         # on ajoute celui au-dessus
            if 0 < pile.nb_pawns:
                self.possible_moves[actual_pile].append(pile)
                self.possible_moves[pile].append(actual_pile)

            if j < 8:  # si en plus on est pas tout à droite
                pile = all_piles[i - 1][j + 1]  # on s'occupe de la diagonale haut droite
                if 0 < pile.nb_pawns:
                    self.possible_moves[actual_pile].append(pile)
                    self.possible_moves[pile].append(actual_pile)

    def check_game_status(self):

        for key, value in self.possible_moves:
            if value:
                return False

        return True

    def handling_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if self.is_paused:
                #self.running = False
                print(self.possible_moves)
                self.is_paused = False


            else:

                # gestion des piles :
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    for pile in self.possible_moves.keys():
                        if pile.rect.collidepoint(event.pos):
                            pile.handle_press()
                            break

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for pile in self.possible_moves.keys():

                        if pile.dragging:
                            pile.handle_release()
                            break

                self.pause_button.handling_event(event)

                if self.pause_button.action:
                    self.is_paused = True

    def update(self):

        # Mettre à jour le minuteur toutes les secondes
        self.timer.update_timer += self.clock.get_time()  # Temps écoulé depuis la dernière frame
        if self.timer.update_timer >= 1000:  # 1000 millisecondes = 1 seconde
            self.timer.tick()
            self.timer.update_timer = 0  # Réinitialiser le compteur

        for pile in self.possible_moves.keys():
            pile.update()

        self.player1.update_score()
        self.player2.update_score()

    def display(self):
        self.bg.draw(self.screen)
        self.black_pawn.draw(self.screen)
        self.pause_button.draw(self.screen)
        self.parchemin_button.draw(self.screen)
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

        for pile in self.possible_moves.keys():
            if pile.dragging or pile.start_time is not None:  # Si le joueur ou le bot est en train de déplacer une pile
                pile_in_drag = pile  # On la stocke pour l'afficher en dernier et qu'elle apparaisse au-dessus
            else:
                pile.draw()

        if pile_in_drag:
            pile_in_drag.draw()

        pygame.display.flip()

    def pause_display(self):

        # Mini gestion d'évenements pour le menu pause
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
    def run(self):
        while self.running:

            if self.is_over:
                pass

            elif self.is_paused:
                self.pause_display()

            elif self.is_rules:
                pass

            else:
                self.handling_events()
                self.update()
                self.display()



            self.clock.tick(60)
