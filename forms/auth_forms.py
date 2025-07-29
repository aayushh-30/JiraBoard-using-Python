from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from models.models_models import RoleName

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_no = StringField('Contact Number', validators=[Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[(role.value, role.value) for role in RoleName], validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[(role.value, role.value) for role in RoleName if role != RoleName.pending], validators=[DataRequired()])

class RoleAssignmentForm(FlaskForm):
    role = SelectField('Role', choices=[(role.value, role.value) for role in RoleName if role != RoleName.pending], validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[Length(max=100)])