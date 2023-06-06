import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


table_player = db.Table(
    'table_player',
    db.Column('table_id', db.Integer, db.ForeignKey('table.id')),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Player {self.firstname}>'


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    players = db.relationship(
        'Player',
        secondary=table_player,
        backref='tables'
    )

    def __repr__(self):
        return f'<Table {self.title}>'


class Availability(db.Model):
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('player.id'),
        primary_key=True
    )
    day = db.Column(db.Date, primary_key=True)
    available = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Availability {self.player_id} {self.day}>'


@app.route("/")
def index():
    players = Player.query.all()
    tables = Table.query.all()
    return render_template('index.html', players=players, tables=tables)


@app.route("/table/<int:table_id>")
def table(table_id):
    table = Table.query.get_or_404(table_id)
    return render_template('table.html', table=table)

@app.route("/player/<int:player_id>")
def player(player_id):
    player = Player.query.get_or_404(player_id)
    return render_template('player.html', player=player)


@app.route('/create/', methods=('GET', 'POST'))
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
