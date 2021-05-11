from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp


GAME_TYPES = [('Ponzi', 'Ponzi Room'), ('Ignatova', 'Ignatova Room'), ('Maddof', 'Maddoff Room')
        ,('Rossem', 'Van Rossem Room')]

class GuessForm(FlaskForm):
    guess = StringField('name', validators=[
                        DataRequired(), Length(min=3, max=3), Regexp('^[0-9]*$')])

class GameForm(FlaskForm):
    game_type = SelectField('Type of Game', choices=GAME_TYPES)
    allowed_players = IntegerField('Number of participants')
    guesses = IntegerField('Amount of guesses')
