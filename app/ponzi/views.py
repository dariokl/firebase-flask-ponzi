from flask import render_template, redirect, session, request, jsonify, flash, url_for
import time
import json
from random import sample, shuffle

from . import ponzibp as view

from ..forms import GuessForm, GameForm

from ..firebase_utils.user import crud_user
from ..firebase_utils.db import db


@view.route('/admin', methods=['POST', 'GET'])
def admin():
    data = {
        'game_type': '',
        'allowed_players': 10,
        'players': "{}",
        'total_players': 0,
        'ready': 0,
        'distribution': {1: 0.75, 2: 0.50, 3: 0.25, 4: 0, 5: -1},
        'guesses': 0,
    }

    form = GameForm()
  
    if request.method == 'POST' and form.validate_on_submit():
        # Editing the game data object.
        data['game_type'] = form.game_type.data
        data['allowed_players'] = form.allowed_players.data
        data['max_players'] = form.allowed_players.data
        data['guesses'] = form.guesses.data

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

    # Cleaning up distribution to show the values inside the rooms chart bars.
    distribution_chart = db.child('game').child(room_key).child('distribution').get().val()
    distribution_chart = [int(x*100) for x in distribution_chart if x != None]
  
    return render_template('join.html', room_key=room_key, distribution_chart=distribution_chart)


@view.route('/ponzi/', methods=['GET', 'POST'])
def ponzi():
    """
    Ponzi view is responsible for game itself , as the applicion doesnt have any sort of
    auth system ponzi view relays on session that is created on /registration route once
    player clicks requests access. 
    
    All the core informations are stored into clients session. Each request that passes form 
    validation subtract the amount of guesses player has by one , until he reaches 0 wich 
    means he failed to solve the puzzle and redirect player to home route.

    Sessions objects "messages" and "guess" are used to show results of previous tries.

    The rest of firebase queriying/logic is happening within app/firebase_utils/user.py,
    even tough functions like set_timer , end_timer are pretty self explanatory check
    them out in order to udnerstand args and logic happening there.
    """
    form = GuessForm()
    # Using session objects to retrieve the current use , session objects are initialized on /register route.
    current_user = crud_user.current_user(
        db, session['email'], session['room_key'])

    # Using the number that is generated and added to session on /register.
    number_to_guess = session['number']

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
            elif guess[index] in number_to_guess:
                clues.append('Wounded')
        
        # counting killed-injured function
        if len(clues) == 0:
            session['messages'].append('Nothing')
        else:
            killed = countX(clues, "Killed"), 'Killed'
            wounded = countX(clues, "Wounded"), 'Wounded'
            session['messages'].append(
                f'There are {killed[0]} Killed, {wounded[0]} Wounded')

        if guess == number_to_guess:
            crud_user.end_timer(db, time.time())
            session['messages'].append('You got it !')
            return redirect(url_for('ponzi.rank', room_key=session['room_key']))
        
        if session['guesses'] <= 0:
            return redirect(url_for("ponzi.home"))

        return redirect(url_for('ponzi.ponzi'))

    return render_template('game.html', number=number_to_guess, counter=session['guesses'], form=form,
                           notification=zip(session['messages'], session['guess']))


@view.route('/register', methods=['GET', 'POST'])
def register():
    """
    A mock register view , since we need a way to auth users with email they use 
    to grant access into room we are storing email and player name values into session.

    Axios post is made from /join view once the player request the access.

    Storing all the vital data in session helps application to work.
    Register view is responsible for generatin of random 3 digits that are used 
    as a number that player should guess once he enters the route.

    Additionally the session data could be formated as a dictionary to gain better
    code readability but ever since applicaion could get firebase authentication in
    future i will keep this way for now.
    """
    if request.method == 'POST':
        user_email = request.get_json()['email']
        player_name = request.get_json()['name']
        room_key = request.get_json()['room_key']
        # All session object needed for proper functionality while playing the guess game.
        session['room_key'] = room_key
        session['email'] = user_email
        session['guesses'] = db.child('game').child(
            room_key).child('guesses').get().val()
        session['messages'] = []
        session['guess'] = []

        # Add user to game if he is not registered already.
        current_user = crud_user.current_user(db, user_email, room_key)
        if not current_user:
            crud_user.create_new_user(db, user_email, player_name , room_key)
        
        letters = sample('0123456789', 3)

        if letters[0] == '0':
            letters.reverse()

        number = ''.join(letters)
        session['number'] = number

        return jsonify({'Message': 'Session intialized'})


@view.route('/rank/<room_key>')
def rank(room_key):
    crud_user.set_position(db)

    return render_template('ranking.html', room_key=room_key)
