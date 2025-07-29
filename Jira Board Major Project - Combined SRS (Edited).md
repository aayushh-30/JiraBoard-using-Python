# 🧑‍💻 Software Requirements Specification (SRS)

## 📘 Jira Board System

This document defines the **functional, non-functional, and security requirements** for the Jira board system, encompassing system-wide enhancements and the specific features available to Admin, Manager, Developer, Client, and Viewer roles. The system is a web-based project management tool designed to facilitate task tracking and collaboration across projects, subprojects, and issues (including tasks and subtasks).

---

## 📄 Table of Contents
1. Overview
2. Functional Requirements
3. Permissions and Restrictions
4. Non-Functional Requirements
5. Security Considerations

---

## 📝 1. Overview

The Jira board system supports multiple user roles: **Admin**, responsible for overseeing the system, managing users, and assigning roles/projects; **Manager**, tasked with creating and managing projects/subprojects, assigning issues, and overseeing progress across multiple projects; **Developer**, focused on executing issues within assigned projects and adding Viewers to issues; **Client**, designed for stakeholders to monitor progress on assigned boards/projects; and **Viewer**, a role for viewing specific assigned issues and public data. The system includes a hierarchical structure of projects (owned by teams, multi-team capable), subprojects (no ownership, member-assigned, e.g., components or linked projects), and issues (tasks and subtasks), with enhancements to improve functionality, accessibility, and extensibility.

---

## ✅ 2. Functional Requirements

### 📋 System-Wide Enhancements

#### 🔗 Integration with External Tools
- Enable synchronization with external tools such as Slack for notifications, Google Drive for file storage, and GitHub for commit linking.
- Automate issue updates based on GitHub commits or Slack messages.

#### 🔍 Advanced Search and Query Language
- Support advanced queries using a JQL-like syntax (e.g., “assignee=John AND priority=High”) with Boolean logic.
- Allow users to save and reuse custom search filters.

#### 📊 Customizable Dashboard Widgets
- Provide draggable widgets (e.g., issue count, overdue issues) for personalized dashboards.
- Display role-specific data, such as team statistics for Managers or personal issue views for Developers.

#### 🔗 Task Dependencies and Gantt Charts
- Allow definition of issue dependencies (e.g., Issue B depends on Issue A completion).
- Offer an interactive Gantt chart for visualizing project timelines.

#### 📜 Audit Trail and Compliance
- Record all system actions (e.g., issue edits, user additions) in a dedicated log.
- Support CSV export of logs for compliance purposes.

#### 🌐 Multi-Language Support
- Implement language switching with support for multiple languages (e.g., English, Spanish) and right-to-left (RTL) compatibility.
- Adjust user interface labels and notifications based on the selected language.

#### ⚙️ Custom Workflows and State Machines
- Enable Managers to define custom issue states (e.g., “Code Review”) and transition rules.
- Enforce conditions, such as requiring all subtasks to be complete before a status change.

#### 🗺️ Epics and Roadmap Planning
- Support grouping related issues under epics for better organization.
- Provide a high-level roadmap view accessible to all roles.

#### 💾 Backup and Restore
- Allow Managers to back up project data (issues, boards) to local storage.
- Include a restore option to recover deleted projects or issues.

#### 🛠️ Public API for Extensibility
- Expose a RESTful API with endpoints for project, subproject, and issue management.
- Restrict API access to authorized users.

#### 🎓 User Onboarding and Training
- Offer an interactive guided tour to help new users learn the interface and features.
- Ensure tutorials are available in multiple languages and include tooltips for accessibility.

#### 🔔 Task Notifications Customization
- Allow users to customize notification preferences (e.g., email frequency, in-app alerts) for issue updates, mentions, and deadlines.
- Store preferences in user profiles.

#### 👥 Real-Time Collaboration
- Enable real-time co-editing of issue details and comments by multiple users.
- Implement basic conflict resolution (e.g., last edit wins with notification).

#### 📥📤 Data Import/Export
- Support importing and exporting project data (e.g., CSV, JSON) for migration or external analysis.
- Ensure compatibility with common project management formats.

#### 📊 User Activity Reports
- Provide Managers with detailed reports on user activity (e.g., time spent, issues completed) beyond performance tracking.
- Allow export of reports in CSV format.

#### 🔗 Issue Linking
- Allow linking of issues (e.g., "relates to," "blocks," "duplicates") to show relationships across projects/subprojects.
- Support manual and automated linking based on issue attributes.

#### ⚙️ Workflow Conditions and Validators
- Enhance custom workflows with conditions (e.g., role-based transitions) and validators (e.g., required fields).
- Ensure validation rules are configurable by Managers.

