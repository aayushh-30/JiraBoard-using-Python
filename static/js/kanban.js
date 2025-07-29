// Kanban Board Functionality for JIRA-style Task Management

class KanbanBoard {
    constructor(projectId) {
        this.projectId = projectId;
        this.columns = new Map();
        this.tasks = new Map();
        this.init();
    }

    init() {
        this.setupDragAndDrop();
        this.loadTasks();
        this.setupColumnManagement();
    }

    setupDragAndDrop() {
        // Enable drag and drop for task cards
        document.addEventListener('dragstart', (e) => {
            if (e.target.classList.contains('task-card')) {
                e.target.classList.add('dragging');
                e.dataTransfer.setData('text/plain', e.target.dataset.taskId);
                e.dataTransfer.effectAllowed = 'move';
            }
        });

        document.addEventListener('dragend', (e) => {
            if (e.target.classList.contains('task-card')) {
                e.target.classList.remove('dragging');
            }
        });

        // Setup drop zones
        document.querySelectorAll('.kanban-column').forEach(column => {
            column.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
                column.classList.add('drag-over');
            });

            column.addEventListener('dragleave', (e) => {
                if (!column.contains(e.relatedTarget)) {
                    column.classList.remove('drag-over');
                }
            });

            column.addEventListener('drop', (e) => {
                e.preventDefault();
                column.classList.remove('drag-over');
                
                const taskId = e.dataTransfer.getData('text/plain');
                const newStatus = column.dataset.status;
                
                this.moveTask(taskId, newStatus);
            });
        });
    }

    async moveTask(taskId, newStatus) {
        try {
            const response = await fetch(`/tasks/${taskId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ status: newStatus })
            });

            if (response.ok) {
                const result = await response.json();
                this.updateTaskPosition(taskId, newStatus);
                toastManager.show(`Task moved to ${newStatus}`, 'success', 2000);
            } else {
                toastManager.show('Failed to move task', 'error', 3000);
            }
        } catch (error) {
            console.error('Error moving task:', error);
            toastManager.show('Error moving task', 'error', 3000);
        }
    }

    updateTaskPosition(taskId, newStatus) {
        const taskCard = document.querySelector(`[data-task-id="${taskId}"]`);
        const targetColumn = document.querySelector(`[data-status="${newStatus}"] .task-list`);
        
        if (taskCard && targetColumn) {
            targetColumn.appendChild(taskCard);
            
            // Update task data
            if (this.tasks.has(taskId)) {
                this.tasks.get(taskId).status = newStatus;
            }
        }
    }

    async loadTasks() {
        try {
            const response = await fetch(`/api/projects/${this.projectId}/tasks`);
            if (response.ok) {
                const tasks = await response.json();
                this.renderTasks(tasks);
            }
        } catch (error) {
            console.error('Error loading tasks:', error);
        }
    }

    renderTasks(tasks) {
        // Clear existing tasks
        document.querySelectorAll('.task-list').forEach(list => {
            list.innerHTML = '';
        });

        tasks.forEach(task => {
            this.tasks.set(task.task_id, task);
            this.renderTask(task);
        });
    }

    renderTask(task) {
        const taskCard = document.createElement('div');
        taskCard.className = 'task-card';
        taskCard.draggable = true;
        taskCard.dataset.taskId = task.task_id;
        
        const priorityClass = this.getPriorityClass(task.priority);
        const typeIcon = this.getTypeIcon(task.type);
        
        taskCard.innerHTML = `
            <div class="task-header">
                <span class="task-type ${typeIcon.class}">
                    <i class="fas ${typeIcon.icon}"></i>
                </span>
                <span class="task-priority ${priorityClass}"></span>
            </div>
            <div class="task-title">${task.title}</div>
            <div class="task-meta">
                <span class="task-id">#${task.task_id.slice(-8)}</span>
                ${task.assigned_to ? `<span class="task-assignee">${task.assigned_to}</span>` : ''}
            </div>
        `;

        const targetColumn = document.querySelector(`[data-status="${task.status}"] .task-list`);
        if (targetColumn) {
            targetColumn.appendChild(taskCard);
        }
    }

    getPriorityClass(priority) {
        const priorities = {
            'high': 'priority-high',
            'medium': 'priority-medium',
            'low': 'priority-low'
        };
        return priorities[priority] || 'priority-medium';
    }

    getTypeIcon(type) {
        const types = {
            'bug': { icon: 'fa-bug', class: 'type-bug' },
            'feature': { icon: 'fa-star', class: 'type-feature' },
            'task': { icon: 'fa-tasks', class: 'type-task' }
        };
        return types[type] || { icon: 'fa-tasks', class: 'type-task' };
    }

    setupColumnManagement() {
        // Add new column functionality
        const addColumnBtn = document.getElementById('add-column-btn');
        if (addColumnBtn) {
            addColumnBtn.addEventListener('click', () => {
                this.showAddColumnModal();
            });
        }
    }

    showAddColumnModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Add New Column</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="add-column-form">
                            <div class="mb-3">
                                <label for="column-name" class="form-label">Column Name</label>
                                <input type="text" class="form-control" id="column-name" required>
                            </div>
                            <div class="mb-3">
                                <label for="column-status" class="form-label">Status Value</label>
                                <input type="text" class="form-control" id="column-status" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="kanbanBoard.addColumn()">Add Column</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }

    async addColumn() {
        const name = document.getElementById('column-name').value;
        const status = document.getElementById('column-status').value;
        
        if (!name || !status) {
            toastManager.show('Please fill all fields', 'warning', 2000);
            return;
        }

        try {
            const response = await fetch(`/api/projects/${this.projectId}/columns`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ name, status })
            });

            if (response.ok) {
                location.reload(); // Refresh to show new column
            } else {
                toastManager.show('Failed to add column', 'error', 3000);
            }
        } catch (error) {
            console.error('Error adding column:', error);
            toastManager.show('Error adding column', 'error', 3000);
        }
    }

    getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }
}

// Initialize Kanban board when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const projectBoard = document.getElementById('kanban-board');
    if (projectBoard) {
        const projectId = projectBoard.dataset.projectId;
        window.kanbanBoard = new KanbanBoard(projectId);
    }
});
