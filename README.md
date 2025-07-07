# Credentials Manager

A secure, Django-based web application for managing passwords, credentials, and secure notes with enterprise-grade encryption and a modern user interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

### Core Functionality
- **Secure Credential Management**: Store passwords, usernames, and login information with military-grade encryption
- **Secure Notes**: Encrypted note storage for sensitive information
- **Advanced Search**: Powerful search across all credentials and notes
- **Favorites System**: Mark frequently used items as favorites
- **Activity Logging**: Complete audit trail of user actions
- **Data Export**: Export credentials to CSV format
- **Type Categorization**: Organize credentials by type (email, banking, work, etc.)

### Security Features
- **End-to-End Encryption**: All sensitive data encrypted using Fernet symmetric encryption
- **User Isolation**: Complete data separation between users
- **Session Security**: Secure session management with CSRF protection
- **Access Tracking**: Monitor when credentials are accessed
- **Secure Password Handling**: Passwords never stored in plain text

### User Experience
- **Modern UI**: Clean, responsive interface built with modern CSS
- **Dark Mode Ready**: UI designed for both light and dark themes
- **Mobile Responsive**: Works seamlessly on all device sizes
- **Fast Search**: Real-time search with instant results
- **Intuitive Navigation**: Easy-to-use interface with clear organization

## 📁 Project Architecture

### High-Level Architecture

```
Credentials Manager
├── Frontend App (UI Layer)
│   ├── Views & Templates
│   ├── User Interactions
│   └── Form Handling
├── Backend App (Business Logic)
│   ├── Models & Database
│   ├── Business Logic Classes
│   ├── API Endpoints
│   └── Security & Encryption
└── Core Configuration
    ├── Settings & URLs
    ├── Authentication
    └── Middleware
```

### App Structure

The project follows a clean separation of concerns with two main Django apps:

#### 🎨 Frontend App (`apps/frontend/`)
Handles all user interface and presentation logic:

```
frontend/
├── views.py           # UI controllers
├── urls.py            # Frontend routes
├── context_processors.py  # Global template context
├── templatetags/      # Custom template filters
├── templates/         # HTML templates
│   └── frontend/      # App-specific templates
└── tests.py          # Frontend tests
```

**Key Responsibilities:**
- Render HTML templates and forms
- Handle user interactions and form submissions
- Delegate business operations to backend
- Manage navigation and user experience
- Template context and UI state management

#### ⚙️ Backend App (`apps/backend/`)
Contains all business logic, data models, and API endpoints:

```
backend/
├── models.py          # Data models & encryption
├── business_logic.py  # Business logic classes
├── api.py            # REST API endpoints
├── views.py          # API controllers
├── forms.py          # Form definitions & validation
├── admin.py          # Django admin interface
├── urls.py           # API routes
└── tests.py          # Backend tests
```

**Key Responsibilities:**
- Data persistence and model management
- Business rule implementation
- API endpoint provisioning
- Security and encryption handling
- Data validation and processing

### Detailed Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[User Interface]
        FORMS[Forms & Validation]
        TEMP[Templates]
        CTX[Context Processors]
    end
    
    subgraph "Backend Layer"
        API[REST API]
        BL[Business Logic]
        MODELS[Data Models]
        ENCRYPT[Encryption Layer]
    end
    
    subgraph "Data Layer"
        DB[(SQLite Database)]
        LOGS[(Activity Logs)]
    end
    
    subgraph "External"
        USER[User Browser]
        AUTH[Django Auth]
    end
    
    USER --> UI
    UI --> FORMS
    FORMS --> BL
    API --> BL
    BL --> MODELS
    MODELS --> ENCRYPT
    ENCRYPT --> DB
    BL --> LOGS
    AUTH --> UI
    
    CTX --> TEMP
    TEMP --> UI
