import copy 
from .Board import Board
from .PlayerBlack import PlayerBlack
from .PlayerWhite import PlayerWhite

class MinMax:

    def __init__(self):
        # Nombre de points pour chaque case du plateau
        self.points = {
            (0, 1): 80, (0, 3): 100, (0, 5): 125, (0, 7): 100, (0, 9): 75,
            (1, 0): 50, (1, 2): 70, (1, 4): 70, (1, 6): 70, (1, 8): 70,
            (2, 1): 25, (2, 3): 20, (2, 5): 20, (2, 7): 20, (2, 9): 40,
            (3, 0): 25, (3, 2): 10, (3, 4): 10, (3, 6): 10, (3, 8): 25,
            (4, 1): 25, (4, 3): 10, (4, 5): 10, (4, 7): 10, (4, 9): 25,
            (5, 0): 25, (5, 2): 10, (5, 4): 10, (5, 6): 10, (5, 8): 25,
            (6, 1): 25, (6, 3): 10, (6, 5): 10, (6, 7): 10, (6, 9): 25,
            (7, 0): 40, (7, 2): 20, (7, 4): 20, (7, 6): 20, (7, 8): 25,
            (8, 1): 70, (8, 3): 70, (8, 5): 70, (8, 7): 70, (8, 9): 50,
            (9, 0): 75, (9, 2): 100, (9, 4): 125, (9, 6): 100, (9, 8): 80
        }
        # La profondeur maximum que l'on souhaite pour l'algorithme
        self.max_depth = 3

    def piece_number(self, white, black, white_kings, black_kings) :
        """
        La fonction nous permet de compter le nombre de pieces de chaque couleur et d'y attribuer une valeur, 1 pour les pions et 2 ou 4 si il reste plus ou moins de 15 pieces au total
        """

        total_piece = black + white + white_kings + black_kings

        if total_piece >= 15:
            black_value = black + black_kings*2
            white_value = white + white_kings*2
        else :
            black_value = black + black_kings*4
            white_value = white + white_kings*4

        return white_value*10, black_value*10

    def position(self, white_position, black_position):
        """
        Compte le nombre total de points des deux camps grâce au tableau de points
        """
        black_points = 0
        white_points = 0

        for i in black_position:
            black_points += self.points[i]

        for i in white_position:
            white_points += self.points[i]

        return black_points, white_points

    def freedom(self, white_freedom, black_freedom):
        """
        Compte le nombre de deplacements possibles des deux camps
        """
        black_points = 0
        white_points = 0

        for i in white_freedom:
            white_points += len(white_freedom[i])

        for i in black_freedom:
            black_points += len(black_freedom[i])

        return black_points*10 , white_points*10


    def eval(self, game):
        """
        Utilise les 3 fonctions précédentes pour donner un nombre qui est l'évaluation de l'IA
        """
        piece_number = self.piece_number(game.player_white.pieces, game.player_black.pieces, game.player_white.pieces_kings, game.player_black.pieces_kings)
        position = self.position(game.player_white.positions, game.player_black.positions)
        freedom = self.freedom(game.player_white.pieces_with_moves, game.player_black.pieces_with_moves)

        white_point = piece_number[0] + position[0] + freedom[0]
        black_point = piece_number[1] + position[1] + freedom[1]

        return black_point - white_point

    def minmax(self, board):
        """
        Va renvoyer le meilleur coup possible à jouer
        """
        best_board = None
        depth = self.max_depth + 1

        while not best_board and depth > 0:
            depth -= 1
            # On récupère le meilleur coup possible à chaque fois
            (best_board, best_value) = self.max(board, depth)
            # Si on a pas de meilleur coup, on renvoie une exception
        if not best_board:
            raise Exception("Could only return null boards")
        #  Sinon on renvoie le meilleur coup
        else:
            ## On change notre vrai plateau par le nouveau
            board.player_black = best_board.player_black
            board.player_white = best_board.player_white
            board.turn = 0

            return (best_board, best_value)        

    def min(self, board, depth):
        """
        Calcule le meilleur coup pour les joueurs blancs ( Joueur )
        """
        return self.play(board, depth, float('inf'))

    def max(self, board, depth):
        """
        Calcule le meilleur coup pour les joueurs noirs ( IA )
        """
        return self.play(board, depth, float('-inf'))


    def play(self, board, depth, best_move):
        """
        Va permettre de jouer les coups pour chaque mouvements possibles dans une copie de la partie 
        """

        # Si la partie est terminée ou qu'on est plus dans une profondeur négative on renvoie la partie actuelle
        if board.finished or depth <= 0:
            return (board, self.eval(board))

        best_board = None  

        ## On fait le coup pour les joueurs noir ( IA ), car le meilleur coup est -infini donc on cherche le mieux possible
        if best_move == float('-inf'):
            pieces_with_moves = board.player_black.pieces_with_moves
            pieces_with_captures = board.player_black.pieces_with_captures

            ## On cherche la meilleure capture possible
            for i in pieces_with_captures:
                for j in pieces_with_captures[i]:
                    # On fait une copie du jeu
                    game_copy = copy.deepcopy(board)
                    # On dit que c'est au tour des noirs
                    game_copy.turn = 1
                    # On effectue la capture
                    game_copy.capture(i[0], i[1], j[0], j[1])

                    # On redescend en profondeur dans l'algorithme pour calculer la plus grande valeur possible
                    value = self.min(board, depth - 1)[1]
                    if value > best_move:
                        best_move = value
                        best_board = game_copy

            ## On cherche le meilleur mouvement possible
            for i in pieces_with_moves:
                for j in pieces_with_moves[i]:
                    # On fait une copie du jeu
                    game_copy = copy.deepcopy(board)
                    # On dit que c'est au tour des noirs
                    game_copy.turn = 1
                    # On effectue le mouvement
                    game_copy.move(i[0], i[1], j[0], j[1])

                    # On redescend en profondeur dans l'algorithme pour calculer la plus grande valeur possible
                    value = self.min(board, depth - 1)[1]
                    if value > best_move:
                        best_move = value
                        best_board = game_copy

            
        ## On fait le coup pour les joueurs blancs ( Joueur ), on part de +infini et on cherche la plus petite valeur possible
        if best_move == float('inf'):
            pieces_with_moves = board.player_white.pieces_with_moves
            pieces_with_captures = board.player_white.pieces_with_captures

            ## On cherche la meilleure capture possible
            for i in pieces_with_captures:
                for j in pieces_with_captures[i]:
                    # On fait une copie du jeu
                    game_copy = copy.deepcopy(board)
                    # On dit que c'est au tour des blancs
                    game_copy.turn = 0
                    # On effectue la capture
                    game_copy.capture(i[0], i[1], j[0], j[1])

                    # On redescend en profondeur dans l'algorithme pour calculer la plus petite valeur possible ( car blancs )
                    value = self.max(board, depth - 1)[1]
                    if value < best_move:
                        best_move = value
                        best_board = game_copy

            for i in pieces_with_moves:
                for j in pieces_with_moves[i]:
                    # On fait une copie du jeu
                    game_copy = copy.deepcopy(board)
                    # On dit que c'est au tour des blancs
                    game_copy.turn = 0
                    # On effectue le mouvement
                    game_copy.move(i[0], i[1], j[0], j[1])

                    # On redescend en profondeur dans l'algorithme pour calculer la plus petite valeur possible ( car blancs )
                    value = self.max(board, depth - 1)[1]
                    if value < best_move:
                        best_move = value
                        best_board = game_copy

            

        return (best_board, best_move)

    