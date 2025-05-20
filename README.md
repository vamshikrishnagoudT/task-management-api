Task Management API
A RESTful API for managing users, projects, and tasks using Flask and PostgreSQL, built for Briskcovey Technologies Pvt. Ltd.
Features

Users: Create, list (paginated), retrieve, and delete users (with constraints for active tasks).
Projects: Create, list (paginated), retrieve, and list project tasks (paginated).
Tasks: Create (with dependency validation), retrieve, update status (with dependency checks), and list by user/status (paginated).
Authentication: JWT-based authentication for protected endpoints.
Constraints: Prevents circular task dependencies, ensures dependencies are completed before task completion, and blocks user deletion if assigned to pending/in-progress tasks.
Testing: Unit tests for critical logic and comprehensive Postman tests.

Setup Instructions

Clone the Repository:
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api


Set Up Virtual Environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Set Up PostgreSQL:
sudo -u postgres psql

CREATE DATABASE task_management;
CREATE USER task_user WITH PASSWORD 'password123';
ALTER ROLE task_user SET client_encoding TO 'utf8';
ALTER ROLE task_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE task_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE task_management TO task_user;
\q


Create .env File:
touch .env

Add:
DATABASE_URL=postgresql://task_user:password123@localhost:5432/task_management
SECRET_KEY=your-secret-key


Seed the Database:
python -m scripts.seed


Run the Application:
python run.py


Run Unit Tests:
pytest tests/test_task.py


Test with Postman:

Import TaskManagementAPI.postman_collection.json and TaskManagementAPI_Dev.postman_environment.json into Postman.
Set environment to TaskManagementAPI_Dev.
Run Login User (POST /api/auth/login) to get a JWT token.
Test endpoints with Authorization: Bearer {{token}} for protected routes.
Use collection runner to automate testing.
Endpoints:
Auth: POST /api/auth/login
Users: POST /api/users, GET /api/users?page=1&per_page=10, GET /api/users/<id>, DELETE /api/users/<id>
Projects: POST /api/projects, GET /api/projects?page=1&per_page=10, GET /api/projects/<id>, GET /api/projects/<id>/tasks?page=1&per_page=10
Tasks: POST /api/tasks, GET /api/tasks/<id>, PUT /api/tasks/<id>/status, GET /api/tasks/user/<user_id>?page=1&per_page=10, GET /api/tasks/status/<status>?page=1&per_page=10





Sprint Status

User endpoints with input validation.
Project endpoints and seed script.
Task endpoints with dependency logic.
JWT authentication, pagination, unit tests, user deletion constraint.

Submission

Repository: https://github.com/yourusername/task-management-api
Postman Files: TaskManagementAPI.postman_collection.json, TaskManagementAPI_Dev.postman_environment.json
Testing: All endpoints tested via Postman, unit tests pass.

