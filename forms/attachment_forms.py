from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import DataRequired

class AttachmentForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])