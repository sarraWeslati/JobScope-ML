# 🚀 Quick Deployment - Job Scope

## ✅ Your Secure Keys (Generated)

Copy these keys - you'll need them for deployment:

```
SECRET_KEY=7wqPk3Bc27Jg3W7eN-COm91cSdJl2J2R3kb2kir1bio
JWT_SECRET_KEY=S6DYsXxDpMLkUsJJnhzKHjnVRpSPxp2vDrV7bS75ZBo
```

---

## 🎯 Recommended: Deploy to Render + Vercel (FREE)

### Step 1: Prepare Your Code

1. **Create GitHub Repository**
```bash
cd c:\Users\ASUS\Desktop\job-matching-project
git init
git add .
git commit -m "Initial commit - Job Scope"

# Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/job-scope.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend to Render

1. Go to **[render.com](https://render.com)** → Sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `job-scope-api`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```
     cd backend && pip install -r requirements.txt && python train_lda_model.py
     ```
   - **Start Command**: 
     ```
     cd backend && python server.py
     ```
   - **Instance Type**: `Free`

5. **Add Environment Variables** (click "Advanced"):
   ```
   FLASK_ENV=production
   SECRET_KEY=7wqPk3Bc27Jg3W7eN-COm91cSdJl2J2R3kb2kir1bio
   JWT_SECRET_KEY=S6DYsXxDpMLkUsJJnhzKHjnVRpSPxp2vDrV7bS75ZBo
   ```

6. Click **"Create Web Service"**
7. Wait 5-10 minutes for deployment
8. **Copy your backend URL** (e.g., `https://job-scope-api.onrender.com`)

### Step 3: Deploy Frontend to Vercel

1. Go to **[vercel.com](https://vercel.com)** → Sign up (free)
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: `Create React App`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

5. **Add Environment Variable**:
   ```
   REACT_APP_API_URL=https://job-scope-api.onrender.com
   ```
   (Use your Render backend URL from Step 2)

6. Click **"Deploy"**
7. Wait 2-3 minutes
8. **Your app is live!** 🎉

### Step 4: Update CORS

After frontend is deployed, update backend CORS:

1. Go to Render dashboard → Your service → Environment
2. Add:
   ```
   FRONTEND_URL=https://your-app.vercel.app
   ```
3. Click "Save Changes" (service will redeploy)

---

## 🔥 Alternative: Deploy to Railway (EASIER)

1. Go to **[railway.app](https://railway.app)**
2. Click **"Start a New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects everything!
5. Add environment variables in dashboard:
   ```
   FLASK_ENV=production
   SECRET_KEY=7wqPk3Bc27Jg3W7eN-COm91cSdJl2J2R3kb2kir1bio
   JWT_SECRET_KEY=S6DYsXxDpMLkUsJJnhzKHjnVRpSPxp2vDrV7bS75ZBo
   ```
6. Done! Railway gives you URLs for both services

---

## 📋 Pre-Deployment Checklist

Before deploying, run these commands:

### 1. Test Backend Locally
```bash
cd backend
python server.py
# Should run without errors
```

### 2. Test Frontend Build
```bash
cd frontend
npm run build
# Should create build/ folder
```

### 3. Verify Model Files Exist
```bash
cd backend/final_model
dir
# Should show: lda_model.joblib, count_vectorizer.joblib, etc.
```

### 4. Update CORS (Important!)
Edit `backend/app/__init__.py` and add your production URL:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "https://*.vercel.app",  # Vercel domains
            "https://*.onrender.com"  # Render domains
        ]
    }
})
```

---

## 🧪 Test After Deployment

### Test Backend
```bash
# Replace with your actual URL
curl https://job-scope-api.onrender.com/api/health
```

### Test Full Flow
1. Open your Vercel URL
2. Register a new account
3. Login
4. Upload a CV file
5. Verify job matches appear

---

## 💡 Tips

- **First deployment takes 10-15 minutes** (model training)
- **Free tiers have cold starts** (~30 seconds when idle)
- **Render free tier sleeps after 15 min inactivity**
- **Keep your secret keys safe** - don't commit to GitHub
- **Monitor logs** in platform dashboards

---

## 🆘 Need Help?

### Common Issues

**"Model not found" error**
→ Ensure build command includes `python train_lda_model.py`

**CORS errors**
→ Add frontend URL to `FRONTEND_URL` env variable

**"Connection refused"**
→ Check backend URL in `REACT_APP_API_URL`

**Build fails**
→ Check logs in deployment dashboard

---

## 📞 Support

If you get stuck:
1. Check deployment logs in platform dashboard
2. Verify all environment variables are set
3. Test backend health endpoint
4. Review [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed guide

---

**Ready to deploy?** Pick your platform and follow the steps above! 🚀

**Estimated time:** 20-30 minutes  
**Cost:** $0 (using free tiers)  
**Result:** Live Job Scope application! ✅
