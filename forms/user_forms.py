from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Optional, Length

class UserProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_no = StringField('Contact Number', validators=[Optional(), Length(max=15)])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    contact_no = StringField('Contact Number', validators=[Optional(), Length(max=15)])
    role = SelectField('Role', choices=[
        ('550e8400-e29b-41d4-a716-446655440301', 'Admin'),
        ('550e8400-e29b-41d4-a716-446655440302', 'Manager'),
        ('550e8400-e29b-41d4-a716-446655440303', 'Developer'),
        ('550e8400-e29b-41d4-a716-446655440304', 'Client')
    ], validators=[DataRequired()])
    is_approved = BooleanField('Approved', default=True)