# AndrofitAI Backend

This is the Python backend for AndrofitAI, containing the voice assistant agent.

## 🚀 Deployment to Railway

### Quick Deploy Steps:

1. **Go to [Railway](https://railway.app)**
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository**
5. **Set the source directory to `backend`**
6. **Add environment variables:**
   ```env
   OPENAI_API_KEY=your_openai_key
   LIVEKIT_API_KEY=your_livekit_key
   LIVEKIT_API_SECRET=your_livekit_secret
   LIVEKIT_URL=your_livekit_url
   ```
7. **Deploy!**

### Environment Variables Required:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LIVEKIT_API_KEY`: Your LiveKit API key
- `LIVEKIT_API_SECRET`: Your LiveKit API secret
- `LIVEKIT_URL`: Your LiveKit server URL

### Local Development:

```bash
cd backend
pip install -r requirements.txt
python agent.py
```

## 📁 Files:

- `agent.py`: Main voice assistant agent
- `requirements.txt`: Python dependencies
- `Procfile`: Railway deployment configuration
- `runtime.txt`: Python version specification 