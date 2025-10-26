# Deployment Guide for MuzScale

## Overview

MuzScale is a Flask-based web application that requires a Python backend server to run. **GitHub Pages does not support Flask applications** as it only hosts static HTML/CSS/JavaScript files. Therefore, this application needs to be deployed to a platform that supports Python web applications.

## Why Can't This Be Deployed on GitHub Pages?

GitHub Pages is a static site hosting service that:
- Only serves HTML, CSS, and JavaScript files
- Cannot run Python code or Flask applications
- Cannot handle server-side processing
- Does not support API integrations requiring backend logic

Since MuzScale uses:
- Flask web framework (Python backend)
- DeepAI API calls (server-side processing)
- File uploads and processing
- Dynamic content generation

It requires a platform that can run Python applications.

## Recommended Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

[Render](https://render.com) offers free hosting for web services with automatic deployments from GitHub.

#### Steps to Deploy on Render:

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up using your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `abdulmoiz0portfolio/muzscale`
   - Grant Render access to the repository

3. **Configure the Service**
   - **Name**: `muzscale` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (Note: Add `gunicorn` to requirements.txt)
   - **Plan**: Select "Free"

4. **Add Environment Variables**
   - Go to "Environment" tab
   - Add: `DEEPAI_API_KEY` = `your_deepai_api_key`
   - (Get your API key from https://deepai.org/dashboard/profile)

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Your app will be available at: `https://muzscale.onrender.com`

#### Update requirements.txt for Render:

Add `gunicorn` to your `requirements.txt`:
```
Flask==2.3.2
Werkzeug==2.3.6
requests==2.31.0
gunicorn==21.2.0
```

### Option 2: Railway

[Railway](https://railway.app) provides simple deployment with GitHub integration.

#### Steps:

1. Go to https://railway.app and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `abdulmoiz0portfolio/muzscale`
4. Railway will auto-detect Flask and deploy
5. Add environment variable: `DEEPAI_API_KEY`
6. Your app will be available at a Railway subdomain

### Option 3: Heroku

[Heroku](https://heroku.com) is a popular platform for deploying web applications.

#### Steps:

1. **Create a Heroku Account**
   - Sign up at https://heroku.com

2. **Create a Procfile**
   - Create a file named `Procfile` (no extension) in the repository root:
   ```
   web: gunicorn app:app
   ```

3. **Deploy via Heroku CLI or GitHub Integration**
   - Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
   - Run:
   ```bash
   heroku login
   heroku create muzscale
   git push heroku main
   heroku config:set DEEPAI_API_KEY=your_api_key
   ```

### Option 4: PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com) specializes in Python web apps.

#### Steps:

1. Create a free account at https://www.pythonanywhere.com
2. Go to "Web" tab → "Add a new web app"
3. Choose "Flask" framework
4. Upload your code or clone from GitHub
5. Configure the WSGI file to point to your app
6. Set environment variables in the web app settings

## Linking Your Deployment to GitHub

Once deployed, you can link your live application to your GitHub repository:

1. **Update README.md**
   - Add a "Live Demo" section with your deployment URL
   - Example:
   ```markdown
   ## Live Demo
   
   🚀 **[View Live Application](https://muzscale.onrender.com)**
   
   The application is deployed on Render and automatically updates with each push to the main branch.
   ```

2. **Add Website to Repository Settings**
   - Go to GitHub repository settings
   - Under "About" section (right sidebar)
   - Add your deployment URL as the website
   - Check "Use your GitHub Pages website"

3. **Add Deployment Badge**
   - Add a deployment status badge to your README
   - For Render:
   ```markdown
   ![Deployment Status](https://img.shields.io/badge/deployed%20on-Render-46E3B7)
   ```

## Environment Variables Required

- `DEEPAI_API_KEY`: Your DeepAI API key for image upscaling
  - Get it from: https://deepai.org/dashboard/profile

## Post-Deployment Checklist

- [ ] Application is accessible via the deployment URL
- [ ] DeepAI API key is properly configured
- [ ] Image upload functionality works
- [ ] Image upscaling completes successfully
- [ ] README.md updated with live demo link
- [ ] GitHub repository "About" section updated with website URL

## Monitoring and Maintenance

### For Render:
- Check logs in the Render dashboard
- Free tier sleeps after 15 minutes of inactivity (first request may be slow)
- Automatic deployments on every git push

### For Railway:
- Monitor usage in the Railway dashboard
- $5/month credit on free tier
- Automatic deployments enabled

### For Heroku:
- Use `heroku logs --tail` to view logs
- Free tier sleeps after 30 minutes of inactivity
- Limited to 1000 hours/month on free tier

## Troubleshooting

### Build Failures
- Ensure `requirements.txt` includes all dependencies
- Check Python version compatibility (3.8+ recommended)
- Verify `gunicorn` is in requirements.txt for production

### Runtime Errors
- Check environment variables are set correctly
- Verify DeepAI API key is valid
- Review application logs in your hosting platform dashboard

### Slow Performance
- Free tiers have resource limitations
- Consider upgrading to paid tier for better performance
- Implement caching for frequently accessed data

## Alternative: Static Frontend + Serverless Backend

If you want to use GitHub Pages, you could restructure the application:

1. **Create a static frontend** (HTML/CSS/JavaScript only)
   - Deploy frontend on GitHub Pages
2. **Deploy backend separately** as serverless functions:
   - Use Vercel Serverless Functions
   - Use AWS Lambda with API Gateway
   - Use Netlify Functions
3. **Connect frontend to backend API**
   - Frontend makes API calls to your serverless backend

This approach is more complex but allows you to use GitHub Pages for the UI.

## Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Verify all environment variables are set
- Ensure DeepAI API has sufficient credits

## Summary

**GitHub Pages cannot host this Flask application.** Instead:
1. ✅ Use **Render** (easiest, free tier)
2. ✅ Use Railway, Heroku, or PythonAnywhere
3. ✅ Update your README with the live demo link
4. ✅ Link the deployment URL in your GitHub repository

Your application will be accessible at a `.onrender.com`, `.up.railway.app`, or `.herokuapp.com` domain, which you can showcase in your portfolio and link from your GitHub repository.
