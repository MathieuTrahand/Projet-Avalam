import pygame

windows_size = (600, 600)
pygame.display.set_caption("AVALAM")

# Définition des polices d'écriture
fonts = {
    'basic_font': pygame.font.SysFont("centurygothic", int(0.03 * min(windows_size))),
    'little_font': pygame.font.SysFont("centurygothic", int(0.025 * min(windows_size))),
    'big_font': pygame.font.SysFont("centurygothic", int(0.04 * min(windows_size))),
    'input_font': pygame.font.SysFont("centurygothic", int(0.06 * min(windows_size)))

    # 'error_font': pygame.font.SysFont("Consolas", int(0.03 * min(windows_size)))
}


class Image:
    def __init__(self, path: str, xy: tuple = (0, 0), size: tuple = (0, 0)):

        self.path = path
        self.image = pygame.image.load(self.path)

        self.xy = xy

        # Si la taille n'est pas spécifiée, utilisez la taille de l'image chargée
        if size == (0, 0):
            self.size = self.image.get_size()
        else:
            self.size = size

        # Redimensionner l'image avec interpolation bilinéaire pour un rendu plus lisse
        self.image = pygame.transform.smoothscale(self.image, self.size)
        self.rect = self.image.get_rect(center=xy)

    def update(self):
        self.image = pygame.image.load(self.path)
        # Redimensionner l'image avec interpolation bilinéaire pour un rendu plus lisse
        self.image = pygame.transform.smoothscale(self.image, self.size)
        self.rect = self.image.get_rect(center=self.xy)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Timer:
    def __init__(self, font=fonts["basic_font"], text_col=pygame.Color("black"), bg_col=pygame.Color("white"),
                 position=(0, 0), anchor='topleft'):
        self.font = font
        self.text_col = text_col
        self.bg_col = bg_col
        self.position = position
        self.anchor = anchor.lower()

        self.seconds = 0
        self.minutes = 0
        self.update_timer = 0

        self.text = Text(
            "Time : 00:00",
            self.font,
            self.text_col,
            self.position,
            self.anchor
        )

    def update(self):
        self.text.text = f"TIME : {self.minutes:02d}:{self.seconds:02d}"
        self.text.update()

    def draw(self, surface):
        self.text.draw(surface)

    def tick(self):
        self.seconds += 1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1
        self.update()


class Text:
    def __init__(self, text="", font: pygame.font = None, text_col=pygame.Color("black"),
                 position=(0, 0), anchor='topleft'):

        self.text = text
        self.font = font if font is not None else fonts['basic_font']
        self.text_col = text_col
        self.position = position
        self.anchor = anchor.lower()
        self.update()

    def update(self, position=None, anchor=None, text=None, text_col=None):
        if position is not None:
            self.position = position
        if anchor is not None:
            self.anchor = anchor.lower()
        if text is not None:
            self.text = text
        if text_col is not None:
            self.text_col = text_col

        self.img = self.font.render(self.text, True, self.text_col)
        self.rect = self.img.get_rect(**{self.anchor: self.position})

    def draw(self, surface, position=None, anchor=None):
        self.update(position, anchor)

        surface.blit(self.img, self.rect)


class Button:
    def __init__(self, path: str, xy: tuple = (0, 0), size: tuple = (0, 0)):
        self.image = Image(path, xy, size)
        self.clicked = False
        self.action = False

    def handling_event(self, event):
        self.action = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.image.rect.collidepoint(event.pos):
                self.clicked = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.clicked:
                self.clicked = False
                self.action = True

    def draw(self, screen):
        self.image.draw(screen)


class Input:

    def __init__(self, x, y, font=fonts['input_font'], text: str = '',
                 text_colour=pygame.Color('grey'), second_color=pygame.Color('grey')):

        self.text = Text(text, font, text_colour, (x, y), 'center')
        self.clic = False
        self.second_color = second_color

    def handling_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.text.rect.collidepoint(event.pos):
                self.clic = True
                self.text.update(text='', text_col=self.second_color)
            else:
                self.clic = False

        elif event.type == pygame.KEYDOWN:
            if self.clic:
                if event.key == pygame.K_BACKSPACE:
                    self.text.update(text=self.text.text[:-1])
                else:
                    self.text.update(text=self.text.text + event.unicode)

    def draw(self, screen):
        self.text.draw(screen)
