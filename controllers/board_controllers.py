from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.board_models import Board
from models.project_models import Project
from models.manager_project_models import ManagerProject
from models.models_models import db, RoleName
from forms.board_forms import BoardForm
from datetime import datetime
import uuid

@login_required
def create_board(project_id):
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=project_id).first():
        flash('Only managers can create boards.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    project = Project.query.get_or_404(project_id)
    form = BoardForm()
    if form.validate_on_submit():
        board = Board(
            board_id=uuid.uuid4(),
            name=form.name.data,
            project_id=project_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(board)
        db.session.commit()
        flash('Board created successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=project_id))
    return render_template('create_board.html', form=form, project=project)

@login_required
def get_board(board_id):
    board = Board.query.get_or_404(board_id)
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=board.project_id).first():
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    return render_template('board_detail.html', board=board)