from graphic_interface import Text, fonts, Image

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


class Stack:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.nb_pawns = 1

        if color == "white":
            self.image = white_pawns[1]
        else:
            self.image = black_pawns[1]
