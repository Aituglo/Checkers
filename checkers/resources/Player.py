class Player:
    """
    Une classe Joueur avec toutes les variables dont on aura besoin pour chaque joueur
    """
    # La positions des pions
    positions = set()
    # La position des reines
    kings = set()
    # Le nombre de pièce
    pieces = len(positions)
    # Le nombre de reines
    pieces_kings = len(kings)
    # La liste des pièces qui peuvent capturer et où
    pieces_with_captures = dict()
    # La list des pièces qui peuvent bouger et où
    pieces_with_moves = dict()
