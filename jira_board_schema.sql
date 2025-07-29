-- Create ENUM types
CREATE TYPE role_name AS ENUM ('admin', 'manager', 'developer', 'client', 'viewer', 'pending');
CREATE TYPE task_status AS ENUM ('todo', 'in_progress', 'done', 'blocked');
CREATE TYPE task_type AS ENUM ('bug', 'feature', 'task');
CREATE TYPE ticket_status AS ENUM ('open', 'in_progress', 'resolved', 'closed');
CREATE TYPE ticket_priority AS ENUM ('low', 'medium', 'high');
CREATE TYPE goal_status AS ENUM ('pending', 'in_progress', 'completed', 'cancelled');
CREATE TYPE goal_priority AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE goal_category AS ENUM ('personal', 'team', 'project', 'organizational');
CREATE TYPE epic_status AS ENUM ('open', 'in_progress', 'completed', 'cancelled');
CREATE TYPE story_status AS ENUM ('todo', 'in_progress', 'done', 'blocked');
CREATE TYPE story_priority AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE notification_status AS ENUM ('unread', 'read');
CREATE TYPE attachment_type AS ENUM ('document', 'image', 'video', 'audio', 'archive', 'other');
CREATE TYPE comment_type AS ENUM ('comment', 'system', 'status_change', 'assignment');

-- Create role table
CREATE TABLE public.role (
    role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_name role_name NOT NULL UNIQUE
);

-- Create user table
CREATE TABLE public."user" (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role_id UUID NOT NULL,
    contact_no VARCHAR(15),
    company_name VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES public.role(role_id)
);

-- Create user_roles junction table for many-to-many relationship
CREATE TABLE public.user_roles (
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by_id UUID,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES public.role(role_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by_id) REFERENCES public."user"(user_id)
);

-- Create login table
CREATE TABLE public.login (
    login_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    login_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    logout_time TIMESTAMP,
    session_token VARCHAR(256) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES public."user"(user_id)
);

-- Create team table
CREATE TABLE public.team (
    team_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    manager_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES public."user"(user_id)
);

