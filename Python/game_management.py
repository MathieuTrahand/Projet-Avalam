from graphic_interface import Text, fonts
import pygame
import time

empty_surface = pygame.Surface((0, 0))

pawns_images = {}

possible_moves = {}

class Player:
    def __init__(self, name, possible_moves, color="blanc"):
        self.name = name
        self.name_text = Text(
            text=self.name,
            font=fonts['big_font']
        )
        self.color = color
        self.possible_moves = possible_moves

        self.score = 0
        self.score_text = Text(
            text="",
            font=fonts["basic_font"]
        )
        self.update_score()

    def update_score(self):
        self.score = 0
        for pile in self.possible_moves.keys():
            if pile.nb_pawns > 0 and pile.color == self.color:
                self.score += 1

        self.score_text.update(text=f"score : {str(self.score)}")


class PawnsPile:
    def __init__(self, game, color="blanc", initial_position=(0, 0), nb_pawns=1, matrix_position=(0, 0)):

        self.game = game
        self.matrix_position = matrix_position
        self.size = min(self.game.screen.get_size()) / 20
        self.color = color
        self.nb_pawns = nb_pawns
        self.initial_position = initial_position
        self.dragging = False
        self.can_drop = False
        self.possible_moves = self.game.possible_moves
        self.image = self.load_image()

        self.rect = self.image.get_rect(center=self.initial_position)

        self.offset = [self.initial_position[0] - self.rect.x, self.initial_position[1] - self.rect.y]

        self.pawn_distance = game.pawn_distance

        # relatif au bot :
        self.drag_bot_time = 0.3
        self.start_time = None

    ## Pour le tri : ##
    """def __lt__(self, other):
        # < par rapport à la position dans la matrice
        if self.matrix_position[0] == other.matrix_position[0]:
            return self.matrix_position[1] < other.matrix_position[1]
        else:
            return self.matrix_position[0] < other.matrix_position[0]

    def __eq__(self, other):
        # Egaux par rapport à la position dans la matrice
        return (self.matrix_position[0], self.matrix_position[1]) == (other.matrix_position[0], other.matrix_position[1])

    def __gt__(self, other):
        # > par rapport à la position dans la matrice
        if self.matrix_position[0] == other.matrix_position[0]:
            return self.matrix_position[1] > other.matrix_position[1]
        else:
            return self.matrix_position[0] > other.matrix_position[0]"""

    def load_image(self):
        if self.nb_pawns > 0:

            # On vérifie si on peut déposer des pions dessus, si c'est lecas on utilise le pion entouré en vert
            if self.can_drop:
                key = f'{self.color, self.nb_pawns}_can_drop'
            else:
                # Charger l'image en fonction de la couleur et du nombre de pions
                key = f'{self.color, self.nb_pawns}'


            # On les met dans un dictionnaire pour éviter d'avoir à les charger 1000 fois et gagner du temps

            if key not in pawns_images:
                if self.can_drop:
                    sup_path = f'v5_vert_'
                else:
                    sup_path = ''

                image_path = f"../IMAGES/pion_{self.color}_{sup_path}{self.nb_pawns}.png"
                image = pygame.image.load(image_path)
                pawns_images[key] = pygame.transform.smoothscale(image, (self.size, self.size))

            return pawns_images[key]

        else:
            self.color = None
            return empty_surface  # Aucune image si aucun pion

    def draw(self, surface=None):
        if not surface:
            surface = self.game.screen

        if self.nb_pawns > 0:

            surface.blit(self.image, self.rect)


    def bot_drag_and_drop(self, target_pile):
        self.target_pile = target_pile
        self.start_time = time.time()

    def update(self):
        if self.dragging:
            # gestion de la position de la pile
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if abs(self.initial_position[0] - mouse_x) <= self.pawn_distance[0] + 0.6 * self.size:
                self.rect.x = mouse_x - self.offset[0]

            if abs(self.initial_position[1] - mouse_y) <= self.pawn_distance[1] + 0.6 * self.size:
                self.rect.y = mouse_y - self.offset[1]

        elif self.start_time is not None:

            current_time = time.time()
            elapsed_time = current_time - self.start_time

            if elapsed_time >= self.drag_bot_time:
                self.start_time = None

                self.drop(self.target_pile)

                # revenir à la position initiale
                self.rect = self.image.get_rect(center=self.initial_position)

                self.target_pile = None


            else:
                progress = elapsed_time / self.drag_bot_time

                new_x = int(self.initial_position[0] + (self.target_pile.initial_position[0] - self.initial_position[0]) * progress)
                new_y = int(self.initial_position[1] + (self.target_pile.initial_position[1] - self.initial_position[1]) * progress)

                self.rect.x = new_x - self.offset[0]
                self.rect.y = new_y - self.offset[1]

    def min_distance(self):
        closest_pile = None
        min_distance = float('inf')  # prend le plus grand nombre possible
        for pile in pygame.sprite.spritecollide(self, self.possible_moves.keys(), False):
            if pile != self and self.rect.colliderect(pile.rect):  # Vérifier la collision

                distance = pygame.math.Vector2(pile.rect.center) - pygame.math.Vector2(self.rect.center)
                distance = distance.length()

                if distance < min_distance:
                    min_distance = distance
                    closest_pile = pile

        return closest_pile

    def can_be_drop_gestion(self, can_drop: bool = True):

        for pile in self.possible_moves[self]:
            pile.can_drop = can_drop
            pile.image = pile.load_image()

    def update_possible_moves(self, pile_to_drop):

        for pile in self.possible_moves[self]:
            self.possible_moves[pile].remove(self)  # on enlève la pile de départ dans les valeurs
        self.possible_moves[self] = [] # on enlève la pile de départ dans les clés

        for pile in self.possible_moves[pile_to_drop]:

            pile.can_drop = False
            pile.image = pile.load_image()

            if pile.nb_pawns + pile_to_drop.nb_pawns > 5:
                self.possible_moves[pile_to_drop].remove(pile)
                self.possible_moves[pile].remove(pile_to_drop)

    def drop_gestion(self, pile_to_drop):
        # Ajouter à la pile la plus proche avec collision
        pile_to_drop.nb_pawns += self.nb_pawns
        self.nb_pawns = 0

        pile_to_drop.color = self.color
        self.color = None

        pile_to_drop.image = pile_to_drop.load_image()
        self.image = self.load_image()

    def drop(self, pile_to_drop):
        self.drop_gestion(pile_to_drop)

        # mettre à jour le dictionnaire des coups possibles
        self.update_possible_moves(pile_to_drop)

        # verifier la fin de partie
        self.game.game_over = self.game.is_game_over()




    def handle_press(self):

        if 0 < self.nb_pawns < 5:

            self.dragging = True

            # gestion des piles où on peut déposer la notre
            self.can_be_drop_gestion(True)

    def handle_release(self):

        self.dragging = False

        self.can_be_drop_gestion(False)

        closest_pile = self.min_distance()  # trouver la pile la plus proche

        if closest_pile is not None:

            if closest_pile in self.possible_moves[self]:
                self.drop(pile_to_drop=closest_pile)

                # tour du prochain joueur
                self.game.is_player1_turn = not self.game.is_player1_turn

        # revenir à la position initiale
        self.rect = self.image.get_rect(center=self.initial_position)