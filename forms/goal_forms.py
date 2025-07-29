from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from models.goal_models import GoalStatus, GoalPriority, GoalCategory

class GoalForm(FlaskForm):
    title = StringField('Goal Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    project_id = SelectField('Project', choices=[], coerce=str, validators=[Optional()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='medium', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending', validators=[DataRequired()])
    target_date = DateField('Target Date', validators=[Optional()])
    progress_percentage = FloatField('Progress (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0.0)
    category = SelectField('Category', choices=[
        ('personal', 'Personal'),
        ('team', 'Team'),
        ('project', 'Project'),
        ('organizational', 'Organizational')
    ], default='personal', validators=[DataRequired()])
    is_milestone = BooleanField('Is Milestone')
    submit = SubmitField('Save Goal')

class GoalFilterForm(FlaskForm):
    status = SelectField('Filter by Status', choices=[
        ('', 'All Statuses'),
        (GoalStatus.PENDING.value, 'Pending'),
        (GoalStatus.IN_PROGRESS.value, 'In Progress'),
        (GoalStatus.COMPLETED.value, 'Completed'),
        (GoalStatus.CANCELLED.value, 'Cancelled')
    ], default='')
    priority = SelectField('Filter by Priority', choices=[
        ('', 'All Priorities'),
        (GoalPriority.LOW.value, 'Low'),
        (GoalPriority.MEDIUM.value, 'Medium'),
        (GoalPriority.HIGH.value, 'High'),
        (GoalPriority.URGENT.value, 'Urgent')
    ], default='')
    category = SelectField('Filter by Category', choices=[
        ('', 'All Categories'),
        (GoalCategory.PERSONAL.value, 'Personal'),
        (GoalCategory.TEAM.value, 'Team'),
        (GoalCategory.PROJECT.value, 'Project'),
        (GoalCategory.ORGANIZATIONAL.value, 'Organizational')
    ], default='')
    project_id = SelectField('Filter by Project', choices=[], coerce=str, default='')
    filter = SubmitField('Apply Filters')

class GoalProgressForm(FlaskForm):
    progress_percentage = FloatField('Progress (%)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    status = SelectField('Status', choices=[
        (GoalStatus.PENDING.value, 'Pending'),
        (GoalStatus.IN_PROGRESS.value, 'In Progress'),
        (GoalStatus.COMPLETED.value, 'Completed'),
        (GoalStatus.CANCELLED.value, 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Progress')
