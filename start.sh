#!/bin/bash
echo "🌤️ Starting Singular Weather Analytics on Railway"
echo "PORT: $PORT"
echo "Starting FastAPI server..."

uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} 