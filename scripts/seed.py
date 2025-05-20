from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(username='john', email='john@example.com'),
        User(username='jane', email='jane@example.com'),
        User(username='bob', email='bob@example.com')
    ]
    for user in users:
        user.set_password('password123')
    db.session.add_all(users)

    projects = [
        Project(name='Website Redesign', description='Redesign company website'),
        Project(name='Mobile App', description='Develop mobile application'),
        Project(name='Data Migration', description='Migrate legacy data')
    ]
    db.session.add_all(projects)
    db.session.commit()

    tasks = [
        Task(title='Design Homepage', status='pending', project_id=1, user_id=1),
        Task(title='Implement Backend', status='in_progress', project_id=1, user_id=2),
        Task(title='Test Features', status='pending', project_id=1),
        Task(title='Deploy App', status='completed', project_id=1, user_id=1)
    ]
    db.session.add_all(tasks)
    db.session.commit()

    task3 = Task.query.get(3)
    task1 = Task.query.get(1)
    task3.dependencies.append(task1)
    db.session.commit()

    print("Database seeded successfully!")