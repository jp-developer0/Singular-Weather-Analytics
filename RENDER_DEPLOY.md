# Render Deployment Guide

## 🚀 Deploy Singular Weather Analytics to Render

### Prerequisites
- GitHub repository with your code
- Render account (free tier available)

### Files Configured for Render
- `requirements.txt` - Updated with Python 3.13 compatible packages
- `runtime.txt` - Specifies Python 3.11.9 for compatibility
- `render.yaml` - Render service configuration (optional)
- `start_server.py` - Alternative startup script

### Deployment Steps

#### Option 1: Direct Web Service (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `singular-weather-analytics`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

#### Option 2: Using render.yaml
1. Update the `repo` URL in `render.yaml` to your GitHub repository
2. Push to GitHub
3. In Render Dashboard, click "New" → "Blueprint"
4. Connect repository and deploy

#### Option 3: Using start_server.py
Use this start command instead:
```
python start_server.py
```

### Environment Variables
Set these in Render dashboard:
- `PORT` - Automatically set by Render (typically 10000)
- `PYTHON_VERSION` - `3.11.9` (if needed)

### Important Notes
1. **Python Version**: Uses Python 3.11.9 for compatibility
2. **Pandas**: Updated to 2.2.0 for Python 3.13 compatibility
3. **Static Files**: Charts and CSV will be generated on startup
4. **Free Tier**: App may sleep after 15 minutes of inactivity

### Verification
After deployment, verify these endpoints:
- `/` - Main dashboard
- `/api/data` - Weather data viewer
- `/health` - Health check
- `/docs` - FastAPI documentation

### Troubleshooting
1. **Build fails**: Check requirements.txt for version conflicts
2. **App doesn't start**: Check logs for port binding issues
3. **Charts missing**: App generates them on first run, wait 30-60 seconds

### Local Testing Before Deploy
```bash
# Install dependencies
pip install -r requirements.txt

# Test locally
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Or test with gunicorn (production setup)
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000` to test locally.

---

🌤️ **Your weather analytics app will be live at**: `https://your-service-name.onrender.com` 