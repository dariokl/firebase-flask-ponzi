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
    guesses = SelectField('# of Guesses', choices=[50,100])
    n_losers = IntegerField('How many lose all money?')
    contribution = IntegerField('How much money to participate?')
    max_return = IntegerField('Desired return for winner in %')

    @staticmethod
    def distribution(n_players, losers, contribution, max_return):
      #commision the game admin takes to cover cost.only changes here no customizable
      admin_cut=0.18
      total_coins=n_players*contribution
      n_earners=(n_players-losers) #money earned can be 0%
      #available pool of money to distribute
      pool_total= (losers*contribution)-(total_coins*admin_cut)
      avrg_return=pool_total/n_earners
      #we are goint to create step following a pythaghorean approach and based on the variables set by user
      hyp=math.sqrt(n_earners**2+max_return**2)
      #width of each step
      width=hyp/n_earners
      #the steps height to build my distribution staircase
      step=math.sqrt(width**2-1)
      #step= step+(step*admin_cut)
      #lets make sure there is enough money to cover the area of the triangle designed by the user
      area=(n_earners*max_return)/2
      area_pr=((step/2)*n_earners)
      diff= (losers-admin_cut)-(area+area_pr)
      adjust=diff/n_earners
      lista=[]
      for i in range(n_earners):
          steps=i
          retorno=max_return-(step*steps)
          gain=1*retorno
          lista.append(gain)
      distribution = [x+adjust for x in lista]
      tail= [-1 for i in range(losers)]
      distribution=distribution+tail
      return distribution
