# Deployment Guide

## Quick Start (Local)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Test:
```bash
# In another terminal
python test_comprehensive.py
```

## Deploy to Render (Recommended)

### Step 1: Prepare Repository
1. Push code to GitHub
2. Ensure these files exist:
   - `main.py`
   - `requirements.txt`
   - `shl_product_catalog.json`
   - `Procfile` (optional, Render auto-detects)

### Step 2: Create Render Service
1. Go to https://render.com
2. Sign up / Log in
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: shl-assessment-recommender
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### Step 3: Add Environment Variable
1. In Render dashboard, go to "Environment"
2. Add: `GEMINI_KEY` = `your_api_key_here`
3. Save

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for build (2-3 minutes)
3. Your API will be at: `https://shl-assessment-recommender.onrender.com`

### Step 5: Test Deployment
```bash
curl https://your-app.onrender.com/health

curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "I need a Java developer assessment"}
    ]
  }'
```

## Deploy to Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python
5. Add environment variable: `GEMINI_KEY`
6. Deploy automatically starts
7. Get URL from Railway dashboard

## Deploy to Fly.io

1. Install flyctl:
```bash
# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

2. Login:
```bash
fly auth login
```

3. Create fly.toml:
```toml
app = "shl-recommender"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

4. Deploy:
```bash
fly launch
fly secrets set GEMINI_KEY=your_key_here
fly deploy
```

## Deploy to Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app:
```bash
heroku create shl-recommender
```

4. Set environment variable:
```bash
heroku config:set GEMINI_KEY=your_key_here
```

5. Deploy:
```bash
git push heroku main
```

## Monitoring & Debugging

### Check Logs (Render)
```bash
# In Render dashboard, click "Logs"
```

### Check Logs (Railway)
```bash
# In Railway dashboard, click on service → "Logs"
```

### Check Logs (Fly.io)
```bash
fly logs
```

### Common Issues

**Issue**: Cold start timeout
- **Solution**: First request may take 30-60s on free tier

**Issue**: Module not found
- **Solution**: Check requirements.txt includes all dependencies

**Issue**: Port binding error
- **Solution**: Use `$PORT` environment variable, not hardcoded port

**Issue**: Gemini API error
- **Solution**: Verify GEMINI_KEY is set correctly

## Performance Optimization

### For Production:
1. Use gunicorn instead of uvicorn:
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Add caching:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def search_assessments_cached(query: str):
    # ...
```

3. Use connection pooling for Gemini API

4. Add request timeout:
```python
from fastapi import Request
import asyncio

@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        return await asyncio.wait_for(call_next(request), timeout=25.0)
    except asyncio.TimeoutError:
        return JSONResponse({"error": "Request timeout"}, status_code=504)
```

## Cost Estimation

### Free Tier Limits:
- **Render**: 750 hours/month, sleeps after 15 min inactivity
- **Railway**: $5 credit/month, ~500 hours
- **Fly.io**: 3 shared VMs, 160GB bandwidth
- **Gemini API**: 60 requests/minute free tier

### Expected Usage:
- Average conversation: 3-5 API calls
- Response time: 1-3 seconds
- Can handle ~1000 conversations/day on free tier
