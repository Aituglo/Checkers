from . import Player


class PlayerWhite(Player.Player):
    """
    Donne toutes les informations du joueur blanc
    Hérite des propriétés de la classe Player
    """
    def __init__(self):
        # Donne les positions du chaque pion blanc
        self.positions = {
            (6, 1), (6, 3), (6, 5), (6, 7), (6, 9),
            (7, 0), (7, 2), (7, 4), (7, 6), (7, 8),
            (8, 1), (8, 3), (8, 5), (8, 7), (8, 9),
            (9, 0), (9, 2), (9, 4), (9, 6), (9, 8)
            
        }
        # La liste des reines
        self.kings = set()
        # Le nombre de pièce
        self.pieces = len(self.positions)
        # Le nombre de reines
        self.pieces_kings = len(self.kings)
        # La liste des pièces qui peuvent capturer et où
        self.pieces_with_captures = dict()
        # La list des pièces qui peuvent bouger et où
        self.pieces_with_moves = dict()
