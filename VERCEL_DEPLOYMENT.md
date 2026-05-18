# Employee Payroll Management System - Vercel Deployment Guide

## Files Added/Modified for Vercel Deployment:

### 1. **requirements.txt** ✅
   - Contains all Python dependencies
   - Includes Django, gunicorn, and python-decouple

### 2. **.python-version** ✅
   - Specifies Python 3.12 version for Vercel build

### 3. **vercel.json** ✅
   - Vercel deployment configuration
   - Routes API and static file handling

### 4. **wsgi.py** ✅
   - Entry point for Vercel WSGI application

### 5. **epms/settings.py (Updated)** ✅
   - Added `import os` for environment variables
   - Changed DEBUG from hardcoded True to `os.getenv('DEBUG', 'False')`
   - Changed ALLOWED_HOSTS to accept Vercel domains
   - Added STATIC_ROOT for static file collection
   - Made SECRET_KEY configurable via environment variable

### 6. **.env.example** ✅
   - Template for environment variables
   - Set appropriate values in Vercel dashboard

### 7. **.vercelignore** ✅
   - Tells Vercel which files to ignore during build

### 8. **build.sh** ✅
   - Build script for Vercel deployments

## Deployment Steps on Vercel:

1. **Connect Your Repository**
   - Go to https://vercel.com/new
   - Connect your GitHub repository

2. **Configure Environment Variables**
   - In Vercel project settings, add:
     - `SECRET_KEY` - Generate a secure key
     - `DEBUG` - Set to `False`

3. **Deploy**
   - Vercel will automatically:
     - Install dependencies from requirements.txt
     - Build the application
     - Run migrations
     - Collect static files

## Important Notes:

⚠️ **Database**: SQLite won't work well in production (read-only filesystem). Consider:
   - PostgreSQL (recommended)
   - MySQL
   - Or use environment-based database config

⚠️ **Static Files**: Configure CDN or use Vercel's storage

⚠️ **Environment Variables**: Set all secrets in Vercel dashboard, never commit .env files

⚠️ **Media Files**: Vercel's filesystem is ephemeral. Use external storage (AWS S3, Cloudinary, etc.)

## Next Steps:

1. Test locally: `python manage.py runserver`
2. Push to GitHub
3. Deploy to Vercel
4. Monitor logs for any issues
