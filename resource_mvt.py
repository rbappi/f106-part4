"""
Nom: Bappi
Prénom: Rahaman
Matricule: 000516227
Section: BA1-INFO
Description: Permet de génerer les mouvements possibles.
"""

from constantes import *
import copy



class Check_mvt():

    def __init__(self):
        self.__mvt_tot_l = []
        self.coord_l = []

    @property
    def mvt_tot_l(self):
        return sorted(self.__mvt_tot_l)

    def mouvements_possibles(self, source, plateau, string=True, corrd = False):
        """
        Description: Permet de connaitre tout les mouvements possibles d'une reine.
        source: La reine.
        plateau: Le plateau.
        return: Une liste de tout les possibiltees.
        """
        import resource_coup_joueur
        self.__mvt_tot_l = []
        self.coord_l = []
        j = 1
        i = 1
        if string:
            source = resource_coup_joueur.Coup().coup_to_tuple(source, len(plateau))
        while j < (len(plateau[i]) - (source[1])) and plateau[source[0]][source[1] + j] == LIBRE:  # EST
            if corrd:
                self.coord_l += [(source[0], source[1] + j)]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0], source[1] + j))]
            j += 1
        j = 1
        while j < source[1] + 1 and plateau[source[0]][source[1] - j] == LIBRE:  # OUEST
            if corrd:
                self.coord_l += [(source[0], source[1] - j)]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0], source[1] - j))]
            j += 1
        i = 1
        while i < (len(plateau) - source[0]) and plateau[source[0] + i][source[1]] == LIBRE:  # NORD
            if corrd:
                self.coord_l += [(source[0] + i, source[1])]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0] + i, source[1]))]
            i += 1
        i = 1
        while i < source[0] + 1 and plateau[source[0] - i][source[1]] == LIBRE:  # SUD
            if corrd:
                self.coord_l += [(source[0] - i, source[1])]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0] - i, source[1]))]
            i += 1
        i = 1
        j = 1
        while i < source[0] + 1 and j < (len(plateau[i]) - (source[1])) and plateau[source[0] - i][
            source[1] + j] == LIBRE:  # SUD-EST
            if corrd:
                self.coord_l += [(source[0] - i, source[1] + j)]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0] - i, source[1] + j))]
            i += 1
            j += 1
        i = 1
        j = 1
        while i < source[0] + 1 and j < source[1] + 1 and plateau[source[0] - i][source[1] - j] == LIBRE:  # SUD-OUEST
            if corrd:
                self.coord_l += [(source[0] - i, source[1] - j)]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0] - i, source[1] - j))]
            i += 1
            j += 1
        i = 1
        j = 1
        while i < (len(plateau) - source[0]) and j < source[1] + 1 and plateau[source[0] + i][
            source[1] - j] == LIBRE:  # NORD-OUEST
            if corrd:
                self.coord_l += [(source[0] + i, source[1] - j)]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0] + i, source[1] - j))]
            i += 1
            j += 1
        i = 1
        j = 1
        while i < (len(plateau) - source[0]) and j < (len(plateau[i]) - (source[1])) and plateau[source[0] + i][
            source[1] + j] == LIBRE:  # NORD-EST
            if corrd:
                self.coord_l += [(source[0] + i, source[1] + j)]
            else:
                self.__mvt_tot_l += [self.__tuple_to_str__((source[0] + i, source[1] + j))]
            i += 1
            j += 1
        if corrd:
            return sorted(self.coord_l)
        return sorted(self.__mvt_tot_l)


    def __tuple_to_str__(self, x):
        """
        Description: permet de transformer le tuple en string.
        x: Le tuple
        return: Un string.
        """
        ligne, colonne = x[0], x[1]
        return str(chr(colonne + 97)) + str(ligne + 1)





