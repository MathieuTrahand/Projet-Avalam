import pygame
import graphic_interface
import game_management
import bot


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

        self.rightfleche_button = graphic_interface.Button(
            path='IMAGES/fleche_droite.png',
            xy=(self.windows_size[0]*0.92, self.windows_size[1]*0.06),
            size=(min(self.windows_size)*0.1, min(self.windows_size)*0.1)
        )

        self.leftfleche_button = graphic_interface.Button(
            path='IMAGES/fleche_gauche.png',
            xy=(self.windows_size[0] * 0.92, self.windows_size[1] * 0.06),
            size=(min(self.windows_size) * 0.1, min(self.windows_size) * 0.1)
        )

        self.pagepause_image = graphic_interface.Image(
            path='IMAGES/menu_pause.png',
            xy=(self.windows_size[0]//2, self.windows_size[1]//2),
            size=(self.windows_size[0]//1.2, self.windows_size[1]//2)
        )

        self.quit_button = graphic_interface.Button(
            path='IMAGES/quitter_.png',
            xy=(self.windows_size[0]*0.72, self.windows_size[1]*0.68),
            size=(min(self.windows_size)*0.15, min(self.windows_size)*0.07)
        )

        self.go_back_button = graphic_interface.Button(
            path='IMAGES/reprendre_.png',
            xy=(self.windows_size[0] * 0.3, self.windows_size[1] * 0.68),
            size=(min(self.windows_size) * 0.23, min(self.windows_size) * 0.07)
        )

        self.croix_button = graphic_interface.Button(
            path='IMAGES/croix.png',
            xy=(self.windows_size[0]*0.92, self.windows_size[1]*0.06),
            size=(min(self.windows_size)*0.1, min(self.windows_size)*1)
        )


        self.menu_rules_1 = graphic_interface.Image(
            path='IMAGES/menu_regles_1.png',
            xy=(self.windows_size[0] , self.windows_size[1] ),
            size=(self.windows_size[0] , self.windows_size[1] )
        )
        self.menu_rules_2 = graphic_interface.Image(
            path='IMAGES/menu_regles_2.png',
            xy=(self.windows_size[0], self.windows_size[1]),
            size=(self.windows_size[0], self.windows_size[1])
        )
        self.menu_rules_3 = graphic_interface.Image(
            path='IMAGES/menu_regles_3.png',
            xy=(self.windows_size[0], self.windows_size[1]),
            size=(self.windows_size[0], self.windows_size[1])
        )
        self.menu_rules_4 = graphic_interface.Image(
            path='IMAGES/menu_regles_4.png',
            xy=(self.windows_size[0], self.windows_size[1]),
            size=(self.windows_size[0], self.windows_size[1])
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
        #

        self.is_rules_1 = False
        self.is_rules_2 = False
        self.is_rules_3 = False
        self.is_rules_4 = False


        self.possible_moves : dict = {}

        self.player1 = game_management.Player(name=players[0], possible_moves=self.possible_moves, color="noir")
        self.player2 = game_management.Player(name=players[1], possible_moves=self.possible_moves, color="blanc")

        self.is_player1_turn : bool = True

        self.pawn_distance = (self.windows_size[0] * 0.0625, self.windows_size[1] * 0.063)
        self.create_piles()

        self.bot = bot.Bot(self)
        self.is_game_over : bool = False


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

                if nb_pawns :

                    all_piles[i][j] = pawn_pile

                    self.possible_moves[pawn_pile] = []

                    self.add_edges(pawn_pile, all_piles)

                    self.display()

                couleur = "noir" if couleur == "blanc" else "blanc"

    def add_edges(self, actual_pile, all_piles):
        i, j = actual_pile.matrix_position

        if j > 0:  # si on est pas tout à gauche de la matrice
            pile = all_piles[i][j - 1]     # on ajoute celui à gauche
            if pile:               # si il y a des pions dedans
                self.possible_moves[actual_pile].append(pile)  # on l'ajoute à la liste des piles où on peut déposer des pions
                self.possible_moves[pile].append(actual_pile)  # et on ajoute la pile actuelle à la liste de l'autre piles

            if i > 0:  # si en plus on est pas tout en haut
                pile = all_piles[i - 1][j - 1]  # on s'occupe de la diagonale haut gauche
                if pile:
                    self.possible_moves[actual_pile].append(pile)
                    self.possible_moves[pile].append(actual_pile)

        if i > 0:  # si on est pas tout en haut
            pile = all_piles[i - 1][j]         # on ajoute celui au-dessus
            if pile:
                self.possible_moves[actual_pile].append(pile)
                self.possible_moves[pile].append(actual_pile)

            if j < 8:  # si en plus on est pas tout à droite
                pile = all_piles[i - 1][j + 1]  # on s'occupe de la diagonale haut droite
                if pile:
                    self.possible_moves[actual_pile].append(pile)
                    self.possible_moves[pile].append(actual_pile)

    def is_game_over(self):

        for pile in self.possible_moves.keys():
            if self.possible_moves[pile]:
                return False

        return True

    def handling_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False


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
                self.parchemin_button.handling_event(event)

                if self.pause_button.action:
                    self.is_paused = True
                if self.parchemin_button.action:
                    self.is_rules = True


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

        add_path = " vert"

        if self.is_player1_turn and self.black_pawn.path != "IMAGES/boule noir" + add_path + ".png":

            self.black_pawn.path = "IMAGES/boule noir" + add_path + ".png"
            self.black_pawn.update()

            self.white_pawn.path = "IMAGES/boule blanche.png"
            self.white_pawn.update()

        elif not self.is_player1_turn and self.white_pawn.path != "IMAGES/boule blanche" + add_path + ".png":

            self.white_pawn.path = "IMAGES/boule blanche" + add_path + ".png"
            self.white_pawn.update()

            self.black_pawn.path = "IMAGES/boule noir.png"
            self.black_pawn.update()

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
        self.pagepause_image.draw(self.screen)
        self.go_back_button.draw(self.screen)
        self.quit_button.draw(self.screen)

        # Mini gestion d'évenements pour le menu pause
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            self.go_back_button.handling_event(event)
            self.quit_button.handling_event(event)

            if self.go_back_button.action:
                self.is_paused = False
            if self.quit_button.action:
                self.running = False


    def rules(self):
        L=['0','1','2','3']

        if self.is_rules_1:

            self.menu_rules_1.draw(self.screen)
            self.rightfleche_button.draw(self.screen)
            self.croix_button.draw(self.screen)
            a=L[0]
        if self.is_rules_2:

            self.menu_rules_2.draw(self.screen)
            self.rightfleche_button.draw(self.screen)
            self.leftfleche_button.draw(self.screen)
            self.croix_button.draw(self.screen)
            a=L[1]

        if self.is_rules_3:
            self.menu_rules_3.draw(self.screen)
            self.rightfleche_button.draw(self.screen)
            self.leftfleche_button.draw(self.screen)
            self.croix_button.draw(self.screen)
            a = L[2]
        if self.is_rules_4:
            self.menu_rules_4.draw(self.screen)
            self.leftfleche_button.draw(self.screen)
            self.croix_button.draw(self.screen)
            a = L[3]

        # Mini gestion d'évènements pour le menu rules
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
            self.rightfleche_button.handling_event(event)
            self.leftfleche_button.handling_event(event)
            self.croix_button.handling_event(event)

            if self.croix_button.draw(self.screen):
                self.is_rules = False

            if self.rightfleche_button.action and a == '0':  #Passage menu règles 1->2
                self.is_rules_1 = False
                self.is_rules_2 = True

            if self.leftfleche_button.action and a == '1':  #Passage menu règles 2->1
                self.is_rules_1 = True
                self.is_rules_2 = False


            if self.rightfleche_button.action and a == '1':  # Passage menu règles 2->3
                self.is_rules_2 = False
                self.is_rules_3 = True

            if self.leftfleche_button.action and a == '2':  # Passage menu règles 2->3
                self.is_rules_2 = True
                self.is_rules_3 = False

            if self.rightfleche_button.action and a == '2':  # Passage menu règles 3->4
                self.is_rules_3 = False
                self.is_rules_4 = True

            if self.leftfleche_button.action and a == '3':  # Passage menu règles 4->3
                self.is_rules_3 = True
                self.is_rules_4 = False





    def run(self):
        while self.running:

            if self.is_over:
                pass

            elif self.is_paused:
                self.pause_display()

            elif self.is_rules:
                self.rules()

            else:
                self.handling_events()
                self.update()
                self.display()

                if not self.is_player1_turn:

                    self.bot.play(deph=3)

                    self.is_player1_turn = True



            self.clock.tick(60)
            pygame.display.flip()