#### 🏃‍♂️ Sprints and Agile Boards
- Introduce sprint management with start/end dates and planning views.
- Provide Agile-specific boards for tracking sprints and burndown charts.

#### 📞 Jira Service Management (Help Desk)
- Add a help desk module for Clients to submit requests.
- Include SLA (Service Level Agreement) tracking for Managers to monitor response times.

#### 📊 Custom Dashboards and Gadgets
- Expand dashboard widgets with pre-built gadgets (e.g., pie charts, two-dimensional filters).
- Allow advanced filtering and customization options.

#### ⏱️ Time Tracking Reports
- Enhance User Activity Reports with detailed time tracking analytics (e.g., work logs by user or issue).
- Support export of time tracking data in CSV format.

#### 🎨 Collaborative Whiteboard Integration
- Integrate a virtual whiteboard for real-time brainstorming or planning within projects.
- Support saving and sharing whiteboard sessions.

#### 💡 Automated Issue Suggestions
- Use rule-based automation to suggest related issues or tasks based on keywords or assignees.
- Provide a manual override option for suggestions.

#### 📈 Project Health Score
- Calculate a health score for projects/subprojects based on completion rates, deadlines, and issue status.
- Display the score on dashboards with color-coded indicators.

#### 🔑 Guest Access Tokens
- Allow Managers to generate temporary access tokens for Viewers or external stakeholders without full accounts.
- Include token expiration and usage limits.

#### 📐 Schema Planning
- Provide a visual tool for Admins and Managers to design and manage database schemas (e.g., project/subproject/issue relationships).
- Export schemas in formats like SQL or JSON.

#### 🎨 Workflow Maker
- Offer a drag-and-drop interface for creating and editing custom workflows, inspired by Excalidraw.
- Support real-time preview and save workflow designs.

### 🧑‍💼 Admin Role Features
- **System Oversight**: Manage all users, roles, and system configurations.
- **Project and Subproject Management**: Create, edit, and delete projects/subprojects across the system.
- **User Management**: Invite, assign roles, and remove users; view all profiles.
- **Issue Oversight**: Create, assign, and manage all issues (tasks/subtasks).
- **Reporting and Monitoring**: Access all reports, audit trails, and performance dashboards.
- **Schema and Workflow Design**: Use Schema Planning and Workflow Maker tools to define system structure and workflows.

### 🧑‍💼 Manager Role Features

#### 📁 Project and Subproject Management
- **Create Projects/Subprojects**: Initiate projects (owned by a team, multi-team capable) and subprojects (member-assigned, e.g., components or linked projects).
- **Edit Project/Subproject Details**: Update names, descriptions, and statuses.
- **Delete Projects/Subprojects**: Remove with a soft-delete option.
- **Create/Delete Boards**: Manage boards within projects/subprojects.
- **Define Board Columns**: Customize issue stages (e.g., To Do, In Progress, Done).

#### 👥 Team & User Management
- **Invite Users**: Add Developers, Clients, and Viewers via email or links.
- **Assign Roles**: Grant and adjust roles; assign Clients/Viewers to specific boards/projects.
- **Remove Users**: Delete inactive or unnecessary team members.
- **View Team Member Profiles**: Access activity history, assigned issues, and performance.

#### ✅ Issue, Task, and Subtask Management
- **Create Issues/Tasks/Subtasks**: Add with title, description, priority, and due date.
- **Assign Issues/Tasks/Subtasks**: Allocate to Developers or teams across multiple projects.
- **Set Priority & Deadlines**: Define urgency levels and deadlines.
- **Add Labels/Tags**: Use customizable labels for filtering.
- **Move Issues Between Columns**: Update status via drag-and-drop.
- **Edit/Reassign Issues/Tasks/Subtasks**: Modify details or reassign ownership.
- **Close/Delete Issues/Tasks/Subtasks**: Mark as done or remove.
- **Issue History/Activity Log**: Track all updates and actions.
- **Attach Files**: Upload supporting files (e.g., mockups, reports).
- **Add Subtasks**: Break issues into smaller units.

#### 📊 Reporting & Analytics
- **Dashboard View**: Access a high-level overview of issue distribution and progress across projects.
- **Track Developer Performance**: Monitor issue completion and missed deadlines.
- **Burn-down Charts / Velocity Graphs**: Visualize project progress (optional).
- **Issue Filtering**: Filter issues by assignee, status, tags, or priority.
- **Export Reports**: Generate CSV/PDF reports for meetings or analysis.

