class Board:
    """
    Garde les paramètres de base du plateau
    """
    columns = rows = 10

    def __init__(self):
        # Le nombre de lignes et de colonnes
        self.columns = 10
        self.rows = 10

    def get_rows(self):
        """
        Renvoie la liste des lignes
        :return list:
        """
        return range(self.rows)

    def get_columns(self):
        """
        Renvoie la liste des colonnes
        :return list:
        """
        return range(self.columns)

    @staticmethod
    def check_if_allowed(row, column):
        """
        Regarde si une case est possible ou non ( Cases grises ou blanches )
        """
        if (row % 2 == 0 and column % 2 != 0) or (row % 2 != 0 and column % 2 == 0):
            return True
        else:
            return False
