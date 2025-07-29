from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.subproject_models import Subproject
from models.project_models import Project
from models.manager_project_models import ManagerProject
from models.models_models import db, RoleName
from forms.subproject_forms import SubprojectForm
from datetime import datetime
import uuid

@login_required
def create_subproject(project_id):
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=project_id).first():
        flash('Only managers can create subprojects.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    project = Project.query.get_or_404(project_id)
    form = SubprojectForm()
    if form.validate_on_submit():
        subproject = Subproject(
            subproject_id=uuid.uuid4(),
            name=form.name.data,
            project_id=project_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(subproject)
        db.session.commit()
        flash('Subproject created successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=project_id))
    return render_template('create_subproject.html', form=form, project=project)

@login_required
def get_subproject(subproject_id):
    subproject = Subproject.query.get_or_404(subproject_id)
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=subproject.project_id).first():
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    tasks = subproject.tasks
    sprints = subproject.sprints
    return render_template('detail_subproject.html', subproject=subproject, tasks=tasks, sprints=sprints)