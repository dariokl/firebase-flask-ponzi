from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, ValidationError
from wtforms.validators import DataRequired, NumberRange, Length, Regexp

import math


GAME_TYPES = [('Ponzi', 'Ponzi Room'), ('Ignatova', 'Ignatova Room'), ('Maddof', 'Maddoff Room')
        ,('Rossem', 'Van Rossem Room')]

class GuessForm(FlaskForm):
    guess = StringField('name', validators=[
                        DataRequired(), Length(min=3, max=3), Regexp('^[0-9]*$')])


class GameForm(FlaskForm):
    game_type = SelectField('Type of Game', choices=GAME_TYPES)
    allowed_players = IntegerField('Number of participants')
    guesses = IntegerField('Amount of guesses')
    n_losers = IntegerField('How many lose all money?')
    contribution = IntegerField('How much money to participate?')
    max_return = IntegerField('Desired return for winner in %')

    @staticmethod
    def distribution(n_players, losers, contribution, max_return):
      # commision the game admin takes to cover cost.only changes here no customizable
        admin_cut = 0.05
        total_coins = n_players*contribution
        n_earners = (n_players-losers)  # money earned can be 0%
  # available pool of money to distribute
        pool_total = (losers*contribution)-(total_coins*admin_cut)
        avrg_return = pool_total/n_earners
  # we are goint to create step following a pythaghorean approach and based on the variables set by user
        hyp = math.sqrt(n_earners**2+max_return**2)
  # width of each step
        width = hyp/n_earners
  # the steps height plus a 10% deeper
        step = math.sqrt(width**2-1)
        step = step+(step*admin_cut)
  # lets make sure there is enough money to cover the area of the triangle designed by the user
        area = (n_earners*(max_return*100))/2
        # just checking there would be anough money fill out the triangle
        excess = pool_total-area
        lista = []
        adjust = []
        for i in range(n_earners):
            steps = i+1
            retorno = max_return-(step*steps)
            gain = 1*retorno
            count = pool_total-gain*100
            pool_total = count
            lista.append(gain)
            adjust.append(count)
        *_, last = adjust
        remaining = last/n_earners/100
        distribution = [x+remaining for x in lista]
        tail = [-1 for i in range(losers)]
        distribution = distribution+tail
        return distribution