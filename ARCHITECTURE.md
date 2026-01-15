# 🏗️ Application Architecture

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Web Browser)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAILWAY PLATFORM                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Flask Application                     │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │              Gunicorn Server                     │  │  │
│  │  │  (2 workers × 4 threads = 8 concurrent requests)│  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │              Flask App (app.py)                  │  │  │
│  │  │  - Routes                                        │  │  │
│  │  │  - Request handling                              │  │  │
│  │  │  - Template rendering                            │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         SQLAlchemy ORM Layer                     │  │  │
│  │  │  - Models (Todo)                                 │  │  │
│  │  │  - Database operations                           │  │  │
│  │  │  - Query building                                │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │                                   │
│                          │ DATABASE_URL                      │
│                          ▼                                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │            PostgreSQL Database                        │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │              Todo Table                          │  │  │
│  │  │  - id (Primary Key)                              │  │  │
│  │  │  - Title                                         │  │  │
│  │  │  - Description                                   │  │  │
│  │  │  - _is_deleted                                   │  │  │
│  │  │  - CreatedOn                                     │  │  │
│  │  │  - DueDate                                       │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow

### 1. User Creates a Todo

```
User fills form
    ↓
Clicks "Add Todo"
    ↓
Browser sends POST /insert
    ↓
Railway receives request
    ↓
Gunicorn worker picks up request
    ↓
Flask routes to insert() function
    ↓
ToDoModel().sql_edit_insert() called
    ↓
SQLAlchemy creates Todo object
    ↓
db.session.add(todo)
    ↓
db.session.commit()
    ↓
SQL INSERT executed on PostgreSQL
    ↓
Redirect to homepage
    ↓
Browser shows updated todo list
```

### 2. User Views Todos

```
User visits homepage
    ↓
Browser sends GET /
    ↓
Railway receives request
    ↓
Gunicorn worker picks up request
    ↓
Flask routes to sql_database() function
    ↓
ToDoModel().list_items() called
    ↓
SQLAlchemy queries: Todo.query.filter_by(_is_deleted=False)
    ↓
SQL SELECT executed on PostgreSQL
    ↓
Results converted to dictionaries
    ↓
Template rendered with data
    ↓
HTML sent to browser
    ↓
User sees todo list
```

---

## 🚀 Deployment Flow

### Initial Deployment

```
Developer pushes to GitHub
    ↓
Railway detects new commit
    ↓
Railway starts build process
    ↓
┌─────────────────────────────────┐
│     Build Phase                 │
│  1. Pull code from GitHub       │
│  2. Read Dockerfile             │
│  3. Build Docker image          │
│  4. Install dependencies        │
│  5. Copy application files      │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│     Deploy Phase                │
│  1. Start container             │
│  2. Execute start.sh            │
│  3. Run flask db upgrade        │
│  4. Run python seed_db.py       │
│  5. Start gunicorn              │
└─────────────────────────────────┘
    ↓
App is live!
```

### Subsequent Deployments

```
Developer makes changes
    ↓
Creates migration (if models changed)
    ↓
Commits to git
    ↓
Pushes to GitHub
    ↓
Railway auto-detects push
    ↓
Rebuilds and redeploys
    ↓
Migrations run automatically
    ↓
App updated with zero downtime
```

---

## 🗄️ Database Migration Flow

### Creating a Migration

```
Developer changes models.py
    ↓
Runs: flask db migrate -m "Add priority column"
    ↓
Flask-Migrate compares:
  - Current database schema
  - New model definitions
    ↓
Generates migration file in migrations/versions/
    ↓
Migration file contains:
  - upgrade() function (apply changes)
  - downgrade() function (undo changes)
    ↓
Developer commits migration file to git
```

### Applying a Migration

```
flask db upgrade command
    ↓
Flask-Migrate checks current database version
    ↓
Finds unapplied migrations
    ↓
Executes upgrade() functions in order
    ↓
Updates alembic_version table
    ↓
Database schema is now up to date
```

---

## 🌱 Database Seeding Flow

```
python seed_db.py executed
    ↓
Script creates Flask app context
    ↓
Checks: Todo.query.count()
    ↓
┌─────────────────────────────────┐
│  If count > 0:                  │
│    Print "Data exists"          │
│    Exit (no seeding)            │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  If count == 0:                 │
│    Loop through sample_todos    │
│    Create Todo objects          │
│    Add to session               │
│    Commit all at once           │
│    Print success message        │
└─────────────────────────────────┘
```

