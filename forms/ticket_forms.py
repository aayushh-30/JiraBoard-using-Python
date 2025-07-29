from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from models.models_models import TicketStatus, TicketPriority

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    status = SelectField('Status', choices=[(e.value, e.value) for e in TicketStatus], default='open')
    priority = SelectField('Priority', choices=[(e.value, e.value) for e in TicketPriority], default='medium')

class HelpdeskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    status = SelectField('Status', choices=[(e.value, e.value) for e in TicketStatus], default='open')
    priority = SelectField('Priority', choices=[(e.value, e.value) for e in TicketPriority], default='medium')