# NER WebApp

A Django-based web application for Named Entity Recognition (NER) tasks, enabling authenticated users to upload multiple documents and generate LLM-powered summaries of document titles using Ollama/DeepSeek-R1.

## Features

-   **🔐 Secure Authentication**: User registration and login with email support
-   **📁 Document Upload**: Upload multiple files (PDFs, images, etc.) organized into `DocumentSet` instances
-   **🤖 LLM Summarization**: Generate summaries of document titles using DeepSeek-R1 via Ollama
-   **📱 Responsive UI**: Modern interface built with Tailwind CSS
-   **🏗️ Modular Design**: Separates authentication and core functionality into dedicated Django apps

## Screenshots

### 1. User Registration

![User Registration](https://i.postimg.cc/2yTxYWwW/Screenshot-2025-06-11-190812.png)

### 2. Sign In

![Sign In](https://i.postimg.cc/5N7mkwjd/Screenshot-2025-06-11-190751.png)

### 3. Document Upload Interface

![Document Upload Interface](https://i.postimg.cc/HL54xRzd/Screenshot-2025-06-11-190719.png)

### 4. Document Summary Interface

![Summary Interface](https://i.postimg.cc/0yzCgbJ6/Screenshot-2025-06-11-190653.png)

### 5. Summary Generation

![Summary Generation](https://i.postimg.cc/RZ2Lv4cg/Screenshot-2025-06-11-190623.png)

## Table of Contents

-   [Requirements](#-requirements)
-   [Installation](#-installation)
-   [Configuration](#-configuration)
-   [Usage](#-usage)
-   [Development](#-development)
-   [Future Enhancements](#-future-enhancements)
-   [Contributing](#-contributing)
-   [License](#-license)

## Requirements

-   **Python**: 3.13.1+
-   **Django**: 4.2.16
-   **Database**: SQLite (default, configurable for other databases)
-   **LLM**: Ollama with DeepSeek-R1 model

### Dependencies

```txt
django==4.2.16
python-decouple==3.8
ollama==0.3.3
PyPDF2==3.0.1
pytesseract==0.3.13
```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ner_project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Ollama

1. **Install Ollama**: Follow the [official installation guide](https://ollama.ai/)
2. **Pull the DeepSeek-R1 model**:
    ```bash
    ollama pull deepseek-r1
    ```

## Configuration

### 1. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 3. Run Development Server

```bash
python manage.py runserver
```

Access the application at **http://127.0.0.1:8000/**

## Usage

### Authentication

1. **Register**: Navigate to `/auth/register/` to create an account
2. **Login**: Access `/auth/login/` to sign in

### Document Management

1. **Upload Documents**:

    - Go to `/dashboard/upload/`
    - Enter a DocumentSet name
    - Select multiple files (PDFs, images, etc.)
    - Files are saved in `media/documents/`

2. **View Summaries**:
    - Go to `/dashboard/summary/`
    - Select a DocumentSet from the dropdown
    - View LLM-generated summaries of document titles

### Admin Interface (Requires Superuser)

Access `/admin/` with superuser credentials to manage users, DocumentSets, and Documents.

## Development

### Database Configuration

The project uses SQLite by default. To use other databases, configure `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        # ... other settings
    }
}
```

### Media Files Configuration

Ensure media files are properly configured in `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

For development, add to `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Ollama Setup

Ensure the DeepSeek-R1 model is running before generating summaries:

```bash
ollama run deepseek-r1
```

## 🚧 Future Enhancements

-   [ ] **Title Extraction**: Implement PDF title extraction using PyPDF2 and OCR with pytesseract
-   [ ] **NER Processing**: Integrate spaCy or Hugging Face transformers for entity extraction
-   [ ] **Email Verification**: Add email confirmation for user registration
-   [ ] **Advanced UI**: Implement file upload previews and interactive summaries
-   [ ] **API Endpoints**: Create REST API for external integrations
-   [ ] **Batch Processing**: Support for bulk document processing
-   [ ] **Export Features**: Allow exporting summaries and extracted entities

## 🚀 Production Deployment (Railway)

This guide walks you through deploying your Django NER WebApp to Railway with Ollama support.

### Prerequisites

-   GitHub account with your code pushed
-   Railway account (sign up at [railway.app](https://railway.app))
-   Basic understanding of environment variables

### Step 1: Set Up Railway Project

1. **Create New Project**
   - Go to [railway.app](https://railway.app) and log in
   - Click **"New Project"** → **"Deploy from GitHub repo"**
   - Select your `NER-WebApp` repository
   - Railway will automatically detect it's a Django app

2. **Add PostgreSQL Database**
   - In your Railway project dashboard, click **"+ New"**
   - Select **"Database"** → **"Add PostgreSQL"**
   - Railway will automatically set the `DATABASE_URL` environment variable

### Step 2: Configure Environment Variables

In your Railway project settings, add these environment variables:

```bash
SECRET_KEY=your-production-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=your-app-name.up.railway.app,*.railway.app
OLLAMA_HOST=http://ollama:11434
```

**Generate a secure SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Deploy Ollama on Railway

Ollama needs to run as a separate service:

1. **Add Ollama Service**
   - In your project, click **"+ New"** → **"Empty Service"**
   - Name it `ollama`
   - Go to **Settings** → **Source** → **Image**
   - Enter: `ollama/ollama:latest`
   - Add environment variable: `OLLAMA_MODELS=deepseek-r1`

2. **Configure Ollama Networking**
   - In the Ollama service settings, go to **Networking**
   - Enable **Private Network** (this allows your Django app to communicate with Ollama)
   - Note the internal URL (usually `ollama.railway.internal:11434`)

3. **Pull DeepSeek Model** (One-time setup)
   - After Ollama deploys, go to its **Deployments** tab
   - Click on the latest deployment → **View Logs**
   - Once running, use Railway's **Terminal** feature (if available) or deploy a custom Dockerfile:

   Create a `Dockerfile.ollama` in your repo root:
   ```dockerfile
   FROM ollama/ollama:latest
   RUN ollama serve & sleep 5 && ollama pull deepseek-r1
   CMD ["ollama", "serve"]
   ```

### Step 4: Deploy Your Django App

1. **Automatic Deployment**
   - Railway will auto-deploy using the `Procfile` and `railway.toml`
   - Monitor deployment logs for any errors

2. **Run Migrations** (First deployment only)
   - Railway automatically runs migrations via `railway.toml`
   - Check logs to ensure migrations completed successfully

3. **Create Superuser** (Optional)
   - Go to your Django service → **Settings** → **Terminal** (if available)
   - Or use Railway CLI:
   ```bash
   railway run python ner_project/manage.py createsuperuser
   ```

### Step 5: Configure Media Files

**Important:** Railway's ephemeral filesystem means uploaded files will be lost on redeployments.

**Options:**
1. **Railway Volumes** (Persistent storage):
   - Go to your Django service → **Settings** → **Volumes**
   - Add a volume mounted at `/app/ner_project/media`

2. **Cloud Storage (Recommended for production)**:
   - Use AWS S3, Cloudinary, or Google Cloud Storage
   - Install `django-storages`: Add to `requirements.txt`
   - Configure in `settings.py` (see django-storages docs)

### Step 6: Access Your App

1. **Get Your URL**
   - Go to your Django service → **Settings** → **Networking**
   - Click **Generate Domain**
   - Your app will be live at `https://your-app-name.up.railway.app`

2. **Update ALLOWED_HOSTS**
   - Update the `ALLOWED_HOSTS` environment variable with your actual Railway domain

### Railway CLI (Optional)

Install for easier management:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# View logs
railway logs

# Run commands
railway run python ner_project/manage.py migrate
```

### Troubleshooting Railway Deployment

**Build Failures:**
- Check Railway logs for missing dependencies
- Ensure `requirements.txt` includes all packages
- Verify Python version in `runtime.txt`

**Database Connection Errors:**
- Confirm PostgreSQL service is running
- Check `DATABASE_URL` is automatically set
- Verify `psycopg2-binary` is in requirements

**Ollama Connection Issues:**
- Ensure Ollama service is running and healthy
- Verify `OLLAMA_HOST` points to internal Railway URL
- Check private networking is enabled for both services

**Static Files Not Loading:**
- Ensure `collectstatic` runs during deployment (check `railway.toml`)
- Verify WhiteNoise is in `MIDDLEWARE`
- Check `STATIC_ROOT` and `STATIC_URL` settings

**File Uploads Disappearing:**
- Implement Railway Volumes or cloud storage (S3, Cloudinary)
- Media files on ephemeral filesystem are lost on redeploy

### Cost Considerations

- **Hobby Plan**: $5/month for 512MB RAM, $5 execution credit
- **PostgreSQL**: Shared resources, adequate for small apps
- **Ollama**: Runs on CPU by default (slower inference), GPU instances cost more
- **Alternative**: Use cloud LLM APIs (OpenAI, Anthropic) instead of self-hosted Ollama

### Performance Tips

1. **Ollama Performance**: Railway's CPU instances are slow for LLM inference. Consider:
   - Using smaller models (`deepseek-r1:1.5b` instead of full model)
   - Implementing request queuing to avoid timeouts
   - Switching to cloud APIs for production

2. **Database Optimization**:
   - Add indexes to frequently queried fields
   - Enable connection pooling (already configured via `dj-database-url`)

3. **Caching**:
   - Add Redis for session/cache storage
   - Cache LLM responses for repeated document sets

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature-name`)
3. **Commit** your changes (`git commit -m "Add feature"`)
4. **Push** to the branch (`git push origin feature-name`)
5. **Open** a pull request

### Guidelines

-   Follow Python PEP 8 style guidelines
-   Include tests for new features
-   Update documentation for significant changes
-   Ensure all tests pass before submitting PR

## License

This project is licensed under the [MIT License](LICENSE).

---

## Troubleshooting

### Common Issues

**OperationalError: no such table**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Ollama Connection Error**

-   Ensure Ollama is running: `ollama serve`
-   Verify DeepSeek-R1 model is available: `ollama list`

**File Upload Issues**

-   Check media directory permissions
-   Verify MEDIA_ROOT and MEDIA_URL settings

---

**Built using Django and Ollama**
