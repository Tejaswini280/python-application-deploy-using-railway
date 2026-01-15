import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            port=os.getenv("DB_PORT", "5432")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        
        # Check if database exists
        db_name = os.getenv("DB_NAME", "todoapp")
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {db_name}')
            print(f"✓ Database '{db_name}' created successfully!")
        else:
            print(f"✓ Database '{db_name}' already exists.")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False

if __name__ == "__main__":
    if create_database():
        print("✓ Database initialization complete!")
        # Now initialize the schema
        from functions.models import Schema
        Schema()
        print("✓ Tables created successfully!")
    else:
        print("✗ Database initialization failed!")
