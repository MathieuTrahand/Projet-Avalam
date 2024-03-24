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

        self.bot_score = 23  # Etat initial
        self.ennemy_score = 23

    def move_gestion(self, start_pile, end_pile):

        # On fait le coup
        end_pile.nb_pawns += start_pile.nb_pawns
        start_pile.nb_pawns = 0

        end_pile.color = start_pile.color
        start_pile.color = None

        start_pile_to_remove = []
        # On retire la pile de départ des coups possibles
        for pile in self.possible_moves[start_pile]:
            self.possible_moves[pile].remove(start_pile)  # on enlève la pile de départ dans les valeurs
            start_pile_to_remove.append(pile)

        self.possible_moves[start_pile] = []  # on enlève la pile de départ dans les clés

        # On gère les nouveaux coups possibles
        end_pile_to_remove = []
        for pile in self.possible_moves[end_pile]:
            if pile.nb_pawns + end_pile.nb_pawns > 5:
                end_pile_to_remove.append(pile)
                self.possible_moves[pile].remove(end_pile)

        for pile in end_pile_to_remove:
            self.possible_moves[end_pile].remove(pile)

        return start_pile_to_remove, end_pile_to_remove

    def move_cancel(self, start_pile, end_pile, start_pile_color, end_pile_color, start_pile_nb_pawns,
                    end_pile_nb_pawns, start_pile_possible_moves, end_pile_possible_moves):

        # On remet les couleurs de base
        start_pile.color = start_pile_color
        end_pile.color = end_pile_color

        # On remet le nombre de pions de base
        start_pile.nb_pawns = start_pile_nb_pawns
        end_pile.nb_pawns = end_pile_nb_pawns

        # On remet à jour le dictionnaire des coups possibles de la case de départ
        for pile in start_pile_possible_moves:
            self.possible_moves[start_pile].append(pile)
            self.possible_moves[pile].append(start_pile)

        # On remet à jour le dictionnaire des coups possibles de la case d'arrivée
        for pile in end_pile_possible_moves:
            self.possible_moves[pile].append(end_pile)
            self.possible_moves[end_pile].append(pile)  # on rajoute le lien entre les 2 piles

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

    def move_weight(self, end_pile):
        weight = 0

        if end_pile.nb_pawns == 5:
            weight += 5

        elif self.possible_moves[end_pile] == []:
            weight += 3

        else:
            for pile in self.possible_moves[end_pile]:
                if pile.color == end_pile.color:
                    if pile.nb_pawns + end_pile.nb_pawns == 5:
                        weight += 2

                else:
                    if pile.nb_pawns + end_pile.nb_pawns == 5:
                        weight -= 5

        return weight


    def minimax(self, deph, maximizing_player, alpha, beta):

        if deph == 0 or self.game.is_game_over():
            score = self.bot_score - self.ennemy_score
            return score, None

        if maximizing_player:
            maxEval = - inf

            for start_pile in self.possible_moves.keys():
                for end_pile in self.possible_moves[start_pile]:

                    if start_pile.nb_pawns + end_pile.nb_pawns > 5:
                        self.possible_moves[start_pile].remove(end_pile)
                        self.possible_moves[end_pile].remove(start_pile)
                        break

                    # récupérer les données pour revenir en arrière
                    start_pile_color = deepcopy(start_pile.color)
                    end_pile_color = deepcopy(end_pile.color)
                    start_pile_nb_pawns = deepcopy(start_pile.nb_pawns)
                    end_pile_nb_pawns = deepcopy(end_pile.nb_pawns)

                    # gérer le coup
                    start_pile_possible_moves, end_pile_possible_moves = self.move_gestion(start_pile, end_pile)

                    # gérer le score
                    self.score_gestion(start_pile_color, end_pile_color)

                    eval = self.minimax(deph - 1, False, alpha, beta)[0]

                    # annuler le coup
                    self.move_cancel(
                        start_pile, end_pile, start_pile_color, end_pile_color, start_pile_nb_pawns,
                        end_pile_nb_pawns, start_pile_possible_moves, end_pile_possible_moves
                    )

                    # annuler le score
                    self.score_gestion(start_pile_color, end_pile_color, cancel=True)

                    # Pondérer le coup
                    eval += self.move_weight(end_pile)

                    # mettre à jour le meilleur coup
                    if eval > maxEval:
                        maxEval = eval
                        best_move = (start_pile, end_pile)

                    alpha = max(alpha, eval)  # mettre à jour alpha
                    if beta <= alpha:  # couper la branche
                        break

            return maxEval, best_move


        else:
            minEval = inf

            for start_pile in self.possible_moves.keys():
                for end_pile in self.possible_moves[start_pile]:

                    if start_pile.nb_pawns + end_pile.nb_pawns > 5:
                        self.possible_moves[start_pile].remove(end_pile)
                        self.possible_moves[end_pile].remove(start_pile)
                        break

                    # récupérer les données pour revenir en arrière
                    start_pile_color = deepcopy(start_pile.color)
                    end_pile_color = deepcopy(end_pile.color)
                    start_pile_nb_pawns = deepcopy(start_pile.nb_pawns)
                    end_pile_nb_pawns = deepcopy(end_pile.nb_pawns)

                    # gérer le coup
                    start_pile_possible_moves, end_pile_possible_moves = self.move_gestion(start_pile, end_pile)

                    # gérer le score
                    self.score_gestion(start_pile_color, end_pile_color)

                    eval = self.minimax(deph - 1, True, alpha, beta)[0]

                    # annuler le coup
                    self.move_cancel(
                        start_pile, end_pile, start_pile_color, end_pile_color, start_pile_nb_pawns,
                        end_pile_nb_pawns, start_pile_possible_moves, end_pile_possible_moves
                    )

                    # annuler le score
                    self.score_gestion(start_pile_color, end_pile_color, True)

                    # Pondérer le coup
                    eval += self.move_weight(end_pile)

                    if eval < minEval:
                        minEval = eval
                        best_move = (start_pile, end_pile)

                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

            return minEval, best_move

    def play(self, deph=2):
        self.bot_score = self.bot_player.score
        self.ennemy_score = self.ennemy_player.score

        best_move = self.minimax(deph, True, -inf, inf)[1]
        self.move_pile(best_move)

    def move_pile(self, move):
        start_pile, end_pile = move
        start_pile.bot_drag_and_drop(end_pile)



