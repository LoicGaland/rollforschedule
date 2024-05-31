from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import text

from app import db
from models import Player, Table

main = Blueprint('main', __name__)


@main.route('/')
def index():
    players = Player.query.all()
    tables = Table.query.all()
    return render_template('index.html', players=players, tables=tables)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)


@main.route('/tables')
def tables():
    tables = Table.query.all()
    return render_template('tables.html', tables=tables)


@main.route("/table/<int:table_id>")
def table(table_id):
    table = Table.query.get_or_404(table_id)
    # TODO : query player's available days to compute days where playing this
    # table is possible, and display the results
    
    # query for days where everyone is available
    query = text(
        f"""
            SELECT day
            FROM availability
            INNER JOIN player ON availability.player_id = player.id
            INNER JOIN table_player ON table_player.player_id = player.id
            WHERE table_id = {table_id} AND available = TRUE
            GROUP BY day
            HAVING COUNT(availability.player_id) = (
                SELECT COUNT(*)
                FROM table_player
                WHERE table_id = {table_id}
            )
        """
    )
    results = db.session.execute(query)
    available_days = [row[0] for row in results]

    # query for days where at least one player is unavailable
    query = text(
        f"""
            SELECT DISTINCT day
            FROM availability
            INNER JOIN player ON availability.player_id = player.id
            INNER JOIN table_player ON table_player.player_id = player.id
            WHERE table_id = {table_id} AND available = FALSE
        """
    )
    results = db.session.execute(query)
    unavailable_days = [row[0] for row in results]
    # TODO : integrate (un)available days in template by making calendar into
    # a macro
    return render_template(
        'table.html', table=table,
        available_days=available_days, unavailable_days=unavailable_days
    )


@main.route("/player/<int:player_id>")
def player(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('player.html', player=player)


@main.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        username = request.form['username']
        player = Player(
            username=username
        )
        db.session.add(player)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')