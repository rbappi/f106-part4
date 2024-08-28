"""
Nom: Bappi
Prénom: Rahaman
Matricule: 000516227
Section: BA1-INFO
Descrption: Ce fichier contient les classes: - Minimax
                                             - Coup_player
                                             - Coup
            qui permettront de faire le coup des joueurs
            et des bots
"""

from constantes import *
import copy
import random


class Coup_player():
    """
    Description: Cette classe permet au joueur et au bot
                 de jouer
    player: Joueur qui joue
    """
    
    def __init__(self, player):
        import resource_mvt
        self.joueur = player
        self.mvt_possible = resource_mvt.Check_mvt()
        self.mvt_fleche = resource_mvt.Check_mvt()

    def coup_joueur(self, position_joueur, plateau):
        """
        Description: Permet de fair un input et de savoir s'il est correct.
        joueur: Le joueur qui est en train de jouer, 1: Blanc et 2:Noir
        position_joueur: Les positions du joueurs.
        plateau: Une matrice qui represente le plateau.
        """
        import resource_plateau
        plate = resource_plateau.Plateau(len(plateau))
        plate.set_plateau(plateau)
        print(MESSAGE_COUP.format(self.joueur))  # Imprime la constante MESSAGE_COUP
        entree_coup = input()  # Permet de faire l'input d'un joueur.
        entree_coup_2 = copy.deepcopy(entree_coup.split(">"))  # Fait une copy et un split du coup.
        sep = ""
        if sep.join(entree_coup_2).isalnum() == False:  # Verifie si tout les caracter sont alphanumerique.
            print(Error.ERREUR_COUP)  # Imprime l'erreur.
            self.coup_joueur(position_joueur, plateau)  # Fait un appel recursive.
        else:
            coup = entree_coup.split(">")  # pos0: rein de depart ; #pos1: pos rein d'arrive ; #pos2: pos fleche
            if len(coup) != 3:
                print(Error.ERREUR_COUP)  # Imprime l'erreur.
                self.coup_joueur(position_joueur, plateau)  # Fait un appel recursive.
            else:
                if coup[
                    0] not in position_joueur:  # Verifie si la premier partie du coup fait partie de la liste des pions du joeur.
                    print(Error.ERREUR_REINE)  # Imprime l'erreur.
                    self.coup_joueur(position_joueur, plateau)  # Fait un appel recursive.
                else:
                    plateau_2 = copy.deepcopy(plateau)  # Fait une copie de la matrice.
                    plate_2 = resource_plateau.Plateau(len(plateau))
                    plate_2.set_plateau(plateau_2)
                    possi_arrive = self.mvt_possible.mouvements_possibles(coup[0],
                                                                          plateau)  # Fait une liste des mouvememts possibles.  #TODO: FAIRE LES MVT_POSSIBES, ET COUP TO TUPLE
                    if coup[
                        1] not in possi_arrive:  # Verifie si la seconde partie du coup n'est pas dans les mouvements possibles.
                        print(Error.ERREUR_CHEMIN)  # Imprime l'erreur.
                        self.coup_joueur(position_joueur, plateau)  # Fait un appel recursive.
                    else:
                        plate_2.remove_pos_plateau(coup[0])
                        plate_2.set_pos_1_blanc(coup[1]) if self.joueur == 1 else plate_2.set_pos_1_noir(coup[1])
                        possi_fleche = self.mvt_fleche.mouvements_possibles(coup[1], plate_2.get_plateau)
                        if coup[1] not in possi_arrive or coup[2] not in possi_fleche or coup[0] not in position_joueur:
                            print(Error.ERREUR_CHEMIN)  # Imprime l'erreur.
                            self.coup_joueur(position_joueur, plateau)  # Fait un appel recursive.
                        else:
                            position_joueur.remove(coup[0])
                            position_joueur.append(coup[1])
                            plate.remove_pos_plateau(coup[0])
                            plate.set_pos_1_blanc(coup[1]) if self.joueur == 1 else plate.set_pos_1_noir(coup[1])
                            plate.set_pos_1_fleche(coup[2])

    def bot_ia(self, pos_noir, plateau, coup_bot):
        """
        Description: Permet à Minimax de jouer
        pos_noir: Les positions du Minimax
        plateau: Le plateau
        coup_bot: Le coup de Minimax
        return: None
        """
        import resource_plateau # Import le fichier du plateau
        coup_l = coup_bot.split(">") # Découpe le coup_bot
        plate = resource_plateau.Plateau(len(plateau)) # Assigne une variable pour utiliser la classe Plateau
        plate.set_plateau(plateau) # Mets le plateau pour qui'il soit utilisé
        pos_noir.remove(coup_l[0]), pos_noir.append(coup_l[1]) # Enleve le point de base du plateau et mets le point finale dans le plateau
        plate.remove_pos_plateau(coup_l[0])
        plate.set_pos_mul_noir(pos_noir) # Place tous les points
        plate.set_pos_1_fleche(coup_l[2]) # Place toutes les fléches
        plateau = plate.get_plateau


