# Credentials Manager API Documentation

## Overview

The Credentials Manager backend provides a RESTful API for managing user credentials, secure notes, and related functionality. All API endpoints require authentication and are accessible under the `/api/` URL prefix.

## Authentication

All API endpoints require user authentication. Users must be logged in via Django's session authentication system.

### Authentication Headers

For session-based authentication, ensure the following:
- Include CSRF token in POST requests
- Maintain session cookies from login

### Authentication Errors

If not authenticated, API calls will return:
```http
HTTP 302 Redirect to /auth/login/
```

## Base URL

All API endpoints are prefixed with:
```
/api/
```

## Content Types

- **Request Content-Type**: `application/json`
- **Response Content-Type**: `application/json`

## Error Handling

### Standard Error Response Format

```json
{
    "success": false,
    "error": "Error message description",
    "details": {
        "field_errors": {},
        "code": "error_code"
    }
}
```

### HTTP Status Codes

- `200 OK`: Success
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## API Endpoints

### 1. User Statistics

Get dashboard statistics for the authenticated user.

**Endpoint**: `GET /api/stats/`

**Description**: Returns comprehensive statistics about the user's credentials, notes, and activities.

**Authentication**: Required

**Request**: No request body required

**Response**:
```json
{
    "success": true,
    "total_credentials": 15,
    "total_notes": 8,
    "favorite_credentials": 3,
    "favorite_notes": 2,
    "recent_activities": [
        {
            "id": 123,
            "action": "create_credential",
            "description": "Created Gmail credential",
            "timestamp": "2024-01-15T14:30:00Z",
            "ip_address": "192.168.1.100"
        }
    ],
    "recent_credentials": [
        {
            "id": 456,
            "label": "Gmail Account",
            "type": "email",
            "created_at": "2024-01-15T14:30:00Z",
            "is_favorite": true,
            "last_accessed": "2024-01-16T09:15:00Z"
        }
    ],
    "recent_notes": [
        {
            "id": 789,
            "title": "Important Note",
            "type": "personal",
            "created_at": "2024-01-14T16:45:00Z",
            "is_favorite": false
        }
    ],
    "type_distribution": {
        "email": 5,
        "website": 4,
        "banking": 2,
        "work": 3,
        "social": 1
    }
}
```

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/stats/ \
  -H "Content-Type: application/json" \
  --cookie "sessionid=your_session_id"
```

**Business Logic**: Uses `DashboardManager.get_dashboard_stats()`

---

### 2. Toggle Favorite

Toggle the favorite status of a credential or note.

**Endpoint**: `POST /api/toggle-favorite/`

**Description**: Toggles the favorite status of a specified credential or secure note.

**Authentication**: Required

**Request Body**:
```json
{
    "type": "credential",  // or "note"
    "id": 123
}
```

**Response**:
```json
{
    "success": true,
    "is_favorite": true,
    "message": "Item marked as favorite"
}
```

**Error Response**:
```json
{
    "success": false,
    "error": "Invalid item type or ID"
}
```

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/toggle-favorite/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your_csrf_token" \
  --cookie "sessionid=your_session_id" \
  -d '{"type": "credential", "id": 123}'
```

**Business Logic**: Uses `FavoriteManager.toggle_favorite()`

**Validation**:
- `type` must be either "credential" or "note"
- `id` must be a valid integer
- User must own the specified item

---

### 3. Search

Search across user's credentials and notes.

**Endpoint**: `POST /api/search/`

**Description**: Performs a comprehensive search across the user's credentials and secure notes.

**Authentication**: Required

**Request Body**:
```json
{
    "query": "gmail",
    "type_filter": "email",     // optional
    "favorites_only": false,    // optional
    "limit": 20                // optional, default 20
}
```

**Response**:
```json
{
    "success": true,
    "query": "gmail",
    "total_credentials": 2,
    "total_notes": 1,
    "credentials": [
        {
            "id": 123,
            "label": "Gmail Personal",
            "type": "email",
            "username": "user@gmail.com",
            "email": "user@gmail.com",
            "website_url": "https://gmail.com",
            "is_favorite": true,
            "created_at": "2024-01-15T14:30:00Z",
            "last_accessed": "2024-01-16T09:15:00Z",
            "tags": ["personal", "email"],
            "type_icon": "fas fa-envelope"
        }
    ],
    "notes": [
        {
            "id": 456,
            "title": "Gmail 2FA Backup Codes",
            "type": "personal",
            "is_favorite": false,
            "created_at": "2024-01-14T16:45:00Z",
            "type_icon": "fas fa-user"
        }
    ],
    "filters_applied": {
        "query": "gmail",
        "type_filter": "email",
        "favorites_only": false
    }
}
```

**Search Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | No | Search term to match against labels, usernames, websites, etc. |
| `type_filter` | string | No | Filter by credential type: `email`, `website`, `banking`, `work`, `social`, `personal`, `server`, `api` |
| `favorites_only` | boolean | No | If true, only return favorited items |
| `limit` | integer | No | Maximum number of results per type (default: 20, max: 100) |

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your_csrf_token" \
  --cookie "sessionid=your_session_id" \
  -d '{
    "query": "gmail",
    "type_filter": "email",
    "favorites_only": false,
    "limit": 10
  }'
