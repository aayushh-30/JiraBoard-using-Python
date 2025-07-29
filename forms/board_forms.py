from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class BoardForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])