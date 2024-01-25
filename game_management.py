from graphic_interface import Text, fonts
import pygame


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
        for pile in self.all_piles:
            if pile.color == self.color:
                self.score += 1

        self.score_text.update(text=f"score : {str(self.score)}")


class PileDePions():
    def __init__(self, screen, all_piles, color="blanc", position=(0, 0), nb_pawns=1):
        self.screen = screen
        self.size = min(self.screen.get_size()) // 20
        self.color = color
        self.nb_pawns = nb_pawns
        self.image = self.load_image()
        self.initial_position = position
        self.rect = self.image.get_rect(topleft=self.initial_position)
        self.dragging = False
        self.offset = [0, 0]
        self.all_piles = all_piles

    def load_image(self):
        if self.nb_pawns > 0:
            # Charger l'image en fonction de la couleur et du nombre de pions

            image_path = f"IMAGES/pion_{self.color}_{self.nb_pawns}.png"  # À adapter
            image = pygame.image.load(image_path)
            return pygame.transform.scale(image, (self.size, self.size))
        else:
            return pygame.Surface((self.size / 10, self.size / 10))  # Aucune image si aucun pion

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.all_piles.remove(self)
                self.all_piles.append(self)
                mouse_x, mouse_y = event.pos
                self.offset = [mouse_x - self.rect.x, mouse_y - self.rect.y]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False

                closest_pile = None
                min_distance = float('inf')  # prend le plus grand nombre possible

                for pile in pygame.sprite.spritecollide(self, self.all_piles, False):
                    if pile != self and self.rect.colliderect(pile.rect):  # Vérifier la collision

                        if pile != self:
                            distance = pygame.math.Vector2(pile.rect.center) - pygame.math.Vector2(self.rect.center)
                            distance = distance.length()

                            if distance < min_distance:
                                min_distance = distance
                                closest_pile = pile

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