#### 💬 Collaboration & Communication
- **Comment on Any Issue**: Provide updates or feedback on issue cards.
- **Mention Users**: Notify specific users with `@username`.
- **Receive Notifications**: Get alerts for issue assignments or deadlines.
- **View Activity Logs**: Review all actions for transparency.

#### 🔐 Access & Permission Control
- **View All Projects & Issues**: Full visibility over all boards and issues across projects.
- **Override Permissions**: Access private issues if needed (optional).
- **Change User Roles**: Promote or demote users within the project.

#### ⚙️ Optional Admin-Level Controls
- **Create Project Templates**: Set predefined workflows for efficiency.
- **Manage Labels, Priorities Globally**: Define consistent taxonomies.
- **Automation Rules**: Create triggers (e.g., auto-close after inactivity).
- **Toggle Notifications Settings**: Enable/disable email or in-app alerts.

### 👨‍💻 Developer Role Features

#### 📁 Project and Subproject Access
- **View Assigned Projects/Subprojects**: Access all projects/subprojects they are part of.
- **View Boards**: Use project boards (Scrum or Kanban) in read/write mode.
- **View Project/Subproject Details**: See descriptions, deadlines, and team members.

#### 📝 Issue, Task, and Subtask Management
- **Create Issues/Tasks/Subtasks**: Create new items within assigned projects.
- **Edit Issues/Tasks/Subtasks**: Update details of assigned items (e.g., labels, estimates).
- **Assign to Self**: Self-assign unassigned issues/tasks/subtasks.
- **Update Status**: Move items between columns (e.g., To Do → Done).
- **Add Subtasks**: Break down issues into smaller units.
- **Attach Files**: Upload attachments (e.g., logs, screenshots).
- **Log Work**: Record time spent on issues.
- **View Issue History**: Access the activity log for assigned items.
- **Add Viewers**: Assign Viewers to specific issues.

#### 💬 Collaboration & Communication
- **Comment on Issues**: Share updates or questions on involved items.
- **Mention Team Members**: Notify colleagues with `@username`.
- **Receive Mentions**: Get notified when tagged.
- **View All Comments**: Read all communications on assigned projects.

#### 📊 Reporting & Tracking
- **View My Issues**: See a list of assigned issues/tasks/subtasks.
- **Filter Issues**: Search and filter by status, label, priority, or assignee.
- **View Progress**: Access read-only sprint burndown charts or dashboards.
- **View Sprint Backlog**: Review upcoming work items.

#### 🔔 Notifications
- **Issue Updates**: Receive alerts for assignments, status changes, and comments.
- **Due Date Reminders**: Get warnings for approaching deadlines.

### 👤 Client Role Features

#### 👀 Project and Board Access
- **View Assigned Boards/Projects**: Access only boards/projects assigned by Managers or Admins.
- **View Project Details**: See title, description, team, and deadlines for assigned projects.
- **View Boards**: View Kanban board layout and public tasks for assigned projects.
- **View Public Boards/Projects/Components**: Access publicly available data.

#### ✅ Issue Viewing & Feedback
- **View Issues/Tasks/Subtasks**: Read visible items (title, description, status, etc.) within assigned boards.
- **Comment on Issues**: Provide feedback or questions on accessible items.
- **Mention Developers or Managers**: Tag team members with `@username`.
- **Attach Files in Comments**: Upload files (e.g., requirements) optionally.
- **View Subtasks**: See breakdowns if visible.
- **Filter Issues**: Use filters by status, assignee, or label (optional).

#### 📊 Progress Tracking
- **View Issue Status**: See items in To Do, In Progress, or Done within assigned boards.
- **Progress Summary View**: Access a summary of issue completion status.
- **View Timelines or Milestones**: View Gantt charts or milestones (if enabled) for assigned boards.

#### 🔔 Notifications & Communication
- **Receive Notifications**: Get alerts when tagged, issues update, or milestones are achieved within assigned boards.
- **Email Notifications**: Optional email updates.
- **Activity Feed**: View a read-only log of project activity for assigned boards.

### 👀 Viewer Role Features
- **View Assigned Issues**: Access only issues assigned by Developers.
- **View Public Boards/Projects/Components**: Access publicly available data.
- **View Issue Status**: See status of assigned issues.
- **View Timelines**: View Gantt charts or milestones if enabled and public.

---

## 🔐 3. Permissions and Restrictions

