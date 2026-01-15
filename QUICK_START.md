# ⚡ Quick Start Guide

## 🏠 Local Development (First Time)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up database (PostgreSQL must be running)
# Edit .env with your database credentials

# 3. Initialize migrations (ONCE only)
flask db init

# 4. Create and apply initial migration
flask db migrate -m "Initial migration"
flask db upgrade

# 5. Seed database with sample data
python seed_db.py

# 6. Run the app
python app.py
```

Visit: http://localhost:5000

---

## 🐳 Docker Development

```bash
# Start everything (database + app)
docker-compose up --build

# Stop
docker-compose down
```

Visit: http://localhost:5000

---

## 🚂 Railway Deployment (3 Steps)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Railway"
git push origin main
```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repository
4. Add PostgreSQL database (+ New → Database → PostgreSQL)

### Step 3: Generate Domain
1. Go to Settings
2. Click "Generate Domain"
3. Visit your URL!

**That's it!** Railway automatically:
- Runs migrations
- Seeds database
- Starts with Gunicorn

---

## 🔄 After Changing Models

```bash
# 1. Create migration
flask db migrate -m "Describe your changes"

# 2. Apply migration
flask db upgrade

# 3. Commit and push (Railway auto-deploys)
git add .
git commit -m "Update models"
git push
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Could not locate Flask application" | Run `flask db init` |
| "Can't locate revision" | Commit `migrations/` folder to git |
| "No module named flask_sqlalchemy" | Run `pip install -r requirements.txt` |
| Railway deployment fails | Check logs in Railway dashboard |
| Database connection error | Verify `DATABASE_URL` in Railway |

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `functions/models.py` | Database models (Todo table) |
| `seed_db.py` | Database seeding script |
| `start.sh` | Railway startup script |
| `Dockerfile` | Docker configuration |
| `requirements.txt` | Python dependencies |
| `migrations/` | Database migration files (commit to git!) |

---

## 🎯 Key Commands

```bash
# Migrations
flask db init              # Initialize (once)
flask db migrate -m "msg"  # Create migration
flask db upgrade           # Apply migrations
flask db downgrade         # Undo last migration

# Database
python seed_db.py          # Seed database

# Run App
python app.py              # Development
gunicorn app:app           # Production

# Docker
docker-compose up          # Start
docker-compose down        # Stop
```

---

For detailed explanations, see `DEPLOYMENT_GUIDE.md`
