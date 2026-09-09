#!/bin/bash

# AdaptivePhish - Simple Startup (Manual Browser Opening)

echo "==============================================="
echo "🛡️  AdaptivePhish - Simple Startup"
echo "==============================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python not found!"
    exit 1
fi

echo "✅ Starting Backend Server..."
echo ""

# Start backend
cd backend
python app.py &
BACKEND_PID=$!
cd ..

echo "Backend PID: $BACKEND_PID"
echo ""
echo "⏳ Waiting for backend to initialize (30-60 seconds)..."
echo "   (AI models are loading for the first time)"
echo ""

# Simple wait with countdown
for i in {60..1}; do
    if curl -s http://localhost:5000/health > /dev/null 2>&1; then
        echo ""
        echo "✅ Backend is ready!"
        break
    fi
    if [ $((i % 10)) -eq 0 ]; then
        echo "   ⏳ Still loading... ($i seconds remaining)"
    fi
    sleep 1
done

echo ""
echo "==============================================="
echo "✅ AdaptivePhish is Running!"
echo "==============================================="
echo ""
echo "📍 Backend API: http://localhost:5000"
echo "📖 API Docs:    http://localhost:5000/docs"
echo ""
echo "🌐 OPEN IN YOUR BROWSER:"
echo "   File: $SCRIPT_DIR/frontend/index.html"
echo ""
echo "   Or copy-paste this path:"
echo "   file:///$SCRIPT_DIR/frontend/index.html"
echo ""
echo "==============================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Wait for Ctrl+C
wait $BACKEND_PID
