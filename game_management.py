from graphic_interface import Text, fonts
import pygame

empty_surface = pygame.Surface((0, 0))

pawns_images = {}


#

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
    def __init__(self, screen, all_piles, color="blanc", position=(0, 0), nb_pawns=1):
        self.screen = screen
        self.size = min(self.screen.get_size()) / 20
        self.color = color
        self.nb_pawns = nb_pawns
        self.initial_position = position
        self.dragging = False
        self.offset = [0, 0]
        self.all_piles = all_piles
        self.image = self.load_image()
        self.rect = self.image.get_rect(topleft=self.initial_position)

        self.pawn_distance = self.min_distance()[1]

    def load_image(self):
        if self.nb_pawns > 0:
            # Charger l'image en fonction de la couleur et du nombre de pions
            key = f'{self.color, self.nb_pawns}'

            # On les met dans un dictionnaire pour éviter d'avoir à les charger 1000 fois

            if key not in pawns_images:
                image_path = f"IMAGES/pion_{self.color}_{self.nb_pawns}.png"  # À adapter
                image = pygame.image.load(image_path)
                pawns_images[key] = pygame.transform.scale(image, (self.size, self.size))

            return pawns_images[key]
        else:
            self.color = None
            return empty_surface  # Aucune image si aucun pion

    def draw(self, screen=None):
        if not screen:
            screen = self.screen

        if self.nb_pawns > 0:
            screen.blit(self.image, self.rect)

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.x = mouse_x - self.offset[0]
            self.rect.y = mouse_y - self.offset[1]

    def min_distance(self):
        closest_pile = None
        min_distance = float('inf')  # prend le plus grand nombre possible

        for ligne in self.all_piles:
            for pile in pygame.sprite.spritecollide(self, ligne, False):
                if pile != self and self.rect.colliderect(pile.rect):  # Vérifier la collision

                    if pile != self:
                        distance = pygame.math.Vector2(pile.rect.center) - pygame.math.Vector2(self.rect.center)
                        distance = distance.length()

                        if distance < min_distance:
                            min_distance = distance
                            closest_pile = pile

        return closest_pile, min_distance

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if 0 < self.nb_pawns < 5:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset = [mouse_x - self.rect.x, mouse_y - self.rect.y]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False

                closest_pile = self.min_distance()[0]

                if closest_pile is not None:
                    if closest_pile.nb_pawns != 0 and closest_pile.nb_pawns + self.nb_pawns <= 5:
                        # Ajouter à la pile la plus proche avec collision
                        closest_pile.nb_pawns += self.nb_pawns
                        self.nb_pawns = 0

                        closest_pile.color = self.color
                        self.color = None

                        closest_pile.image = closest_pile.load_image()
                        self.image = self.load_image()

                        closest_pile.draw(self.screen)
                        self.draw(self.screen)

                # revenir à la position initiale
                self.rect = self.image.get_rect(topleft=self.initial_position)