| Feature                        | Admin   | Manager  | Developer | Client  | Viewer  |
|--------------------------------|---------|----------|-----------|---------|---------|
| Integration with External Tools| ✅ (manage) | ✅        | ✅ (read-only) | ❌      | ❌      |
| Advanced Search and Query Language | ✅       | ✅        | ✅         | ✅ (assigned only) | ✅ (assigned only) |
| Customizable Dashboard Widgets | ✅       | ✅        | ✅         | ✅ (assigned only) | ✅ (assigned only) |
| Task Dependencies and Gantt Charts | ✅       | ✅        | ✅ (view-only) | ✅ (view-only, assigned) | ✅ (view-only, assigned) |
| Audit Trail and Compliance     | ✅ (manage) | ✅ (manage) | ✅ (view)  | ❌      | ❌      |
| Multi-Language Support         | ✅       | ✅        | ✅         | ✅      | ✅      |
| Custom Workflows and State Machines | ✅       | ✅        | ❌         | ❌      | ❌      |
| Epics and Roadmap Planning     | ✅       | ✅        | ✅ (view-only) | ✅ (view-only, assigned) | ✅ (view-only, public) |
| Backup and Restore             | ✅       | ✅        | ❌         | ❌      | ❌      |
| Public API for Extensibility   | ✅ (manage) | ✅ (manage) | ❌         | ❌      | ❌      |
| User Onboarding and Training   | ✅ (manage) | ✅ (manage) | ✅ (access) | ✅ (access) | ✅ (access, public only) |
| Task Notifications Customization | ✅       | ✅        | ✅         | ✅      | ❌      |
| Real-Time Collaboration        | ✅       | ✅        | ✅         | ✅ (comments only) | ❌      |
| Data Import/Export             | ✅       | ✅        | ❌         | ❌      | ❌      |
| User Activity Reports          | ✅       | ✅        | ❌         | ❌      | ❌      |
| Issue Linking                  | ✅       | ✅        | ✅         | ❌      | ❌      |
| Workflow Conditions and Validators | ✅       | ✅        | ❌         | ❌      | ❌      |
| Sprints and Agile Boards       | ✅       | ✅        | ✅ (manage sprints) | ❌      | ❌      |
| Jira Service Management (Help Desk) | ✅       | ✅        | ❌         | ✅ (submit requests) | ❌      |
| Custom Dashboards and Gadgets  | ✅       | ✅        | ✅         | ✅ (assigned only) | ✅ (assigned only) |
| Time Tracking Reports          | ✅       | ✅        | ✅ (own issues) | ❌      | ❌      |
| Collaborative Whiteboard Integration | ✅       | ✅        | ✅         | ✅ (view only) | ❌      |
| Automated Issue Suggestions    | ✅       | ✅        | ✅         | ❌      | ❌      |
| Project Health Score           | ✅       | ✅        | ✅ (view-only) | ✅ (view-only, assigned) | ✅ (view-only, public) |
| Guest Access Tokens            | ✅       | ✅        | ❌         | ❌      | ❌      |
| Schema Planning                | ✅       | ✅        | ❌         | ❌      | ❌      |
| Workflow Maker                 | ✅       | ✅        | ❌         | ❌      | ❌      |
| Create Projects                | ✅       | ✅        | ❌         | ❌      | ❌      |
| Edit Project Details           | ✅       | ✅        | ❌         | ❌      | ❌      |
| Delete Projects                | ✅       | ✅        | ❌         | ❌      | ❌      |
| Create/Delete Boards           | ✅       | ✅        | ❌         | ❌      | ❌      |
| Define Board Columns           | ✅       | ✅        | ❌         | ❌      | ❌      |
| Invite Users                   | ✅       | ✅        | ❌         | ❌      | ❌      |
| Assign Roles                   | ✅       | ✅        | ❌         | ❌      | ❌      |
| Remove Users                   | ✅       | ✅        | ❌         | ❌      | ❌      |
| View Team Member Profiles      | ✅       | ✅        | ❌         | ❌      | ❌      |
| Create Issues/Tasks/Subtasks   | ✅       | ✅        | ✅ (own projects) | ❌      | ❌      |
| Assign Issues/Tasks/Subtasks   | ✅       | ✅        | ❌         | ❌      | ❌      |
| Set Priority & Deadlines       | ✅       | ✅        | ❌         | ❌      | ❌      |
| Add Labels/Tags                | ✅       | ✅        | ✅         | ❌      | ❌      |
| Move Issues Between Columns    | ✅       | ✅        | ✅         | ✅ (assigned only) | ❌      |
| Edit/Reassign Issues/Tasks/Subtasks | ✅       | ✅        | ✅ (own items) | ❌      | ❌      |
| Close/Delete Issues/Tasks/Subtasks | ✅       | ✅        | ❌         | ❌      | ❌      |
| Issue History/Activity Log     | ✅       | ✅        | ✅         | ✅ (assigned only) | ✅ (assigned only) |
| Attach Files                   | ✅       | ✅        | ✅         | ✅ (comments only) | ❌      |
| Add Subtasks                   | ✅       | ✅        | ✅         | ✅ (view only) | ❌      |
| Dashboard View                 | ✅       | ✅        | ✅ (read-only) | ✅ (assigned only) | ✅ (assigned only) |
| Track Developer Performance    | ✅       | ✅        | ❌         | ❌      | ❌      |
| Burn-down Charts / Velocity Graphs | ✅       | ✅        | ✅ (read-only) | ✅ (read-only, assigned) | ✅ (read-only, public) |
| Issue Filtering                | ✅       | ✅        | ✅         | ✅ (assigned only) | ✅ (assigned only) |
| Export Reports                 | ✅       | ✅        | ❌         | ❌      | ❌      |
| Comment on Any Issue           | ✅       | ✅        | ✅         | ✅ (assigned only) | ❌      |
| Mention Users                  | ✅       | ✅        | ✅         | ✅ (assigned only) | ❌      |
| Receive Notifications          | ✅       | ✅        | ✅         | ✅      | ❌      |
| View Activity Logs             | ✅       | ✅        | ✅         | ✅ (read-only, assigned) | ❌      |
| View All Projects & Issues     | ✅       | ✅        | ❌         | ❌      | ❌      |
| Override Permissions           | ✅       | ✅        | ❌         | ❌      | ❌      |
| Change User Roles              | ✅       | ✅        | ❌         | ❌      | ❌      |
| Create Project Templates       | ✅       | ✅        | ❌         | ❌      | ❌      |
| Manage Labels, Priorities Globally | ✅       | ✅        | ❌         | ❌      | ❌      |
| Automation Rules               | ✅       | ✅        | ❌         | ❌      | ❌      |
| Toggle Notifications Settings  | ✅       | ✅        | ✅         | ✅      | ❌      |
| View Assigned Projects/Subprojects | ✅       | ✅        | ✅         | ✅ (assigned only) | ❌      |
| View Project/Subproject Details| ✅       | ✅        | ✅         | ✅ (assigned only) | ❌      |
| View Boards                    | ✅       | ✅        | ✅         | ✅ (assigned only) | ✅ (public only) |

