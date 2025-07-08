#!/usr/bin/env python3
"""
Simple uvicorn startup script for Render deployment
Alternative to gunicorn if worker issues persist
"""

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    
    print(f"🌤️ Starting Singular Weather Analytics (Simple Mode)")
    print(f"🚀 Running on port {port}")
    print(f"📍 Using uvicorn directly")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    ) 