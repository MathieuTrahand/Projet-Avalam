from graphic_interface import Text, fonts, Image
import pygame

empty_surface = pygame.Surface((0, 0))

pawns_images = {}


class Player:
    def __init__(self, name, all_piles, color="blanc"):
        self.name = name
        self.name_text = Text(
            text=self.name,
            font=fonts['big_font']
        )
        self.color = color
        self.all_piles = all_piles

        self.score = 0
        self.score_text = Text(
            text="",
            font=fonts["basic_font"]
        )
        self.update_score()

    def update_score(self):
        self.score = 0
        for ligne in self.all_piles:
            for pile in ligne:
                if pile.nb_pawns > 0 and pile.color == self.color:
                    self.score += 1

        self.score_text.update(text=f"score : {str(self.score)}")


class PawnsPile:
    def __init__(self, screen, all_piles, color="blanc", initial_position=(0, 0), nb_pawns=1,
                 pawn_distance=(0, 0), matrice_position=(0, 0)):

        self.screen = screen
        self.size = min(self.screen.get_size()) / 20
        self.color = color
        self.nb_pawns = nb_pawns
        self.initial_position = initial_position
        self.matrice_position = matrice_position
        self.dragging = False
        self.can_drop = False
        self.all_piles = all_piles
        self.image = self.load_image()

        self.rect = self.image.get_rect(center=self.initial_position)

        self.offset = [self.initial_position[0] - self.rect.x, self.initial_position[1] - self.rect.y]

        self.pawn_distance = pawn_distance

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

                image_path = f"IMAGES/pion_{self.color}_{sup_path}{self.nb_pawns}.png"
                image = pygame.image.load(image_path)
                pawns_images[key] = pygame.transform.smoothscale(image, (self.size, self.size))

            return pawns_images[key]

        else:
            self.color = None
            return empty_surface  # Aucune image si aucun pion

    def draw(self, surface=None):
        if not surface:
            surface = self.screen

        if self.nb_pawns > 0:

            surface.blit(self.image, self.rect)

            """ Créer un cercle autour de la pile si on peut déposer des pions dessus
            if self.can_drop:
                #pygame.draw.rect(surface, "green", self.rect, width=2)

                pygame.draw.circle(
                    surface, "green",
                    self.rect.center,
                    self.size * 0.5,
                    width=2
                )"""


    def update(self):
        if self.dragging:
            # gestion de la position de la pile
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if abs(self.initial_position[0] - mouse_x) <= self.pawn_distance[0] + 0.6 * self.size:
                self.rect.x = mouse_x - self.offset[0]

            if abs(self.initial_position[1] - mouse_y) <= self.pawn_distance[1] + 0.6 * self.size:
                self.rect.y = mouse_y - self.offset[1]

    def min_distance(self):
        closest_pile = None
        min_distance = float('inf')  # prend le plus grand nombre possible
        for ligne in self.all_piles:
            for pile in pygame.sprite.spritecollide(self, ligne, False):
                if pile != self and self.rect.colliderect(pile.rect):  # Vérifier la collision

                    distance = pygame.math.Vector2(pile.rect.center) - pygame.math.Vector2(self.rect.center)
                    distance = distance.length()

                    if distance < min_distance:
                        min_distance = distance
                        closest_pile = pile

        return closest_pile

    def can_drop_gestion(self, can_drop: bool = True):

        i, j = self.matrice_position  # i ligne j colonne

        # GESTION GAUCHE / DROITE & DIAGONALES

        if j > 0:  # si on est pas tout à gauche de la matrice
            pile = self.all_piles[i][j - 1]
            if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:  # on verifie que c'est possible
                pile.can_drop = can_drop            # on met la variable can_drop à True ou False
                pile.image = pile.load_image()      # on recharge l'image pour qu'elle soit verte ou non

            if i > 0:  # si en plus on est pas tout en haut
                pile = self.all_piles[i - 1][j - 1]  # on s'occupe de la diagonale haut gauche
                if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:
                    pile.can_drop = can_drop
                    pile.image = pile.load_image()

            if i < 8:  # si en plus on est pas tout en bas
                pile = self.all_piles[i + 1][j - 1]  # on s'occupe de la diagonale bas gauche
                if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:
                    pile.can_drop = can_drop
                    pile.image = pile.load_image()

        if j < 8:  # si on est pas tout à droite
            pile = self.all_piles[i][j + 1]
            if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:
                pile.can_drop = can_drop
                pile.image = pile.load_image()

            if i > 0:  # si en plus on est pas tout en haut
                pile = self.all_piles[i - 1][j + 1]  # on s'occupe de la diagonale haut droite
                if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:
                    pile.can_drop = can_drop
                    pile.image = pile.load_image()

            if i < 8:  # si en plus on est pas tout en bas
                pile = self.all_piles[i + 1][j + 1]  # on s'occupe de la diagonale bas droite
                if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:
                    pile.can_drop = can_drop
                    pile.image = pile.load_image()

        # GESTION HAUT / BAS

        if i > 0:  # si on est pas tout en haut
            pile = self.all_piles[i - 1][j]
            if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:
                pile.can_drop = can_drop
                pile.image = pile.load_image()

        if i < 8:  # si on est pas tout en bas
            pile = self.all_piles[i + 1][j]
            if 0 < pile.nb_pawns and pile.nb_pawns + self.nb_pawns <= 5:
                pile.can_drop = can_drop
                pile.image = pile.load_image()

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if 0 < self.nb_pawns < 5:

                if self.rect.collidepoint(event.pos):
                    self.dragging = True

                    # gestion des piles où on peut déposer la notre
                    self.can_drop_gestion(True)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False

                closest_pile = self.min_distance()  # trouver la pile la plus proche

                if closest_pile is not None:

                    if closest_pile.can_drop:
                        # Ajouter à la pile la plus proche avec collision
                        closest_pile.nb_pawns += self.nb_pawns
                        self.nb_pawns = 0

                        closest_pile.color = self.color
                        self.color = None

                        closest_pile.image = closest_pile.load_image()
                        self.image = self.load_image()

                # on remet tout à False
                self.can_drop_gestion(False)

                # revenir à la position initiale
                self.rect = self.image.get_rect(center=self.initial_position)
