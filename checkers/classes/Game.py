
from time import time
from math import fabs
from .Board import Board
from .PlayerBlack import PlayerBlack
from .PlayerWhite import PlayerWhite
from .MinMax import MinMax


class Game:

    def __init__(self):
        """
        Classe Game, principale du jeu
        """
        # ID du joueur
        self.player = 0
        # ID de l'ia
        self.ia = 1
        # Tour de quel joueur
        self.turn = 0
        # Combien de tours
        self.round = 1
        # Si la partie est terminée
        self.finished = None
        # Plateau
        self.board = Board()
        # Lignes
        self.rows = self.board.get_rows()
        # Colonnes
        self.columns = self.board.get_columns()
        # Joueur Noir
        self.player_black = PlayerBlack()
        # Joueur Blanc
        self.player_white = PlayerWhite()
        # Algorithme minmax
        self.minmax = MinMax()
        # Mettre à jour les coups possibles
        self.update_possible_moves()
        # Mettre à jour les captures possibles
        self.update_possible_captures()
        # Regarder où en est la partie
        self.check_status()


    def change_turn(self):
        """
        Permet de changer de tour
        :return boolean:
        """
        ok = False

        if self.turn == self.player:
            self.turn = self.ia
            ok = True
        elif self.turn == self.ia:
            self.turn = self.player
            ok = True

        if ok:
            self.round += 1

        return ok


    def check_status(self):
        """
        Regarder où en est la partie, si elle est terminée ou non et renvoie qui a gagné
        """
        if not self.player_black.pieces_with_moves and not self.player_black.pieces_with_captures \
            and not self.player_white.pieces_with_moves and not self.player_white.pieces_with_captures:
            self.finished = True
        else:
            if not self.player_black.pieces or \
                    (not self.player_black.pieces_with_moves and not self.player_black.pieces_with_captures):
                self.finished = self.ia  # Les blancs Gagnent
            elif not self.player_white.pieces or \
                    (not self.player_white.pieces_with_moves and not self.player_white.pieces_with_captures):
                self.finished = self.player # Les noirs Gagnent

        return self.finished

    def check_select(self, coordinate_x, coordinate_y):
        """
        Cette fonction vérifie si une pièce sélectionnée appartient à un joueur à qui c'est son tour.
        Il s'assure également que le joueur ne peut choisir qu'une pièce qui a une capture disponible (s'il y en a une).
        :param int coordinate_x: Coordonnée X de la pièce.
        :param int coordinate_y:  Coordonnée Y de la pièce.
        :return boolean: Renvoie True si on peut.
        """
        # Tour de l'IA
        if self.turn == self.ia:
            if (coordinate_x, coordinate_y) in self.player_black.positions:
                if not self.player_black.pieces_with_moves or \
                        (coordinate_x, coordinate_y) in self.player_black.pieces_with_moves \
                        or not self.player_black.pieces_with_captures or \
                        (coordinate_x, coordinate_y) in self.player_black.pieces_with_captures:
                    return True

        # Tour du joueur
        if self.turn == self.player:
            if (coordinate_x, coordinate_y) in self.player_white.positions:
                if not self.player_white.pieces_with_moves or \
                        (coordinate_x, coordinate_y) in self.player_white.pieces_with_moves \
                        or not self.player_white.pieces_with_captures or \
                        (coordinate_x, coordinate_y) in self.player_white.pieces_with_captures:
                    return True

        return False

    def add_kings(self):
        """
        Ajoute une reine si c'est le cas
        :return boolean: Vrai si une pièce est transformée en reine
        """

        for piece in self.player_black.positions:
            # Si on est sur la dernière ligne et que la pièce est noire, on ajoute une reine noire
            if piece[0] == 9 and piece not in self.player_black.kings:
                self.player_black.kings.add(piece)
                return True

        for piece in self.player_white.positions:
            # Si on est sur la première ligne et que la pièce est blanche, on ajoute une reine blanche
            if piece[0] == 0 and piece not in self.player_white.kings:
                self.player_white.kings.add(piece)
                return True

        return False

    def handle_move(self, coordinate_x, coordinate_y, to_x, to_y):
        """
        Fonction qui gère le déplacement d'une pièce : soit un simple déplacement, soit une capture.
        :param int coordinate_x: Coordonnée X de la pièce.
        :param int coordinate_y: Coordonnée Y de la pièce.
        :param int to_x: Coordonnée X du lieu désiré
        :param int to_y: Coordonnée Y du lieu désiré
        :return boolean: True si le mouvement est possible, False sinon
        """
        # IA
        if self.turn == self.ia and (coordinate_x, coordinate_y) in self.player_black.positions:
            if self.move(coordinate_x, coordinate_y, to_x, to_y):
                # On ajoute des reines si c'est le cas
                self.add_kings()
                # On met à jour les mouvements possibles
                self.update_possible_moves()
                return True
        # Joueur
        elif self.turn == self.player and (coordinate_x, coordinate_y) in self.player_white.positions:
            if self.move(coordinate_x, coordinate_y, to_x, to_y):
                # On ajoute des reines si c'est le cas
                self.add_kings()
                # On met à jour les mouvements possibles
                self.update_possible_moves()
                return True
        return False

    def move(self, coordinate_x, coordinate_y, to_x, to_y):
        """
        Vérifie si un coup est d'une ou deux cases (en diagonale).
        Si plus loin, alors il appelle la fonction capture(), comme se déplacer par deux n'est possible que lors de la capture.
        :param int coordinate_x: Coordonnée X de la pièce.
        :param int coordinate_y: Coordonnée Y de la pièce.
        :param int to_x: Coordonnée X du lieu désiré
        :param int to_y: Coordonnée Y du lieu désiré
        :return boolean: True si le mouvement est valide, False sinon
        """
        # 0. Si il y a des captures possibles et que la pièce ne peut pas -> FAAAUUUX
        if self.turn == self.ia and len(self.player_black.pieces_with_captures):
            if not (coordinate_x, coordinate_y) in self.player_black.pieces_with_captures:
                return False
        elif self.turn == self.player and len(self.player_white.pieces_with_captures):
            if not (coordinate_x, coordinate_y) in self.player_white.pieces_with_captures:
                return False
        # 1. Si les coordonnés en diagonales sont possible, c'est bon
        if fabs(coordinate_x - to_x) <= 1 and fabs(coordinate_y - to_y) <= 1:
            if self.turn == self.ia:  # Tour noir
                if (coordinate_x, coordinate_y) in self.player_black.pieces_with_captures:
                    return False
                if (to_x, to_y) not in self.player_white.positions and (to_x, to_y) not in self.player_black.positions:
                    # On enleve le pion de sa position
                    self.player_black.positions.remove((coordinate_x, coordinate_y))
                    # On la rajoute aux nouvelles coordonnées
                    self.player_black.positions.add((to_x, to_y))
                    # Le cas si c'est une reine
                    if (coordinate_x, coordinate_y) in self.player_black.kings:
                        self.player_black.kings.remove((coordinate_x, coordinate_y))
                        self.player_black.kings.add((to_x, to_y))
                    # On met à jour les captures possibles
                    self.update_possible_captures()
                    # On change de tour
                    self.change_turn()
                    return True
                else:
                    return False
            elif self.turn == self.player:  # Tour blanc
                if (coordinate_x, coordinate_y) in self.player_white.pieces_with_captures:
                    return False
                if (to_x, to_y) not in self.player_black.positions and (to_x, to_y) not in self.player_white.positions:
                    # On enleve le pion de sa position
                    self.player_white.positions.remove((coordinate_x, coordinate_y))
                    # On la rajoute aux nouvelles coordonnées
                    self.player_white.positions.add((to_x, to_y))
                    # Le cas si c'est une reine
                    if (coordinate_x, coordinate_y) in self.player_white.kings:
                        self.player_white.kings.remove((coordinate_x, coordinate_y))
                        self.player_white.kings.add((to_x, to_y))
                    # On met à jour les captures possibles
                    self.update_possible_captures()
                    # On change de tour
                    self.change_turn()
                    return True
                else:
                    return False
        # 2. Si diagonale par 2 on regarde si la capture est possible
        elif fabs(coordinate_x - to_x) <= 2 or fabs(coordinate_y - to_y) <= 2:
            return self.capture(coordinate_x, coordinate_y, to_x, to_y)
        # 3. Si plus que 2 par diagonale c'est impossible
        else:
            return False

    def capture(self, coordinate_x, coordinate_y, to_x, to_y):
        """
        Cette fonction gère la capture si une pièce se déplace de deux cases.
        Il calcule les coordonnées du carré entre ces deux positions,
        et vérifie si l'ennemi en a une pièce.
        Si c'est le cas, alors cette pièce doit être capturée et le coup est valide.
        Sinon, le coup n'est pas valable.
        :param int coordinate_x: Coordonnée X de la pièce.
        :param int coordinate_y: Coordonnée Y de la pièce.
        :param int to_x: Coordonnée X du lieu désiré
        :param int to_y: Coordonnée Y du lieu désiré
        :return boolean: True si la capture est valide, False sinon
        """

        # Calcul des coordonnées de la potentielle pièce à capturer
        med_x = (coordinate_x + to_x) / 2
        med_y = (coordinate_y + to_y) / 2

        # Tour de l'IA, donc si les coordonnées sont blanches
        if self.turn == self.ia and (med_x, med_y) in self.player_white.positions:
            # Si les coordonnées sont bien des les captures possibles
            if (self.player_black.pieces_with_captures and (coordinate_x, coordinate_y) in self.player_black.pieces_with_captures
                    and (to_x, to_y) in self.player_black.pieces_with_captures.get((coordinate_x, coordinate_y))) \
                    or not self.player_black.pieces_with_captures:
                # On enleve le pion
                self.player_black.positions.remove((coordinate_x, coordinate_y))
                # On l'ajoute aux nouvelles coordonnées
                self.player_black.positions.add((to_x, to_y))
                # Cas d'une reine
                if (coordinate_x, coordinate_y) in self.player_black.kings:
                    self.player_black.kings.remove((coordinate_x, coordinate_y))
                    self.player_black.kings.add((to_x, to_y))
                # On enleve le pion blanc qu'on a capturé
                self.player_white.positions.remove((med_x, med_y))
                # On réduit le nombre de pions blancs
                self.player_white.pieces -= 1
                # Cas d'une reine
                if (med_x, med_y) in self.player_white.kings:
                    self.player_white.kings.remove((med_x, med_y))
                # On met à jour les captures possibles
                self.update_possible_captures()
            # On regarde si on peut re capturer
            if (to_x, to_y) in self.player_black.pieces_with_captures:
                self.update_possible_captures_for_one(to_x, to_y)
            # Sinon on change de tour
            else:
                self.change_turn()
            return True

        # Tour du joueur, donc si les coordonnées sont noires
        elif self.turn == self.player and (med_x, med_y) in self.player_black.positions:
            # Si les coordonnées sont bien des les captures possibles
            if (self.player_white.pieces_with_captures and (coordinate_x, coordinate_y) in self.player_white.pieces_with_captures) \
                    and (to_x, to_y) in self.player_white.pieces_with_captures.get((coordinate_x, coordinate_y)) \
                    or not self.player_white.pieces_with_captures:
                # On enleve le pion
                self.player_white.positions.remove((coordinate_x, coordinate_y))
                # On l'ajoute aux nouvelles coordonnées
                self.player_white.positions.add((to_x, to_y))
                # Cas d'une reine
                if (coordinate_x, coordinate_y) in self.player_white.kings:
                    self.player_white.kings.remove((coordinate_x, coordinate_y))
                    self.player_white.kings.add((to_x, to_y))
                # On enleve le pion noir qu'on a capturé
                self.player_black.positions.remove((med_x, med_y))
                # On réduit le nombre de pions noirs
                self.player_black.pieces -= 1
                # Cas d'une reine
                if (med_x, med_y) in self.player_black.kings:
                    self.player_black.kings.remove((med_x, med_y))
                #  On met à jour les captures possibles
                self.update_possible_captures()
            # On regarde si on peut re capturer
            if (to_x, to_y) in self.player_white.pieces_with_captures:
                self.update_possible_captures_for_one(to_x, to_y)
            # Sinon on change de tour
            else:
                self.change_turn()
            return True

        return False

    def update_possible_captures_for_one(self, coordinate_x, coordinate_y):
        """
        Regarde si on peut re-capturer après avoir capturer
        :param int coordinate_x: Coordonnée X de la pièce.
        :param int coordinate_y: Coordonnée Y de la pièce.
        :return: Renvoie True si c'est possible sinon False
        """

        # On enlèves les captures possibles
        self.player_black.pieces_with_captures.clear()
        self.player_white.pieces_with_captures.clear()

        # Joueur noir
        if (coordinate_x, coordinate_y) in self.player_black.positions:
            possible_captures = self.check_possible_captures(coordinate_x, coordinate_y)
            if possible_captures:
                self.player_black.pieces_with_captures[(coordinate_x, coordinate_y)] = possible_captures
            return True
        # Joueur blanc
        elif (coordinate_x, coordinate_y) in self.player_white.positions:
            possible_captures = self.check_possible_captures(coordinate_x, coordinate_y)
            if possible_captures:
                self.player_white.pieces_with_captures[(coordinate_x, coordinate_y)] = possible_captures
            return True
        else:
            return False

    def update_possible_captures(self):
        """
        Met à jour la liste des captures possibles
        :return: boolean
        """

        # On enlèves les captures possibles
        self.player_black.pieces_with_captures.clear()
        self.player_white.pieces_with_captures.clear()

        # Joueur noir
        for piece in self.player_black.positions:
            possible_captures = self.check_possible_captures(piece[0], piece[1])
            if possible_captures:
                self.player_black.pieces_with_captures[piece] = possible_captures
        # Joueur blanc
        for piece in self.player_white.positions:
            possible_captures = self.check_possible_captures(piece[0], piece[1])
            if possible_captures:
                self.player_white.pieces_with_captures[piece] = possible_captures
        return True

    def check_possible_captures(self, coordinate_x, coordinate_y):
        """
        Regarde toutes les captures possible pour une pièce
        :param int coordinate_x: Coordonnée X de la pièce.
        :param int coordinate_y: Coordonnée Y de la pièce.
        :return: Renvoie la liste des captures possibles si il y en a, sinon False
        """
        # Toutes les positions de captures possibles
        targets = [
            ((coordinate_x + 2), (coordinate_y + 2)),
            ((coordinate_x + 2), (coordinate_y - 2)),
            ((coordinate_x - 2), (coordinate_y + 2)),
            ((coordinate_x - 2), (coordinate_y - 2))
        ]
        # Les diagonales entre ces positons pour voir si il y a une pièce d'une autre couleur
        mids = [
            ((coordinate_x + targets[0][0]) // 2, (coordinate_y + targets[0][1]) // 2),
            ((coordinate_x + targets[1][0]) // 2, (coordinate_y + targets[1][1]) // 2),
            ((coordinate_x + targets[2][0]) // 2, (coordinate_y + targets[2][1]) // 2),
            ((coordinate_x + targets[3][0]) // 2, (coordinate_y + targets[3][1]) // 2)
        ]

        valid_targets = list()

        for i in range(len(targets)):
            if targets[i][0] in self.board.get_rows() and targets[i][1] in self.board.get_columns():
                # Si les coordonnés de la cible sont des cases vides
                if targets[i] not in self.player_black.positions and targets[i] not in self.player_white.positions:
                    # Si le pion est blanc
                    if (coordinate_x, coordinate_y) in self.player_white.positions:
                        if targets[i][0] < coordinate_x or \
                                (targets[i][0] > coordinate_x and (coordinate_x, coordinate_y) in self.player_white.kings):
                            if mids[i] in self.player_black.positions:
                                valid_targets.append(targets[i])
                    # Si le pion est noir
                    elif (coordinate_x, coordinate_y) in self.player_black.positions:
                        if targets[i][0] > coordinate_x or \
                                (targets[i][0] < coordinate_x and (coordinate_x, coordinate_y) in self.player_black.kings):
                            if mids[i] in self.player_white.positions:
                                valid_targets.append(targets[i])
        if not valid_targets:
            return False
        return valid_targets

    def update_possible_moves(self):
        """
        Met à jour la liste des mouvements possibles
        :return boolean: Renvoie True
        """
        self.player_black.pieces_with_moves.clear()
        self.player_white.pieces_with_moves.clear()

        for piece in self.player_black.positions:
            possible_moves = self.check_possible_moves(piece[0], piece[1])
            if possible_moves:
                self.player_black.pieces_with_moves[piece] = possible_moves

        for piece in self.player_white.positions:
            possible_moves = self.check_possible_moves(piece[0], piece[1])
            if possible_moves:
                self.player_white.pieces_with_moves[piece] = possible_moves

        return True

    def check_possible_moves(self, coordinate_x, coordinate_y):
        """
        Regarde les mouvements possibles pour une pièce donnée
        :param int coordinate_x: Coordonnée X de la pièce.
        :param int coordinate_y: Coordonnée Y de la pièce.
        :return boolean|array: Renvoie soit les mouvements possibles, sinon False
        """
        # Les différentes positions possibles
        targets_plus_x = [
            ((coordinate_x + 1), (coordinate_y + 1)),
            ((coordinate_x + 1), (coordinate_y - 1))
        ]
        targets_minus_x = [
            ((coordinate_x - 1), (coordinate_y + 1)),
            ((coordinate_x - 1), (coordinate_y - 1))
        ]

        # Si le pion est noir
        if (coordinate_x, coordinate_y) in self.player_black.positions:
            if (coordinate_x, coordinate_y) in self.player_black.kings:
                targets = targets_plus_x + targets_minus_x
            else:
                targets = targets_plus_x
        # Si le pion est blanc
        elif (coordinate_x, coordinate_y) in self.player_white.positions:
            if (coordinate_x, coordinate_y) in self.player_white.kings:
                targets = targets_plus_x + targets_minus_x
            else:
                targets = targets_minus_x
        else:
            targets = []

        valid_targets = []

        for i in range(len(targets)):
            if targets[i][0] in self.board.get_rows() and targets[i][1] in self.board.get_columns():
                if targets[i] not in self.player_black.positions and targets[i] not in self.player_white.positions:
                    valid_targets.append(targets[i])

        if valid_targets:
            return valid_targets
        return False
