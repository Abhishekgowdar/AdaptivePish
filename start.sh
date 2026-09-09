#!/bin/bash

# AdaptivePhish - Single Command Startup Script
# Works on Windows (Git Bash), Mac, and Linux

echo "==============================================="
echo "🛡️  AdaptivePhish System Startup"
echo "==============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to check if backend is ready
check_backend() {
    curl -s http://localhost:5000/health > /dev/null 2>&1
    return $?
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping AdaptivePhish..."

    # Kill backend process if it exists
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped"
    fi

    echo "✅ Shutdown complete"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python not found!"
    echo "Please install Python 3.11+ and try again."
    exit 1
fi

echo "${BLUE}[1/3]${NC} Starting Backend Server..."
echo ""

# Start backend in background
cd backend
python app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "Backend PID: $BACKEND_PID"
echo "⏳ Waiting for AI models to load (30-60 seconds)..."
echo ""

# Wait for backend to be ready (max 120 seconds)
COUNTER=0
MAX_WAIT=120

while [ $COUNTER -lt $MAX_WAIT ]; do
    if check_backend; then
        echo ""
        echo "${GREEN}✅ Backend is ready!${NC}"
        break
    fi

    # Show progress
    if [ $((COUNTER % 10)) -eq 0 ]; then
        echo "⏳ Still loading... ($COUNTER seconds elapsed)"
    fi

    sleep 2
    COUNTER=$((COUNTER + 2))
done

if [ $COUNTER -ge $MAX_WAIT ]; then
    echo ""
    echo "${YELLOW}⚠️  Warning: Backend took longer than expected${NC}"
    echo "Check backend.log for errors"
fi

echo ""
echo "${BLUE}[2/3]${NC} Opening Frontend in Browser..."
echo ""

# Open browser (cross-platform)
FRONTEND_PATH="$SCRIPT_DIR/frontend/index.html"

if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash) - Convert to Windows path
    WINDOWS_PATH=$(cygpath -w "$FRONTEND_PATH" 2>/dev/null || echo "$FRONTEND_PATH")
    cmd.exe /c start "" "$WINDOWS_PATH" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "${YELLOW}⚠️  Could not auto-open browser${NC}"
        echo "Please manually open: $FRONTEND_PATH"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$FRONTEND_PATH"
else
    # Linux
    xdg-open "$FRONTEND_PATH" 2>/dev/null || sensible-browser "$FRONTEND_PATH" 2>/dev/null
fi

echo "${GREEN}✅ Frontend ready${NC}"
echo ""
echo "==============================================="
echo "🎉 AdaptivePhish is now running!"
echo "==============================================="
echo ""
echo "📍 Backend:  http://localhost:5000"
echo "📖 API Docs: http://localhost:5000/docs"
echo "🌐 Frontend: file://$FRONTEND_PATH"
echo ""
echo "📋 Backend logs: backend.log"
echo ""
echo "${BLUE}[3/3]${NC} System Ready! Press ${YELLOW}Ctrl+C${NC} to stop all services"
echo ""

# Keep script running and show backend logs
tail -f backend.log 2>/dev/null &
TAIL_PID=$!

# Wait indefinitely (until Ctrl+C)
wait $BACKEND_PID

# If backend crashes, cleanup
cleanup