```

## 🏗️ Business Logic Architecture

### Manager Classes

The backend implements a manager-based architecture with specialized classes:

#### 📊 DashboardManager
```python
# Get comprehensive dashboard statistics
stats = DashboardManager.get_dashboard_stats(user)
```
- User statistics calculation
- Recent activity aggregation  
- Type distribution analysis
- Performance-optimized queries

#### 🔐 CredentialsManager
```python
# Complete credential lifecycle management
credentials = CredentialsManager.get_user_credentials(user, search_params)
credential, errors = CredentialsManager.create_credential(user, form_data)
```
- CRUD operations for credentials
- Search and filtering
- Validation and error handling
- User isolation enforcement

#### 📝 SecureNotesManager
```python
# Secure note management
notes = SecureNotesManager.get_user_notes(user, search_params)
note, errors = SecureNotesManager.create_note(user, form_data)
```
- Encrypted note operations
- Type categorization
- Content search capabilities

#### 🔍 SearchManager
```python
# Advanced search across all data
results = SearchManager.search_all_user_data(user, query="gmail")
```
- Cross-model search
- Advanced filtering options
- Performance optimization
- Relevance ranking

#### ⭐ FavoriteManager
```python
# Favorite status management
is_favorite = FavoriteManager.toggle_favorite(credential, user)
favorites = FavoriteManager.get_user_favorites(user)
```
- Toggle favorite status
- Retrieve user favorites
- Activity logging integration

#### 📈 ActivityManager
```python
# Comprehensive activity tracking
ActivityManager.log_activity(user, 'create_credential', 'Created Gmail account')
activities = ActivityManager.get_user_activities(user, limit=20)
```
- Action logging and auditing
- IP address tracking
- Activity retrieval and filtering

#### 📤 DataExportManager
```python
# Data export functionality
csv_data = DataExportManager.export_user_data_csv(user)
```
- CSV export generation
- Data formatting and sanitization
- Privacy and security considerations

### Encryption Architecture

```python
class EncryptionMixin:
    @staticmethod
    def encrypt_data(data):
        """Encrypt sensitive data using Fernet"""
        
    @staticmethod
    def decrypt_data(encrypted_data):
        """Decrypt data with error handling"""
```

**Encryption Features:**
- **Algorithm**: Fernet (AES 128 in CBC mode with HMAC SHA256)
- **Key Management**: Derived from Django SECRET_KEY
- **Error Handling**: Graceful degradation for corrupted data
- **Performance**: Optimized for frequent encrypt/decrypt operations

## 🛠️ Technology Stack

### Core Technologies
- **Backend**: Django 4.2+ (Python 3.8+)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django's built-in auth system
- **Encryption**: Cryptography library (Fernet)

### Frontend Technologies
- **Templates**: Django Templates with custom filters
- **CSS**: Modern CSS with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS for interactive features
- **Icons**: Font Awesome 6
- **Responsive**: Mobile-first responsive design

### Development Tools
- **Testing**: Django TestCase with comprehensive coverage
- **Linting**: Python code style enforcement
- **Documentation**: Markdown with Mermaid diagrams
- **Version Control**: Git with conventional commits

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Quick Start

1. **Clone the Repository**
```bash
git clone <repository-url>
cd credentials_manager
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
DEBUG=True
SECRET_KEY=your-secret-key-here
```

5. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Run Development Server**
```bash
python manage.py runserver
```

7. **Access Application**
- Web Interface: http://localhost:8000
- Admin Interface: http://localhost:8000/admin
- API Endpoints: http://localhost:8000/api/

### Production Deployment

#### Environment Variables
```bash
# Required settings
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Security settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### Security Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use PostgreSQL in production
- [ ] Enable HTTPS/SSL
- [ ] Configure secure cookies
- [ ] Set up proper backup procedures
- [ ] Implement rate limiting
- [ ] Configure logging

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.backend
python manage.py test apps.frontend

# Run with coverage
coverage run --source='.' manage.py test
coverage html  # Generate HTML report
coverage report  # Terminal report
```

### Test Structure

```
tests/
├── Backend Tests
│   ├── Model Tests (encryption, validation)
│   ├── Business Logic Tests (managers)
│   ├── API Tests (endpoints, authentication)
│   ├── Form Tests (validation, security)
│   └── Integration Tests (workflows)
└── Frontend Tests
    ├── View Tests (rendering, permissions)
    ├── Template Tests (context, display)
    ├── Form Tests (UI, validation)
    ├── Permission Tests (access control)
    └── Integration Tests (user workflows)
```

### Test Coverage Goals
- **Models**: 100% coverage
- **Business Logic**: 95%+ coverage
- **Views/APIs**: 90%+ coverage
- **Forms**: 95%+ coverage
- **Integration**: 80%+ coverage

## 📚 API Documentation

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats/` | GET | User dashboard statistics |
| `/api/search/` | POST | Search credentials and notes |
| `/api/toggle-favorite/` | POST | Toggle favorite status |

### Authentication
All API endpoints require authentication via Django sessions.

### Example API Usage

```bash
# Get user statistics
curl -X GET http://localhost:8000/api/stats/ \
  --cookie "sessionid=your_session_id"

# Search for items
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your_csrf_token" \
  --cookie "sessionid=your_session_id" \
  -d '{"query": "gmail", "type_filter": "email"}'
```

For complete API documentation, see [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).

## 🔒 Security Features

