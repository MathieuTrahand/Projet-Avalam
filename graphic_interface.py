import pygame

windows_size = (600, 600)
pygame.display.set_caption("AVALAM")

# Définition des polices d'écriture
fonts = {
    'basic_font': pygame.font.SysFont("arialblack", int(0.04 * min(windows_size))),
    'little_font': pygame.font.SysFont("arialblack", int(0.025 * min(windows_size))),
    'big_font': pygame.font.SysFont("arialblack", int(0.045 * min(windows_size))),
    'error_font': pygame.font.SysFont("Consolas", int(0.03 * min(windows_size)))
}


class Image:
    def __init__(self, path: str, xy: tuple = (0, 0), size: tuple = (0, 0)):
        self.image = pygame.image.load(path)

        # Si la taille n'est pas spécifiée, utilisez la taille de l'image chargée
        if size == (0, 0):
            self.size = self.image.get_size()
        else:
            self.size = size

        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=xy)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Timer:
    def __init__(self, screen, xy: tuple = (0, 0), size: tuple = (0, 0), anchor='topleft'):
        self.screen = screen
        self.anchor=anchor
        self.size = size
        self.seconds = 0
        self.xy = xy
        self.is_running = False
    def start(self):
        self.is_running = True
    def stop(self):
        self.is_running = False
    def reset(self):
        self.seconds = 0
    def update(self,xy=None,anchor=None):
        if self.is_running:
            self.seconds += 1
            if xy is not None:
                self.xy = xy
            if anchor is not None:
                self.anchor = anchor.lower()
    def draw(self, surface, xy=None,anchor=None):
        self.update(surface,xy, anchor)
        self.surface = surface

        pygame.draw.rect(self.surface, self.xy, self.anchor)


class Text:
    def __init__(self, text="", font: pygame.font = None, text_col=pygame.Color("black"),
                 bg_col=pygame.Color("white"), position=(0, 0), anchor='topleft'):
        self.text = text
        self.font = font if font is not None else font['basic_font']
        self.bg_col = bg_col
        self.text_col = text_col
        self.position = position
        self.anchor = anchor.lower()
        self.update()


    def update(self, position=None, anchor=None):
        if position is not None:
            self.position = position
        if anchor is not None:
            self.anchor = anchor.lower()

        self.img = self.font.render(self.text, True, self.text_col)
        self.bg_rect = self.img.get_rect(**{self.anchor: self.position})

    def draw(self, surface, position=None, anchor=None):
        self.update(position, anchor)
        self.surface = surface

        pygame.draw.rect(self.surface, self.bg_col, self.bg_rect)
        self.surface.blit(self.img, self.bg_rect.topleft)


def Input_Interface():
    pass

    # Tant que y a rien :
    #       return None
    # Si y a qqch
    #       return nom1, nom2
    #       ne pas oublier dans le code principale self.window = "game"
