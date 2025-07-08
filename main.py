#!/usr/bin/env python3
"""
Main entry point for the Singular Weather Analytics application
"""

import os
import uvicorn
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🌤️ Starting Singular Weather Analytics on port {port}")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    ) 