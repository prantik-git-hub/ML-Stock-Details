# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class TickerForm(FlaskForm):
    ticker = StringField('Ticker Symbol', validators=[DataRequired()])
    submit = SubmitField('Analyze')
