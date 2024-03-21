from copy import deepcopy
from math import inf

class Bot:
    def __init__(self, game, color="blanc"):

        self.game = game
        self.possible_moves = self.game.possible_moves

        # determine le bot et l'adversaire
        if color == "blanc":
            self.bot_player = game.player2
            self.ennemy_player = game.player1
        else:
            self.bot_player = game.player1
            self.ennemy_player = game.player2

        self.color = color

        self.bot_score = 23     # Etat initial
        self.ennemy_score = 23

        self.memo = {}

    def move_gestion(self, possible_moves, start_pile, end_pile):

        # On fait le coup
        end_pile.nb_pawns += start_pile.nb_pawns
        start_pile.nb_pawns = 0

        end_pile.color = start_pile.color
        start_pile.color = None

        for pile in possible_moves[start_pile]:
            possible_moves[pile].remove(start_pile)
        possible_moves[start_pile] = []

        # On gère les nouveaux coups possibles
        piles_to_remove = []
        for pile in possible_moves[end_pile]:
            if pile.nb_pawns + end_pile.nb_pawns > 5:
                possible_moves[pile].remove(end_pile)
                piles_to_remove.append(pile)


        for pile in piles_to_remove:
            possible_moves[end_pile].remove(pile)


    def cancel_move(self, start_pile, end_pile, start_color, end_color, start_nb_pawns, end_nb_pawns):

        start_pile.color = start_color
        start_pile.nb_pawns = start_nb_pawns

        end_pile.color = end_color
        end_pile.nb_pawns = end_nb_pawns

    def score_gestion(self, start_pile_color, end_pile_color, cancel=False):

        add_bot = 0
        add_ennemy = 0

        if end_pile_color == start_pile_color:
            if start_pile_color == self.color:
                add_bot = -1
            else:
                add_ennemy = -1

        else:
            if start_pile_color == self.color:
                add_bot = 1
                add_ennemy = -1
            else:
                add_ennemy = 1
                add_bot = -1

        if cancel:
            add_bot = -add_bot
            add_ennemy = -add_ennemy

        self.bot_score += add_bot
        self.ennemy_score += add_ennemy

    def minimax(self, possible_moves, deph, maximizing_player, alpha, beta):

        #tuple_possible_moves = tuple(sorted(possible_moves.items(), key=lambda x: (x[1].matrix_position , x[1].index)))

        tuple_possible_moves = tuple((k,tuple(v)) for k,v in deepcopy(possible_moves))

        if tuple_possible_moves in self.memo:
            return self.memo[tuple_possible_moves]

        if deph == 0 or self.game.is_game_over():
            score = self.bot_score - self.ennemy_score
            self.memo[tuple_possible_moves] = (score, None)
            return score, None


        if maximizing_player:
            maxEval = - inf

            for start_pile in possible_moves.keys():
                for end_pile in possible_moves[start_pile]:

                    # récupérer les données pour revenir en arrière
                    start_pile_color = start_pile.color
                    end_pile_color = end_pile.color
                    start_pile_nb_pawns = start_pile.nb_pawns
                    end_pile_nb_pawns = end_pile.nb_pawns

                    new_possible_moves = deepcopy(possible_moves)

                    # gérer le coup
                    self.move_gestion(new_possible_moves, start_pile, end_pile)

                    # gérer le score
                    self.score_gestion(start_pile_color, end_pile_color)

                    eval = self.minimax(new_possible_moves, deph - 1, False, alpha, beta)[0]

                    # annuler le score
                    self.score_gestion(start_pile_color, end_pile_color, cancel=True)

                    #annuler le coup
                    self.cancel_move(start_pile, end_pile, start_pile_color, end_pile_color, start_pile_nb_pawns, end_pile_nb_pawns)

                    # mettre à jour le meilleur coup
                    if eval > maxEval:
                        maxEval = eval
                        best_move = (start_pile, end_pile)

                    alpha = max(alpha, eval)            # mettre à jour alpha
                    if beta <= alpha:                   # couper la branche
                        break

            self.memo[tuple_possible_moves] = (maxEval, best_move)
            return maxEval, best_move


        else:
            minEval = inf


            for start_pile in possible_moves.keys():
                for end_pile in possible_moves[start_pile]:

                    # récupérer les données pour revenir en arrière
                    start_pile_color = start_pile.color
                    end_pile_color = end_pile.color
                    start_pile_nb_pawns = start_pile.nb_pawns
                    end_pile_nb_pawns = end_pile.nb_pawns

                    new_possible_moves = deepcopy(possible_moves)

                    # gérer le coup
                    self.move_gestion(new_possible_moves, start_pile, end_pile)

                    # gérer le score
                    self.score_gestion(start_pile_color, end_pile_color)

                    eval = self.minimax(new_possible_moves, deph - 1, True, alpha, beta)[0]

                    # annuler le score
                    self.score_gestion(start_pile_color, end_pile_color, True)

                    # annuler le coup
                    self.cancel_move(start_pile, end_pile, start_pile_color, end_pile_color, start_pile_nb_pawns,
                                     end_pile_nb_pawns)

                    if eval < minEval:
                        minEval = eval
                        best_move = (start_pile, end_pile)

                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

            self.memo[tuple_possible_moves] = (minEval, best_move)
            return minEval, best_move

    def play(self, deph=2):
        self.bot_score = self.bot_player.score
        self.ennemy_score = self.ennemy_player.score

        possible_moves = deepcopy(self.possible_moves)

        best_move = self.minimax(possible_moves, deph, True, -inf, inf)[1]
        self.move_pile(best_move)

    def move_pile(self, move):
        start_pile, end_pile = move
        start_pile.bot_drag_and_drop(end_pile)

