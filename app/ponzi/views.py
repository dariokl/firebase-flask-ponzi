from flask import render_template, redirect, session, request, jsonify, flash, url_for
import time
import json
from random import sample, shuffle

from . import ponzibp as view

from ..forms import GuessForm, GameForm

from ..firebase_utils.user import crud_user
from ..firebase_utils.game import crud_game
from ..firebase_utils.db import db


@view.route('/create-room', methods=['POST', 'GET'])
def create_room():
    data = {
        'game_type': 'Ponzi',
        'allowed_players': 0,
        'players': "{}",
        'total_players': 0,
        'ready': 0,
        'distribution': "{}",
        'skewness':0,
        'guesses': 0,
        'n_losers':0,
        'contribution':0,
        'max_return':0,
        'status': 'OPEN',
        'solved_n': 0

    }

    form = GameForm()
    create_rooms = db.child('game').order_by_child('status').equal_to('OPEN').get()

    if request.method == 'POST' and form.validate_on_submit():

        if len(create_rooms.val()) <= 6:
            # Editing the game data object.
            data['allowed_players'] = form.allowed_players.data
            data['max_players'] = form.allowed_players.data
            data['n_losers'] = form.n_losers.data
            data['contribution'] = form.contribution.data
            data['max_return'] = form.max_return.data/100
            data['guesses'] = int(form.guesses.data)
            distibution, skewness=form.distribution(data['allowed_players'],data['n_losers'],data['contribution'],data['max_return'])
            data['distribution'] = dict(zip(range(1,len(distibution)+1),distibution))
            data['skewness'] = skewness
            if skewness < 4:
                data['game_type'] = 'Maddof'
            elif skewness <=6:
                data['game_type'] = 'Rossem'
            elif skewness <=9:
                data['game_type'] = 'Ponzi'
            else:
                data['game_type'] = 'Ignatova'
            # We can add separate class from Games instead of using User class, for now its obsolete.
            crud_game.create_new_game(db, data)
            flash('Successfuly created New Game')
            return redirect(url_for('ponzi.home'))
        else:
            flash ('Maximum amout of opened rooms reached, please try again later !')

    return render_template('admin.html', form=form)


@view.route('/')
def home():
    games = db.child('game').get()
    create_rooms = db.child('game').order_by_child('status').equal_to('OPEN').get()

    # Boolean field for create new button.
    if len(create_rooms.val()) >= 6:
        create_rooms = False
    else:
        create_rooms = True
    # Check if any games exists in firebase
    if games.val() == None:
        games = []

    return render_template('index.html', games=games, create_rooms=create_rooms)

@view.route('/join/<room_key>')
def join(room_key):
    # Clearing all previous sessions.
    session.clear()

    # Cleaning up distribution to show the values inside the rooms chart bars.
    distribution_chart = db.child('game').child(room_key).child('distribution').get().val()
    distribution_chart = [round(x*100,1) for x in distribution_chart if x != None]
    contribution = db.child('game').child(room_key).child('contribution').get().val()

    return render_template('join.html', room_key=room_key, distribution_chart=distribution_chart, contribution=contribution)


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
        if session['guesses'] <= 1:
            crud_user.end_timer(db, time.time(), failed=True)
            crud_game.add_solved(db, session['room_key'])
            crud_game.check_game_status(db, session['room_key'])
            return redirect(url_for('ponzi.rank', room_key=session['room_key']))
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
        elif has_doubles(guess) is True:
            session['messages'].append('You can repeat numbers. Please, try again.')
        else:
            killed = countX(clues, "Killed"), 'Killed'
            wounded = countX(clues, "Wounded"), 'Wounded'
            session['messages'].append(
                f'There are {wounded[0]}🧨, {killed[0]} 💥')

        if guess == number_to_guess:
            crud_user.end_timer(db, time.time())
            crud_game.add_solved(db, session['room_key'])
            crud_game.check_game_status(db, session['room_key'])
            flash (number_to_guess)
            session['messages'].append('You got it !')
            return redirect(url_for('ponzi.rank', room_key=session['room_key']))

        if session['guesses'] <= 0:
            return redirect(url_for("ponzi.home"))




        return redirect(url_for('ponzi.ponzi'))

    return render_template('game.html', number=number_to_guess, counter=session['guesses'], form=form,
                           notification=zip(session['messages'], session['guess']))


@view.route('/rank/<room_key>')
def rank(room_key):
    crud_user.set_position(db, room_key)

    return render_template('ranking.html', room_key=room_key)


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
        else:
            return jsonify({'data': 'Player already exists'}, 403)

        letters = sample('0123456789', 3)

        if letters[0] == '0':
            letters.reverse()

        number = ''.join(letters)
        session['number'] = number

        return jsonify({'data': 'Session intialized'}, 201)
