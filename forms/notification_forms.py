from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

class NotificationTemplateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=1000)])