# Quick Start - Deploying to Vercel

## ⚡ 5-Minute Quick Start

### Step 1: Generate SECRET_KEY (1 minute)
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Copy the output - you'll need it.

### Step 2: Commit & Push (1 minute)
```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### Step 3: Create Vercel Project (1 minute)
1. Go to https://vercel.com/new
2. Connect your GitHub repository
3. Select your Employee Payroll repo

### Step 4: Set Environment Variables (1 minute)
In Vercel Dashboard → Settings → Environment Variables:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Paste the generated key |
| `ALLOWED_HOSTS` | `your-project.vercel.app` |
| `PYTHON_VERSION` | `3.12` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-project.vercel.app` |

### Step 5: Deploy (1 minute)
1. Click "Deploy"
2. Wait for build to complete (usually 2 minutes)
3. Once deployed, you'll get a live URL like `https://your-project.vercel.app`

### Step 6: Create Admin User (1 minute)
In terminal:
```bash
vercel env pull .env.local
vercel run "python manage.py createsuperuser"
```

### Step 7: Test
- Visit your deployment URL
- Go to `/admin/`
- Login with your admin credentials
- ✓ Done!

---

## 🔧 Troubleshooting

### Build Failed Error?
Check the logs:
```bash
vercel logs your-project-id --follow
```

### 500 Error on visit?
1. Check environment variables are set
2. Check logs: `vercel logs your-project-id`
3. Ensure SECRET_KEY is set

### Static files missing?
1. Verify WhiteNoise is configured (✓ already done)
2. Check build logs for collectstatic errors

### Database errors?
- Currently using SQLite (works fine for testing)
- For production data persistence, set up PostgreSQL

---

## 📚 Full Documentation

For detailed information, see:
- `VERCEL_DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Pre/post deployment checklist
- `CHANGES_SUMMARY.md` - All changes made for deployment

---

## ✅ What's Already Done

- [x] Django settings configured for production
- [x] WhiteNoise integrated for static files
- [x] Environment variables properly handled
- [x] Security settings enabled
- [x] All dependencies updated
- [x] Documentation created
- [x] Code tested and verified

**Status: READY TO DEPLOY!** 🚀

