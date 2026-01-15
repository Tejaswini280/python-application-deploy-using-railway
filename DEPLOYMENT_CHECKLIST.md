# ✅ Railway Deployment Checklist

Use this checklist to ensure your app is ready for Railway deployment.

---

## 📋 Pre-Deployment Checklist

### 1. Code Preparation

- [ ] All changes saved and working locally
- [ ] No syntax errors in Python files
- [ ] All imports are correct
- [ ] No hardcoded passwords or secrets in code

### 2. Dependencies

- [ ] `requirements.txt` includes all packages:
  - [ ] Flask
  - [ ] Flask-SQLAlchemy
  - [ ] Flask-Migrate
  - [ ] psycopg2-binary
  - [ ] python-dotenv
  - [ ] gunicorn

### 3. Database Migrations

- [ ] `migrations/` folder exists
- [ ] Initial migration created: `flask db migrate -m "Initial migration"`
- [ ] Migration tested locally: `flask db upgrade`
- [ ] `migrations/` folder is committed to git (NOT in .gitignore)

### 4. Configuration Files

- [ ] `Dockerfile` exists and is correct
- [ ] `start.sh` exists and is executable
- [ ] `railway.json` exists (optional but recommended)
- [ ] `.env` is in `.gitignore` (NOT committed)
- [ ] `.env.example` exists (template for others)

### 5. Application Files

- [ ] `app.py` has DATABASE_URL support
- [ ] `app.py` converts `postgres://` to `postgresql://`
- [ ] `functions/models.py` uses SQLAlchemy models
- [ ] `seed_db.py` exists and checks for existing data

### 6. Git Repository

- [ ] All files committed to git
- [ ] `.env` is NOT in git (check with `git status`)
- [ ] `migrations/` IS in git
- [ ] Pushed to GitHub: `git push origin main`

### 7. Local Testing

- [ ] App runs locally: `python app.py`
- [ ] App runs with Docker: `docker-compose up`
- [ ] Migrations work: `flask db upgrade`
- [ ] Seeding works: `python seed_db.py`
- [ ] All CRUD operations work (Create, Read, Update, Delete)

---

## 🚂 Railway Deployment Steps

### Step 1: Railway Account Setup