- **Notes**: 
  - **Admin**: Has unrestricted access to manage the system, including all projects and assignments.
  - **Manager**: Full control over multiple projects/subprojects, assigns Clients/Viewers.
  - **Developer**: Manages issues within assigned projects, adds Viewers to issues.
  - **Client**: Limited to assigned boards/projects, plus public data.
  - **Viewer**: Restricted to assigned issues, plus public boards/projects/components.
  - "✅ (assigned only)" indicates access is limited to explicitly assigned items.
  - "✅ (public only)" indicates access to publicly visible data.
  - "✅ (own projects/items)" indicates control over issues within their assigned scope.
  - "✅ (manage sprints)" indicates Developer control over sprint planning.
  - "✅ (submit requests)" indicates Client ability to log help desk requests.

---

## ⚙️ 4. Non-Functional Requirements
- **Performance**: Search, widget, and sprint updates within 2 seconds for 500 users.
- **Scalability**: Handle 5,000 issues/tasks/subtasks per project/subproject without lag.
- **Usability**: New features should require <5-minute onboarding with tooltips.
- **Reliability**: 99.5% uptime with backups every 24 hours.
- **Error Handling and Recovery**: Provide user-friendly error messages and recovery options for failed operations (e.g., backups, sync issues).
- **Performance Monitoring**: Include a dashboard for Admins to monitor response times and active users.

---

## 🔐 5. Security Considerations
- **API Security**: Use OAuth 2.0 with rate limiting for API access.
- **Data Privacy**: Encrypt backup files, audit logs, imported/exported data, and whiteboard sessions.
- **Access Control**: Limit workflow, backup, import/export, schema planning, and workflow maker to Admins and Managers; restrict Viewer/Client access to assigned data.
- **Compliance**: Ensure audit trails meet basic regulatory standards (e.g., GDPR).
- **Role-Based Access Control**: Enforce strict boundaries for Developers (assigned issues), Clients (assigned boards), and Viewers (assigned issues).
- **Issue Visibility**: Verify issue visibility (public, assigned, or private) before rendering.
- **Guest Access Security**: Enforce expiration and usage limits on guest tokens.