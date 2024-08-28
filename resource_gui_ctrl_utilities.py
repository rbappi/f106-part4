"""
Nom: Bappi
Prénom: Rahaman
Matricule: 000516227
Section: BA1-INFO
Descrption: Ce fichier est un set d'outils pour le GUI
"""


from resource_end import End

class Utilities():
    """
    Outils pour le gui
    """
    def __init__(self):
        self.bidon = None #TODO

    def coup_to_tuple(self, coup, taille):
        """
        Coup to tuple adapte a GUI
        coup: Le coup a traduire en str
        taille: La taille du plateau en int
        """
        coup_2 = [i for i in coup]  # Creer une liste a partir de coup.
        if len(coup) <= 2:
            colonne, ligne = coup_2[0], coup_2[1]  # Decompose en deux variables.
        else:
            colonne, ligne = coup_2[0], (coup_2[1] + coup_2[2])  # Decompose en deux variables.
        if (ord(colonne) - 97) < taille and int(ligne) - 1 < taille and int(ligne) != 0:  # Verifie si la colonne, ligne est plus petit que taille, et que la valeur de ligne n'equivaut pas a 0.
            coup_tuple = (taille - int(ligne), (ord(colonne) - 97))
        return coup_tuple # TODO VERIFY

    def qt_tuple_to_old(self, qt, taille):
        """
        Permet de traduire les nouveaux types de coordonnes au ancien
        """
        return (taille-qt[0]-1, qt[1])

    def tuple_to_str(self, x):
        """
        Description: permet de transformer le tuple en string.
        x: Le tuple
        return: Un string.
        """
        ligne, colonne = x[0], x[1]
        return str(chr(colonne + 97)) + str(ligne + 1)

    def tuple_to_str_new(self, x, taille):
        """
        Description: permet de transformer le tuple en string adapter au GUI
        x: Le tuple
        return: Un string.
        """
        ligne, colonne = x[0], x[1]
        return str(chr(colonne + 97)) + str(taille - ligne)

    def old_to_qt(self, old, taille):
        return (old[0]-taille+1, old[1])
    
    def check_end(self, plateau, position_noir, position_blanc, player):
        """
        Verifie la fin
        """
        return End(player).fin(plateau, position_noir, position_blanc)
    
    def tour_ai(self, tour, j1, j2):
        """
        Verifie quelle IA joue
        """
        res = (None, False)
        if tour == 0 and j1 == "IA":
            res = ("IA-0-1", True)
        elif tour == 1 and j2 == "IA":
            res = ("IA-1-2", True)
        return res
    

    def music(self, choice):
        """
        Ajoute la musique selon le choix de l'utilisateur
        """
        import pygame
        dict_music = {"Jazz": "resource_gui/jazz_2.ogg", "Stressante": "resource_gui/stressante.ogg"}
        pygame.init()
        pygame.mixer.music.load(dict_music[choice])
        pygame.mixer.music.play(-1)
    