-- Create project table
CREATE TABLE public.project (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create subproject table
CREATE TABLE public.subproject (
    subproject_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    project_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES public.project(project_id)
);

-- Create sprint table
CREATE TABLE public.sprint (
    sprint_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    project_id UUID NOT NULL,
    subproject_id UUID,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES public.project(project_id),
    FOREIGN KEY (subproject_id) REFERENCES public.subproject(subproject_id)
);

-- Create ticket table
CREATE TABLE public.ticket (
    ticket_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status ticket_status NOT NULL DEFAULT 'open',
    priority ticket_priority NOT NULL DEFAULT 'medium',
    raised_by_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (raised_by_id) REFERENCES public."user"(user_id)
);

-- Create task table
CREATE TABLE public.task (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status task_status NOT NULL DEFAULT 'todo',
    type task_type NOT NULL DEFAULT 'task',
    priority VARCHAR(10) DEFAULT 'medium',
    project_id UUID NOT NULL,
    subproject_id UUID,
    sprint_id UUID,
    story_id UUID,
    assigned_to_id UUID,
    parent_task_id UUID,
    estimated_hours FLOAT,
    logged_hours FLOAT DEFAULT 0.0,
    due_date TIMESTAMP,
    labels JSON,
    custom_fields JSON,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES public.project(project_id),
    FOREIGN KEY (subproject_id) REFERENCES public.subproject(subproject_id),
    FOREIGN KEY (sprint_id) REFERENCES public.sprint(sprint_id),
    FOREIGN KEY (story_id) REFERENCES public.story(story_id),
    FOREIGN KEY (assigned_to_id) REFERENCES public."user"(user_id),
    FOREIGN KEY (parent_task_id) REFERENCES public.task(task_id)
);

-- Create attachment table
CREATE TABLE public.attachment (
    attachment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_name VARCHAR(100) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_size BIGINT,
    file_type attachment_type DEFAULT 'document',
    mime_type VARCHAR(100),
    task_id UUID,
    ticket_id UUID,
    story_id UUID,
    created_by_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES public.task(task_id),
    FOREIGN KEY (ticket_id) REFERENCES public.ticket(ticket_id),
    FOREIGN KEY (story_id) REFERENCES public.story(story_id),
    FOREIGN KEY (created_by_id) REFERENCES public."user"(user_id),
    CONSTRAINT check_single_entity CHECK (
        (task_id IS NOT NULL AND ticket_id IS NULL AND story_id IS NULL) OR 
        (task_id IS NULL AND ticket_id IS NOT NULL AND story_id IS NULL) OR
        (task_id IS NULL AND ticket_id IS NULL AND story_id IS NOT NULL)
    )
);

-- Create comment table
CREATE TABLE public.comment (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    comment_type comment_type DEFAULT 'comment',
    task_id UUID,
    ticket_id UUID,
    story_id UUID,
    created_by_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES public.task(task_id),
    FOREIGN KEY (ticket_id) REFERENCES public.ticket(ticket_id),
    FOREIGN KEY (story_id) REFERENCES public.story(story_id),
    FOREIGN KEY (created_by_id) REFERENCES public."user"(user_id),
    CONSTRAINT check_single_entity CHECK (
        (task_id IS NOT NULL AND ticket_id IS NULL AND story_id IS NULL) OR 
        (task_id IS NULL AND ticket_id IS NOT NULL AND story_id IS NULL) OR
        (task_id IS NULL AND ticket_id IS NULL AND story_id IS NOT NULL)
    )
);

-- Create report table
CREATE TABLE public.report (
    report_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    task_id UUID,
    project_id UUID,
    manager_id UUID,
    client_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES public.task(task_id),
    FOREIGN KEY (project_id) REFERENCES public.project(project_id),
    FOREIGN KEY (manager_id) REFERENCES public."user"(user_id),
    FOREIGN KEY (client_id) REFERENCES public."user"(user_id)
);

-- Create board table
CREATE TABLE public.board (
    board_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    project_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES public.project(project_id)
);

-- Create developer_team table
CREATE TABLE public.developer_team (
    developer_id UUID NOT NULL,
    team_id UUID NOT NULL,
    PRIMARY KEY (developer_id, team_id),
    FOREIGN KEY (developer_id) REFERENCES public."user"(user_id),
    FOREIGN KEY (team_id) REFERENCES public.team(team_id)
);

-- Create manager_project table
CREATE TABLE public.manager_project (
    manager_id UUID NOT NULL,
    project_id UUID NOT NULL,
    PRIMARY KEY (manager_id, project_id),
    FOREIGN KEY (manager_id) REFERENCES public."user"(user_id),
    FOREIGN KEY (project_id) REFERENCES public.project(project_id)
);

-- Create developer_project table
CREATE TABLE public.developer_project (
    developer_id UUID NOT NULL,
    project_id UUID NOT NULL,
    PRIMARY KEY (developer_id, project_id),
    FOREIGN KEY (developer_id) REFERENCES public."user"(user_id),
    FOREIGN KEY (project_id) REFERENCES public.project(project_id)
);

-- Create notification_template table
CREATE TABLE public.notification_template (
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create goal table
CREATE TABLE public.goal (
    goal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    project_id UUID,
    user_id UUID NOT NULL,
    priority goal_priority NOT NULL DEFAULT 'medium',
    status goal_status NOT NULL DEFAULT 'pending',
    target_date TIMESTAMP,
    completion_date TIMESTAMP,
    progress_percentage FLOAT DEFAULT 0.0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    category goal_category NOT NULL DEFAULT 'personal',
    is_milestone BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES public.project(project_id),
    FOREIGN KEY (user_id) REFERENCES public."user"(user_id)
);

-- Create epic table
CREATE TABLE public.epic (
    epic_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    project_id UUID NOT NULL,
    status epic_status DEFAULT 'open',
    start_date TIMESTAMP,
    target_date TIMESTAMP,
    created_by_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES public.project(project_id),
    FOREIGN KEY (created_by_id) REFERENCES public."user"(user_id)
);

-- Create story table
CREATE TABLE public.story (
    story_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    acceptance_criteria TEXT,
    epic_id UUID,
    project_id UUID NOT NULL,
    sprint_id UUID,
    status story_status DEFAULT 'todo',
    priority story_priority DEFAULT 'medium',
    story_points INTEGER,
    assigned_to_id UUID,
    created_by_id UUID NOT NULL,
    estimated_hours FLOAT,
    actual_hours FLOAT,
    start_date TIMESTAMP,
    due_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (epic_id) REFERENCES public.epic(epic_id),
    FOREIGN KEY (project_id) REFERENCES public.project(project_id),
    FOREIGN KEY (sprint_id) REFERENCES public.sprint(sprint_id),
    FOREIGN KEY (assigned_to_id) REFERENCES public."user"(user_id),
    FOREIGN KEY (created_by_id) REFERENCES public."user"(user_id)
);

-- Create notification table
CREATE TABLE public.notification (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    status notification_status DEFAULT 'unread',
    related_entity_type VARCHAR(50),
    related_entity_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES public."user"(user_id)
);

-- Create indexes for performance
CREATE INDEX idx_user_role_id ON public."user"(role_id);
CREATE INDEX idx_user_roles_user_id ON public.user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON public.user_roles(role_id);
CREATE INDEX idx_user_roles_primary ON public.user_roles(user_id, is_primary) WHERE is_primary = TRUE;
CREATE UNIQUE INDEX idx_user_roles_unique_primary ON public.user_roles(user_id) WHERE is_primary = TRUE;
CREATE INDEX idx_task_project_id ON public.task(project_id);
CREATE INDEX idx_task_subproject_id ON public.task(subproject_id);
CREATE INDEX idx_task_sprint_id ON public.task(sprint_id);
CREATE INDEX idx_task_story_id ON public.task(story_id);
CREATE INDEX idx_task_assigned_to_id ON public.task(assigned_to_id);
CREATE INDEX idx_ticket_raised_by_id ON public.ticket(raised_by_id);
CREATE INDEX idx_comment_task_id ON public.comment(task_id);
CREATE INDEX idx_comment_ticket_id ON public.comment(ticket_id);
CREATE INDEX idx_comment_story_id ON public.comment(story_id);
CREATE INDEX idx_attachment_task_id ON public.attachment(task_id);
CREATE INDEX idx_attachment_ticket_id ON public.attachment(ticket_id);
CREATE INDEX idx_attachment_story_id ON public.attachment(story_id);
CREATE INDEX idx_sprint_project_id ON public.sprint(project_id);
CREATE INDEX idx_sprint_subproject_id ON public.sprint(subproject_id);
CREATE INDEX idx_board_project_id ON public.board(project_id);
CREATE INDEX idx_report_project_id ON public.report(project_id);
CREATE INDEX idx_goal_project_id ON public.goal(project_id);
CREATE INDEX idx_goal_user_id ON public.goal(user_id);
CREATE INDEX idx_goal_status ON public.goal(status);
CREATE INDEX idx_goal_priority ON public.goal(priority);
CREATE INDEX idx_goal_target_date ON public.goal(target_date);
CREATE INDEX idx_epic_project_id ON public.epic(project_id);
CREATE INDEX idx_epic_created_by_id ON public.epic(created_by_id);
CREATE INDEX idx_epic_status ON public.epic(status);
CREATE INDEX idx_story_epic_id ON public.story(epic_id);
CREATE INDEX idx_story_project_id ON public.story(project_id);
CREATE INDEX idx_story_sprint_id ON public.story(sprint_id);
CREATE INDEX idx_story_assigned_to_id ON public.story(assigned_to_id);
CREATE INDEX idx_story_status ON public.story(status);
CREATE INDEX idx_story_priority ON public.story(priority);
CREATE INDEX idx_notification_user_id ON public.notification(user_id);
CREATE INDEX idx_notification_status ON public.notification(status);