# Credentials Manager

<div align="center">
  <img src="https://img.shields.io/badge/Django-5.2+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</div>

<div align="center">
  <h3>🔐 A modern, secure password and credentials management system</h3>
  <p>Built with Django and inspired by Cursor.com's elegant design system</p>
</div>

---

## 🌟 Features

### 🔒 **Security First**
- **AES-256 Encryption**: All passwords and sensitive data encrypted at rest
- **Secure Authentication**: Django's robust user authentication system
- **Activity Logging**: Comprehensive audit trail for security monitoring
- **Session Management**: Secure session handling with configurable timeouts

### 📱 **Modern UI/UX**
- **Dark Theme**: Professional, easy-on-eyes design inspired by Cursor.com
- **Responsive Design**: Perfect on desktop, tablet, and mobile devices
- **Golden Ratio Layout**: Mathematically pleasing proportions and spacing
- **Smooth Animations**: Subtle animations for enhanced user experience

### ⚡ **Core Functionality**
- **Credential Management**: Store, organize, and retrieve passwords securely
- **Secure Notes**: Encrypted notes for sensitive information
- **Advanced Search**: Fast, comprehensive search across all data
- **Favorites System**: Quick access to frequently used credentials
- **Data Export**: Export your data securely for backup purposes
- **Real-time Updates**: Live search and instant feedback

### 🛠 **Developer Features**
- **Modular Architecture**: Clean separation between backend logic and frontend
- **RESTful APIs**: Well-structured API endpoints for extensibility
- **Comprehensive Testing**: Extensive test coverage for reliability
- **Type Hints**: Python type annotations for better code quality
- **Detailed Logging**: Structured logging for debugging and monitoring

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (3.11+ recommended)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd credentials_manager
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your settings
   nano .env
   ```

5. **Initialize the database**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Login with your superuser credentials

---

## 📋 Detailed Setup Guide

### Environment Configuration

Create a `.env` file in the project root with the following settings:

```bash
# Basic Configuration
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost:5432/credentials_manager

# Security Settings
SESSION_COOKIE_AGE=3600
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Application Settings
PAGINATION_SIZE=12
ACTIVITY_LOG_RETENTION_DAYS=90
ENABLE_ACTIVITY_LOGGING=True

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@credentialsmanager.com
```

### Database Options

#### SQLite (Default - Development)
No additional setup required. The SQLite database file will be created automatically.

#### PostgreSQL (Recommended for Production)
1. Install PostgreSQL
2. Create a database:
   ```sql
   CREATE DATABASE credentials_manager;
   CREATE USER credentials_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE credentials_manager TO credentials_user;
   ```
3. Update your `.env` file:
   ```bash
   DATABASE_URL=postgresql://credentials_user:your_password@localhost:5432/credentials_manager
   ```

### Production Deployment

#### Using Docker (Recommended)

1. **Build the Docker image**
   ```bash
   docker build -t credentials-manager .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

#### Manual Deployment

1. **Install production dependencies**
   ```bash
   pip install gunicorn psycopg2-binary
   ```

2. **Configure production settings**
   ```bash
   export DEBUG=False
   export SECRET_KEY="your-production-secret-key"
   export DATABASE_URL="your-production-database-url"
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn core.wsgi:application --bind 0.0.0.0:8000
   ```

---

## 🎯 Usage Guide

### Creating Your First Credential

1. **Navigate to Dashboard**
   - After logging in, you'll see the main dashboard
   - Click "Add Credential" or go to Credentials → Add New

2. **Fill in the Details**
   - **Label**: Descriptive name (e.g., "Gmail Account")
   - **Type**: Select from predefined categories
   - **Username/Email**: Your login credentials
   - **Password**: Will be encrypted automatically
   - **Website URL**: Optional link to the service
   - **Notes**: Additional information
   - **Tags**: Comma-separated tags for organization

3. **Save and Access**
   - Click "Save" to store your credential
   - Access it anytime from the Credentials list
   - Use the copy buttons for quick password copying

### Managing Secure Notes

1. **Create a Note**
   - Go to Notes → Add New
   - Enter a title and content
   - Select a category type
   - Add tags for organization

2. **Organization Features**
   - Mark items as favorites for quick access
   - Use tags to group related items
   - Search across all content

### Advanced Features

#### Search Functionality
- **Global Search**: Use the search bar to find credentials and notes
- **Filter by Type**: Narrow results by credential type
- **Tag Search**: Find items by their tags
- **Favorites Filter**: View only your starred items

#### Activity Monitoring
- **Activity Log**: View all account activities
- **Security Events**: Monitor login/logout events
- **Data Changes**: Track when credentials are created/modified
- **Export Options**: Download your activity history

#### Data Management
- **Export Data**: Download all your data in JSON format
- **Backup Strategy**: Regular exports recommended
- **Data Portability**: Standard format for easy migration

---

## 🏗 Architecture Overview

### Project Structure

```
credentials_manager/
├── apps/
│   ├── authentication/          # User authentication & profiles
│   │   ├── views.py            # Auth views (login, register, profile)
│   │   ├── forms.py            # Authentication forms
│   │   └── templates/          # Auth templates
│   ├── backend/                # Core business logic
│   │   ├── models.py           # Database models
│   │   ├── forms.py            # Data input forms
│   │   ├── business_logic.py   # Business logic layer
│   │   ├── api.py              # API endpoints
│   │   └── admin.py            # Django admin configuration
│   └── frontend/               # User interface
│       ├── views.py            # Frontend views
│       ├── urls.py             # URL routing
│       ├── templates/          # HTML templates
│       ├── static/             # CSS, JS, images
│       └── context_processors.py
├── core/                       # Django project configuration
│   ├── settings.py             # Application settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI application
├── docs/                       # Documentation
├── static/                     # Collected static files
├── media/                      # User uploads
├── requirements.txt            # Python dependencies
└── manage.py                   # Django management script
```