```

**Business Logic**: Uses `SearchManager.search_all_user_data()`

**Search Behavior**:
- Case-insensitive search
- Searches across: labels, usernames, emails, website URLs, tags, note titles
- Returns exact and partial matches
- Results ordered by relevance and creation date

---

## Data Models

### Credential Object

```json
{
    "id": 123,
    "label": "Service Name",
    "type": "email|website|banking|work|social|personal|server|api",
    "username": "username",
    "email": "user@example.com",
    "website_url": "https://example.com",
    "note": "Additional notes",
    "tags": ["tag1", "tag2"],
    "is_favorite": false,
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-16T09:15:00Z",
    "last_accessed": "2024-01-16T09:15:00Z",
    "type_icon": "fas fa-envelope"
}
```

**Note**: Password and secret key fields are not included in API responses for security.

### Secure Note Object

```json
{
    "id": 456,
    "title": "Note Title",
    "type": "personal|work|finance|health|other",
    "is_favorite": false,
    "created_at": "2024-01-14T16:45:00Z",
    "updated_at": "2024-01-15T10:20:00Z",
    "type_icon": "fas fa-user"
}
```

**Note**: Content field is not included in API responses for security.

### Activity Log Object

```json
{
    "id": 789,
    "action": "create_credential",
    "description": "Created Gmail credential",
    "timestamp": "2024-01-15T14:30:00Z",
    "ip_address": "192.168.1.100"
}
```

## Business Logic Classes

The API endpoints delegate to specialized business logic classes:

### DashboardManager
- `get_dashboard_stats(user)`: Get comprehensive dashboard statistics

### FavoriteManager
- `toggle_favorite(item, user)`: Toggle favorite status
- `get_user_favorites(user)`: Get all user favorites

### SearchManager
- `search_all_user_data(user, **params)`: Comprehensive search
- `search_credentials(user, **params)`: Search credentials only
- `search_notes(user, **params)`: Search notes only

### ActivityManager
- `log_activity(user, action, description, ip=None)`: Log user activity
- `get_user_activities(user, limit=10)`: Get recent activities

### CredentialsManager
- `get_user_credentials(user, search_params=None)`: Get credentials with filtering
- `create_credential(user, form_data)`: Create new credential
- `update_credential(credential, form_data)`: Update existing credential
- `delete_credential(credential)`: Delete credential

### SecureNotesManager
- `get_user_notes(user, search_params=None)`: Get notes with filtering
- `create_note(user, form_data)`: Create new note
- `update_note(note, form_data)`: Update existing note
- `delete_note(note)`: Delete note

## Security Considerations

### Data Encryption
- All sensitive fields (passwords, secret keys, note content) are encrypted at rest
- Encryption uses Fernet symmetric encryption with a project-specific key
- Encrypted fields are never returned in API responses

### Access Control
- Users can only access their own data
- All database queries are filtered by the authenticated user
- Cross-user data access is prevented at the business logic layer

### CSRF Protection
- All POST/PUT/DELETE requests require valid CSRF tokens
- CSRF tokens can be obtained from Django's CSRF cookie

### Rate Limiting
Consider implementing rate limiting for production:
- Search API: 100 requests per minute per user
- Toggle favorite: 50 requests per minute per user
- Stats API: 20 requests per minute per user

## Performance Considerations

### Database Optimization
- Queries use `select_related()` and `prefetch_related()` where appropriate
- Indexes are present on frequently searched fields
- Pagination is implemented for large result sets

### Caching
- Dashboard stats can be cached for 5 minutes
- Search results can be cached for 1 minute
- Use Django's cache framework for implementation

### Response Size
- API responses are limited to essential data
- Large text fields (content, notes) are excluded from list views
- Use pagination for collections with many items

## Development and Testing

### Running Tests
```bash
# Run all backend tests
python manage.py test apps.backend

# Run API-specific tests
python manage.py test apps.backend.tests.APIEndpointsTestCase

# Run with coverage
coverage run --source='.' manage.py test apps.backend
coverage html
```

### API Testing Examples

Using Python requests:
```python
import requests

# Login first
session = requests.Session()
login_data = {'username': 'testuser', 'password': 'password'}
session.post('http://localhost:8000/auth/login/', data=login_data)

# Get CSRF token
csrf_token = session.cookies['csrftoken']

# Call API
headers = {'X-CSRFToken': csrf_token, 'Content-Type': 'application/json'}
response = session.get('http://localhost:8000/api/stats/', headers=headers)
print(response.json())
```

Using JavaScript (from frontend):
```javascript
// Get CSRF token
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Call API
fetch('/api/stats/', {
    method: 'GET',
    headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
    },
    credentials: 'same-origin'
})
.then(response => response.json())
.then(data => console.log(data));
```

## Error Examples

### Invalid Authentication
```json
{
    "success": false,
    "error": "Authentication required",
    "details": {
        "code": "authentication_required"
    }
}
```

### Invalid Request Data
```json
{
    "success": false,
    "error": "Invalid request data",
    "details": {
        "field_errors": {
            "type": ["This field is required"],
            "id": ["Invalid value"]
        },
        "code": "validation_error"
    }
}
```

### Resource Not Found
```json
{
    "success": false,
    "error": "Credential not found or access denied",
    "details": {
        "code": "not_found"
    }
}
```

### Server Error
```json
{
    "success": false,
    "error": "Internal server error",
    "details": {
        "code": "server_error"
    }
}
```

## Changelog

### Version 1.0.0 (Current)
- Initial API implementation
- User statistics endpoint
- Toggle favorite functionality
- Comprehensive search API
- Full authentication and authorization

### Future Enhancements
- Bulk operations API
- Data export API endpoints  
- Webhook support for activity notifications
- GraphQL API implementation
- API versioning support 