class Minimax():
    """
    Description: Permet au bot de sortir son coup
    """

    def __init__(self, plateau, position_blanc, position_noir, black=True):
        self.__plateau = plateau
        self.__position_blanc = position_blanc
        self.__position_noir = position_noir
        


    def minimax_black(self, profondeur=2, maxi=True):
        """
        Description: IA qui joue contre le joueur humain
        plateau: Le plateau ou les joueur jouent.
        profondeur: Nous indiques quelle joueur nous allons etudiers.
        param maxi: Verifient que c'est le IA qui joue.
        return: Un tuple avec 2 parametres.
        """
        import resource_end
        import resource_plateau
        import resource_mvt
        finish_player_1 = resource_end.End(1)
        if profondeur == 0 or finish_player_1.fin(self.__plateau, self.__position_noir, self.__position_blanc)[
            0] != 0:  # Verifie si le profondeur vaut 0 ou si c'est la fin du jeu
            end_2 = finish_player_1.fin(self.__plateau, self.__position_noir, self.__position_blanc)[
                0]  # Fait appele fin pour connaitre la fin du jeu.
            if end_2 == 0:
                res = 0
            elif end_2 == 1:
                res = -1
            else:
                res = 1
            return (None, res)

        if maxi:  # Verifie si c'est au tout de l'IA.
            best_s = -1000  # Mets une forme de limiteur
            best_c = []  # Initialise une liste vide ou on va ajouter les coups
            plateau_2 = copy.deepcopy(self.__plateau)  # Copie le plateau.
            plate_2 = resource_plateau.Plateau(len(plateau_2))
            plate_2.set_plateau(plateau_2)
            for reine in self.__position_noir:  # Va simuler pour tout les reines.
                mvt_possible_bot_1 = resource_mvt.Check_mvt()
                l_posi_noir = mvt_possible_bot_1.mouvements_possibles(reine,
                                                                      plateau_2)  # Va prendre tout les mouvemnt possible de reine
                for mvt_reine in l_posi_noir:  # Va simuler pour tout les mouvement possibles.
                    mvt_possible_bot_2 = resource_mvt.Check_mvt()
                    plate_2.remove_pos(reine)
                    plate_2.set_pos_1_noir(mvt_reine)
                    self.__position_noir.remove(reine)
                    self.__position_noir.append(mvt_reine)
                    l_posi_fleche = mvt_possible_bot_2.mouvements_possibles(mvt_reine,
                                                                            plateau_2)  # Va prendre tout les fleches possibles a partir position modifier
                    for fleche in l_posi_fleche:  # Va simuler pour tout les fleches possibles
                        finish_bot_1 = resource_end.End(2)
                        plate_2.set_pos_1_fleche(fleche)
                        score = self.minimax_black(profondeur - 1, False)[
                            1]  # Fait un appel recursive.
                        coup = f"{reine}>{mvt_reine}>{fleche}"  # Prepare le coup
                        end = finish_bot_1.fin(plateau_2, self.__position_noir,
                                               self.__position_blanc)  # Verifie si la partie est finis
                        if end[0] == 1:
                            gagnant = -1
                        elif end[0] == 2:
                            gagnant = 1
                        else:
                            gagnant = 0
                        if best_s < score:
                            best_s = score
                            best_c = [(coup, gagnant)]
                        elif best_s == score:
                            best_c += [(coup, gagnant)]
                        plate_2.remove_pos_plateau(fleche)
                    plate_2.set_pos_1_noir(reine)
                    plate_2.remove_pos_plateau(mvt_reine)
                    self.__position_noir.remove(mvt_reine)  # Remet au position de base
                    self.__position_noir.append(reine)  # Remet au position de base
        else:
            best_s = 1000  # Mets une forme de limiteur
            best_c = []  # Initialise une liste vide ou on va ajouter les coups
            plateau_2 = copy.deepcopy(self.__plateau)  # Copie le plateau.
            plate_2 = resource_plateau.Plateau(len(plateau_2))
            plate_2.set_plateau(plateau_2)
            for reine in self.__position_blanc:  # Va simuler pour tout les reines.
                mvt_possible_player_1 = resource_mvt.Check_mvt()
                l_posi_blanc = mvt_possible_player_1.mouvements_possibles(reine,
                                                                          plateau_2)  # Va prendre tout les mouvemnt possible de reine
                for mvt_reine in l_posi_blanc:  # Va simuler pour tout les mouvement possibles.
                    mvt_possible_player_2 = resource_mvt.Check_mvt()
                    plate_2.remove_pos_plateau(reine)
                    plate_2.set_pos_1_blanc(mvt_reine)
                    self.__position_blanc.remove(reine)
                    self.__position_blanc.append(mvt_reine)
                    l_posi_fleche = mvt_possible_player_2.mouvements_possibles(mvt_reine,
                                                                               plateau_2)  # Va prendre tout les fleches possibles a partir position modifier
                    for fleche in l_posi_fleche:  # Va simuler pour tout les fleches possibles
                        finish_player_2 = resource_end.End(1)
                        plate_2.set_pos_1_fleche(fleche)
                        score = self.minimax_black(profondeur - 1, True)[
                            1]  # Fait un appel recursive.
                        coup = f"{reine}>{mvt_reine}>{fleche}"  # Prepare le coup
                        end = finish_player_2.fin(plateau_2, self.__position_noir,
                                                  self.__position_blanc)  # Verifie si la partie est finis
                        if end[0] == 1:
                            gagnant = -1
                        elif end[0] == 2:
                            gagnant = 1
                        else:
                            gagnant = 0
                        if best_s > score:
                            best_s = score
                            best_c = [(coup, gagnant)]
                        elif best_s == score:
                            best_c += [(coup, gagnant)]
                        plate_2.remove_pos_plateau(fleche)
                    plate_2.set_pos_1_blanc(reine)
                    plate_2.remove_pos_plateau(mvt_reine)
                    self.__position_blanc.remove(mvt_reine)  # Remet au position de base
                    self.__position_blanc.append(reine)  # Remet au position de base
        if len(best_c) == 0:
            return (None, -1)
        return (random.choice(best_c))  # Retourn un coup au hasard

    def minimax_white(self, profondeur=2, maxi=True):
        """
        Description: IA qui joue contre le joueur humain
        plateau: Le plateau ou les joueur jouent.
        profondeur: Nous indiques quelle joueur nous allons etudiers.
        param maxi: Verifient que c'est le IA qui joue.
        return: Un tuple avec 2 parametres.
        """
        import resource_end
        import resource_plateau
        import resource_mvt
        finish_player_1 = resource_end.End(2)
        if profondeur == 0 or finish_player_1.fin(self.__plateau, self.__position_noir, self.__position_blanc)[
            0] != 0:  # Verifie si le profondeur vaut 0 ou si c'est la fin du jeu
            end_2 = finish_player_1.fin(self.__plateau, self.__position_noir, self.__position_blanc)[
                0]  # Fait appele fin pour connaitre la fin du jeu.
            if end_2 == 0:
                res = 0
            elif end_2 == 1:
                res = -1
            else:
                res = 1
            return (None, res)

        if maxi:  # Verifie si c'est au tout de l'IA.
            best_s = -1000  # Mets une forme de limiteur
            best_c = []  # Initialise une liste vide ou on va ajouter les coups
            plateau_2 = copy.deepcopy(self.__plateau)  # Copie le plateau.
            plate_2 = resource_plateau.Plateau(len(plateau_2))
            plate_2.set_plateau(plateau_2)
            for reine in self.__position_blanc:  # Va simuler pour tout les reines.
                mvt_possible_bot_1 = resource_mvt.Check_mvt()
                l_posi_blanc = mvt_possible_bot_1.mouvements_possibles(reine,
                                                                      plateau_2)  # Va prendre tout les mouvemnt possible de reine
                for mvt_reine in l_posi_blanc:  # Va simuler pour tout les mouvement possibles.
                    mvt_possible_bot_2 = resource_mvt.Check_mvt()
                    plate_2.remove_pos(reine)
                    plate_2.set_pos_1_blanc(mvt_reine)
                    self.__position_blanc.remove(reine)
                    self.__position_blanc.append(mvt_reine)
                    l_posi_fleche = mvt_possible_bot_2.mouvements_possibles(mvt_reine,
                                                                            plateau_2)  # Va prendre tout les fleches possibles a partir position modifier
                    for fleche in l_posi_fleche:  # Va simuler pour tout les fleches possibles
                        finish_bot_1 = resource_end.End(1)
                        plate_2.set_pos_1_fleche(fleche)
                        score = self.minimax_white(profondeur - 1, False)[
                            1]  # Fait un appel recursive.
                        coup = f"{reine}>{mvt_reine}>{fleche}"  # Prepare le coup
                        end = finish_bot_1.fin(plateau_2, self.__position_noir,
                                               self.__position_blanc)  # Verifie si la partie est finis
                        if end[0] == 1:
                            gagnant = -1
                        elif end[0] == 2:
                            gagnant = 1
                        else:
                            gagnant = 0
                        if best_s < score:
                            best_s = score
                            best_c = [(coup, gagnant)]
                        elif best_s == score:
                            best_c += [(coup, gagnant)]
                        plate_2.remove_pos_plateau(fleche)
                    plate_2.set_pos_1_blanc(reine)
                    plate_2.remove_pos_plateau(mvt_reine)
                    self.__position_blanc.remove(mvt_reine)  # Remet au position de base
                    self.__position_blanc.append(reine)  # Remet au position de base
        else:
            best_s = 1000  # Mets une forme de limiteur
            best_c = []  # Initialise une liste vide ou on va ajouter les coups
            plateau_2 = copy.deepcopy(self.__plateau)  # Copie le plateau.
            plate_2 = resource_plateau.Plateau(len(plateau_2))
            plate_2.set_plateau(plateau_2)
            for reine in self.__position_noir:  # Va simuler pour tout les reines.
                mvt_possible_player_1 = resource_mvt.Check_mvt()
                l_posi_noir = mvt_possible_player_1.mouvements_possibles(reine,
                                                                          plateau_2)  # Va prendre tout les mouvemnt possible de reine
                for mvt_reine in l_posi_noir:  # Va simuler pour tout les mouvement possibles.
                    mvt_possible_player_2 = resource_mvt.Check_mvt()
                    plate_2.remove_pos_plateau(reine)
                    plate_2.set_pos_1_noir(mvt_reine)
                    self.__position_noir.remove(reine)
                    self.__position_noir.append(mvt_reine)
                    l_posi_fleche = mvt_possible_player_2.mouvements_possibles(mvt_reine,
                                                                               plateau_2)  # Va prendre tout les fleches possibles a partir position modifier
                    for fleche in l_posi_fleche:  # Va simuler pour tout les fleches possibles
                        finish_player_2 = resource_end.End(2)
                        plate_2.set_pos_1_fleche(fleche)
                        score = self.minimax_white(profondeur - 1, True)[
                            1]  # Fait un appel recursive.
                        coup = f"{reine}>{mvt_reine}>{fleche}"  # Prepare le coup
                        end = finish_player_2.fin(plateau_2, self.__position_noir,
                                                  self.__position_blanc)  # Verifie si la partie est finis
                        if end[0] == 1:
                            gagnant = -1
                        elif end[0] == 2:
                            gagnant = 1
                        else:
                            gagnant = 0
                        if best_s > score:
                            best_s = score
                            best_c = [(coup, gagnant)]
                        elif best_s == score:
                            best_c += [(coup, gagnant)]
                        plate_2.remove_pos_plateau(fleche)
                    plate_2.set_pos_1_noir(reine)
                    plate_2.remove_pos_plateau(mvt_reine)
                    self.__position_noir.remove(mvt_reine)  # Remet au position de base
                    self.__position_noir.append(reine)  # Remet au position de base
        if len(best_c) == 0:
            return (None, -1)
        return (random.choice(best_c))  # Retourn un coup au hasard



