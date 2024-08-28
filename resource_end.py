"""
Nom: Bappi
Prénom: Rahaman
Matricule: 000516227
Section: BA1-INFO
Description: Ce fichier contient la classe End pour predire la fin.
"""
#
from resource_mvt import *
import copy


class End():
    """
    Description: Permet de savoir si le jeu est terminée ou non, en le prédisant ou non.
    """
    def __init__(self, player):
        self.joueur = player
        self.__end_res = (0, 0, 0)

    @property
    def end_res(self):
        return self.__end_res

    def fin(self, plateau, position_noir, position_blanc):
        """
        Description: Permet de verifier si la fin du jeu est atteint.
        plateau: Une matrice de string
        position_noir: Liste des positions des pions noir.
        position_blanc: Liste des positions des pions blancs.
        joueur: Le joueur qui est en train de jouer
        return: Un tuple
        """
        l_posi_noir = []
        l_posi_blanc = []
        for i in position_noir:
            l_posi_noir += Check_mvt().mouvements_possibles(i,
                                                            plateau)  # Ajoute toute les possiblitees de tout les pions noirs
        for j in position_blanc:
            l_posi_blanc += Check_mvt().mouvements_possibles(j,
                                                             plateau)  # Ajoute toute les possiblitees de tout les pions blancs
        if len(l_posi_blanc) == 0 and len(l_posi_noir) == 0:  # Verifie les deux listes sont vides.
            self.__end_res = (
                self.joueur, 1 if self.joueur == 1 else 0,
                1 if self.joueur == 2 else 0)  # Mets comme gagnant le dernier joueurs qui a jouer.
        elif len(l_posi_blanc) == 0 or len(l_posi_noir) == 0:  # Verifie si l'une des deux liste est vide.
            self.__end_res = (1 if len(l_posi_noir) == 0 else 2, 1 if len(l_posi_noir) == 0 else 0,
                              1 if len(l_posi_blanc) == 0 else 0)  # Mets comme gagnant celui qui peut encore bouger.
        conv = self.check_form(plateau, position_noir, position_blanc)
        if conv != None:
            if conv[0] > conv[1]:
                self.__end_res = (2, 0, 1)
            elif conv[0] < conv[1]:
                self.__end_res = (1, 1, 0)
        return self.__end_res

    def label_all_components(self, grid):
        """
        Description: Permet de détécter les différentes zones connexes.
        grid: Matrice de tableau.
        return: Une matrice avec les zones connexes.
        """
        labels = [[0 for _ in range(len(grid))] for _ in range(len(grid))]
        id = 0 # Identifiant de la zone
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[j][i] != FLECHE and labels[j][i] == 0:
                    id += 1
                    self.label_component(grid, id, labels, i, j)
        return labels

    def label_component(self, grid, id, labels, x, y):
        """
        Description: Algorithme qui permet de réellement les zones.
        grid: Matrice du plateau.
        id: Identifiant de la zone.
        labels: Matrice avec les zones connexes.
        x: La position au sein de la matrice en x
        y: La position au sein de la matrice en y
        """
        labels[y][x] = id
        for i in range(-1, 2):
            for j in range(-1, 2):
                x_new = x + i
                y_new = y + j
                if -1 < x_new < len(labels) and -1 < y_new < len(labels) and grid[y_new][x_new] != FLECHE and \
                        labels[y_new][x_new] == 0:
                    self.label_component(grid, id, labels, x_new, y_new) # Appel récursive

    def quickhull(self, s):
        """
        Description: Permet de connaitre les coins de l'enveloppe connexe.
        s: Une liste de points
        return: Une liste de points pour l'neveloppe connexe.
        """
        c = []
        s = sorted(s)
        if len(s) <= 2: # Arrete directement l'algorithme car pas assez de points
            return s
        else:
            a = s.pop(0) # Enleve le point le plus proche
            b = s.pop(-1) # Enleve le point le plus lointain
            left_right = self.find_left_right(a, b, s) # Permet ded découper la liste de point selon si ils se trouvent à droite ou à gauche du segment.
            s0 = left_right[0] # Les points à gauches
            s1 = left_right[1] # Les points à droites
            c += [a] + [b] # Ajoutes ces points dans le resultats
            self.find_hull(s0, a, b, c)
            self.find_hull(s1, b, a, c)
        return sorted(c)

    def find_hull(self, s, a, b, c):
        if len(s) == 0:
            return []
        far = self.find_far(a, b, s)  # Le points le plus lointains selon le segment ab
        s.remove(far)
        c += [far] # Le point est ajouté dans le résultat
        left_right_a = self.find_left_right(a, far, s) # Permet ded découper la liste de point selon si ils se trouvent à droite ou à gauche du segment.
        left_right_b = self.find_left_right(b, far, s)
        new_s1 = left_right_a[0] # Les points à gauches
        new_s2 = left_right_b[1] # Les points à droites
        self.find_hull(new_s1, a, far, c)
        self.find_hull(new_s2, far, b, c)

    def find_far(self, a, b, s):
        """
        Description: Permet de connaitre le points le plus éloigné d'un segment.
        a: Un pooint
        b: Un point
        s: Une liste de points
        return: Un points
        """
        res = None
        dist_plus = -1
        for elem in s:
            dist_1 = abs(((a[1] - b[1]) * elem[0]) + ((b[0] - a[0]) * elem[1]) + ((a[0] * b[1]) - (b[0] * a[1])))
            dist = dist_1 / ((((a[1] - b[1]) ** 2) + ((b[0] - a[0]) ** 2)) ** (1 / 2))
            if dist > dist_plus: # Détecte si la distance actuel est plus grande que la distance la plus grande ancienne
                dist_plus = dist
                res = elem
        return res

    def find_left_right(self, a, b, s):
        """
        Descritpion: Permet de connaitre les points à gauche ou à droite d'un segment.
        a: Un point
        b: Un point
        s: Une liste de points
        return: Une matrice de liste de points
        """
        left = []
        right = []
        res = [left, right]
        if a[0] - b[0] == 0:
            return res
        else:
            for elem in s:
                if ((b[0] - a[0]) * (elem[1] - a[1])) - ((b[1] - a[1]) * (elem[0] - a[1])) < 0: # A droite
                    right += [elem]
                elif ((b[0] - a[0]) * (elem[1] - a[1])) - ((b[1] - a[1]) * (elem[0] - a[1])) > 0: # A gauche
                    left += [elem]
        return res

    def find_points(self, l):
        """
        Permet de trouver les points des labels
        l: Une matrice
        return: Un dictionnaire
        """
        res = {}
        for i in range(len(l)):
            for j in range(len(l)):
                if l[i][j] != 0:
                    if l[i][j] not in res:
                        res[l[i][j]] = [(i, j)] # Créer la clé s'il n'existe pas encore
                    else:
                        res[l[i][j]] += [(i, j)]
        return res

    def count_line(self, l):
        """
        Description: Permet de détecter le nombre de coup au sein d'une ligne
        l: Une liste de points
        return: Un integer
        """
        if l[0][0] == l[1][0]: # Meme x
            res = abs(l[0][1] - l[1][1])
        elif l[0][1] == l[1][1]: # Meme y
            res = abs(l[0][0] - l[1][0])
        else:
            res = abs(l[0][0] - l[1][0])
        return res

    def count_rectangle(self, l):
        """
        Description: Permet de détecter le nombre de coup au sein d'un rectangle.
        l: Une liste de points
        return: Un integer
        """
        l = sorted(l)
        res = None
        if (abs(l[0][0] - l[2][0]) == abs(l[1][0] - l[3][0])) and abs(l[0][1] - l[1][1]) == abs(l[2][1] - l[3][1]):
            if l[0][0] == l[1][0] and l[1][1] == l[3][1]:
                res = ((abs(l[0][1] - l[1][1]) + 1) * (abs(l[0][0] - l[3][0]) + 1)) - 1
        return res

    def count_triangle(self, l):
        """
        Description: Permet de détecter le nombre de coup au sein d'un rectangle.
        l: Une liste de points
        return: Un integer
        """
        l.sort()
        ab = (((l[1][0] - l[0][0]) ** (2)) + ((l[1][1] - l[0][1]) ** (2))) ** (1 / 2)
        bc = (((l[2][0] - l[1][0]) ** (2)) + ((l[2][1] - l[1][1]) ** (2))) ** (1 / 2)
        ca = (((l[0][0] - l[1][0]) ** (2)) + ((l[0][1] - l[1][1]) ** (2))) ** (1 / 2)
        s = (1 / 2) * (ab + bc + ca)
        res = (s * (s - ab) * (s - bc) * (s - ca)) ** (1 / 2)
        return int(res)

    def check_form(self, plateau, pos_noir, pos_blanc):
        """
        Description: La fonction qui va permettre de rearrenger les points selon les position des joueurs.
        plateau: Une matrice
        pos_noir: Une liste de points des noires
        pos_blanc: Une listes de points des blancs
        return: Un liste de points des joueur
        """
        res = None
        quick_points_noir = {}
        quick_points_blanc = {}
        label = self.label_all_components(plateau)
        points_dict = self.find_points(label)
        finish = False
        points_dict_keys = list(points_dict.keys())
        k = 0
        while k < (len(points_dict_keys)) and not finish: # Boucle permettant de donner les ré-attribuer les points selon les joueurs
            finish_2 = False
            i = 0
            while not finish_2 and i < len(points_dict[points_dict_keys[k]]):
                if points_dict[points_dict_keys[k]][i] in pos_noir: # Reassigne les points aux noir
                    quick_points_noir[points_dict_keys[k]] = self.quickhull(points_dict[points_dict_keys[k]])
                    finish_2 = True
                    points_dict_keys.remove(points_dict_keys[k])
                    k -= 1
                elif points_dict[points_dict_keys[k]][i] in pos_blanc: # Reassigne les points aux noir
                    quick_points_blanc[points_dict_keys[k]] = self.quickhull(points_dict[points_dict_keys[k]])
                    finish_2 = True
                    points_dict_keys.remove(points_dict_keys[k])
                    k -= 1
                i += 1
            k += 1
            if len(points_dict_keys) == 0:
                finish = True
        form_noir = self.decide_form(quick_points_noir)
        form_blanc = self.decide_form(quick_points_blanc)
        if form_noir != None and form_blanc != None: # Permets de ne pas le comptabiliser si un des zones n'est utilisable
            res = (form_noir, form_blanc)
        return res

    def decide_form(self, dict):
        """
        Description: Decide la forme et fait appele les fonctions valables
        dict: Un dictionnaire
        return: Un score en int
        """
        nbre_tot = 0
        good_form = 0
        for elem in dict:
            if len(dict[elem]) == 2: # Si c'est une droite
                form = self.count_line(dict[elem])
                if isinstance(form, int): # Ajoute le point si c'est un int
                    nbre_tot += form
                    good_form += 1
            elif len(dict[elem]) == 4: # Si c'est un carré, rectangle
                form = self.count_rectangle(dict[elem])
                if isinstance(form, int):
                    nbre_tot += form
                    good_form += 1
            elif len(dict[elem]) == 3: # Si c'est un triangle
                form = self.count_triangle(dict[elem])
                if isinstance(form, int):
                    nbre_tot += form
                    good_form += 1
            elif len(dict[elem]) == 1:
                good_form += 1
        if nbre_tot == 0 or good_form != len(dict): # Ne considére pas les point si les formes ne sont pas valables
            nbre_tot = None
        return nbre_tot
