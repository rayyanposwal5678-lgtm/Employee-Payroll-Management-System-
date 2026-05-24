# Employee Payroll Management System - Vercel Deployment Guide

## ✅ Pre-Deployment Checklist

All necessary files have been configured for Vercel deployment:

### 1. **Configuration Files**
- ✅ `vercel.json` - Vercel deployment configuration
- ✅ `wsgi.py` - WSGI entry point with WhiteNoise middleware
- ✅ `.python-version` - Specifies Python 3.12
- ✅ `.vercelignore` - Files to ignore during build
- ✅ `build.sh` - Automated build script
- ✅ `.gitignore` - Prevents committing sensitive files

### 2. **Django Settings** (epms/settings.py)
- ✅ `DEBUG` - Environment variable based (defaults to False)
- ✅ `SECRET_KEY` - Environment variable based
- ✅ `ALLOWED_HOSTS` - Environment variable based
- ✅ `STATIC_ROOT` - Configured for `staticfiles/`
- ✅ `STATIC_URL` - Set to `/static/`
- ✅ WhiteNoise middleware enabled for static file serving
- ✅ Security settings for production (HTTPS, HSTS, cookies)

### 3. **Dependencies** (requirements.txt)
- ✅ Django 5.2.9
- ✅ gunicorn 23.0.0
- ✅ python-decouple 3.8
- ✅ whitenoise 6.6.0 (Static file serving)
- ✅ psycopg2-binary 2.9.9 (PostgreSQL support)
- ✅ APScheduler 3.10.4 (Scheduled tasks)

### 4. **Environment Configuration**
- ✅ `.env.example` - Template with all required variables
- ✅ `.gitignore` - Prevents committing sensitive files

---

## 🚀 Deployment Steps on Vercel

### Step 1: Prepare Your Git Repository
```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Connect to Vercel
1. Go to https://vercel.com/new
2. Select "Import Git Repository"
3. Connect your GitHub account and select this repository
4. Select the root directory as the project root

### Step 3: Configure Environment Variables
In the Vercel Dashboard, go to **Settings** → **Environment Variables** and add:

**Required Variables:**
```
DEBUG=False
SECRET_KEY=generate-a-secure-random-string-here
ALLOWED_HOSTS=yourdomain.vercel.app,www.yourdomain.com,yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.vercel.app,https://www.yourdomain.com
PYTHON_VERSION=3.12
```

**Optional Database Variables** (if using PostgreSQL):
```
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Step 4: Generate a Secure SECRET_KEY
In your terminal, run:
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Copy the output and paste it as the `SECRET_KEY` environment variable in Vercel.

### Step 5: Deploy
1. Click "Deploy" button
2. Wait for the build to complete (usually 1-2 minutes)
3. Your app will be available at `https://your-project.vercel.app`

---

## 🗄️ Database Configuration

### SQLite (Current - Not Recommended for Production)
- Works locally but has limitations on Vercel's filesystem
- Suitable only for testing/development

### PostgreSQL (Recommended for Production)
1. Create a PostgreSQL database on Heroku, AWS RDS, or Supabase
2. Add `DATABASE_URL` environment variable to Vercel
3. Uncomment PostgreSQL settings in `epms/settings.py` (if added)
4. Run migrations:
   ```bash
   python manage.py migrate --database=default
   ```

---

## 📁 Static Files Handling

WhiteNoise is configured to serve static files:
1. During build, `python manage.py collectstatic` runs automatically
2. Static files are collected to `staticfiles/` directory
3. WhiteNoise serves them with proper caching headers
4. CSS, JS, and images are available immediately

---

## 🔐 Security Configuration

Production security settings are automatically enabled when `DEBUG=False`:
- ✅ HTTPS redirect (SECURE_SSL_REDIRECT)
- ✅ HTTP Strict Transport Security (HSTS)
- ✅ Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- ✅ CSRF protection with trusted origins
- ✅ X-Frame-Options header for clickjacking protection

---

## ✅ Post-Deployment Steps

### 1. Create Superuser
```bash
# Via Vercel CLI (recommended)
vercel env pull .env.local
vercel run "python manage.py createsuperuser"
```

Or use the web interface if accessible.

### 2. Run Migrations
The build script automatically runs migrations. Check the build logs:
```bash
vercel logs <project-id>
```

### 3. Test Your Application
1. Visit your deployment URL
2. Check the admin panel at `/admin/`
3. Login with superuser credentials
4. Verify all pages load correctly

### 4. Setup Monitoring
- Enable Vercel Analytics
- Setup error tracking (e.g., Sentry)
- Monitor database performance

---

## 🐛 Troubleshooting

### Build Fails with "Static files not found"
```bash
# Clear and rebuild
python manage.py collectstatic --noinput --clear
git add staticfiles/
git commit -m "Update static files"
git push
```

### 500 Error After Deployment
1. Check Vercel logs: `vercel logs <project-id> --follow`
2. Common issues:
   - Missing environment variables
   - Database connection string incorrect
   - Static files not collected
   - SECRET_KEY not set

### CSRF Token Mismatch
- Ensure `CSRF_TRUSTED_ORIGINS` includes your domain
- Check that cookies are sent with requests (not blocked)

### Database Connection Error
- Verify database URL is correct
- Check database is accessible from Vercel (IP allowlist)
- Ensure database user has proper permissions

---

## 📝 Local Testing Before Deployment

### 1. Test with Production Settings
```bash
# Set environment variables locally
export DEBUG=False
export SECRET_KEY="your-secret-key"
export ALLOWED_HOSTS="localhost,127.0.0.1"

# Collect static files
python manage.py collectstatic --noinput --clear

# Run the server
python manage.py runserver
```

### 2. Test Static Files
```bash
# Verify CSS/JS loads
curl -I http://localhost:8000/static/css/style.css
```

### 3. Test Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔄 Updates and Redeployment

To redeploy after code changes:
1. Commit your changes locally
2. Push to your Git repository
3. Vercel automatically redeploys (if auto-deploy is enabled)

---

## 📚 Additional Resources

- [Vercel Django Documentation](https://vercel.com/guides/deploying-django-with-vercel)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

---

## ✨ Notes

- **Automatic Builds**: Enabled on push to main branch
- **Build Duration**: Usually 1-2 minutes
- **Scaling**: Serverless functions scale automatically
- **Costs**: Generous free tier available

**Status**: ✅ Ready for Production Deployment
