from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from models.task_models import Task

class ReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=1000)])
    task_id = SelectField('Task', coerce=str, choices=[('', 'None')], validate_choice=False)

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.task_id.choices += [(str(task.task_id), task.title) for task in Task.query.all()]