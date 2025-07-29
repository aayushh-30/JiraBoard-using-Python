from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SubprojectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])