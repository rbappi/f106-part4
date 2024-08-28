"""
Nom: Bappi
Prénom: Rahaman
Matricule: 000516227
Section: BA1-INFO
Descrption: Ce fichier le code pour afficher et jouer avec un GUI.
"""

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from resource_mvt import Check_mvt
from resource_plateau import Plateau
from resource_coup_joueur import Coup, Minimax
from resource_gui_ctrl_utilities import Utilities
import threading
import copy
import time
import sys



class App(QWidget):
    """
    Description: La classe du GUI
    """
    def __init__(self, taille=10, plateau=[]):
        super().__init__()
        self.title = 'Jeu des Amazones'
        self.left = 10
        self.top = 10
        self.width = 1650
        self.height = 750
        self.dict_image = {"blanc": "resource_gui/blanc.png", "noir": "resource_gui/noir.png", "mur": "resource_gui/dot.png"}
        self.taille = taille
        self.plateau = plateau
        self.j1 = "j1"
        self.j2 = "j2"
        self.utilities = Utilities()
        self.chck_pos = Check_mvt()
        self.init_values()
        self.init_other_values()
        self.initUI()
        
    def init_values(self):
        """
        Initialisation de certaine valeur dynamique pour le bon fonctionneent du jeu
        """
        self.list_pos_black = []
        self.list_pos_white = []
        self.list_mur = []
        self.tour = 0
        self.fin = False
    
    def reset_data(self):
        """
        Initialisation de certaine valeur dynamique pour gerer le "gameplay"
        """
        self.pos_queen_b_clicked = False # Tous les variables clicked verifie temporairement si une cellule a ete cliquer aupravant
        self.pos_dest_b_clicked = False
        self.pos_mur_b_clicked = False
        self.pos_queen_w_clicked = False
        self.pos_dest_w_clicked = False
        self.pos_mur_w_clicked = False
        self.list_possibilities_black = [] # Tous les varibles possibilities et poss, sauvegarde temporairement les possibilitees
        self.list_possibilities_white = []
        self.list_mur_poss = []
        self.mur_b_poss = []
        self.mur_w_poss = []
        self.depart_pos = None # Tous les varibles pos permettent de savoir temporairement la position en tuple
        self.dest_pos = None
        self.mur_des_pos = None
        self.depart_hist = "" # Tous les variables hist permettent de savoir quoi ecrire pour la partie historique
        self.dest_hist = ""
        self.mur_hist = ""

    def init_other_values(self):
        """
        Initialisation de varables qui vont reseter constante au cours de la partie
        """
        self.file = None
        self.start = False
        self.restart = False
        self.table_exists = False
        self.rediff = None

    def initUI(self):
        """
        Initalise les differentes partie de l'interface graphique
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.init_buttons()
        self.layout_options = QVBoxLayout() # Creation du layout des options
        self.layout_main = QHBoxLayout() # Creation du layout princpale
        self.layout_options.addWidget(self.start_b)
        self.layout_options.addWidget(self.j1_b)
        self.layout_options.addWidget(self.j1_t)
        self.layout_options.addWidget(self.j2_b)
        self.layout_options.addWidget(self.j2_t)
        self.layout_options.addWidget(self.delai_IA_t)
        self.layout_options.addWidget(self.delai_IA_b)
        self.layout_options.addWidget(self.save_t)
        self.layout_options.addWidget(self.save_b)
        self.layout_options.addWidget(self.rediff_t)
        self.layout_options.addWidget(self.rediff_b)
        self.layout_options.addWidget(self.file_rediff)
        self.layout_options.addWidget(self.music_chooser_t)
        self.layout_options.addWidget(self.music_chooser_b)
        self.layout_options.addWidget(self.music_enable)
        self.layout_options.addWidget(self.file_t)
        self.layout_options.addWidget(self.file_b)
        self.layout_main.addLayout(self.layout_options)
        self.setLayout(self.layout_main)
        self.show()
        QMessageBox.question(self, "Attention", f"""
        Veillez à faire attention au message suivant : 

        - Si vous vous voulez rediffuser une partie, veillez à suivre les règles suivantes pour le format du fichier : 
            - Les lignes 1 à 4 sont les lignes classiques : 1: Taille, 2: Position noir, 3: Position blanche, 4: Positions murs 
            - Les lignes 6 a ... sont les lignes des coups qui devront être écrits selon le format suivant: 
            15:10:21: Joueur 1: c1>d2>d4 
            15:10:25: Joueur 2: b4>a3>a4 
            - Il y a un fichier exemple à votre disposition nommé: ex_rediff.txt 
            - Remarque: Actuellement la rediffusion n'est pas parfaitement fonctionnelle mais l'enregistrement l'est. 
        - Pour activer la musique, veillez bien à cocher la case et à avoir impérativement pygame installer, si vous ne l'avez pas, 
        veuillez ne pas cocher la case.
        - Les paramètres ne peuvent pas être changées en pleine partie, ni en fin de partie, vous devrez relancer le jeu pour les changées. 
        - Lors du choix du fichier .txt, veillez bien à choisir un fichier .txt conforme et de ne pas fermer la fenêtre sans avoir choisis. 
        - Ce jeu a ete devoloppees sur et pour Linux Ubuntu.
        - Veuillez si possible lancer le jeu avec "python partie4.py" car sans cel les images ne s'afficheront pas bien
        Merci beaucoup pour d'avoir pris le temps de lire et bon jeu ! 
        Bappi Rahaman 
        000516227 
        BA1-INFO 
                                                """, QMessageBox.Yes)

    def init_buttons(self):
        """
        Initalise tous les dfferents bouttons
        """
        # Start
        self.start_b = QPushButton('Commencer', self)
        self.start_b.setToolTip('Ce bouton permet de (re)commencer la partie')
        self.start_b.move(1125,70) #TODO CENTER
        self.start_b.clicked.connect(self.start_game)


        # Joueur 1
        self.j1_t = QLabel('Ce menu permet de\n choisir le joueur 1', self)
        self.j1_t.move(1100, 100)
        self.j1_b = QComboBox(self)
        self.j1_b.setToolTip('Ce menu permet de choisir le joueur 1')
        self.j1_b.addItems(["Joueur", "IA"])
        self.j1_b.move(1125, 150)
        self.j1_b.currentIndexChanged.connect(self.selection)

        # Joueur 2
        self.j2_t = QLabel('Ce menu permet de\n choisir le joueur 2', self)
        self.j2_t.move(1100, 180)
        self.j2_b = QComboBox(self)
        self.j2_b.setToolTip('Ce menu permet de choisir le joueur 2')
        self.j2_b.addItems(["Joueur", "IA"])
        self.j2_b.move(1125, 230)
        self.j2_b.currentIndexChanged.connect(self.selection)


        # Fichier de reine
        self.file_t = QLabel("Ce bouton permet de\n choisir un fichier du plateau")
        self.file_t.move(1100, 260)
        self.file_b = QPushButton("Fichier du plateau",self)
        self.file_b.setToolTip("Ce bouton permet de choisir un fichier du plateau")
        self.file_b.move(1125, 310)
        self.file_b.clicked.connect(self.slot_method_file)

        # Temps Bot
        self.delai_IA_t = QLabel("Ce menu permet de\n choisir le delai de l'IA")
        self.delai_IA_b = QComboBox(self)
        self.delai_IA_b.setToolTip("Ce menu permet de\n choisir le delai de l'IA")
        self.delai_IA_b.addItems(["2s","5s","10s", "20s", "25s", "30s", "35s", "40s", "45s", "50s", "55s", "60s", "65s"])

        # Choix rediff/enregistrement
        self.save_t = QLabel("Cette boite permet d'enregistrer la partie")
        self.save_b = QCheckBox("Enregistrement")
        self.rediff_t = QLabel("Cette boite permet de rediffuser une partie")
        self.rediff_b = QCheckBox("Rediffusion")
        self.file_rediff = QPushButton("Fichier de rediffusion")
        self.rediff_b.clicked.connect(self.verify_rediff)
        self.save_b.clicked.connect(self.verify_rediff)
        self.file_rediff.clicked.connect(self.slot_method_file)

        # Choix musique
        self.music_chooser_t = QLabel("Ce menu permet de\n choisir la musiqe qui va se jouer")
        self.music_chooser_b = QComboBox(self)
        self.music_chooser_b.addItems(["Jazz", "Stressante"])
        self.music_enable = QCheckBox("Music")
        self.music_enable.clicked.connect(self.verify_pygame)


        

    def init_buttons_other(self):
        """
        Initilise les bouttons et widget qui vont etre afficher a droite du plateau
        """
        self.start_b.setText("Recommencer") # Change le bouton start pour recommencer
        save_j1 = "Joueur" if self.j1 == "j1" else "IA"
        save_j2 = "Joueur" if self.j2 == "j2" else "IA"
        self.j1_b.blockSignals(True) # Bloque le changement d'option
        self.j2_b.blockSignals(True)
        delai = self.delai_IA_b.currentText() # Sauvgarde la valeur du delai
        if len(delai) == 3:
            self.delai = int(delai[:2])
        else:
            self.delai = int(delai[:1])
        self.delai_IA_b.blockSignals(True)
        self.parametre_show = QLabel(f"Parametre actuel\nJoueur 1: {save_j1}\nJoueur 2: {save_j2}\nDelai de l'IA : {self.delai}seconde\nAttention: Les parametres\nne peuvent pas etre changer\nen cours de partie, ni en fin de partie!")
        self.parametre_show.setFont(QFont("AnyStyle", 10, QFont.Bold))
        self.layout_options.addWidget(self.parametre_show)
        current_time = time.strftime("%H:%M:%S")
        self.old_historique = f"Historique des coup:\nLa partie a commence a {current_time}\n" # Permet de montrer l'historique des coups jouees
        self.history = QLabel(self.old_historique, self)
        self.history.setFont(QFont("AnyStyle", 15))
        self.layout_main.addWidget(self.history) # Ajout des widgets a droite du plateau


    def verify_pygame(self):
        if self.music_enable.isChecked():
            QMessageBox.question(self, "Attention", "Veillez a avoir pygame installee pour la musique!", QMessageBox.Yes)

    def verify_rediff(self):
        """
        Verifie si le jeu doit rediffuser la partie
        """
        if self.save_b.isChecked() and self.rediff_b.isChecked():
            QMessageBox.question(self, "Erreur", "Vous ne pouvez pas enregistrer et rediffuser en meme temps!", QMessageBox.Yes)
        if self.rediff_b.isChecked():
            self.rediff = True
            QMessageBox.question(self, "Attention", f"Cette partie du jeu n'est pas vraiment fonctionnel!\nVeillez a le tester a vos risques et periles", QMessageBox.Yes)
        elif not self.rediff_b.isChecked():
            self.rediff = False

    def start_game(self):
        """
        Verifie que tout est bon avant de commencer la partie
        """
        if self.file != None:
            QMessageBox.question(self, "C'est partie !", "C'est partie !", QMessageBox.Yes)
            if self.music_enable.isChecked():
                self.utilities.music(self.music_chooser_b.currentText()) # Initialisation de la musique
            if self.rediff: # Si c'est une rediffusion
                self.reset_data()
                self.rediff_play()

            elif not self.start: # Si c'est une partie normale
                self.reset_data()
                self.start = True
                self.init_buttons_other()

            else: # Si nous devons recommncer la partie
                self.restart = True
                self.init_values()
                self.slot_method_file()
                self.history.deleteLater()
                self.parametre_show.deleteLater()
                self.init_buttons_other()
                self.reset_data()
            if self.j1 == "IA": # Commence si le joueur 1 est un bot
                self.cell_clicked(None, True)
        else:
            QMessageBox.question(self, "Erreur", "Pas de fichier .txt charge", QMessageBox.Yes)

    def selection(self):
        """
        Change la selection des joueurs
        """
        if self.j1_b.currentText() == "IA":
            self.j1 = "IA"
        else:
            self.j1 = "j1"
        if self.j2_b.currentText() == "IA":
            self.j2 = "IA"
        else:
            self.j2 = "j2"
        if self.j1 == "IA" and self.j2 == "IA":
            QMessageBox.question(self, "Attention", "Malheureusement, avoir deux joueur etant des IA n'est pas parfaitement fonctionnel\nVous n'allez pas pouvoir bien distingue les coups.\nVeuillez m'excuser pour le desagrement", QMessageBox.Yes)

    def slot_method_file(self):
        """
        Permet d'initialiser les valeurs pour afficher le plateau
        """
        if self.file is None:
            self.board_management = Plateau(self.taille) # Permet de simuler le plateau
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.file, _ = QFileDialog.getOpenFileName(self,"Choix du plateau (seulement un fichier .txt conforme !)","","Text Files (*.txt)", options=options)
        if self.rediff:
            fichier = lire_fichier(self.file, True) # Lecture de fichier differente a cas ou c'est une redifusion
        else:
            fichier = lire_fichier(self.file, False)
        self.taille, tmp_list_pos_black, tmp_list_pos_white, tmp_list_mur = fichier[0], fichier[1], fichier[2], fichier[3]
        self.board_management = Plateau(self.taille)
        self.board_management.set_pos_mul_noir(tmp_list_pos_black), self.board_management.set_pos_mul_blanc(tmp_list_pos_white), self.board_management.set_pos_mul_fleche(tmp_list_mur)
        for pos in tmp_list_pos_black:
            self.list_pos_black += [self.utilities.coup_to_tuple(pos, self.taille)]
        for pos in tmp_list_pos_white:
            self.list_pos_white += [self.utilities.coup_to_tuple(pos, self.taille)]
        for pos in tmp_list_mur:
            self.list_mur += [self.utilities.coup_to_tuple(pos, self.taille)]
        self.plateau = self.board_management.get_plateau
        if not self.restart:
            self.createTable()
            self.layout_main.addWidget(self.tableWidget)
            self.setLayout(self.layout_main)
        elif self.restart:
            self.tableWidget.deleteLater()
            self.createTable()
            self.layout_main.addWidget(self.tableWidget)
            self.setLayout(self.layout_main)
    
    def createTable(self):
        """
        Affiche le plateau
        """
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.taille) 
        self.tableWidget.setColumnCount(self.taille)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        list_Hor_head = [chr(i+97) for i in range(self.taille)]
        list_Ver_head = [str(i) for i in range(self.taille, -1, -1)]
        self.tableWidget.setHorizontalHeaderLabels(list_Hor_head)
        self.tableWidget.setVerticalHeaderLabels(list_Ver_head)
        black = True
        for i in range(self.taille-1, -1, -1):
            
            for j in range(self.taille):
                self.tableWidget.setItem(i, j, QTableWidgetItem(""))
                if (i, j) in self.list_pos_white:
                    self.set_image("blanc", (i, j))
                elif (i, j) in self.list_pos_black:
                    self.set_image("noir", (i, j))
                elif (i, j) in self.list_mur:
                    self.set_image("mur", (i, j))
                if black:
                    self.tableWidget.item(i, j).setBackground(QColor(128, 128, 128))
                    if j == self.taille - 1:
                        black = True
                    else:
                        black = False
                else:
                    self.tableWidget.item(i, j).setBackground(QColor(255, 153, 51))
                    if j == self.taille - 1:
                        black = False
                    else:
                        black = True  
        self.tableWidget.blockSignals(False) # Debloque le signal au cas ou il a ete bloque   
        self.tableWidget.clicked.connect(self.cell_clicked)
    
    def verify_bot_round(self, tour, check=False):
        """
        Verifie bien que c'est le bot qui doit jouer
        tour: A qui le tour en int
        check: bool permettant de savoir si c'est seulement une verification
        """
        if ((tour == 0 and self.j1 == "IA") or (tour == 1 and self.j2 == "IA")) and check:
            return self.cell_clicked(None, True)
        elif ((tour == 0 and self.j1 == "IA") or (tour == 1 and self.j2 == "IA")) and not check:
            return True
        else:
            return False

    def modify_cell(self, start, dest, black):
        """
        Permet de modifier l'affichage des pions
        start: Pion a enlever en tuple
        dest: Pion a ajouter en tuple
        black: Qulle type de pion
        """
        if black != None:
            self.tableWidget.cellWidget(start[0], start[1]).deleteLater()
        if  black == False:
            self.set_image("blanc", dest)
        elif black == True:
            self.set_image("noir", dest)
        elif black == None:
            self.set_image("mur", dest)

    def table_start_black(self, act_pos):
        """
        Modification de depart lorsque le joueur noir joue
        act_pos: Position actuel
        """
        self.pos_queen_b_clicked = True
        self.depart_pos = act_pos # Position de depart
        self.depart_hist = self.utilities.tuple_to_str_new(act_pos,self.taille)
        tmp_list_possibilities_black = self.chck_pos.mouvements_possibles(self.utilities.qt_tuple_to_old(act_pos, self.taille), self.board_management.get_plateau, False, True) # Genere les possibilitees
        for coord in tmp_list_possibilities_black:
            self.list_possibilities_black += [self.utilities.qt_tuple_to_old(coord, self.taille)] # TODO
        
    
    def table_dest_black(self, act_pos):
        """
        Modification d'arrive lorsque le joueur noir joue
        act_pos: Position actuel
        """
        self.board_management.remove_pos(self.utilities.tuple_to_str_new(self.depart_pos, self.taille))
        self.board_management.remove_pos_plateau(self.utilities.tuple_to_str_new(self.depart_pos, self.taille))
        self.board_management.set_pos_1_noir(self.utilities.tuple_to_str_new(act_pos, self.taille))
        self.pos_dest_b_clicked = True
        tmp_mur_b_poss = self.chck_pos.mouvements_possibles(self.utilities.qt_tuple_to_old(act_pos, self.taille), self.board_management.get_plateau, False, True) # Genere les possibilitees
        for coord in tmp_mur_b_poss:
            self.mur_b_poss += [self.utilities.qt_tuple_to_old(coord, self.taille)] # TODO
        self.modify_cell(self.depart_pos, act_pos, True)
        self.dest_pos = act_pos # Position d'arrive
        self.dest_hist = self.utilities.tuple_to_str_new(act_pos, self.taille)
        self.pos_queen_b_clicked = False
        self.list_pos_black.remove(self.depart_pos)
        self.list_pos_black += [act_pos]
        self.list_possibilities_black = []
        self.depart_pos = None
        
    
    def table_fleche_black(self, act_pos):
        """
        Modification de la fleche lorsque le joueur noir joue
        act_pos: Position actuel
        """
        self.mur_hist = self.utilities.tuple_to_str_new(act_pos, self.taille)
        self.modify_cell(self.dest_pos, act_pos, None)
        self.pos_dest_b_clicked = False
        self.board_management.set_pos_1_fleche(self.utilities.tuple_to_str_new(act_pos, self.taille))
        self.mur_b_poss = []
        self.dest_pos = None
        

    def table_start_white(self, act_pos):
        """
        Modification de depart lorsque le joueur blanc joue
        act_pos: Position actuel
        """
        self.pos_queen_w_clicked = True
        self.depart_pos = act_pos # Position de depart
        self.depart_hist = self.utilities.tuple_to_str_new(act_pos,self.taille)
        tmp_list_possibilities_white = self.chck_pos.mouvements_possibles(self.utilities.qt_tuple_to_old(act_pos, self.taille), self.plateau, False, True) # Genere les possibilitees
        for coord in tmp_list_possibilities_white:
            self.list_possibilities_white += [self.utilities.qt_tuple_to_old(coord, self.taille)] # TODO
        
    
    def table_dest_white(self, act_pos):
        """
        Modification d'arrive lorsque le joueur blanc joue
        act_pos: Position actuel
        """
        self.pos_dest_w_clicked = True
        self.board_management.remove_pos(self.utilities.tuple_to_str_new(self.depart_pos, self.taille))
        self.board_management.remove_pos_plateau(self.utilities.tuple_to_str_new(self.depart_pos, self.taille))
        self.board_management.set_pos_1_blanc(self.utilities.tuple_to_str_new(act_pos, self.taille))
        self.modify_cell(self.depart_pos, act_pos, False)
        tmp_mur_w_poss = self.chck_pos.mouvements_possibles(self.utilities.qt_tuple_to_old(act_pos, self.taille), self.board_management.get_plateau, False, True) # Genere les possibilitees
        for coord in tmp_mur_w_poss:
            self.mur_w_poss += [self.utilities.qt_tuple_to_old(coord, self.taille)]
        self.dest_pos = act_pos # Position d'arrive
        self.dest_hist = self.utilities.tuple_to_str_new(act_pos, self.taille)
        self.pos_queen_w_clicked = False
        self.list_pos_white += [act_pos]
        self.list_possibilities_white = []
        self.depart_pos = None
        
    
    def table_fleche_white(self, act_pos):
        """
        Modification de la fleche lorsque le joueur blanc joue
        act_pos: Position actuel
        """
        self.mur_hist = self.utilities.tuple_to_str_new(act_pos, self.taille)
        self.modify_cell(self.dest_pos, act_pos, None)
        self.pos_dest_w_clicked = False
        self.board_management.set_pos_1_fleche(self.utilities.tuple_to_str_new(act_pos, self.taille))
        self.mur_w_poss = []
        self.dest_pos = None
        
    
    def bot_round(self):
        """
        Permet de simuler le coup du bot
        """
        end = self.utilities.check_end(self.board_management.get_plateau, self.board_management.pos_noir, self.board_management.pos_blanc, 1 if self.tour == 0 else 0) # Verifie que ce n'est pas encore la fin
        if end[0] != 0:
            return self.end_game(end[0])
        bot_check = self.utilities.tour_ai(self.tour, self.j1, self.j2) # Verifie quelle bot joue
        if bot_check[1]:
            QMessageBox.question(self, "Information", "Veuillez patienter que l'IA joue", QMessageBox.Yes)
            coup_bot_str = None
            if self.tour == 0:
                coup_bot_str = Minimax(self.board_management.get_plateau, self.board_management.pos_blanc, self.board_management.pos_noir).minimax_white() # Fait appel au minimax blanc
            elif self.tour == 1:
                coup_bot_str = Minimax(self.board_management.get_plateau, self.board_management.pos_blanc, self.board_management.pos_noir).minimax_black() # Fait appel au minimax noir
            if coup_bot_str:
                if coup_bot_str[0] is None: # Dans le cas ou il ne peux pas jouer de coup
                    if self.tour == 0:
                        gagnant = 2
                    else:
                        gagnant = 1
                    self.end_game(gagnant)
                else:
                    coup_bot_l = coup_bot_str[0].split(">")
                    coup_bot_l = [self.utilities.coup_to_tuple(elem, self.taille) for elem in coup_bot_l]
                    if self.tour == 0:
                        self.coup_bot(coup_bot_l, 0) # Fait appel a la fonction qui modifie le plateau pour simuler le jeu
                        self.write_history(1, f"{self.depart_hist}>{self.dest_hist}>{self.mur_hist}")
                        QMessageBox.question(self, "Tour", "Tour du joueur 2", QMessageBox.Yes)
                    elif self.tour == 1:
                        self.coup_bot(coup_bot_l, 1) # Fait appel a la fonction qui modifie le plateau pour simuler le jeu
                        self.write_history(2, f"{self.depart_hist}>{self.dest_hist}>{self.mur_hist}") 
                        QMessageBox.question(self, "Tour", "Tour du joueur 1", QMessageBox.Yes)
                end = self.utilities.check_end(self.board_management.get_plateau, self.board_management.pos_noir, self.board_management.pos_blanc, 1 if self.tour == 0 else 0)
                if end[0] != 0:
                    self.end_game(end[0])
                else:
                    self.history.setText(self.old_historique)
                    self.reset_data() # Reset les varibles temporaires
                    if self.tour == 1:
                        self.tour = 0
                    elif self.tour == 0:
                        self.tour = 1
                    self.verify_bot_round(self.tour, True)
    

    def coup_bot(self, coup, player):
        """
        Simule les coup sur le plateau
        coup: Le coup en liste de tuple
        player: Qui joue en int
        """
        delai = self.delai // 3
        if player == 0:
            threading.Event().wait(delai)
            self.table_start_white(coup[0]) # Depart
            threading.Event().wait(delai)
            self.table_dest_white(coup[1]) # Arrivee
            threading.Event().wait(delai)
            self.table_fleche_white(coup[2]) # Fleche
        elif player == 1:
            threading.Event().wait(delai)
            self.table_start_black(coup[0]) # Depart
            threading.Event().wait(delai)
            self.table_dest_black(coup[1]) # Arrive
            threading.Event().wait(delai)
            self.table_fleche_black(coup[2]) # Fleche


    def cell_clicked(self, item, bot=False):
        """
        Est appeler lorsque une cellule du plateau a ete clique
        item: La position
        bot: bool pour verifier si c'est le bo qui joue
        """
        if not bot:
            act_pos = (item.row(), item.column()) # Sauvegarde le coup en tuple
        if self.start:
            if self.tour == 1 and self.j2 == "j2": # Si c'est au tour du joueur noir humain

                if act_pos in self.list_pos_black and self.pos_queen_b_clicked == False and self.depart_pos == None: # Verifie que le joueur a appuye sur une case de la reine
                    self.table_start_black(act_pos)

                elif act_pos in self.list_possibilities_black and self.pos_queen_b_clicked and self.depart_pos != None: # Verifie que le joueur a appuye sur une case d'arrive de la reine
                    self.table_dest_black(act_pos)

                elif act_pos in self.mur_b_poss and self.pos_dest_b_clicked: # Verifie que le joueur a appuye sur une case mur
                    self.table_fleche_black(act_pos)
                    QMessageBox.question(self, "Tour", "Tour du joueur 1", QMessageBox.Yes)
                    self.tour = 0
                    self.write_history(2, f"{self.depart_hist}>{self.dest_hist}>{self.mur_hist}")
                    end = self.utilities.check_end(self.board_management.get_plateau, self.board_management.pos_noir, self.board_management.pos_blanc, 2)
                    self.reset_data() # Reset les varibles temporaires
                    print(end)
                    if end[0] != 0:
                        self.end_game(end[0])
                    else:
                        self.verify_bot_round(self.tour, True)

            elif self.tour == 0 and self.j1 == "j1": # Si c'est au tour du joueur blanc humain

                if act_pos in self.list_pos_white and self.pos_queen_w_clicked == False and self.depart_pos == None:
                    self.table_start_white(act_pos)

                elif act_pos in self.list_possibilities_white and self.pos_queen_w_clicked and self.depart_pos != None:
                    self.table_dest_white(act_pos)

                elif act_pos in self.mur_w_poss and self.pos_dest_w_clicked:
                    self.table_fleche_white(act_pos)
                    QMessageBox.question(self, "Tour", "Tour du joueur 2", QMessageBox.Yes)
                    self.tour = 1
                    self.write_history(1, f"{self.depart_hist}>{self.dest_hist}>{self.mur_hist}")
                    end = self.utilities.check_end(self.board_management.get_plateau, self.board_management.pos_noir, self.board_management.pos_blanc, 1)
                    self.reset_data() # Reset les varibles temporaires
                    if end[0] != 0:
                        self.end_game(end[0])
                    else:
                        self.verify_bot_round(self.tour, True)

            else:
                if self.verify_bot_round(self.tour): # Si c'est au tour du bot
                    self.bot_round()
                else:
                    QMessageBox.question(self, "Erreur", "Ce n'est pas votre tour", QMessageBox.Yes)
        else:
            QMessageBox.question(self, "Erreur", "Partie non commence", QMessageBox.Yes)
    

            
    def rediff_play(self):
        """
        Permet de rediffuser une partie
        """
        QMessageBox.question(self, "Attention", f"Cette partie du jeu n'est pas fonctionnel!\nVeillez a le tester a vos risques et perile", QMessageBox.Yes)
        self.init_buttons_other()
        with open(self.file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            lines =lines[6:]
            for elem in lines:
                coup = elem.strip().split(":")
                coup_bot_l = coup[4].strip().split(">")
                coup_bot_l = [self.utilities.coup_to_tuple(elem, self.taille) for elem in coup_bot_l]
                print(coup_bot_l)
                if coup[3].strip() == "Joueur 1":
                    tour = 1
                    self.coup_bot(coup_bot_l, 0)
                if coup[3].strip() == "Joueur 2":
                    tour = 2
                    self.coup_bot(coup_bot_l, 1)
            self.end_game(tour)


    def write_history(self, player, message):
        """
        Permet d'afficher l'historique des coups
        player: Le joueur actuel en int
        message: Le message a ajouter en str
        """
        current_time = time.strftime("%H:%M:%S")
        self.old_historique += f"{current_time}: Joueur {player}: {message}\n"
        self.history.setText(self.old_historique)
    

    def set_image(self, player, pos):
        """
        Permet d'afficher les images
        player: Qui joue en str
        pos: Ou afficher en tuple
        """
        label_image = QLabel(self) #TODO
        pixmap = QPixmap(self.dict_image[player])
        label_image.setPixmap(pixmap)
        label_image.setScaledContents(True)
        self.tableWidget.setCellWidget(pos[0],pos[1], label_image)


    def end_game(self, winner):
        """
        Permet de finire le jeu
        winner: Le gagnant en int
        """
        QMessageBox.question(self, "Fin de la partie", f"Fin de la partie\nBravo au joueur {winner}!\nVous venez officiellement de gagner ma gratitude\nVeuillez recommencer la partie", QMessageBox.Yes)
        if self.save_b.isChecked(): # Verifie si le jeu doit etre enregistrer
            with open("save.txt", "w+", encoding="utf-8") as f:
                with open(self.file, "r", encoding="utf-8") as f_to_write:
                    lines_to_writes = f_to_write.read()
                history_to_write = self.old_historique.split("\n")
                history_to_write = history_to_write[2:]
                f.write(lines_to_writes)
                f.write("\n\n")
                f.write("\n".join(history_to_write))
            QMessageBox.question(self, "Fin de la partie", f"Partie sauvegarde dans save.txt", QMessageBox.Yes)
        self.tableWidget.blockSignals(True)

def lire_fichier(nom, rediff=False):
    """
    Description: Lis le fichier qui va être utilisé pour le jeu.
    nom: Le fichier qui va etre lu.
    return: Un tuple de taille 3.
    """
    with open(nom, "r", encoding="utf-8") as fichier:
        fichier_0 = fichier.readlines()
        if rediff:
            fichier_0 = fichier_0[:4]
            if fichier_0[3] == "\n":
                fichier_0 = fichier_0[:3]
            print(fichier_0)
        return (int(fichier_0[0]), fichier_0[1].strip().split(","), fichier_0[2].strip().split(","),
                fichier_0[3].strip().split(",") if len(fichier_0) == 4 else [])
        # 0. Taille du plateau, int,
        # 1. Positions des reines noires, en format case en string, séparées par des virgules,
        # 2. Positions des reines blanches, en format case en string, séparées par des virgules
        # 3. Positions des flèches déjà tirées, en format case en string, séparées par des virgules


def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
