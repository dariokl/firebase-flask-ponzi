from flask import render_template, redirect, session, request, jsonify, flash, url_for
import time
import json
from random import sample, shuffle
from hashids import Hashids

from . import ponzibp as view

from ..forms import GuessForm, GameForm

from ..firebase_utils.user import crud_user
from ..firebase_utils.db import db


@view.route('/admin', methods=['POST', 'GET'])
def admin():
    data = {
        'allowed_players': 10,
        'players': "{}",
        'total_players': 0,
        'ready': 0,
        'distribution': {1: 0.75, 2: 0.50, 3: 0.25, 4: 0, 5: -1},
        'secret': '',
        'guesses': 0
    }

    form = GameForm()
    hashids = Hashids()

    # The secret number generation.
    letters = sample('0123456789', 3)

    if letters[0] == '0':
        letters.reverse()

    number = ''.join(letters)

    if request.method == 'POST' and form.validate_on_submit():
        # Editing the game data object.
        data['allowed_players'] = form.allowed_players.data
        data['guesses'] = form.guesses.data
        data['secret'] = hashids.encode(int(number))

        # We can add separate class from Games instead of using User class, for now its obsolete.
        crud_user.create_new_game(db, data)
        flash('Successfuly created New Game')
        return redirect(url_for('ponzi.admin'))

    return render_template('admin.html', form=form)


@view.route('/')
def home():
    games = db.child('game').get()

    # Check if any games exists in firebase
    if games.val() == None:
        games = []

    return render_template('index.html', games=games)


@view.route('/join/<room_key>')
def join(room_key):
    # Clearing all previous sessions.
    session.clear()

    return render_template('join.html', room_key=room_key)


@view.route('/ponzi/', methods=['GET', 'POST'])
def ponzi():
    form = GuessForm()

    # Using session objects to retrieve the current use , session objects are initialized on /register route.
    current_user = crud_user.current_user(
        db, session['email'], session['room_key'])

    # Decoding the secret number inside the game.
    hashids = Hashids()
    number_to_guess = db.child('game').child(
        session['room_key']).child('secret').get().val()
    number_to_guess = ''.join(map(str, hashids.decode(number_to_guess)))

    def has_doubles(n):
        return len(set(str(n))) < len(str(n))

    # counting killed-injured function
    def countX(lst, x):
        count = 0
        for ele in lst:
            if (ele == x):
                count = count + 1
        return count

    if form.validate_on_submit() and request.method == 'POST':
        crud_user.set_timer(db, time.time())
        # Moving the amount of guesses
        session['guesses'] -= 1
         # The number that player has on form input.
        guess = request.form['guess']

        # Using guess list in order to display valid messages on front-end.
        session['guess'].append(guess)
 
        clues = []
        # check if input repeats digits function to warn player
        for index in range(3):
            if guess[index] == number_to_guess[index]:
                clues.append('Killed')
            elif guess[index] in number_to_guess[index]:
                clues.append('Wounded')

        # counting killed-injured function
        if len(clues) == 0:
            session['messages'].append('Nothing')
        else:
            killed = countX(clues, "Killed"), 'Killed'
            wounded = countX(clues, "Wounded"), 'Wounded'
            session['messages'].append(
                f'There are {killed[0]} {killed[1]}, {wounded[0]} {wounded[1]}')

        if guess == number_to_guess:
            crud_user.end_timer(db, time.time())
            crud_user.set_position(db)
            session['messages'].append('You got it !')
            return redirect(url_for('ponzi.rank', room_key=session['room_key']))
        
        if session['guesses'] <= 0:
            return redirect(url_for("ponzi.home"))

        return redirect(url_for('ponzi.ponzi'))

    return render_template('game.html', number=number_to_guess, counter=session['guesses'], form=form,
                           notification=zip(session['messages'], session['guess']))


@view.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.get_json()['email']
        room_key = request.get_json()['room_key']
        # All session object needed for proper functionality while playing the guess game.
        session['room_key'] = room_key
        session['email'] = user
        session['guesses'] = db.child('game').child(
            room_key).child('guesses').get().val()
        session['messages'] = []
        session['guess'] = []

        # Add user to game if he is not registered already.
        current_user = crud_user.current_user(db, user, room_key)
        if not current_user:
            crud_user.create_new_user(db, user, room_key)

        return jsonify({'Message': 'Session intialized'})


@view.route('/rank/<room_key>')
def rank(room_key):

    return render_template('ranking.html', room_key=room_key)
