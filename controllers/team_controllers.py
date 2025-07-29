from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from permissions import (
    require_permission, 
    require_any_permission,
    manager_or_admin_required,
    team_access_required,
    can_user_access_team
)
from models.team_models import Team
from models.developer_team_models import DeveloperTeam
from models.models_models import db, RoleName
from forms.team_forms import TeamForm, TeamMembershipForm
from datetime import datetime
import uuid

@login_required
@require_permission('team_create')
def create_team():
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(
            team_id=uuid.uuid4(),
            name=form.name.data,
            manager_id=current_user.manager.manager_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(team)
        db.session.commit()
        flash('Team created successfully!', 'success')
        return redirect(url_for('team.teams'))
    return render_template('team_create.html', form=form)

@login_required
@require_permission('team_view')
def get_teams():
    # Permission-based team filtering is now handled by the decorator
    # Additional role-based filtering for data display
    user_role = getattr(current_user, 'role_name', None)
    
    if user_role == 'admin':
        teams = Team.query.all()
    elif user_role == 'manager' and hasattr(current_user, 'manager'):
        teams = Team.query.filter_by(manager_id=current_user.manager.manager_id).all()
    else:
        # For other roles, show teams they have access to
        teams = Team.query.all()  # This could be filtered further based on team membership
    
    return render_template('team_list.html', teams=teams)

@login_required
@require_permission('team_assign_users')
@team_access_required
def add_team_member(team_id):
    team = Team.query.get_or_404(team_id)
    
    form = TeamMembershipForm()
    if form.validate_on_submit():
        developer_team = DeveloperTeam(
            developer_id=form.developer_id.data,
            team_id=team_id
        )
        db.session.add(developer_team)
        db.session.commit()
        flash('Developer added to team successfully!', 'success')
        return redirect(url_for('team.get_team', team_id=team_id))
    return render_template('team_add_member.html', form=form, team=team)

@login_required
@require_permission('team_view')
@team_access_required
def get_team(team_id):
    team = Team.query.get_or_404(team_id)
    return render_template('team_detail.html', team=team)

@login_required
@require_permission('team_edit')
@team_access_required
def update_team(team_id):
    team = Team.query.get_or_404(team_id)
    form = TeamForm()
    
    if form.validate_on_submit():
        team.name = form.name.data
        team.description = form.description.data
        team.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Team updated successfully!', 'success')
        return redirect(url_for('team.detail', team_id=team_id))
    
    # Pre-populate form with existing data
    form.name.data = team.name
    form.description.data = getattr(team, 'description', '')
    
    return render_template('team_edit.html', form=form, team=team)