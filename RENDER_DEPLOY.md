# Render Deployment Guide

## 🚀 Deploy Singular Weather Analytics to Render

### Prerequisites
- GitHub repository with your code
- Render account (free tier available)

### Python 3.13 Compatibility Fixed! ✅
This deployment configuration now works with both Python 3.11 and 3.13 by:
- Using **pandas 2.2.3** (first version with full Python 3.13 support)
- Forcing **binary-only installs** to avoid compilation errors
- **NumPy version constraint** for stability

### Files Configured for Render
- `requirements.txt` - Updated with Python 3.13 compatible packages (pandas 2.2.3)
- `runtime.txt` - Specifies Python 3.11.10 for stability
- `render.yaml` - Complete Render service configuration with build optimizations
- `start_server.py` - Alternative startup script
- `check_environment.py` - Environment verification script

### Deployment Steps

#### Option 1: Direct Web Service (Recommended)
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `singular-weather-analytics`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install --only-binary=all -r requirements.txt`
   - **Start Command**: `gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

#### Option 2: Using render.yaml (Updated)
1. Update the `repo` URL in `render.yaml` to your GitHub repository
2. Push to GitHub
3. In Render Dashboard, click "New" → "Blueprint"
4. Connect repository and deploy

#### Option 3: Using start_server.py
Use this start command instead:
```
python start_server.py
```

### Environment Variables (Auto-configured in render.yaml)
- `PORT` - Automatically set by Render (typically 10000)
- `PYTHON_VERSION` - `3.11.10`
- `PIP_ONLY_BINARY` - `:all:` (forces binary wheels only)
- `PIP_NO_COMPILE` - `1` (prevents source compilation)

### Key Build Fixes Applied
1. **Binary-only installation**: `--only-binary=all` prevents compilation
2. **Pandas 2.2.3**: First version with full Python 3.13 compatibility
3. **NumPy constraint**: `<2.0.0` for stability
4. **Environment variables**: Force binary wheels, prevent compilation

### Local Testing
```bash
# Verify environment
python check_environment.py

# Install dependencies
pip install -r requirements.txt

# Test locally
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Or test with gunicorn (production setup)
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port 8000
```

### Verification After Deployment
After deployment, verify these endpoints:
- `/` - Main dashboard
- `/api/data` - Weather data viewer
- `/health` - Health check
- `/docs` - FastAPI documentation

### Troubleshooting

#### Build Fails with Compilation Errors
✅ **FIXED**: Using `--only-binary=all` prevents compilation
- Build command now forces binary wheels only
- No more pandas/numpy compilation errors

#### Python 3.13 Compatibility Issues
✅ **FIXED**: Updated to pandas 2.2.3
- First pandas version with full Python 3.13 support
- Released September 2024 specifically for Python 3.13

#### App doesn't start
- Check logs for port binding issues
- Verify `gunicorn` startup command
- Use health check endpoint: `/health`

#### Charts missing
- App generates them on first run
- Wait 30-60 seconds after deployment
- Check `/api/data` endpoint for data status

### Performance Notes
1. **Free Tier**: App may sleep after 15 minutes of inactivity
2. **Startup Time**: ~30-60 seconds for weather data scraping
3. **Binary Wheels**: Faster installs, no compilation needed

---

🌤️ **Your weather analytics app will be live at**: `https://your-service-name.onrender.com`

### Recent Updates
- ✅ Python 3.13 compatibility fixed
- ✅ Pandas compilation errors resolved
- ✅ Binary-only installation configured
- ✅ Environment verification script added 