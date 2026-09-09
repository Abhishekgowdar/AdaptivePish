#!/bin/bash

# AdaptivePhish - Stop Script
# Stops all running backend processes

echo "🛑 Stopping AdaptivePhish Backend..."

# Find and kill Python processes running app.py
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    taskkill //F //FI "WINDOWTITLE eq *python*app.py*" 2>/dev/null
    taskkill //F //IM python.exe //FI "MEMUSAGE gt 100000" 2>/dev/null
else
    # Unix-like systems
    pkill -f "python.*app.py"
fi

echo "✅ All backend processes stopped"

# Clean up log file
if [ -f "backend.log" ]; then
    echo "📋 Backend logs saved in: backend.log"
fi
