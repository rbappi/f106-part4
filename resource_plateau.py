"""
Nom: Bappi
Prénom: Rahaman
Matricule: 000516227
Section: BA1-INFO
Description: Ce fichier contient la classe Plateau, pour gérer le plateau.
"""

from constantes import *
from resource_coup_joueur import *


class Plateau():
    """
    Description: Gére le plateau
    """
    def __init__(self, n):
        self.__plateau = [[LIBRE for _ in range(n)] for _ in range(n)]
        self.__pos_noir = []
        self.__pos_blanc = []
        self.__pos_fleche = []
        self.__taille = n
        self.__res_str_plat = ""
        self.__alpha = self.__l_alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                                         "q", "r", "s",
                                         "t"]

    @property
    def get_plateau(self):
        """
        Description: Retourne le plateau.
        """
        return self.__plateau

    @property
    def pos_noir(self):
        """
        Description: Retourne les position noir
        """
        return self.__pos_noir

    @property
    def pos_blanc(self):
        """
        Description: Retourne les position noir
        """
        return self.__pos_blanc

    def set_pos_mul_noir(self, pos_noir):
        """
        Description: Place les positions noires
        pos_noir: Positions noir
        """
        self.__pos_noir = pos_noir
        for elem in self.__pos_noir:
            pos = Coup().coup_to_tuple(elem, self.__taille)
            self.__plateau[pos[0]][pos[1]] = JOUEUR_NOIR

    def set_pos_1_noir(self, pos_noir):
        """
        Description: Place la position noire
        pos_noir: Position noir à ajouter
        """
        self.__pos_noir += [pos_noir]
        for elem in self.__pos_noir:
            pos = Coup().coup_to_tuple(elem, self.__taille)
            self.__plateau[pos[0]][pos[1]] = JOUEUR_NOIR

    def set_pos_mul_blanc(self, pos_blanc):
        """
        Description: Place les position blanc
        pos_blanc: Positions blanc à ajouter
        """
        self.__pos_blanc = pos_blanc
        for elem in self.__pos_blanc:
            pos = Coup().coup_to_tuple(elem, self.__taille)
            self.__plateau[pos[0]][pos[1]] = JOUEUR_BLANC

    def set_pos_1_blanc(self, pos_blanc):
        """
        Description: Place la position blanc
        pos_blanc: Position blanc à ajouter
        """
        self.__pos_blanc += [pos_blanc]
        for elem in self.__pos_blanc:
            pos = Coup().coup_to_tuple(elem, self.__taille)
            self.__plateau[pos[0]][pos[1]] = JOUEUR_BLANC

    def set_pos_mul_fleche(self, pos_fleche):
        """
        Description: Place les positions fléches
        pos_fleche: Positions des fléches
        """
        self.__pos_fleche = pos_fleche
        for elem in self.__pos_fleche:
            pos = Coup().coup_to_tuple(elem, self.__taille)
            self.__plateau[pos[0]][pos[1]] = FLECHE

    def set_pos_1_fleche(self, pos_fleche):
        """
        Description: Place les positions fléches
        pos_fleche: Positions des fléches
        """
        self.__pos_fleche += [pos_fleche]
        for elem in self.__pos_fleche:
            pos = Coup().coup_to_tuple(elem, self.__taille)
            self.__plateau[pos[0]][pos[1]] = FLECHE

    def set_plateau(self, plateau):
        """
        Description: Place le plateau
        plateau: Le plateau à placer
        """
        self.__plateau = plateau

    def remove_pos_plateau(self, pos_to_remove):
        """
        Descritption: Points à enlever au sein de la matrice
        pos_to_remove: Points
        """
        pos = Coup().coup_to_tuple(pos_to_remove, self.__taille)
        self.__plateau[pos[0]][pos[1]] = LIBRE

    def remove_pos(self, pos):
        """
        Description: Points à enlever de la listes
        pos: Points
        """
        if pos in self.__pos_blanc:
            self.__pos_blanc.remove(pos)
        elif pos in self.__pos_noir:
            self.__pos_noir.remove(pos)
        elif pos in self.__pos_fleche:
            self.__pos_fleche.remove(pos)

    def string_plateau(self, plateau):
        """
        Description: Permets d'afficher en string le plateau
        plateau: Une matrice de string.
        return: Une string.
        """

        compteur = len(plateau)  # Va permettre d'ajouter les nombres
        for i in range(len(plateau) - 1, -1, -1):
            if compteur >= 10:  # Verifie si le compteur est egale ou plus grand quer 10.
                self.__res_str_plat += str(compteur) + ""  # Ajoute aucune espace apres.
            else:
                self.__res_str_plat += str(compteur) + " "  # Ajoute un espace apres.
            for j in range(len(plateau[i])):
                if j == len(plateau) - 1:  # Verifie si on se trouve a la fin de la matrice.
                    self.__res_str_plat += " " + str(plateau[i][j]) + "\n"  # Fait un passage a ligne.
                else:
                    self.__res_str_plat += " " + str(plateau[i][j])
            compteur -= 1
        for l in range(len(plateau[-1])):
            if l == 0:  # Verifie si l equivaut a 0
                self.__res_str_plat += "   " + self.__l_alpha[l]  # Ajoute trois espace a partir de la premiere lettre
            else:
                self.__res_str_plat += " " + self.__l_alpha[l]  # Ajoute un espace entre les lettres.
        return self.__res_str_plat

    def __str__(self):
        return self.__res_str_plat
