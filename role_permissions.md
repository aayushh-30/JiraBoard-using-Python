# Role-Based Access Control (RBAC) - JIRA System

## Role Hierarchy
1. **Admin** - Full system access
2. **Manager** - Project and team management
3. **Developer** - Development tasks and team collaboration
4. **Client** - Limited project visibility and interaction
5. **Viewer** - Read-only access to assigned projects
6. **Pending** - No access until role is approved

---

## Feature Access Matrix

### 🔴 ADMIN ROLE
**Full system administration and oversight**

#### User Management
- ✅ Create, edit, delete all users
- ✅ Assign and change user roles
- ✅ View all user profiles and contact information
- ✅ Manage user login sessions
- ✅ Reset user passwords
- ✅ Deactivate/reactivate accounts

#### Project Management
- ✅ Create, edit, delete all projects
- ✅ View all projects across the system
- ✅ Assign project managers
- ✅ Archive/restore projects
- ✅ Manage project templates

#### Team Management
- ✅ Create, edit, delete teams
- ✅ Assign team managers
- ✅ Add/remove team members
- ✅ View all team structures

#### Task & Story Management
- ✅ Create, edit, delete all tasks and stories
- ✅ Assign tasks to any user
- ✅ Change task status, priority, type
- ✅ Manage epic hierarchies
- ✅ Access all sprints and boards

#### System Features
- ✅ Generate all reports
- ✅ View system notifications and templates
- ✅ Manage notification templates
- ✅ Access audit logs
- ✅ System configuration
- ✅ Data export/import

---

### 🟠 MANAGER ROLE
**Project and team leadership capabilities**

#### User Management
- ✅ View team member profiles
- ✅ View client contact information
- ❌ Create/delete users
- ❌ Change user roles

#### Project Management
- ✅ Create new projects
- ✅ Edit projects they manage
- ✅ View all projects they're assigned to
- ✅ Assign developers to their projects
- ❌ Delete projects
- ❌ Access projects they're not assigned to

#### Team Management
- ✅ Manage teams they lead
- ✅ Add/remove developers from their teams
- ✅ View team performance metrics
- ❌ Create/delete teams
- ❌ Manage other managers' teams

#### Task & Story Management
- ✅ Create, edit tasks in their projects
- ✅ Assign tasks to team members
- ✅ Change task status and priority
- ✅ Create and manage epics and stories
- ✅ Manage sprints for their projects
- ✅ Create and manage boards

#### Goal Management
- ✅ Create team and project goals
- ✅ Track goal progress
- ✅ Update goal status
- ❌ Create organizational goals

#### Reporting & Analytics
- ✅ Generate project reports
- ✅ View team performance reports
- ✅ Access project analytics
- ❌ System-wide reports

#### Communication
- ✅ Add comments to all project items
- ✅ Upload attachments
- ✅ Receive project notifications
- ✅ Submit and view tickets

---

### 🟢 DEVELOPER ROLE
**Development and collaboration features**

#### User Management
- ✅ View own profile
- ✅ Edit own contact information
- ✅ View team member profiles
- ❌ Edit other users
- ❌ Create/delete users

#### Project Access
- ✅ View projects they're assigned to
- ✅ Access project details and documentation
- ❌ Create/edit projects
- ❌ Assign other developers

#### Task & Story Management
- ✅ View assigned tasks and stories
- ✅ Update status of assigned tasks
- ✅ Add time estimates and actual hours
- ✅ Create subtasks for assigned work
- ✅ View sprint boards and backlogs
- ❌ Assign tasks to others
- ❌ Delete tasks

#### Goal Management
- ✅ Create personal goals
- ✅ View team goals
- ✅ Update personal goal progress
- ❌ Create team/project goals

#### Communication
- ✅ Add comments to tasks/stories
- ✅ Upload attachments to work items
- ✅ Receive task notifications
- ✅ Submit support tickets
- ❌ Delete comments from others

#### Reporting
- ✅ View personal progress reports
- ✅ Access task history
- ❌ Generate team reports

---

### 🔵 CLIENT ROLE
**External stakeholder access**

#### Project Visibility
- ✅ View projects they're associated with
- ✅ Access project progress reports
- ✅ View high-level project status
- ❌ Edit any project details
- ❌ Access internal project data

#### Task & Story Viewing
- ✅ View completed stories and deliverables
- ✅ Access public project boards
- ❌ View in-progress technical tasks
- ❌ Edit any tasks or stories

#### Communication
- ✅ Add comments to client-facing items
- ✅ Submit tickets for support/requests
- ✅ Upload requirement documents
- ✅ Receive project milestone notifications
- ❌ Access internal team communications

#### Reporting
- ✅ View client reports and dashboards
- ✅ Access project milestone reports
- ❌ Access detailed development reports

#### Goal Visibility
- ✅ View project goals related to their business
- ❌ Create or edit any goals

---

### 🟡 VIEWER ROLE
**Read-only access for stakeholders**

#### Limited Project Access
- ✅ View assigned projects (read-only)
- ✅ Access public project information
- ❌ Edit any content
- ❌ Create new items

#### Task & Story Viewing
- ✅ View public tasks and stories
- ✅ Access completed work items
- ❌ Edit or comment on items

#### Communication
- ✅ View public comments
- ❌ Add comments or attachments
- ❌ Submit tickets

#### Reporting
- ✅ View public reports and dashboards
- ❌ Generate any reports

#### Notifications
- ✅ Receive read-only notifications
- ❌ Configure notification preferences

---

### ⚫ PENDING ROLE
**No system access until approved**

#### Access Level
- ❌ No system access
- ❌ Cannot login to application
- ✅ Can receive account activation email
- ✅ Account exists but is inactive

---

## Feature Summary by Entity

### Projects
- **Admin**: Full CRUD access to all projects
- **Manager**: Create/edit own projects, view assigned projects
- **Developer**: View assigned projects only
- **Client**: View associated projects (limited data)
- **Viewer**: View public project information
- **Pending**: No access

### Tasks & Stories
- **Admin**: Full CRUD access to all tasks/stories
- **Manager**: CRUD for team tasks, view all project tasks
- **Developer**: Edit assigned tasks, view team tasks
- **Client**: View completed deliverables only
- **Viewer**: View public tasks only
- **Pending**: No access

### Teams
- **Admin**: Full team management
- **Manager**: Manage own teams only
- **Developer**: View team information
- **Client**: No team access
- **Viewer**: No team access
- **Pending**: No access

### Reports
- **Admin**: All system reports
- **Manager**: Project and team reports
- **Developer**: Personal reports only
- **Client**: Client-specific reports
- **Viewer**: Public reports only
- **Pending**: No access

### Goals
- **Admin**: Full goal management
- **Manager**: Team/project goals
- **Developer**: Personal goals
- **Client**: View business-related goals
- **Viewer**: View public goals
- **Pending**: No access

---

## Implementation Notes

### Database Security
- Use row-level security (RLS) policies in PostgreSQL
- Implement role-based WHERE clauses in queries
- Create database views for role-specific data access

### API Security
- Implement middleware for role verification
- Use JWT tokens with role claims
- Apply permission decorators to endpoints

### Frontend Security
- Conditional rendering based on user role
- Route guards for protected pages
- Hide/disable features based on permissions

### Audit Trail
- Log all permission-sensitive actions
- Track role changes and access attempts
- Maintain compliance audit logs
