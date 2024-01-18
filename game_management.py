from graphic_interface import Text, fonts

class Player:
    def __init__(self, name):
        self.name = name
        self.text = Text(
            text=name,
            font=fonts['big_font']
        )
