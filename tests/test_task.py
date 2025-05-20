import unittest
from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username='test', email='test@example.com')
            user.set_password('test123')
            project = Project(name='Test Project')
            db.session.add_all([user, project])
            db.session.commit()
            self.user_id = user.id
            self.project_id = project.id

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_circular_dependency(self):
        with self.app.app_context():
            task1 = Task(title='Task 1', project_id=self.project_id)
            task2 = Task(title='Task 2', project_id=self.project_id)
            db.session.add_all([task1, task2])
            db.session.commit()
            task1.dependencies.append(task2)
            db.session.commit()
            self.assertTrue(task2.has_circular_dependency(task1.id, task1.id))

    def test_dependency_completion(self):
        with self.app.app_context():
            task1 = Task(title='Task 1', project_id=self.project_id, status='pending')
            task2 = Task(title='Task 2', project_id=self.project_id, status='pending')
            db.session.add_all([task1, task2])
            db.session.commit()
            task2.dependencies.append(task1)
            self.assertFalse(task2.are_dependencies_completed())
            task1.status = 'completed'
            db.session.commit()
            self.assertTrue(task2.are_dependencies_completed())

    def test_user_deletion_with_active_tasks(self):
        with self.app.app_context():
            task = Task(title='Task', project_id=self.project_id, user_id=self.user_id, status='pending')
            db.session.add(task)
            db.session.commit()
            response = self.client.delete(f'/api/users/{self.user_id}', headers={'Authorization': f'Bearer {self.get_token()}'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json['error'], 'Cannot delete user with pending or in-progress tasks')

    def get_token(self):
        response = self.client.post('/api/auth/login', json={'email': 'test@example.com', 'password': 'test123'})
        return response.json['token']

if __name__ == '__main__':
    unittest.main()