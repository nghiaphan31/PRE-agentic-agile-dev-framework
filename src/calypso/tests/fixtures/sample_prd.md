# Sample PRD — Agentic Task Manager (Test Fixture)

> **Note:** This is a test fixture for Calypso end-to-end tests.
> It is intentionally minimal to keep test costs low.

## Product Vision

Build a simple task manager that allows users to create, assign, and track tasks
within a team. The system must support real-time notifications and role-based access.

## Requirements

### REQ-1: Task Creation
Users can create tasks with a title, description, assignee, due date, and priority.

**Acceptance Criteria:**
- Task form validates all required fields
- Task is persisted to database on submission
- Creator receives confirmation notification

### REQ-2: Role-Based Access Control
Three roles: Admin, Manager, Developer. Each role has different permissions.

**Acceptance Criteria:**
- Admin can create/edit/delete any task
- Manager can create/edit tasks in their team
- Developer can only edit tasks assigned to them

### REQ-3: Real-Time Notifications
Users receive notifications when tasks are assigned or updated.

**Acceptance Criteria:**
- Notification delivered within 5 seconds of event
- Notification includes task title and action taken
- Users can configure notification preferences
