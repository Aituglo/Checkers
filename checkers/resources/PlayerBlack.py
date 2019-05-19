from . import Player


class PlayerBlack(Player.Player):
    """
    Donne toutes les informations du joueur noir
    Hérite des propriétés de la classe Player
    """
    def __init__(self):
        # Donne les positions du chaque pion noir
        self.positions = {
            (0, 1), (0, 3), (0, 5), (0, 7), (0, 9),
            (1, 0), (1, 2), (1, 4), (1, 6), (1, 8),
            (2, 1), (2, 3), (2, 5), (2, 7), (2, 9),
            (3, 0), (3, 2), (3, 4), (3, 6), (3, 8)
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
 

 