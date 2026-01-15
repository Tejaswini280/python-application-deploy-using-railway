from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy (will be configured in app.py)
db = SQLAlchemy()

# ---------------- Todo Model -----------------
class Todo(db.Model):
    __tablename__ = 'Todo'
    
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    _is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    CreatedOn = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    DueDate = db.Column(db.Date, nullable=True)
    
    def __repr__(self):
        return f'<Todo {self.id}: {self.Title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'Title': self.Title,
            'Description': self.Description,
            '_is_deleted': self._is_deleted,
            'CreatedOn': self.CreatedOn.isoformat() if self.CreatedOn else None,
            'DueDate': self.DueDate.isoformat() if self.DueDate else None
        }

# ---------------- ToDoModel (Backward Compatible) -----------------
class ToDoModel:
    def list_items(self, where_clause=""):
        query = Todo.query.filter_by(_is_deleted=False)
        if where_clause:
            if "id=" in where_clause:
                try:
                    todo_id = int(where_clause.split("id=")[1].strip())
                    query = query.filter_by(id=todo_id)
                except (ValueError, IndexError):
                    pass
        todos = query.all()
        return [todo.to_dict() for todo in todos]
    
    def sql_edit_insert(self, var):
        title, description, due_date = var
        parsed_date = None
        if due_date and due_date.strip():
            try:
                parsed_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            except ValueError:
                parsed_date = None
        new_todo = Todo(Title=title, Description=description, DueDate=parsed_date)
        db.session.add(new_todo)
        db.session.commit()
    
    def sql_delete(self, ID):
        todo = Todo.query.get(ID[0] if isinstance(ID, tuple) else ID)
        if todo:
            todo._is_deleted = True
            db.session.commit()
    
    def sql_edit(self, var):
        title, description, due_date, old_id = var
        parsed_date = None
        if due_date and due_date.strip():
            try:
                parsed_date = datetime.strptime(due_date, '%Y-%m-%d').date()
            except ValueError:
                parsed_date = None
        todo = Todo.query.get(old_id)
        if todo:
            todo.Title = title
            todo.Description = description
            todo.DueDate = parsed_date
            db.session.commit()