---

## 🐳 Docker Architecture

### Local Development (docker-compose)

```
┌─────────────────────────────────────────────┐
│           Docker Compose                    │
│  ┌───────────────────────────────────────┐  │
│  │     db service (PostgreSQL)           │  │
│  │  - Port: 5432                         │  │
│  │  - Volume: postgres_data              │  │
│  │  - Health check enabled               │  │
│  └───────────────────────────────────────┘  │
│                    ▲                         │
│                    │                         │
│                    │ DB connection           │
│                    │                         │
│  ┌───────────────────────────────────────┐  │
│  │     web service (Flask)               │  │
│  │  - Port: 5000                         │  │
│  │  - Depends on: db                     │  │
│  │  - Volume: . (live code reload)       │  │
│  │  - Runs: start.sh                     │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Railway Deployment

```
┌─────────────────────────────────────────────┐
│           Railway Project                   │
│  ┌───────────────────────────────────────┐  │
│  │     PostgreSQL Service                │  │
│  │  - Managed by Railway                 │  │
│  │  - Automatic backups                  │  │
│  │  - Provides DATABASE_URL              │  │
│  └───────────────────────────────────────┘  │
│                    ▲                         │
│                    │                         │
│                    │ DATABASE_URL            │
│                    │                         │
│  ┌───────────────────────────────────────┐  │
│  │     Web Service (Flask)               │  │
│  │  - Built from Dockerfile              │  │
│  │  - Auto-assigned PORT                 │  │
│  │  - Runs: start.sh                     │  │
│  │  - Public domain                      │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 📦 Application Layers

### Layer 1: Presentation (Frontend)

```
┌─────────────────────────────────┐
│      templates/todo.html        │
│  - HTML structure               │
│  - Bootstrap styling            │
│  - Forms for CRUD operations    │
│  - Jinja2 templating            │
└─────────────────────────────────┘
```

### Layer 2: Application (Backend)

```
┌─────────────────────────────────┐
│          app.py                 │
│  - Route definitions            │
│  - Request handling             │
│  - Response generation          │
│  - Template rendering           │
│  - Error handling               │
└─────────────────────────────────┘
```

### Layer 3: Business Logic

```
┌─────────────────────────────────┐
│    functions/models.py          │
│  - ToDoModel class              │
│  - CRUD operations              │
│  - Data validation              │
│  - Business rules               │
└─────────────────────────────────┘
```

### Layer 4: Data Access (ORM)

```
┌─────────────────────────────────┐
│      SQLAlchemy ORM             │
│  - Todo model definition        │
│  - Query building               │
│  - SQL generation               │
│  - Connection management        │
└─────────────────────────────────┘
```

### Layer 5: Database

```
┌─────────────────────────────────┐
│      PostgreSQL                 │
│  - Data storage                 │
│  - ACID transactions            │
│  - Indexing                     │
│  - Constraints                  │
└─────────────────────────────────┘
```

---

## 🔐 Security Architecture

### Environment Variables

```
Local Development:
  .env file (not in git)
    ↓
  python-dotenv loads variables
    ↓
  os.getenv() reads values

Railway Production:
  Railway dashboard
    ↓
  Environment variables set
    ↓
  Automatically injected into container
    ↓
  os.getenv() reads values
```

### Database Connection Security

```
Local:
  Individual credentials (DB_HOST, DB_USER, etc.)
    ↓
  Built into connection string
    ↓
  PostgreSQL authentication

Railway:
  DATABASE_URL provided by Railway
    ↓
  Contains: postgres://user:pass@host:port/db
    ↓
  Converted to: postgresql://user:pass@host:port/db
    ↓
  SSL connection (automatic)
```

---

## 🔄 Data Flow Diagram

### Create Todo

```
User Input
    ↓
HTML Form (POST /insert)
    ↓
Flask Route (insert())
    ↓
ToDoModel.sql_edit_insert()
    ↓
SQLAlchemy (Todo object)
    ↓
db.session.add()
    ↓
db.session.commit()
    ↓
PostgreSQL (INSERT)
    ↓
Redirect to /
    ↓
Display updated list
```

