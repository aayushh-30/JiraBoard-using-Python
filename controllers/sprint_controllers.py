from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.sprint_models import Sprint
from models.project_models import Project
from models.manager_project_models import ManagerProject
from models.models_models import db, RoleName
from forms.sprint_forms import SprintForm
from datetime import datetime
import uuid

@login_required
def create_sprint(project_id):
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=project_id).first():
        flash('Only managers can create sprints.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    project = Project.query.get_or_404(project_id)
    form = SprintForm()
    if form.validate_on_submit():
        sprint = Sprint(
            sprint_id=uuid.uuid4(),
            name=form.name.data,
            project_id=project_id,
            subproject_id=form.subproject_id.data or None,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(sprint)
        db.session.commit()
        flash('Sprint created successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=project_id))
    return render_template('create_sprint.html', form=form, project=project)

@login_required
def get_sprint(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=sprint.project_id).first():
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    tasks = sprint.tasks
    return render_template('detail_sprint.html', sprint=sprint, tasks=tasks)