- [ ] Created account at [railway.app](https://railway.app)
- [ ] Signed in with GitHub
- [ ] Authorized Railway to access repositories

### Step 2: Create Project

- [ ] Clicked "New Project"
- [ ] Selected "Deploy from GitHub repo"
- [ ] Chose correct repository
- [ ] Railway detected Dockerfile

### Step 3: Add Database

- [ ] Clicked "+ New" in project
- [ ] Selected "Database" → "PostgreSQL"
- [ ] Database created successfully
- [ ] `DATABASE_URL` variable appears automatically

### Step 4: Monitor Deployment

- [ ] Went to "Deployments" tab
- [ ] Clicked latest deployment
- [ ] Watched logs for:
  - [ ] "🚀 Starting Railway deployment..."
  - [ ] "📦 Running database migrations..."
  - [ ] "✅ Migrations completed successfully"
  - [ ] "🌱 Seeding database..."
  - [ ] "✅ Successfully seeded X todo items"
  - [ ] "🎯 Starting Gunicorn server..."

### Step 5: Generate Domain

- [ ] Went to "Settings" tab
- [ ] Scrolled to "Domains" section
- [ ] Clicked "Generate Domain"
- [ ] Received URL like: `your-app.up.railway.app`

### Step 6: Verify Deployment

- [ ] Visited generated domain
- [ ] App loads without errors
- [ ] Sample todos are visible
- [ ] Can create new todo
- [ ] Can edit existing todo
- [ ] Can delete todo

---

## 🔍 Post-Deployment Verification

### Functionality Tests

- [ ] Homepage loads (`/`)
- [ ] Health check works (`/hey`)
- [ ] Create todo works (`/insert`)
- [ ] Edit todo works (`/edit`)
- [ ] Delete todo works (`/delete`)
- [ ] No 500 errors in logs

### Database Tests

- [ ] Database has sample data
- [ ] New data persists after creation
- [ ] Edits save correctly
- [ ] Deletes work (soft delete)
- [ ] No duplicate data from seeding

### Performance Tests

- [ ] Page loads in < 3 seconds
- [ ] No timeout errors
- [ ] Multiple requests work
- [ ] App doesn't crash under load

---

## 🐛 Troubleshooting Checklist

If deployment fails, check:

### Build Failures

- [ ] Check Railway logs for specific error
- [ ] Verify Dockerfile syntax
- [ ] Ensure all files are in git
- [ ] Check requirements.txt for typos

### Migration Failures

- [ ] Verify `migrations/` folder is in git
- [ ] Check migration files for errors
- [ ] Ensure DATABASE_URL is set
- [ ] Check PostgreSQL is added to project

### Database Connection Failures

- [ ] PostgreSQL service is running
- [ ] DATABASE_URL exists in variables
- [ ] postgres:// converted to postgresql://
- [ ] No hardcoded database credentials

### Application Failures

- [ ] Check for Python syntax errors
- [ ] Verify all imports are correct
- [ ] Ensure PORT is not hardcoded
- [ ] Check Gunicorn is starting

### Seeding Issues

- [ ] Check seed_db.py for errors
- [ ] Verify database connection works
- [ ] Ensure models are correct
- [ ] Check for duplicate data

---

## 🔄 Redeployment Checklist

When making changes and redeploying:

### Code Changes

- [ ] Made changes locally
- [ ] Tested locally: `python app.py`
- [ ] Tested with Docker: `docker-compose up`
- [ ] All tests pass

### Database Changes

If you changed models:
- [ ] Created migration: `flask db migrate -m "Description"`
- [ ] Applied locally: `flask db upgrade`
- [ ] Verified migration works
- [ ] Committed migration files to git

### Git Workflow

- [ ] Committed changes: `git add .`
- [ ] Added commit message: `git commit -m "Description"`
- [ ] Pushed to GitHub: `git push origin main`
- [ ] Railway auto-deploys (watch logs)

### Verification

- [ ] Railway deployment succeeded
- [ ] Migrations ran automatically
- [ ] App still works
- [ ] New features work
- [ ] Old data preserved

---

## 📊 Environment Variables Reference

### Railway (Automatic)

These are set automatically by Railway:

| Variable | Set By | Purpose |
|----------|--------|---------|
| `DATABASE_URL` | Railway | PostgreSQL connection string |
| `PORT` | Railway | Application port |

### Optional Variables

You can add these in Railway → Settings → Variables:

| Variable | Value | Purpose |
|----------|-------|---------|
| `FLASK_ENV` | `production` | Flask environment |
| `FLASK_DEBUG` | `False` | Disable debug mode |

**Note:** Don't set `DB_HOST`, `DB_NAME`, etc. on Railway - use `DATABASE_URL` instead!

---

## 🎯 Success Indicators

Your deployment is successful when:

### ✅ Build Phase
- Docker image builds without errors
- All dependencies install correctly
- No syntax errors in code

### ✅ Migration Phase
- Migrations run without errors
- Database schema is up to date
- No migration conflicts

### ✅ Seeding Phase
- Sample data added (if database was empty)
- No duplicate data created
- Seeding completes successfully

### ✅ Runtime Phase
- Gunicorn starts successfully
- App responds to requests
- No crashes or errors
- All routes work

### ✅ User Experience
- Domain loads quickly
- UI displays correctly
- CRUD operations work
- No error messages

---

## 🆘 Emergency Procedures

### If Deployment Completely Fails

1. **Check Logs First:**
   - Railway → Deployments → Latest → Logs
   - Look for first error message

2. **Test Locally:**
   ```bash
   docker-compose up --build
   ```
   If local works but Railway doesn't, it's a config issue.

3. **Verify Git:**
   ```bash
   git status  # Check what's committed
   git log     # Check recent commits
   ```

4. **Redeploy:**
   - Railway → Deployments → Click "Redeploy"

### If Database is Corrupted

1. **Delete PostgreSQL Service:**
   - Railway → PostgreSQL → Settings → Delete

2. **Add New PostgreSQL:**
   - Railway → + New → Database → PostgreSQL

3. **Redeploy App:**
   - Railway auto-redeploys
   - Migrations run automatically
   - Database seeded fresh

### If App Won't Start

1. **Check Gunicorn:**
   - Look for "Starting Gunicorn" in logs
   - Verify start.sh is executable
   - Check app.py has `app = Flask(__name__)`

2. **Check Port:**
   - Ensure app binds to `0.0.0.0:$PORT`
   - Don't hardcode port 5000

3. **Check Dependencies:**
   - Verify requirements.txt is complete
   - Check for version conflicts

---

## 📞 Getting Help

If you're stuck:

1. **Check Documentation:**
   - [ ] Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - [ ] Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
   - [ ] Check [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)

2. **Gather Information:**
   - [ ] Copy error message from Railway logs
   - [ ] Note what you tried
   - [ ] Check which step failed

3. **Debug Systematically:**
   - [ ] Test locally first
   - [ ] Check one thing at a time
   - [ ] Read error messages carefully
   - [ ] Search error message online

---

## 🎉 Final Checklist

Before considering deployment complete:

- [ ] App is live on Railway domain
- [ ] All CRUD operations work
- [ ] Sample data is visible
- [ ] No errors in Railway logs
- [ ] Domain is bookmarked
- [ ] Shared with friends/team
- [ ] Documented any custom changes
- [ ] Celebrated success! 🎊

---

## 📝 Notes Section

Use this space to track your deployment:

**Deployment Date:** _______________

**Railway Domain:** _______________

**Issues Encountered:**
- 
- 
- 

**Solutions Applied:**
- 
- 
- 

**Custom Changes Made:**
- 
- 
- 

---

**Congratulations on deploying your Flask app to Railway!** 🚀

For future deployments, just:
1. Make changes
2. Commit to git
3. Push to GitHub
4. Railway auto-deploys!