### Key Components

#### Models (`apps/backend/models.py`)
- **Credentials**: Encrypted password storage with metadata
- **SecureNote**: Encrypted note storage
- **ActivityLog**: Security and usage tracking
- **EncryptionMixin**: Shared encryption functionality

#### Business Logic (`apps/backend/business_logic.py`)
- **CredentialsManager**: CRUD operations for credentials
- **SecureNotesManager**: Note management operations
- **ActivityManager**: Activity logging and retrieval
- **SearchManager**: Cross-model search functionality

#### Frontend (`apps/frontend/`)
- **Views**: Django views handling user requests
- **Templates**: HTML templates with modern design
- **Static Files**: CSS, JavaScript, and assets

### Security Architecture

#### Encryption
- **Algorithm**: AES-256 encryption for all sensitive data
- **Key Management**: Django's SECRET_KEY used for encryption key derivation
- **Data at Rest**: All passwords and note content encrypted in database
- **Secure Transmission**: HTTPS recommended for production

#### Authentication
- **Session Management**: Django's built-in session framework
- **Password Requirements**: Configurable password strength validation
- **Activity Tracking**: All user actions logged for security auditing

---

## 🧪 Development

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test apps.backend

# Run tests with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Development Tools

#### Django Debug Toolbar
```bash
# Install debug toolbar
pip install django-debug-toolbar

# Add to INSTALLED_APPS in settings.py
# Automatically configured in development mode
```

#### Code Quality
```bash
# Install development tools
pip install black flake8 mypy

# Format code
black .

# Check code style
flake8

# Type checking
mypy .
```

### API Documentation

The application provides RESTful API endpoints for programmatic access:

#### Authentication Required Endpoints
- `GET /api/user-stats/` - User statistics
- `POST /api/search/` - Search credentials and notes
- `POST /api/toggle-favorite/` - Toggle favorite status

#### API Usage Example
```javascript
// Search for credentials
fetch('/api/search/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({
        query: 'github',
        type_filter: 'all'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🔧 Configuration

### Application Settings

Key settings in `core/settings.py`:

```python
# Application-specific settings
CREDENTIALS_MANAGER = {
    'APP_NAME': 'Credentials Manager',
    'APP_VERSION': '1.0.0',
    'PAGINATION_SIZE': 12,
    'MAX_EXPORT_ITEMS': 1000,
    'ACTIVITY_LOG_RETENTION_DAYS': 90,
    'ENABLE_ACTIVITY_LOGGING': True,
    'ENABLE_FAVORITES': True,
    'ENABLE_SEARCH': True,
    'ENABLE_EXPORT': True,
}
```

### Security Configuration

```python
# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
X_FRAME_OPTIONS = 'DENY'
```

### Logging Configuration

Structured logging is configured for different environments:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'apps.backend': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

4. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add tests for new functionality
   - Update documentation as needed

5. **Run tests and checks**
   ```bash
   python manage.py test
   black .
   flake8
   ```

6. **Submit a pull request**

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **JavaScript**: Use modern ES6+ syntax
- **CSS**: Follow BEM methodology for class naming
- **HTML**: Use semantic HTML5 elements

### Commit Messages

Use conventional commit format:
```
feat: add new search functionality
fix: resolve password visibility toggle issue
docs: update installation instructions
style: improve button hover animations
```

---

## 🛡 Security

### Security Features

- **Encryption**: AES-256 encryption for all sensitive data
- **Authentication**: Secure user authentication with session management
- **CSRF Protection**: Cross-site request forgery protection
- **XSS Protection**: Cross-site scripting prevention
- **Secure Headers**: Security headers configured for production

### Security Best Practices

1. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Regular Security Audits**
   ```bash
   pip install safety
   safety check
   ```

3. **Environment Variables**
   - Never commit sensitive data to version control
   - Use strong, unique SECRET_KEY for production
   - Regularly rotate encryption keys

4. **Database Security**
   - Use strong database passwords
   - Enable database encryption at rest
   - Regular database backups

### Reporting Security Issues

If you discover a security vulnerability, please:
1. **Do not** open a public issue
2. Email us directly at security@yourproject.com
3. Include detailed steps to reproduce
4. Allow time for us to respond and fix the issue

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Credentials Manager

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

### Getting Help

- **Documentation**: Check this README and the `/docs` folder
- **Issues**: Open an issue on GitHub for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and community support

### Common Issues

#### Installation Problems
```bash
# If you get permission errors on Windows
pip install --user -r requirements.txt

# If you get SSL errors
pip install --trusted-host pypi.org --trusted-host pypi.python.org pip setuptools
```

#### Database Issues
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### Static Files Issues
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput
```

---

## 🔄 Changelog

### Version 1.0.0 (2025-01-XX)

#### ✨ Features
- Complete credentials management system
- Secure notes functionality
- Modern dark theme UI
- Advanced search capabilities
- Activity logging and monitoring
- Data export functionality
- Responsive design
- RESTful API endpoints

#### 🔧 Technical
- Django 5.2+ compatibility
- AES-256 encryption
- Comprehensive test coverage
- Production-ready configuration
- Docker support
- Security best practices

---

<div align="center">
  <p>Made with ❤️ by the Credentials Manager team</p>
  <p>⭐ Star this repository if you find it helpful!</p>
</div>
