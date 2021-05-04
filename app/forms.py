from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp

class GuessForm(FlaskForm):
    guess = StringField('name', validators=[DataRequired(), Length(min=3, max=3), Regexp('^[0-9]*$')])