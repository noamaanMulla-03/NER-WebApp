# 🚀 Complete Railway Deployment Guide for NER WebApp

This guide provides **extremely detailed, step-by-step** instructions for deploying your Django NER WebApp to Railway with PostgreSQL and Ollama.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Part 1: Prepare Your Code](#part-1-prepare-your-code)
- [Part 2: Set Up Railway Account](#part-2-set-up-railway-account)
- [Part 3: Create Railway Project](#part-3-create-railway-project)
- [Part 4: Deploy PostgreSQL Database](#part-4-deploy-postgresql-database)
- [Part 5: Configure Environment Variables](#part-5-configure-environment-variables)
- [Part 6: Deploy Django Application](#part-6-deploy-django-application)
- [Part 7: Deploy Ollama Service](#part-7-deploy-ollama-service)
- [Part 8: Connect Services Together](#part-8-connect-services-together)
- [Part 9: Run Database Migrations](#part-9-run-database-migrations)
- [Part 10: Create Superuser](#part-10-create-superuser)
- [Part 11: Configure Media File Storage](#part-11-configure-media-file-storage)
- [Part 12: Testing & Verification](#part-12-testing--verification)
- [Troubleshooting](#troubleshooting)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

Before starting, ensure you have:

- ✅ **GitHub Account**: Your code must be in a GitHub repository
- ✅ **Railway Account**: Free tier available at [railway.app](https://railway.app)
- ✅ **Git Installed**: On your local machine
- ✅ **Code Pushed to GitHub**: All your latest changes committed and pushed
- ✅ **Credit Card** (Optional): For Railway usage beyond free tier ($5/month hobby plan recommended)

---

## Part 1: Prepare Your Code

### Step 1.1: Verify All Files Are Present

Check that these files exist in your repository root:

```bash
cd /workspaces/NER-WebApp
ls -la
```

**Required files:**
- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `railway.toml` - Railway deployment configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - Python dependencies
- ✅ `.env.example` - Environment variable template
- ✅ `.gitignore` - Prevents committing sensitive files

### Step 1.2: Generate a Production Secret Key

Run this command to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Example output:**
```
django-insecure-x7$k9#mz@w2v!p3&8q*5n^0h$j6u+r4t@9s-2l=c1v(e)d#m
```

**⚠️ SAVE THIS KEY** - You'll need it in Part 5.

### Step 1.3: Commit All Changes

```bash
# Check status
git status

# Add all files
git add .

# Commit with message
git commit -m "Prepare for Railway deployment with Ollama and PostgreSQL"

# Push to GitHub
git push origin main
```

**Verification:** Go to your GitHub repository and confirm all files are visible.

---

## Part 2: Set Up Railway Account

### Step 2.1: Create Railway Account

1. **Go to Railway**: Navigate to [railway.app](https://railway.app)
2. **Click "Login"** or "Start a New Project"
3. **Sign Up Options**:
   - **GitHub** (Recommended): Click "Login with GitHub"
   - **Email**: Use email/password
4. **Authorize Railway**: Grant access to your GitHub repositories
5. **Verify Email**: Check your inbox and verify if required

### Step 2.2: Add Payment Method (Optional but Recommended)

1. **Click your profile** (bottom left corner)
2. **Go to "Account Settings"**
3. **Click "Billing"**
4. **Add Payment Method**:
   - Free tier: $5 credit/month
   - Hobby plan: $5/month + usage-based pricing
   - Pro plan: $20/month + usage-based pricing

**Recommendation:** Start with Hobby plan ($5/month) for better resource allocation.

---

## Part 3: Create Railway Project

### Step 3.1: Initialize New Project

1. **Dashboard**: From Railway dashboard, click **"+ New Project"**
2. **Select Deployment Method**:
   - Click **"Deploy from GitHub repo"**
3. **Authorize GitHub**: If prompted, grant Railway access to your repositories
4. **Select Repository**:
   - Find and click **"NER-WebApp"** (or your repository name)
5. **Configure Deployment**:
   - Railway will auto-detect it's a Python project
   - Click **"Deploy Now"** or **"Add Variables"**

### Step 3.2: Name Your Project

1. **Top-left corner**: Click the project name (usually "production")
2. **Rename**: Type something meaningful like **"ner-webapp-prod"**
3. **Press Enter** to save

**Your project structure will eventually have 3 services:**
- 🐘 PostgreSQL (Database)
- 🐍 Django App (Web Application)
- 🤖 Ollama (LLM Service)

---

## Part 4: Deploy PostgreSQL Database

### Step 4.1: Add PostgreSQL Service

1. **In your project dashboard**, click **"+ New"** (top right)
2. **Select "Database"**
3. **Choose "Add PostgreSQL"**
4. **Railway will**:
   - Create a new PostgreSQL instance
   - Generate random credentials
   - Automatically set `DATABASE_URL` environment variable

### Step 4.2: Verify PostgreSQL Deployment

1. **Click on the PostgreSQL service card**
2. **Go to "Variables" tab**
3. **You should see**:
   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=<random-password>
   POSTGRES_DB=railway
   DATABASE_URL=postgresql://postgres:<password>@<host>:5432/railway
   ```

4. **Copy the DATABASE_URL** - You'll reference this later

### Step 4.3: Configure PostgreSQL Settings (Optional)

1. **Click "Settings" tab**
2. **Service Name**: Rename to **"postgres-db"** for clarity
3. **Resource Limits** (if on paid plan):
   - Memory: 512 MB minimum
   - CPU: 0.5 vCPU minimum

---

## Part 5: Configure Environment Variables

### Step 5.1: Navigate to Django Service

1. **Click on your Django service** (named after your repo: "NER-WebApp")
2. **Click "Variables" tab**

### Step 5.2: Add Required Variables

Click **"+ New Variable"** for each of the following:

#### **1. SECRET_KEY**
```
SECRET_KEY=<paste-the-key-you-generated-in-step-1.2>
```
**Example:**
```
SECRET_KEY=django-insecure-x7$k9#mz@w2v!p3&8q*5n^0h$j6u+r4t@9s-2l=c1v(e)d#m
```

#### **2. DEBUG**
```
DEBUG=False
```
**⚠️ NEVER set DEBUG=True in production!**

#### **3. ALLOWED_HOSTS**
```
ALLOWED_HOSTS=.railway.app
```
**Note:** The dot (.) before railway.app is important - it allows all Railway subdomains.

#### **4. DATABASE_URL**
**This should already be set automatically by Railway!** 
- Check if `DATABASE_URL` appears in the variables list
- If not, click **"+ Reference"** → Select **"postgres-db"** → Choose **"DATABASE_URL"**

#### **5. OLLAMA_HOST** (We'll set this later)
```
OLLAMA_HOST=http://ollama.railway.internal:11434
```
**Note:** Add this AFTER deploying Ollama in Part 7.

### Step 5.3: Verify All Variables

Your variables should look like this:

```
SECRET_KEY=django-insecure-x7$k9#mz@w2v!p3&8q*5n^0h$j6u+r4t@9s-2l=c1v(e)d#m
DEBUG=False
ALLOWED_HOSTS=.railway.app
DATABASE_URL=postgresql://postgres:password@postgres-db.railway.internal:5432/railway
```

---

## Part 6: Deploy Django Application

### Step 6.1: Trigger Deployment

Railway should **automatically deploy** after you added variables. If not:

1. **Click "Deployments" tab**
2. **Click "Deploy"** or **"Redeploy"**
3. **Monitor the deployment**:
   - Click on the active deployment
   - Watch the build logs in real-time

### Step 6.2: Monitor Build Process

You'll see several stages:

```
1. 🔄 Cloning repository from GitHub...
2. 📦 Installing dependencies from requirements.txt...
3. 🏗️  Building application...
4. 🚀 Starting with railway.toml configuration...
5. ✅ Deployment successful
```

**Common issues at this stage:**
- ❌ **Missing dependencies**: Check `requirements.txt`
- ❌ **Python version mismatch**: Verify `runtime.txt`
- ❌ **Import errors**: Check logs for missing packages

### Step 6.3: Check Deployment Status

1. **Look for green checkmark** ✅ next to deployment
2. **Click "View Logs"** to see runtime output
3. **Verify these log messages**:
   ```
   Running migrations...
   Collecting static files...
   Starting Gunicorn server...
   Listening on 0.0.0.0:PORT
   ```

### Step 6.4: Generate Public URL

1. **Go to "Settings" tab**
2. **Scroll to "Networking" section**
3. **Click "Generate Domain"**
4. **Railway will create**: `your-app-name.up.railway.app`

**⚠️ IMPORTANT:** Copy this URL - you'll test it later!

### Step 6.5: Update ALLOWED_HOSTS (Optional but Recommended)

1. **Go back to "Variables" tab**
2. **Click on ALLOWED_HOSTS**
3. **Update to include your specific domain**:
   ```
   ALLOWED_HOSTS=your-app-name.up.railway.app,.railway.app
   ```
4. **Save** - This triggers a redeploy

---

## Part 7: Deploy Ollama Service

This is the **most critical part** for your LLM functionality.

### Step 7.1: Create Ollama Service

1. **In your project dashboard**, click **"+ New"**
2. **Select "Empty Service"**
3. **Name it "ollama"**

### Step 7.2: Configure Ollama Docker Image

1. **Click on the "ollama" service card**
2. **Go to "Settings" tab**
3. **Scroll to "Source"**
4. **Click "Source Image"**
5. **Enter**:
   ```
   ollama/ollama:latest
   ```
6. **Click "Deploy"**

### Step 7.3: Enable Private Networking

1. **Still in "Settings" tab**
2. **Scroll to "Networking"**
3. **Enable "Private Networking"**
4. **Note the internal URL**: `ollama.railway.internal:11434`

### Step 7.4: Configure Resource Allocation

1. **Scroll to "Resources"** in Settings
2. **Set resource limits** (Hobby plan or higher):
   - **Memory**: 2048 MB (2 GB) minimum
   - **CPU**: 1.0 vCPU minimum

**⚠️ Note:** Ollama requires significant resources. Free tier may be insufficient.

### Step 7.5: Add Persistent Volume (Important!)

Ollama stores models on disk. Without a volume, models are lost on restart.

1. **In "Settings" tab**, scroll to **"Volumes"**
2. **Click "+ Add Volume"**
3. **Mount Path**: `/root/.ollama`
4. **Size**: 10 GB minimum (models are large!)
5. **Click "Add"**

### Step 7.6: Verify Ollama is Running

1. **Go to "Deployments" tab**
2. **Click on active deployment**
3. **View Logs** - You should see:
   ```
   Listening on [::]:11434
   ```

---

## Part 8: Connect Services Together

### Step 8.1: Update Django Environment Variables

1. **Go to Django service** → **"Variables" tab**
2. **Add or update OLLAMA_HOST**:
   ```
   OLLAMA_HOST=http://ollama.railway.internal:11434
   ```
3. **Save** - This triggers a redeploy

### Step 8.2: Pull DeepSeek Model into Ollama

This is **critical** - the model must be downloaded into Ollama.

**Option A: Using Railway Terminal (if available)**

1. **Click on Ollama service**
2. **Go to "Settings"** → **"Terminal"** (if available)
3. **Run**:
   ```bash
   ollama pull deepseek-r1
   ```
4. **Wait** - This takes 5-15 minutes depending on model size

**Option B: Using Custom Dockerfile (Recommended)**

Create a custom Ollama setup that pre-downloads the model:

1. **In your local repository**, create `Dockerfile.ollama`:

```dockerfile
FROM ollama/ollama:latest

# Set environment
ENV OLLAMA_HOST=0.0.0.0:11434

# Start Ollama in background and pull model
RUN ollama serve & \
    sleep 10 && \
    ollama pull deepseek-r1 && \
    pkill ollama

# Start Ollama server
CMD ["ollama", "serve"]
```

2. **Commit and push**:
```bash
git add Dockerfile.ollama
git commit -m "Add Ollama Dockerfile with deepseek-r1"
git push
```

3. **Update Ollama service on Railway**:
   - Go to Ollama service → **"Settings"** → **"Source"**
   - Change from "Image" to **"Repo"**
   - Select your **NER-WebApp** repository
   - **Dockerfile Path**: `Dockerfile.ollama`
   - **Deploy**

4. **Monitor deployment** - Check logs for model download progress

**Option C: Manual Model Installation via SSH/Terminal**

If Railway provides SSH access:

1. **Install Railway CLI** locally:
```bash
npm i -g @railway/cli
```

2. **Login**:
```bash
railway login
```

3. **Link project**:
```bash
railway link
```

4. **Select Ollama service**:
```bash
railway service
# Select 'ollama' from the list
```

5. **Run command**:
```bash
railway run ollama pull deepseek-r1
```

### Step 8.3: Verify Model Installation

1. **Go to Ollama service** → **"Deployments"** → **"View Logs"**
2. **Look for**:
   ```
   pulling manifest
   pulling layers...
   success
   ```

3. **Test model availability** (if terminal access):
   ```bash
   ollama list
   ```
   **Should show**:
   ```
   NAME              ID        SIZE
   deepseek-r1:latest abc123   7.5GB
   ```

---

## Part 9: Run Database Migrations

### Step 9.1: Verify Auto-Migration

Railway should auto-run migrations via `railway.toml`. Check Django logs:

1. **Django service** → **"Deployments"** → **Latest deployment**
2. **View Logs** → Look for:
   ```
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     Applying dashboard.0001_initial... OK
     ...
   ```

### Step 9.2: Manual Migration (if needed)

If migrations didn't run automatically:

**Using Railway CLI:**
```bash
railway link
railway service  # Select Django service
railway run python ner_project/manage.py migrate
```

**Via Re-deployment:**
1. **Django service** → **"Deployments"**
2. **Click "Redeploy"** - Migrations run automatically

---

## Part 10: Create Superuser

### Step 10.1: Using Railway CLI

```bash
# Ensure you're linked to the right project
railway link

# Select your Django service
railway service

# Create superuser
railway run python ner_project/manage.py createsuperuser
```

**Follow prompts**:
```
Username: admin
Email: admin@example.com
Password: <strong-password>
Password (again): <strong-password>
Superuser created successfully.
```

### Step 10.2: Alternative - Django Shell

```bash
railway run python ner_project/manage.py shell
```

Then:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'your-password')
exit()
```

---

## Part 11: Configure Media File Storage

### ⚠️ Critical Issue: Ephemeral Filesystem

Railway uses **ephemeral storage** - uploaded files are **deleted on every redeploy!**

### Solution A: Railway Volumes (Temporary Fix)

1. **Django service** → **"Settings"** → **"Volumes"**
2. **Add Volume**:
   - **Mount Path**: `/app/ner_project/media`
   - **Size**: 5 GB
3. **Click "Add"**
4. **Redeploy** the service

**⚠️ Limitation:** Volumes persist between deploys but may not be suitable for production scale.

### Solution B: Cloud Storage (Production Recommended)

#### B1. Install django-storages

Add to `requirements.txt`:
```
django-storages[boto3]==1.14.2
```

#### B2. Configure AWS S3

In `settings.py`, add:
```python
# AWS S3 Configuration
if not DEBUG:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'private'
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

#### B3. Add Environment Variables

Railway Variables:
```
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

---

## Part 12: Testing & Verification

### Step 12.1: Access Your Application

1. **Open your Railway URL**: `https://your-app-name.up.railway.app`
2. **Expected**: Login page should load

### Step 12.2: Test Authentication

1. **Click "Register"**
2. **Create a test account**:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `TestPass123!`
3. **Login** with credentials

### Step 12.3: Test Document Upload

1. **Navigate to Upload page**
2. **Enter Document Set Name**: `Test Set 1`
3. **Upload 2-3 files** (PDFs or images)
4. **Click "Upload"**
5. **Verify**: Files should upload successfully

### Step 12.4: Test LLM Summary

1. **Navigate to Summary page**
2. **Select** your document set
3. **Click "Generate Summary"**
4. **Wait** (30-60 seconds for LLM processing)
5. **Verify**: Summaries appear for each document

**If this works** ✅ - Your deployment is complete!

### Step 12.5: Test Admin Panel

1. **Go to**: `https://your-app-name.up.railway.app/admin`
2. **Login** with superuser credentials
3. **Verify**: Can see Users, Document Sets, Documents

---

## Troubleshooting

### Problem 1: Application Won't Start

**Symptoms:**
- Deployment fails with error
- Logs show `ModuleNotFoundError`

**Solutions:**
1. **Check `requirements.txt`**: Ensure all packages listed
2. **Verify Python version**: Check `runtime.txt` matches your local version
3. **View detailed logs**: Django service → Deployments → View Logs

### Problem 2: Database Connection Error

**Symptoms:**
- `django.db.utils.OperationalError`
- `could not connect to server`

**Solutions:**
1. **Verify DATABASE_URL**: Variables tab → Confirm it's set
2. **Check PostgreSQL status**: Click PostgreSQL service → Should be "Active"
3. **Recreate database reference**:
   - Remove `DATABASE_URL` variable
   - Add via "+ Reference" → Select postgres-db → DATABASE_URL

### Problem 3: Static Files Not Loading

**Symptoms:**
- Page loads but no CSS/styling
- 404 errors for `/static/` files

**Solutions:**
1. **Check WhiteNoise**: Verify it's in `MIDDLEWARE` in `settings.py`
2. **Run collectstatic manually**:
   ```bash
   railway run python ner_project/manage.py collectstatic --noinput
   ```
3. **Verify STATIC_ROOT**: Check `settings.py` has `STATIC_ROOT = BASE_DIR / 'staticfiles'`

### Problem 4: Ollama Not Responding

**Symptoms:**
- Summary generation fails
- `ConnectionRefusedError` in logs
- Timeout errors

**Solutions:**
1. **Check Ollama service status**: Should show "Active" with green indicator
2. **Verify OLLAMA_HOST variable**: Should be `http://ollama.railway.internal:11434`
3. **Check model is loaded**:
   ```bash
   railway service  # Select ollama
   railway run ollama list
   ```
4. **Increase Ollama resources**: Settings → Resources → Increase memory to 4GB
5. **Check private networking**: Settings → Networking → Ensure enabled

### Problem 5: Model Not Found

**Symptoms:**
- Error: `model 'deepseek-r1' not found`
- LLM requests fail

**Solutions:**
1. **Pull model again**:
   ```bash
   railway service  # Select ollama
   railway run ollama pull deepseek-r1
   ```
2. **Check volume**: Ensure Ollama has persistent volume at `/root/.ollama`
3. **Wait for download**: Large models take 10-20 minutes

### Problem 6: File Uploads Disappear

**Symptoms:**
- Files upload successfully
- After redeploy, files are gone

**Solutions:**
1. **Add Railway Volume**: Settings → Volumes → Mount at `/app/ner_project/media`
2. **Implement S3 storage**: Follow Part 11, Solution B
3. **Avoid redeployments**: Minimize unnecessary redeploys

### Problem 7: 502 Bad Gateway

**Symptoms:**
- Site returns 502 error
- Can't access application

**Solutions:**
1. **Check deployment status**: Should be "Active"
2. **Verify Gunicorn port binding**: Logs should show `Listening on 0.0.0.0:$PORT`
3. **Check environment variables**: Ensure all required vars are set
4. **Redeploy**: Deployments → Redeploy

### Problem 8: Django Admin Static Files Missing

**Symptoms:**
- Admin panel has no styling
- Login page loads but looks broken

**Solutions:**
1. **Collectstatic with admin**:
   ```bash
   railway run python ner_project/manage.py collectstatic --noinput
   ```
2. **Verify STATIC_ROOT**: Should include Django's admin static files
3. **Check STORAGES setting**: Ensure WhiteNoise is configured correctly

---

## Monitoring & Maintenance

### Daily Monitoring

1. **Check Service Health**:
   - Railway dashboard → All services should be green
   - No error indicators

2. **Review Logs**:
   - Django service → Deployments → View Logs
   - Look for errors or warnings

3. **Monitor Resource Usage**:
   - Settings → Metrics
   - Check CPU, Memory, Network usage

### Weekly Tasks

1. **Database Backups**:
   - PostgreSQL service → Backups → Create manual backup
   - Railway auto-backs up daily on paid plans

2. **Check Ollama Model**:
   ```bash
   railway run ollama list
   ```
   - Verify model still exists after any volume issues

3. **Review Logs for Errors**:
   - Search for error patterns
   - Fix recurring issues

### Monthly Maintenance

1. **Update Dependencies**:
   ```bash
   pip list --outdated
   pip install --upgrade <package>
   ```
   - Update `requirements.txt`
   - Test locally
   - Push and redeploy

2. **Security Updates**:
   - Check Django security releases
   - Update to latest patch version

3. **Cost Review**:
   - Railway dashboard → Billing
   - Review usage and costs
   - Optimize resource allocation

### Useful Railway CLI Commands

```bash
# Link to project
railway link

# View logs
railway logs

# Run migrations
railway run python ner_project/manage.py migrate

# Create superuser
railway run python ner_project/manage.py createsuperuser

# Django shell
railway run python ner_project/manage.py shell

# Check environment variables
railway variables

# Switch service
railway service

# Deploy specific branch
railway up
```

---

## Cost Estimation

### Free Tier
- **Included**: $5 execution credit/month
- **Limitations**: 
  - 500 MB RAM per service
  - 500 MB disk per service
  - Limited build minutes
- **Realistic for**: Development/testing only

### Hobby Plan ($5/month)
- **Included**: $5 base + usage credits
- **Better for**: 
  - 8 GB RAM across services
  - 100 GB disk
  - Unlimited build minutes
- **Estimated total**: $10-15/month for this app

### Pro Plan ($20/month)
- **Best for**: Production workloads
- **Includes**: Priority support, better resources
- **Estimated total**: $25-40/month

### Resource Breakdown for This App
- **Django**: 512 MB RAM, 0.5 vCPU
- **PostgreSQL**: 512 MB RAM, 0.5 vCPU
- **Ollama**: 2048 MB RAM, 1.0 vCPU (minimum)
- **Total**: ~3 GB RAM, 2 vCPU

---

## Alternative: Using Cloud LLM APIs Instead of Ollama

If Ollama is too resource-intensive, consider cloud APIs:

### OpenAI Integration

1. **Update `dashboard/views.py`**:
```python
import openai

openai.api_key = config('OPENAI_API_KEY')

# Replace ollama.chat() with:
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)
summary = response['choices'][0]['message']['content']
```

2. **Update `requirements.txt`**:
```
openai==1.3.0
```

3. **Railway Variables**:
```
OPENAI_API_KEY=sk-your-api-key-here
```

4. **Remove Ollama service** from Railway

**Pros:** Cheaper, faster, more reliable
**Cons:** API costs, external dependency

---

## Final Checklist

Before considering deployment complete:

- [ ] All services are "Active" and green
- [ ] PostgreSQL is connected and migrations ran
- [ ] Ollama service is running
- [ ] DeepSeek-R1 model is downloaded
- [ ] Environment variables are all set correctly
- [ ] Public URL is generated and accessible
- [ ] Can register and login users
- [ ] Can upload documents
- [ ] Can generate LLM summaries
- [ ] Admin panel is accessible
- [ ] Static files load correctly
- [ ] Media storage configured (volume or S3)
- [ ] Superuser account created
- [ ] Backups configured
- [ ] Monitoring set up

---

## Support & Resources

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Django Docs**: https://docs.djangoproject.com
- **Ollama Docs**: https://github.com/ollama/ollama
- **This Project's Issues**: https://github.com/noamaanMulla-03/NER-WebApp/issues

---

**🎉 Congratulations!** If you've followed all steps, your Django NER WebApp should now be live on Railway with PostgreSQL and Ollama!

**Your live URL**: `https://your-app-name.up.railway.app`
