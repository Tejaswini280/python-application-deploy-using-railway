# CI/CD Workflows

This directory contains GitHub Actions workflows for automated testing and deployment.

## Workflows

### 1. CI Pipeline (`ci.yml`)
**Triggers:** Pull requests and pushes to `dev` and `main` branches

**Jobs:**
- **Lint and Test**: Runs code quality checks, linting, and tests
- **Security Scan**: Scans for security vulnerabilities using Trivy

### 2. Deploy to Staging (`staging.yml`)
**Triggers:** Pushes to `dev` branch

**Environment:** staging

**Steps:**
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Run tests
5. Deploy to Railway staging environment

### 3. Deploy to Production (`production.yml`)
**Triggers:** Pushes to `main` branch

**Environment:** production

**Steps:**
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Run tests
5. Deploy to Railway production environment

## Required Secrets

Configure these secrets in your GitHub repository settings:

### Staging Environment
- `RAILWAY_TOKEN_STAGING`: Railway API token for staging
- `RAILWAY_SERVICE_STAGING`: Railway service ID for staging

### Production Environment
- `RAILWAY_TOKEN_PRODUCTION`: Railway API token for production
- `RAILWAY_SERVICE_PRODUCTION`: Railway service ID for production

## How to Set Up Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its corresponding value

### Getting Railway Tokens

1. Go to [Railway Dashboard](https://railway.app/account/tokens)
2. Create a new token
3. Copy the token and add it to GitHub secrets

### Getting Railway Service ID

1. Go to your Railway project
2. Click on your service
3. Go to **Settings**
4. Copy the **Service ID**

## Workflow Environments

Configure environments in GitHub:

1. Go to **Settings** → **Environments**
2. Create `staging` and `production` environments
3. Add protection rules (optional):
   - Required reviewers for production
   - Wait timer before deployment
   - Restrict to specific branches

## Manual Deployment

You can manually trigger deployments using the **workflow_dispatch** event:

1. Go to **Actions** tab
2. Select the workflow (staging or production)
3. Click **Run workflow**
4. Select the branch and click **Run workflow**

## Branch Strategy

- `dev` → Staging environment (automatic deployment)
- `main` → Production environment (automatic deployment)

## Testing Locally

Before pushing, test your changes locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
flake8 .
black --check .

# Build Docker image
docker build -t todo-app:test .

# Run Docker container
docker run -p 5000:5000 todo-app:test
```
