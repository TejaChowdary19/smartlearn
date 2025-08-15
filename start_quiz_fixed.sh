#!/bin/bash

# SmartLearn Quiz Fixed App Startup Script
echo "🎓 Starting SmartLearn Enhanced (Quiz Fixed Version)..."

# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/tejachowdary/Smartlearn

# Start the corrected enhanced Streamlit app
echo "🌟 Launching enhanced features in background..."
python3 -m streamlit run src/app_quiz_fixed.py --server.port 8516

echo "✅ SmartLearn Enhanced Quiz Fixed App started on port 8516"
echo "🌐 Open your browser to: http://localhost:8516"
echo "💡 Advanced features are running silently in the background!"
echo "🔧 Quiz is now properly formatted with interactive options!"
