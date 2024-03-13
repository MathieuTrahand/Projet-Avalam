class Bot:
    def __init__(self, bot_player, ennemy_player, possible_moves):
        self.bot_player = bot_player
        self.ennemy_player = ennemy_player

        self.possible_moves = possible_moves

        self.bot_score = 0
        self.ennemy_score = 0


    def minimax(self, deph):
        if deph == 0:
            return self.bot_score - self.ennemy_score

    def get_move(self, state):
        pass

    def move_pile(self, start_pile, end_pile):
        start_pile.bot_drag_and_drop(end_pile)

