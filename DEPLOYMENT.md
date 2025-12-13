# 🚀 Job Scope - Deployment Guide

## Quick Deployment Options

### Option 1: Deploy to Render (Recommended - Free Tier Available)

#### Backend Deployment
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: job-scope-api
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt && python train_lda_model.py`
   - **Start Command**: `cd backend && python server.py`
   - **Instance Type**: Free
5. Add Environment Variables:
   - `FLASK_ENV=production`
   - `JWT_SECRET_KEY=your-secret-key-here`
   - `FRONTEND_URL=https://your-frontend-url.vercel.app`
6. Click "Create Web Service"

#### Frontend Deployment
1. Go to [vercel.com](https://vercel.com) and sign up
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: build
5. Add Environment Variable:
   - `REACT_APP_API_URL=https://your-backend-url.onrender.com`
6. Click "Deploy"

---

### Option 2: Deploy to Heroku

#### Prerequisites
```bash
# Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login
```

#### Backend Deployment
```bash
cd c:\Users\ASUS\Desktop\job-matching-project

# Create Heroku app
heroku create job-scope-api

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set JWT_SECRET_KEY=your-super-secret-key-here
heroku config:set FRONTEND_URL=https://your-frontend.vercel.app

# Deploy
git init
git add .
git commit -m "Deploy Job Scope"
git push heroku main

# View your app
heroku open
```

#### Frontend Deployment (Vercel)
```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Set production environment variable
vercel env add REACT_APP_API_URL production
# Enter: https://job-scope-api.herokuapp.com

# Deploy to production
vercel --prod
```

---

### Option 3: Deploy to Railway (Easiest)

#### All-in-One Deployment
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect and deploy both backend and frontend
6. Add environment variables in the Railway dashboard:
   - `FLASK_ENV=production`
   - `JWT_SECRET_KEY=your-secret-key`
   - `REACT_APP_API_URL=${{RAILWAY_STATIC_URL}}`
7. Done! Railway provides URLs for both services

---

## Pre-Deployment Checklist

### 1. Update CORS Configuration
Edit `backend/app/__init__.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # Local development
            "https://your-frontend.vercel.app",  # Production
            "https://your-domain.com"  # Custom domain
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 2. Update Frontend API URL
Edit `frontend/src/services/api.js`:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

### 3. Build Frontend for Production
```bash
cd frontend
npm run build
# Creates optimized production build in build/ folder
```

### 4. Test Production Build Locally
```bash
# Install serve
npm install -g serve

# Serve production build
serve -s build -p 3000
```

---

## Environment Variables Summary

### Backend (.env)
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key-minimum-32-characters
JWT_SECRET_KEY=your-jwt-secret-key-minimum-32-characters
DATABASE_URL=sqlite:///job_matching.db
FRONTEND_URL=https://your-frontend-url.com
```

### Frontend (.env.production)
```
REACT_APP_API_URL=https://your-backend-api-url.com
```

---

## Generate Secure Secret Keys

```bash
# Python method
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use this PowerShell command
[System.Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
```

---

## Post-Deployment Testing

### Test Backend API
```bash
# Health check
curl https://your-backend-url.com/api/health

# Register user
curl -X POST https://your-backend-url.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'

# Login
curl -X POST https://your-backend-url.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'
```

### Test Frontend
1. Open your deployed URL
2. Register a new account
3. Upload a sample CV
4. Verify job matches appear

---

## Common Issues & Solutions

### Issue: "Model not found" error
**Solution**: Ensure `train_lda_model.py` runs during build
```bash
# Add to build command
cd backend && python train_lda_model.py
```

### Issue: CORS errors in browser
**Solution**: Update CORS origins in `backend/app/__init__.py`
```python
origins=["https://your-actual-frontend-url.com"]
```

### Issue: "Module not found" errors
**Solution**: Ensure all dependencies are in requirements.txt
```bash
cd backend
pip freeze > requirements.txt
```

### Issue: Frontend can't connect to backend
**Solution**: Set REACT_APP_API_URL environment variable
```bash
# In Vercel/Netlify dashboard
REACT_APP_API_URL=https://your-backend-url.com
```

---

## Monitoring & Maintenance

### View Logs
```bash
# Heroku
heroku logs --tail -a job-scope-api

# Render
# View logs in Render dashboard

# Railway
# View logs in Railway dashboard
```

### Database Backup
```bash
# Download SQLite database
heroku run "cd backend/instance && cat job_matching.db" > backup.db
```

---

## Custom Domain (Optional)

### Add Custom Domain to Vercel
1. Go to project settings → Domains
2. Add your domain (e.g., jobscope.com)
3. Update DNS records as instructed
4. SSL certificate auto-generated

### Add Custom Domain to Render/Heroku
1. Go to settings → Custom Domains
2. Add domain
3. Update DNS CNAME record
4. SSL auto-configured

---

## Need Help?

**Which platform should I use?**
- **Beginners**: Railway (easiest setup)
- **Free tier**: Render + Vercel
- **Established projects**: Heroku
- **Full control**: AWS/DigitalOcean

**Next Steps:**
1. Choose your platform
2. Follow the specific guide above
3. Set environment variables
4. Deploy!
5. Test thoroughly

---

**Status**: Ready to Deploy ✅  
**Estimated Time**: 15-30 minutes  
**Cost**: Free tier available on all platforms
