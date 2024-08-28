

JOUEUR_BLANC = '\u25CB'
JOUEUR_NOIR = '\u25CF'
FLECHE = "X"
LIBRE = "."
MESSAGE_COUP = "Joueur {}, donnez un coup de format 'position reine avant > position reine après > position flèche' " \
                       "(ex : a7>b7>a8) >> "


class Error(Exception):

    ERREUR_COUP = "Format du coup non valide"
    ERREUR_REINE = "Pas de reine à la position de départ"
    ERREUR_CHEMIN = "Le coup n'est pas valide, soit parce qu'il ne respecte pas les règles du jeu d'échec, soit parce que " \
                        "le chemin est occupé"
