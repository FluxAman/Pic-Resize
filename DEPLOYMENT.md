# Deployment Guide for Render

This guide will help you deploy the Pic-resize Django application to Render.

## Prerequisites

- A [Render](https://render.com) account
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
- PostgreSQL database configured on Render

## Pre-Deployment Checklist

- [x] All dependencies have version numbers in `requirements.txt`
- [x] `SECRET_KEY` uses environment variable
- [x] `DEBUG` is set to `False` in production
- [x] Security headers configured for production
- [x] Static files configuration with WhiteNoise
- [x] Database configuration uses `dj-database-url`
- [x] Build script (`build.sh`) is ready

## Deployment Steps

### 1. Create PostgreSQL Database

1. Log in to your Render dashboard
2. Click **New** → **PostgreSQL**
3. Configure your database:
   - **Name**: `pic-resize-db`
   - **Database**: `pic_resize`
   - **User**: `pic_resize_user`
   - **Region**: Choose closest to your users
   - **Plan**: Select appropriate plan (Free tier available)
4. Click **Create Database**
5. Wait for the database to be provisioned

### 2. Create Web Service

1. Click **New** → **Web Service**
2. Connect your Git repository
3. Configure the service:
   - **Name**: `pic-resize`
   - **Environment**: `Python 3`
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

### 3. Configure Environment Variables

In the Render dashboard, add the following environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `SECRET_KEY` | *Auto-generated* | Render will generate this automatically |
| `DATABASE_URL` | *From database* | Link to your PostgreSQL database |
| `DEBUG` | `False` | **Important**: Must be False for production |
| `WEB_CONCURRENCY` | `4` | Number of Gunicorn workers |
| `PYTHON_VERSION` | `3.11.0` | Python version to use |
| `RENDER_EXTERNAL_HOSTNAME` | `your-app.onrender.com` | Your Render app URL (without https://) |

**To link the database:**
1. For `DATABASE_URL`, select **Add from Database** → Choose your `pic-resize-db`
2. This automatically connects your web service to the database

**To auto-generate SECRET_KEY:**
1. Click **Generate** next to the SECRET_KEY field
2. Render will create a secure random key

### 4. Deploy

1. Click **Create Web Service**
2. Render will automatically:
   - Clone your repository
   - Run `build.sh` (install dependencies, collect static files, run migrations)
   - Start your application with Gunicorn
3. Monitor the deployment logs for any errors

### 5. Post-Deployment Verification

Once deployed, verify the following:

#### ✅ Application Health
- [ ] Visit your app URL: `https://your-app.onrender.com`
- [ ] Homepage loads without errors
- [ ] Static files (CSS, JS, images) load correctly

#### ✅ Authentication
- [ ] User registration works
- [ ] Login functionality works
- [ ] Google OAuth works (if configured)
- [ ] Logout works

#### ✅ Core Features
- [ ] Image upload works
- [ ] Image processing (resize, filters, crop) works
- [ ] Processed images can be saved
- [ ] Profile page displays saved images
- [ ] Media files are accessible

#### ✅ Security
- [ ] HTTPS is enforced (Render provides this automatically)
- [ ] DEBUG is False (check by triggering a 404 - should show generic error page)
- [ ] Admin panel is accessible at `/admin`

## Troubleshooting

### Build Fails

**Issue**: Dependencies fail to install
- Check `requirements.txt` for syntax errors
- Ensure all version numbers are valid
- Check Render logs for specific error messages

**Issue**: Static files collection fails
- Verify `STATIC_ROOT` is set correctly in `settings.py`
- Check that `whitenoise` is installed

### Application Won't Start

**Issue**: `ALLOWED_HOSTS` error
- Verify `RENDER_EXTERNAL_HOSTNAME` is set correctly
- Should be just the domain: `your-app.onrender.com` (no `https://`)

**Issue**: Database connection error
- Verify `DATABASE_URL` is linked to your PostgreSQL database
- Check database is running and accessible

### Static Files Not Loading

**Issue**: CSS/JS files return 404
- Run `python manage.py collectstatic` locally to test
- Verify `WhiteNoiseMiddleware` is in `MIDDLEWARE` settings
- Check `STATICFILES_STORAGE` is set to WhiteNoise

### Media Files Not Persisting

**Issue**: Uploaded images disappear after deployment
- **Note**: Render's free tier uses ephemeral storage
- Consider using cloud storage (AWS S3, Cloudinary) for production
- For testing, files will persist during the current deployment

## Updating Your Application

To deploy updates:

1. Push changes to your Git repository
2. Render will automatically detect changes and redeploy
3. Or manually trigger deployment from Render dashboard

## Environment-Specific Settings

### Development
```bash
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (Render)
```bash
DEBUG=False
RENDER_EXTERNAL_HOSTNAME=your-app.onrender.com
SECRET_KEY=<auto-generated>
DATABASE_URL=<from-database>
```

## Additional Configuration

### Custom Domain

1. Go to your web service settings
2. Click **Custom Domains**
3. Add your domain and follow DNS configuration instructions

### Scaling

1. Go to your web service settings
2. Upgrade to a paid plan for:
   - More resources (CPU/RAM)
   - Faster build times
   - No sleep on inactivity
   - Persistent storage options

## Support

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- Check Render logs for detailed error messages

## Security Best Practices

- ✅ Never commit `.env` files or secrets to Git
- ✅ Use environment variables for all sensitive data
- ✅ Keep `DEBUG=False` in production
- ✅ Regularly update dependencies for security patches
- ✅ Use HTTPS (Render provides this automatically)
- ✅ Set strong `SECRET_KEY` (auto-generated by Render)
