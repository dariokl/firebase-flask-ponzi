from flask import render_template, redirect, session, request, jsonify
import time
import json
from random import sample, shuffle

from . import ponzibp as view

from ..forms import GuessForm

from ..firebase_utils.user import crud_user
from ..firebase_utils.db import db

@view.route('/')
def root():
    # It shoud have been game_crud.create_new_game , so separated class for database events should be created.    
    crud_user.create_new_game(db)

    return render_template('index.html')

@view.route('/join')
def join():
    session.clear()

    return render_template('join.html')

@view.route('/ponzi', methods=['GET', 'POST'])
def ponzi():
    form = GuessForm()
    
    email = session['email']
    current_user = crud_user.current_user(db, email)
    if not current_user:
        crud_user.create_new_user(db, email)

    letters = sample('0123456789', 3)

    if letters[0] == '0':
        letters.reverse()

    number = ''.join(letters)

    def has_doubles(n):
        return len(set(str(n))) < len(str(n))
    #counting killed-injured function
    def countX(lst, x):
        count = 0
        for ele in lst:
            if (ele == x):
                count = count + 1
        return count

    if form.validate_on_submit() and request.method == 'POST':
        crud_user.set_timer(db, time.time())
        # Making the counter run down to 0
        session['guesses'] -= 1
        if session['guesses'] < 0:
            return redirect('/')
         # The input from player
        guess = request.form['guess']
        session['guess'].append(guess)
        # the previous number is stored in session because once the post is made it generates new number
        number_to_guess = session['number']

        # Clues list
        clues = []
        #check if input repeats digits function to warn player
        for index in range(3):
            if guess[index] == number_to_guess[index]:
                clues.append('Killed')
            elif guess[index] in number_to_guess[index]:
                clues.append('Wounded')

        #counting killed-injured function
        if len(clues) == 0:
            session['messages'].append('Nothing')
        else:
            killed = countX(clues, "Killed"), 'Killed'
            wounded = countX(clues, "Wounded"), 'Wounded'
            session['messages'].append(f'There are {killed[0]} {killed[1]}, {wounded[0]} {wounded[1]}')

        if guess == session['number']:
            crud_user.end_timer(db, time.time())
            crud_user.set_position(db)
            session['messages'].append('You got it !')
            return redirect('/rank')
        
        # add the new number into session
        session['number'] = number

        return redirect('/ponzi')

    return render_template('game.html', number=session['number'], counter=session['guesses'], form=form, notification=zip(session['messages'], session['guess']))

@view.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.get_json()['email']

        # Creating all session objects once user submits the email to join.
        session['email'] = user
        session['guesses'] = 10
        session['messages'] = []
        session['guess'] = []

        letters = sample('0123456789', 3)

        if letters[0] == '0':
            letters.reverse()

        number = ''.join(letters)
        session['number'] = number

        return jsonify({'Message': 'Session intialized'})

@view.route('/rank')
def rank():

    return render_template('ranking.html')