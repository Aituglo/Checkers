from flask import Flask, render_template, redirect, url_for, request, flash
from .classes.Game import Game

app = Flask(__name__)
app.secret_key = 'TIP 2018/2019'

games = Game()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/play")
def play():
    return render_template('play.html')

@app.route("/restart")
def restart():
    games.restart()

    return render_template('play.html')


@app.route('/board/select/<int:coordinate_x>/<int:coordinate_y>')
def select(coordinate_x, coordinate_y):
    """
    Permet de séléctionner une pièce 
    :param int coordinate_x: La coordonnée x de la pièce séléctionnée
    :param int coordinate_y: La coordonnée y de la pièce séléctionnée
    :return render_template() or redirect():


    SI c'est le tour du joueur noir ET la pièce choisie Appartient au joueur noir :
        Tout va bien, c'est au tour des noirs
        et la pièce choisie lui appartient.
        Il peut le sélectionner pour le déplacer, par exemple.

    SI c'est le tour du joueur blanc ET la pièce choisie appartient au joueur blanc :
            Tout va bien, tout va bien. C'est à White de jouer.
            et la pièce choisie lui appartient.
            Il peut le sélectionner pour le déplacer, par exemple.
        
    SI ce n'est PAS le premier ET PAS le deuxième :
            Ça veut dire que quelque chose ne va pas.
            (1) C'est le tour des noirs, et la pièce sélectionnée appartient aux blancs,
                ou vice versa.
            (2) Aucun des joueurs n'a une pièce avec de telles coordonnées.
                Très probablement, quelqu'un a entré une adresse URL
                avec les coordonnées d'une pièce inexistante.
    """
    game = Game()

    if games.check_select(coordinate_x, coordinate_y):
        return render_template('play.html', coordinate_x=coordinate_x, coordinate_y=coordinate_y)
    else:
        return redirect(url_for('play'))

@app.route('/board/select/<int:coordinate_x>/<int:coordinate_y>/move/<int:to_x>/<int:to_y>')
def move(coordinate_x, coordinate_y, to_x, to_y):
    """
    Bouger une pièce d'une coordonnée à une autre
    :param int coordinate_x: This is a x coordinate of the piece we want to move.
    :param int coordinate_y: This is a y coordinate of the piece we want to move.
    :param int to_x: This is a x coordinate of the box to which we want to move the piece.
    :param int to_y: This is a y coordinate of the box to which we want to move the piece.
    :return redirect():
    """

    if not games.check_select(coordinate_x, coordinate_y):
        flash('Vous ne pouvez pas sélectionner cette pièce !', 'error')
        return redirect(url_for('game' ))

    # On regarde si un mouvement est possible
    # 1. N'est pas dans le plateau
    if to_x not in games.board.get_rows() or to_y not in games.board.get_columns():
        flash("Ce coup n'est pas valable !", 'error')
        return redirect(url_for('select',  coordinate_x=coordinate_x, coordinate_y=coordinate_y))

    # 2. N'est pas dans les zones impossibles
    if not games.board.check_if_allowed(to_x, to_y):
        flash("Ce coup n'est pas valable !", 'error')
        return redirect(url_for('select',  coordinate_x=coordinate_x, coordinate_y=coordinate_y))

    # 3. N'est pas sur une autre pièce
    if (to_x, to_y) in games.player_white.positions or (to_x, to_y) in games.player_black.positions:
        flash("Ce coup n'est pas valable !", 'error')
        return redirect(url_for('select',  coordinate_x=coordinate_x, coordinate_y=coordinate_y))

    # 3.A. Si ce n'est pas une reine, on ne peut pas bouger en arrière
    if (games.turn == games.player and (coordinate_x, coordinate_y) not in games.player_black.kings
            and coordinate_x <= to_x):
        flash("Ce coup n'est pas valable ! Seuls les reines peuvent reculer.", 'error')
        return redirect(url_for('select',  coordinate_x=coordinate_x, coordinate_y=coordinate_y))
    if (games.turn == games.ia and (coordinate_x, coordinate_y) not in games.player_white.kings
            and coordinate_x >= to_x):
        flash("Ce coup n'est pas valable ! Seuls les reines peuvent reculer.", 'error')
        return redirect(url_for('select',  coordinate_x=coordinate_x, coordinate_y=coordinate_y))

    # On peut enfin bouger
    if games.handle_move(coordinate_x, coordinate_y, to_x, to_y):
        # On regarde si une pièce ne se transforme pas en reine
        if games.add_kings():
            flash('Une reine couronné !', 'black')
    else:
        flash("Ce coup n'est pas valable !", 'error')
        return redirect(url_for('select',  coordinate_x=coordinate_x, coordinate_y=coordinate_y))


    return redirect(url_for('play'))

@app.context_processor
def inject_variables():
    """
    Injecte des variables dans chaque vue.
    :return dict:
    """

    # Si c'est le tour de l'IA, on appelle notre fonction minmax
    if games.turn == 1:
        games.minmax.minmax(games)

    return dict(
            rule = str(request.url_rule),
            player=games.player,
            ia=games.ia,
            board={'rows': games.rows, 'columns': games.columns},
            player_black=games.player_black,
            minmax=games.minmax,
            player_white=games.player_white,
            turn=games.turn,
            round=games.round,
            game=games
    )