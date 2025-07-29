from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired, Length
from models.subproject_models import Subproject

class SprintForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    subproject_id = SelectField('Subproject', coerce=str, choices=[('', 'None')], validate_choice=False)

    def __init__(self, *args, **kwargs):
        super(SprintForm, self).__init__(*args, **kwargs)
        self.subproject_id.choices += [(str(subproject.subproject_id), subproject.name) for subproject in Subproject.query.all()]