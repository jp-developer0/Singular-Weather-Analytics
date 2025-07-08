#!/usr/bin/env python3
"""
Startup script for Render deployment
"""

import os
import sys

def main():
    # Get port from environment or default to 10000 (Render's default)
    port = int(os.environ.get("PORT", 10000))
    
    print(f"🌤️ Starting Singular Weather Analytics on port {port}")
    print(f"Python version: {sys.version}")
    
    # Start the server using gunicorn with uvicorn workers
    os.system(f'gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --host 0.0.0.0 --port {port}')

if __name__ == "__main__":
    main() 