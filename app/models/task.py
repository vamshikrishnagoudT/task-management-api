from app import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    dependencies = db.relationship(
        'Task',
        secondary='task_dependencies',
        primaryjoin='Task.id==task_dependencies.c.task_id',
        secondaryjoin='Task.id==task_dependencies.c.depends_on_id',
        backref='dependent_tasks',
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'dependencies': [dep.id for dep in self.dependencies]
        }

    def has_circular_dependency(self, depends_on_id, new_task_id=None, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = set()
        if new_task_id and depends_on_id == new_task_id:
            return True
        if depends_on_id in visited:
            return False
        if depends_on_id in path:
            return True
        path.add(depends_on_id)
        task = Task.query.get(depends_on_id)
        if task:
            for dep in task.dependencies:
                if self.has_circular_dependency(dep.id, new_task_id, visited, path):
                    return True
        path.remove(depends_on_id)
        visited.add(depends_on_id)
        return False

    def are_dependencies_completed(self):
        return all(dep.status == 'completed' for dep in self.dependencies)