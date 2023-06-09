from flask import Blueprint, render_template
from flask_login import login_required, current_user

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


@main.route("/table/<int:table_id>")
def table(table_id):
    table = Table.query.get_or_404(table_id)
    return render_template('table.html', table=table)


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