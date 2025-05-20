from app import create_app, db
from app.models.user import User
from app.models.project import Project

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Seed users
    users = [
        User(username='john', email='john@example.com'),
        User(username='jane', email='jane@example.com'),
        User(username='bob', email='bob@example.com')
    ]
    db.session.add_all(users)

    # Seed projects
    projects = [
        Project(name='Website Redesign', description='Redesign company website'),
        Project(name='Mobile App', description='Develop mobile application'),
        Project(name='Data Migration', description='Migrate legacy data')
    ]
    db.session.add_all(projects)

    db.session.commit()
    print("Database seeded successfully!")