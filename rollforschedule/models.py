from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from app import db


table_player = db.Table(
    'table_player',
    db.Column('table_id', db.Integer, db.ForeignKey('table.id')),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
)


class Player(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    admin_rights = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Player {self.username}>'


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
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(
        db.Integer,
        db.ForeignKey('player.id')
    )
    player = db.relationship('Player', backref=db.backref('available', lazy='dynamic'))
    day = db.Column(db.Date)
    available = db.Column(db.Boolean)
    __table_args__ = (UniqueConstraint('player_id', 'day', name='_player_availability'),)

    def __repr__(self):
        return f'<Availability {self.player_id} {self.day}>'