### Read Todos

```
User Request (GET /)
    ↓
Flask Route (sql_database())
    ↓
ToDoModel.list_items()
    ↓
SQLAlchemy Query
    ↓
PostgreSQL (SELECT)
    ↓
Convert to dictionaries
    ↓
Render template
    ↓
HTML Response
    ↓
Display in browser
```

### Update Todo

```
User clicks Edit
    ↓
GET /query_edit?ID=5
    ↓
Load todo data
    ↓
Display in form
    ↓
User submits changes
    ↓
POST /edit
    ↓
ToDoModel.sql_edit()
    ↓
SQLAlchemy (UPDATE)
    ↓
PostgreSQL (UPDATE)
    ↓
Redirect to /
    ↓
Display updated list
```

### Delete Todo (Soft Delete)

```
User clicks Delete
    ↓
GET /delete?ID=5
    ↓
ToDoModel.sql_delete()
    ↓
Set _is_deleted = True
    ↓
SQLAlchemy (UPDATE)
    ↓
PostgreSQL (UPDATE)
    ↓
Redirect to /
    ↓
Todo hidden from list
```

---

## 🚀 Startup Sequence

### Local Development

```
1. docker-compose up
2. Start PostgreSQL container
3. Wait for health check
4. Start Flask container
5. Execute start.sh:
   - flask db upgrade
   - python seed_db.py
   - python app.py
6. Flask dev server starts
7. App available at localhost:5000
```

### Railway Production

```
1. Railway receives deployment trigger
2. Build Docker image
3. Start container
4. Execute start.sh:
   - flask db upgrade (apply migrations)
   - python seed_db.py (seed if empty)
   - gunicorn app:app (start server)
5. Health check passes
6. Traffic routed to new deployment
7. Old deployment terminated
8. App available at Railway domain
```

---

## 📊 Technology Stack

```
┌─────────────────────────────────────────────┐
│              Frontend                       │
│  - HTML5                                    │
│  - Bootstrap 5                              │
│  - Jinja2 Templates                         │
└─────────────────────────────────────────────┘
                    ▲
                    │
┌─────────────────────────────────────────────┐
│              Backend                        │
│  - Python 3.11                              │
│  - Flask 2.3.3                              │
│  - Flask-SQLAlchemy 3.0.5                   │
│  - Flask-Migrate 4.0.5                      │
└─────────────────────────────────────────────┘
                    ▲
                    │
┌─────────────────────────────────────────────┐
│              Server                         │
│  - Gunicorn 21.2.0                          │
│  - 2 workers × 4 threads                    │
└─────────────────────────────────────────────┘
                    ▲
                    │
┌─────────────────────────────────────────────┐
│              Database                       │
│  - PostgreSQL 15                            │
│  - psycopg2-binary driver                   │
└─────────────────────────────────────────────┘
                    ▲
                    │
┌─────────────────────────────────────────────┐
│              Infrastructure                 │
│  - Docker                                   │
│  - Railway Platform                         │
└─────────────────────────────────────────────┘
```

---

## 🎯 Key Design Decisions

### 1. SQLAlchemy ORM vs Raw SQL

**Decision:** Use SQLAlchemy ORM

**Reasons:**
- Type safety
- Easier to maintain
- Database-agnostic
- Built-in migration support
- Less error-prone

### 2. Soft Delete vs Hard Delete

**Decision:** Soft delete (set _is_deleted = True)

**Reasons:**
- Data recovery possible
- Audit trail maintained
- Safer for production
- Can be purged later

### 3. Gunicorn vs Flask Dev Server

**Decision:** Gunicorn for production

**Reasons:**
- Production-ready
- Multi-worker support
- Better performance
- Industry standard

### 4. Environment Variables vs Config Files

**Decision:** Environment variables

**Reasons:**
- Railway compatibility
- Security (no secrets in code)
- Environment-specific config
- 12-factor app methodology

### 5. Automatic Migrations vs Manual

**Decision:** Automatic via start.sh

**Reasons:**
- Zero-downtime deployments
- No manual intervention
- Consistent across environments
- Reduces human error

---

This architecture provides a solid foundation for a production-ready Flask application with proper separation of concerns, security, and scalability.