class Timer():
    def __init__(self):
        self.start_timer = None
        self.__begin_timer()
    
    def __begin_timer(self):
        self.start_timer = time.perf_counter()
    
    def act_timer(self):
        return (time.perf_counter() - self.start_timer())
    
    def ok_timer(self):
        return 1.75 > self.act_timer



class Coup():
    """
    Description : Permet de re-traduir en tuple
    """
    def __init__(self):
        self.__coup_tuple = None

    @property
    def coup_tuple(self):
        return self.__coup_tuple

    def coup_to_tuple(self, coup, taille):
        """
        Description: Permet de transformer le string en tuple.
        coup: Un coup en string.
        taille: La taille du plateau.
        return: Un tuple
        """
        coup_2 = [i for i in coup]  # Creer une liste a partir de coup.
        if len(coup) <= 2:
            colonne, ligne = coup_2[0], coup_2[1]  # Decompose en deux variables.
        else:
            colonne, ligne = coup_2[0], (coup_2[1] + coup_2[2])  # Decompose en deux variables.
        if (ord(colonne) - 97) < taille and int(ligne) - 1 < taille and int(
                ligne) != 0:  # Verifie si la colonne, ligne est plus petit que taille, et que la valeur de ligne n'equivaut pas a 0.
            self.__coup_tuple = (int(ligne) - 1, (ord(colonne) - 97))
        return self.__coup_tuple
