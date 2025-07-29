from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.report_models import Report
from models.project_models import Project
from models.task_models import Task
from models.models_models import db, RoleName
from forms.report_forms import ReportForm
from datetime import datetime
import uuid

@login_required
def create_report(project_id):
    if current_user.role.role_name not in [RoleName.admin, RoleName.manager, RoleName.client]:
        flash('Only admins, managers and clients can create reports.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    project = Project.query.get_or_404(project_id)
    form = ReportForm()
    if form.validate_on_submit():
        report = Report(
            report_id=uuid.uuid4(),
            title=form.title.data,
            content=form.content.data,
            task_id=form.task_id.data or None,
            project_id=project_id,
            manager_id=current_user.manager.manager_id if current_user.role.role_name == RoleName.manager else None,
            client_id=current_user.client.client_id if current_user.role.role_name == RoleName.client else None,
            created_at=datetime.utcnow()
        )
        db.session.add(report)
        db.session.commit()
        flash('Report created successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=project_id))
    return render_template('create_report.html', form=form, project=project)

@login_required
def get_reports():
    if current_user.role.role_name not in [RoleName.admin, RoleName.manager, RoleName.client]:
        flash('Only admins, managers and clients can view reports.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    
    if current_user.role.role_name == RoleName.admin:
        # Admin can see all reports
        reports = Report.query.all()
    elif current_user.role.role_name == RoleName.manager:
        reports = Report.query.filter_by(manager_id=current_user.manager.manager_id).all()
    else:
        reports = Report.query.filter_by(client_id=current_user.client.client_id).all()
    return render_template('report_list.html', reports=reports)