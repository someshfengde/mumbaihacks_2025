#!/bin/bash
# MindGuard - Run Script
# Starts both the backend API and the Streamlit frontend

cleanup() {
    echo ""
    echo "🛑 Shutting down MindGuard..."
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    exit 0
}

# Set up trap for cleanup on script exit
trap cleanup EXIT INT TERM

echo "🧠 Starting MindGuard..."
echo ""

# Start FastAPI backend in background
echo "📡 Starting backend API on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

# Start Streamlit frontend
echo "🌐 Starting Streamlit frontend on port 8501..."
echo ""
streamlit run frontend/app.py --server.port 8501 --server.headless true
