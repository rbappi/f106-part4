import random
import time
from abc import ABCMeta, abstractmethod
from resource_tournoi.const import *
from resource_tournoi.exceptions import *
from resource_tournoi.action import Action
from resource_tournoi.players import Player, AIPlayer



class TournoiAiPlayer(AIPlayer):
    """
    Spécialisation de la classe Player représentant un joueur utilisant un minimax
    """
    def __init__(self, board, player_id):
        super().__init__(board, player_id)
        self.player_id = player_id
        
    def _play(self):
        """
        Détermine le meilleur coup à jouer

        Returns:
            Action: le meilleur coup déterminé via minimax
        """
        i = 1
        best_soluce = None

        self.timer = Timer()
        while self.timer.ok_timer():
            self.best_soluce = self.minimax(i)
            i += 1
        return self.board.act(best_soluce) #TODO METHODE ACT

    def minimax(self, depth=2, maximizing=True):
        """
        Détermine le coup optimal à jouer selon l'algorithme minimax.

        Args:
            depth (int): la profondeur à explorer dans l'arbre des coups possibles
            maximizing (bool): True si on cherche à maximiser le score et False si on cherche à le maximiser

        Returns:
            Action: le meilleur coup trouvé dans la profondeur explorée
        """
        if not self.timer.ok_timer:
                return self.best_soluce
        if depth == 0:
            return (None, DRAW)
        if maximizing:
            best_score = -INF
            player = self.player_id
        else:
            best_score = +INF
            player = self.other_player_id
        best_actions = []
        assert self.board.has_moves(player)
        for action in self.board.possible_actions(player):
            if not self.timer.ok_timer:
                return self.best_soluce
            self.board.act(action)
            winner = self.board.status.winner
            if winner is not None:
                score = WIN+depth  # Il vaut mieux gagner tôt (ou perdre tard) que de gagner tard (ou perdre tôt)
                if winner == self.other_player_id:
                    score *= -1
            else:
                score = self.minimax(depth-1, not maximizing)[1]
            self.board.undo()
            # Si on trouve un meilleur score
            if (score > best_score and maximizing) or (score < best_score and not maximizing):
                best_score = score
                best_actions = [action]
            elif score == best_score:
                best_actions.append(action)
        return random.choice(best_actions), best_score


class Timer():
    def __init__(self):
        self.start_timer = None
        self.__begin_timer()
    
    def __begin_timer(self):
        self.start_timer = time.perf_counter()
    
    def act_timer(self):
        return (time.perf_counter() - self.start_timer())
    
    def ok_timer(self):
        return 1.85 > self.act_timer