# NER WebApp

A Django-based web application for Named Entity Recognition (NER) tasks, enabling authenticated users to upload multiple documents and generate LLM-powered summaries of document titles using Ollama/DeepSeek-R1.

## 🚀 Features

-   **🔐 Secure Authentication**: User registration and login with email support
-   **📁 Document Upload**: Upload multiple files (PDFs, images, etc.) organized into `DocumentSet` instances
-   **🤖 LLM Summarization**: Generate summaries of document titles using DeepSeek-R1 via Ollama
-   **📱 Responsive UI**: Modern interface built with Tailwind CSS
-   **🏗️ Modular Design**: Separates authentication and core functionality into dedicated Django apps

## 📸 Screenshots

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

## 📋 Table of Contents

-   [Requirements](#-requirements)
-   [Installation](#-installation)
-   [Configuration](#-configuration)
-   [Usage](#-usage)
-   [Development](#-development)
-   [Future Enhancements](#-future-enhancements)
-   [Contributing](#-contributing)
-   [License](#-license)

## 🛠️ Requirements

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

## 📥 Installation

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

## ⚙️ Configuration

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

## 🎯 Usage

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

## 🔧 Development

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
-   [ ] **Production Deployment**: Set up Gunicorn, Nginx, and S3 for media storage
-   [ ] **Email Verification**: Add email confirmation for user registration
-   [ ] **Advanced UI**: Implement file upload previews and interactive summaries
-   [ ] **API Endpoints**: Create REST API for external integrations
-   [ ] **Batch Processing**: Support for bulk document processing
-   [ ] **Export Features**: Allow exporting summaries and extracted entities

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

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🆘 Troubleshooting

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

**Built with ❤️ using Django and Ollama**