### Data Protection
- **Encryption at Rest**: All sensitive data encrypted before database storage
- **User Isolation**: Complete data separation between users  
- **Access Control**: Role-based permissions system
- **Audit Trail**: Complete activity logging

### Security Headers
- CSRF Protection enabled
- Secure session cookies
- XSS protection headers
- Content Security Policy ready

### Best Practices
- Passwords never stored in plain text
- Sensitive data never logged
- Input validation and sanitization
- SQL injection prevention
- Cross-user data access prevention

## 🎯 Usage Examples

### Creating a Credential
1. Navigate to "Add Credential"
2. Fill in the form with:
   - Label: "Gmail Personal"
   - Type: "Email"
   - Username: "your.email@gmail.com"
   - Password: "your_secure_password"
3. Save and view the encrypted credential

### Searching Credentials
1. Use the search bar on any page
2. Enter search terms: "gmail" or "banking"
3. Filter by type, favorites, or other criteria
4. View instant results across all your data

### Managing Favorites
1. Click the star icon on any credential or note
2. View favorites from the dashboard
3. Filter lists to show only favorites

### Exporting Data
1. Go to Settings → Export Data
2. Download CSV file with all credentials
3. Passwords are included for backup purposes

## 🗂️ Directory Structure

```
credentials_manager/
├── core/                   # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI application
├── apps/                   # Django applications
│   ├── frontend/           # Frontend app
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── context_processors.py
│   │   ├── templates/
│   │   └── templatetags/
│   └── backend/            # Backend app
│       ├── models.py
│       ├── business_logic.py
│       ├── api.py
│       ├── views.py
│       ├── forms.py
│       └── admin.py
├── templates/              # Global templates
│   ├── layouts/            # Base templates
│   ├── accounts/           # Authentication templates
│   └── partials/           # Reusable components
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript
│   └── img/               # Images
├── docs/                   # Documentation
│   └── API_DOCUMENTATION.md
├── requirements.txt        # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

## 🤝 Contributing

### Development Workflow

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make Changes**
   - Follow coding standards
   - Add tests for new features
   - Update documentation
4. **Run Tests**
   ```bash
   python manage.py test
   ```
5. **Submit Pull Request**

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maintain test coverage above 90%
- Update documentation for new features

### Commit Messages
Use conventional commit format:
```
feat: add user export functionality
fix: resolve encryption key rotation issue
docs: update API documentation
test: add integration tests for search
```

## 📖 Documentation

- **[API Documentation](docs/API_DOCUMENTATION.md)**: Complete API reference
- **[Architecture Guide](docs/ARCHITECTURE.md)**: Detailed system architecture
- **[Security Guide](docs/SECURITY.md)**: Security implementation details
- **[Deployment Guide](docs/DEPLOYMENT.md)**: Production deployment instructions

## 🐛 Troubleshooting

### Common Issues

**Database Migration Errors**
```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial
python manage.py makemigrations
python manage.py migrate
```

**Encryption Key Issues**
```bash
# Ensure SECRET_KEY is properly set
python manage.py shell
>>> from django.conf import settings
>>> print(len(settings.SECRET_KEY))  # Should be > 32 chars
```

**Template Not Found**
- Check `INSTALLED_APPS` includes both apps
- Verify template path in `TEMPLATES` setting
- Ensure template files exist in correct directories

**Permission Denied**
- Verify user authentication
- Check object ownership in views
- Review URL patterns and namespaces

### Performance Optimization

**Database Optimization**
```python
# Use select_related for foreign keys
credentials = Credentials.objects.select_related('user')

# Use prefetch_related for reverse lookups
users = User.objects.prefetch_related('credentials_set')
```

**Caching Strategy**
```python
# Cache dashboard stats
from django.core.cache import cache
cache.set(f'dashboard_stats_{user.id}', stats, timeout=300)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

### Version 2.0 Features
- [ ] Two-factor authentication (2FA)
- [ ] Shared credentials with team members
- [ ] Browser extension
- [ ] Mobile app (React Native)
- [ ] Advanced password generator
- [ ] Security breach monitoring
- [ ] Automated backup to cloud storage

### Version 2.1 Features
- [ ] API rate limiting
- [ ] GraphQL API
- [ ] Advanced audit reports
- [ ] Custom field types
- [ ] Bulk import/export
- [ ] Advanced search filters
- [ ] Email notifications

## 📞 Support

### Getting Help

- **Documentation**: Check the docs/ directory
- **Issues**: Create GitHub issues for bugs
- **Questions**: Use GitHub discussions
- **Security**: Email security@example.com

### Reporting Bugs

When reporting bugs, please include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Environment details (Python version, OS, etc.)
5. Error messages and stack traces

---

**Built with ❤️ for secure credential management**
