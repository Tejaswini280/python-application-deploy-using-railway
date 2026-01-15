"""
Database Seeding Script
This script safely seeds the database with initial data
It checks for existing data to avoid duplicates
"""

from app import app, db
from functions.models import Todo
from datetime import datetime, timedelta

def seed_database():
    """
    Seed the database with sample todo items
    Only runs if the database is empty (no todos exist)
    """
    with app.app_context():
        # Check if data already exists
        existing_count = Todo.query.count()
        
        if existing_count > 0:
            print(f"✅ Database already has {existing_count} todo(s). Skipping seeding.")
            return
        
        print("🌱 Seeding database with sample data...")
        
        # Sample todo items
        sample_todos = [
            {
                'Title': 'Welcome to Your Todo App',
                'Description': 'This is a sample todo item. Feel free to edit or delete it!',
                'DueDate': datetime.now().date() + timedelta(days=7)
            },
            {
                'Title': 'Learn Flask-SQLAlchemy',
                'Description': 'Understand how ORM works and database migrations',
                'DueDate': datetime.now().date() + timedelta(days=14)
            },
            {
                'Title': 'Deploy to Railway',
                'Description': 'Successfully deploy this app to Railway platform',
                'DueDate': datetime.now().date() + timedelta(days=3)
            }
        ]
        
        # Add sample todos to database
        for todo_data in sample_todos:
            todo = Todo(**todo_data)
            db.session.add(todo)
        
        # Commit all changes
        db.session.commit()
        
        print(f"✅ Successfully seeded {len(sample_todos)} todo items!")

if __name__ == '__main__':
    seed_database()
