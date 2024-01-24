from graphic_interface import Text, fonts, Image
import pygame

black_pawns = {
    1: Image("IMAGES/boule noir.png"),
    2: Image("IMAGES/boule noir.png"),
    3: Image("IMAGES/boule noir.png"),
    4: Image("IMAGES/boule noir.png"),
    5: Image("IMAGES/boule noir.png")
}

white_pawns = {
    1: Image("IMAGES/boule blanche.png"),
    2: Image("IMAGES/boule blanche.png"),
    3: Image("IMAGES/boule blanche.png"),
    4: Image("IMAGES/boule blanche.png"),
    5: Image("IMAGES/boule blanche.png")
}


class Player:
    def __init__(self, name):
        self.name = name
        self.text = Text(
            text=name,
            font=fonts['big_font']
        )


class PileDePions(pygame.sprite.Sprite):
    def __init__(self, screen, couleur, position, nb_pions):
        super().__init__()
        self.screen = screen
        self.couleur = couleur
        self.nb_pions = nb_pions
        self.image = self.load_image()
        self.initial_position = position
        self.rect = self.image.get_rect(topleft=self.initial_position)
        self.dragging = False
        self.offset = [0, 0]

    def load_image(self):
        if self.nb_pions > 0:
            # Charger l'image en fonction de la couleur et du nombre de pions
            # Remplacez cette partie du code avec votre propre logique pour charger les images
            if self.couleur == (0,0,0):
                couleur_pion = "noir"
            else:
                couleur_pion = "blanc"

            image_path = f"IMAGES/pion_{couleur_pion}_{self.nb_pions}.png"  # À adapter
            image = pygame.image.load(image_path)
            return pygame.transform.scale(image, (width/10, width/10))
        else:
            return pygame.Surface((width/10, width/10))  # Aucune image si aucun pion

    def draw(self, screen):
        if self.nb_pions > 0:
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
                all_piles.remove(self)
                all_piles.append(self)
                mouse_x, mouse_y = event.pos
                self.offset = [mouse_x - self.rect.x, mouse_y - self.rect.y]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False

                closest_pile = None
                min_distance = float('inf')

                for pile in pygame.sprite.spritecollide(self, all_piles, False):
                    if pile != self and self.rect.colliderect(pile.rect):  # Vérifier la collision

                        if pile != self:
                            distance = pygame.math.Vector2(pile.rect.center) - pygame.math.Vector2(self.rect.center)
                            distance = distance.length()

                            if distance < min_distance:
                                min_distance = distance
                                closest_pile = pile

                if closest_pile is not None:
                    if closest_pile.nb_pions != 0 and closest_pile.nb_pions + self.nb_pions<=5:
                        # Ajouter à la pile la plus proche avec collision
                        closest_pile.nb_pions += self.nb_pions
                        self.nb_pions = 0

                        closest_pile.couleur = self.couleur
                        self.couleur = None

                        closest_pile.image = closest_pile.load_image()
                        self.image = self.load_image()

                        closest_pile.draw(self.screen)
                        self.draw(self.screen)


                # revenir à la position initiale
                self.rect = self.image.get_rect(topleft=self.initial_position)
