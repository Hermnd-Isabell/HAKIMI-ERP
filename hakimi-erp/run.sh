#!/bin/bash

# HAKIMI-ERP: UNIFIED STARTUP SCRIPT for macOS/Linux

BASE_DIR=$(dirname "$0")
cd "$BASE_DIR"

echo "===================================================="
echo "  HAKIMI-ERP: UNIFIED STARTUP SCRIPT"
echo "===================================================="

# Start Backend
echo "[1/2] Starting Backend (FastAPI)..."
osascript -e "tell application \"Terminal\" to do script \"cd '$BASE_DIR/backend' && source venv/bin/activate && python main.py\""

# Start Frontend
echo "[2/2] Starting Frontend (Vue 3 / Vite)..."
osascript -e "tell application \"Terminal\" to do script \"cd '$BASE_DIR/frontend' && npm run dev\""

echo ""
echo "===================================================="
echo "  Backend and Frontend are starting in separate windows."
echo "  - Backend: http://localhost:8000"
echo "  - Frontend: http://localhost:5173"
echo "===================================================="
