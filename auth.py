from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from models import Player

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    player = Player.query.filter_by(email=email).first()

    # check if the player actually exists
    # take the player-supplied password, hash it, and compare it to the hashed
    # password in the database
    if not player or not check_password_hash(player.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
        # if the player doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the player has the right
    # credentials
    login_user(player, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add player to database goes here
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    # if this returns a player, then the email already exists in database
    player = Player.query.filter_by(email=email).first()

    # if a player is found, we want to redirect back to signup page so player
    # can try again
    if player:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new player with the form data. Hash the password so the
    # plaintext version isn't saved.
    new_player = Player(
        email=email,
        username=username,
        password=generate_password_hash(password, method='sha256')
    )

    # add the new player to the database
    db.session.add(new_player)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
