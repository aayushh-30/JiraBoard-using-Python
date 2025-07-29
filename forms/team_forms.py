from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from models.user_models import User

class TeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    team_lead = SelectField('Team Lead', coerce=str, validators=[DataRequired()], choices=[])
    
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.team_lead.choices = [(str(user.user_id), user.username) for user in User.query.filter(User.role.has(role_name='manager')).all()]

class TeamMembershipForm(FlaskForm):
    developer_id = SelectField('Developer', coerce=str, validators=[DataRequired()], choices=[])

    def __init__(self, *args, **kwargs):
        super(TeamMembershipForm, self).__init__(*args, **kwargs)
        self.developer_id.choices = [(str(user.user_id), user.username) for user in User.query.filter(User.role.has(role_name='developer')).all()]