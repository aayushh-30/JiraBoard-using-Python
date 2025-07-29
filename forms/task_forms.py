from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from models.models_models import TaskStatus, TaskType
from models.user_models import User
from models.subproject_models import Subproject
from models.sprint_models import Sprint

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    status = SelectField('Status', choices=[(e.value, e.value) for e in TaskStatus], default='open')
    type = SelectField('Type', choices=[(e.value, e.value) for e in TaskType], default='task')
    subproject_id = SelectField('Subproject', coerce=str, choices=[('', 'None')], validate_choice=False)
    sprint_id = SelectField('Sprint', coerce=str, choices=[('', 'None')], validate_choice=False)
    assigned_to = SelectField('Assigned To', coerce=str, choices=[('', 'Unassigned')], validate_choice=False)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.subproject_id.choices += [(str(subproject.subproject_id), subproject.name) for subproject in Subproject.query.all()]
        self.sprint_id.choices += [(str(sprint.sprint_id), sprint.name) for sprint in Sprint.query.all()]
        self.assigned_to.choices += [(str(user.user_id), user.username) for user in User.query.filter(User.role.has(role_name='developer')).all()]