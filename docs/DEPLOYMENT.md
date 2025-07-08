# Railway Deployment Guide for Credentials Manager

This guide will walk you through deploying your Django Credentials Manager to Railway.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)
3. **PostgreSQL Database**: Railway provides managed PostgreSQL

## Step 1: Prepare Your Project

### 1.1 Files Already Created
✅ `Procfile` - Defines how Railway runs your app
✅ `railway.toml` - Railway-specific configuration
✅ `runtime.txt` - Specifies Python version
✅ `requirements.txt` - Python dependencies

### 1.2 Verify Settings
Your `core/settings.py` is already configured for production with:
- Environment variable support via `python-decouple`
- Database URL parsing with `dj-database-url`
- Static file serving with `whitenoise`
- Proper security settings

## Step 2: Deploy to Railway

### 2.1 Create New Project
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your credentials manager repository

### 2.2 Add PostgreSQL Database
1. In your Railway project dashboard
2. Click "New" → "Database" → "Add PostgreSQL"
3. Railway will automatically create a `DATABASE_URL` environment variable

### 2.3 Configure Environment Variables

In Railway dashboard, go to your service → Variables and add:

#### Required Variables:
```bash
# Django Configuration
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,*.railway.app

# Database (auto-created by Railway PostgreSQL)
DATABASE_URL=postgresql://... (automatically set by Railway)

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email (optional - configure if you want email features)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

#### Optional Variables:
```bash
# Cache (Redis - if you add Redis service)
REDIS_URL=redis://...

# App Configuration
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
PAGINATION_SIZE=12

# Admin
ADMIN_URL=secure-admin-url/

# Backup (if implementing)
BACKUP_ENABLED=False
```

### 2.4 Generate SECRET_KEY
Run this in your local terminal to generate a secure secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 3: Deploy and Test

### 3.1 Trigger Deployment
1. Push your changes to your Git repository
2. Railway will automatically detect changes and deploy
3. Monitor the build logs in Railway dashboard

### 3.2 Check Deployment
1. Visit your Railway app URL (found in dashboard)
2. You should see your credentials manager
3. Check `/health/` endpoint for health status

### 3.3 Create Superuser (Important!)
After successful deployment, create an admin user:

1. In Railway dashboard, go to your service
2. Click "Settings" → "Deploy"
3. Under "Build Command" temporarily change to:
   ```bash
   python manage.py migrate && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'your-secure-password')" | python manage.py shell
   ```
4. Redeploy, then change it back to the original build command

Or use Railway's terminal feature if available.

## Step 4: Post-Deployment Setup

### 4.1 Test Core Features
- [ ] User registration/login
- [ ] Credential creation/viewing
- [ ] Secure note creation/viewing
- [ ] Search functionality
- [ ] Favorite toggling
- [ ] Data export

### 4.2 Configure Custom Domain (Optional)
1. In Railway dashboard → Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed

### 4.3 Monitor Application
- Check Railway logs for any errors
- Monitor database usage
- Set up alerts if needed

## Step 5: Production Security Checklist

### 5.1 Environment Variables Security
- [ ] SECRET_KEY is unique and secure
- [ ] DEBUG=False in production
- [ ] Database credentials are secure
- [ ] Email credentials are app-specific passwords

### 5.2 Application Security
- [ ] HTTPS is enforced (Railway provides this)
- [ ] Admin URL is changed from default
- [ ] Strong password policies are enforced
- [ ] Regular security updates

### 5.3 Data Protection
- [ ] Database backups are configured
- [ ] Encryption keys are secure
- [ ] User data is properly encrypted

## Troubleshooting

### Common Issues:

#### 1. Static Files Not Loading
```bash
# In Railway environment variables, ensure:
DISABLE_COLLECTSTATIC=0
```

#### 2. Database Connection Errors
- Verify DATABASE_URL is set correctly
- Check if PostgreSQL service is running
- Ensure your IP isn't blocked

#### 3. Application Won't Start
- Check Railway build logs
- Verify all required environment variables are set
- Check Python/Django versions compatibility

#### 4. CSRF Token Issues
```bash
# Add to environment variables:
CSRF_TRUSTED_ORIGINS=https://your-app-name.railway.app
```

### Getting Help:
1. Check Railway documentation
2. Review Django deployment guides
3. Monitor application logs in Railway dashboard

## Useful Commands

### Local Development with Production Settings
```bash
# Test with production-like settings
export DEBUG=False
export DATABASE_URL=sqlite:///prod_test.db
python manage.py runserver
```

### Backup Database (if needed)
```bash
# Local backup
python manage.py dumpdata > backup.json

# Restore backup
python manage.py loaddata backup.json
```

## Cost Optimization

### Railway Pricing Tips:
1. Monitor resource usage in dashboard
2. Use sleep mode for development apps
3. Optimize database queries to reduce CPU usage
4. Use Railway's built-in metrics

---

**🎉 Your Credentials Manager should now be live on Railway!**

Visit your app URL and test all functionality. Remember to keep your environment variables secure and regularly update your dependencies. 