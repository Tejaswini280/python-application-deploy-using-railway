"""
Database Seeding Script
This script safely seeds the database with initial data
It checks for existing data to avoid duplicates and uses database-level locking
"""

from app import app, db
from functions.models import Todo
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

def seed_database():
    """
    Seed the database with sample todo items
    Only runs if the database is empty (no todos exist)
    Uses advisory lock to prevent race conditions in multi-worker environments
    """
    with app.app_context():
        try:
            # Use PostgreSQL advisory lock to prevent concurrent seeding
            # Lock ID: 123456 (arbitrary number for this seeding operation)
            lock_acquired = db.session.execute(
                text("SELECT pg_try_advisory_lock(123456)")
            ).scalar()
            
            if not lock_acquired:
                print("⏳ Another process is seeding the database. Skipping.")
                return
            
            try:
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
                
            finally:
                # Always release the advisory lock
                db.session.execute(text("SELECT pg_advisory_unlock(123456)"))
                
        except IntegrityError as e:
            db.session.rollback()
            print(f"⚠️ Seeding skipped - data may already exist: {e}")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during seeding: {e}")

if __name__ == '__main__':
    seed_database()
