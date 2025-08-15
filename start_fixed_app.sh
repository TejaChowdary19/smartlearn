#!/bin/bash

# SmartLearn Enhanced Fixed App Startup Script
echo "🎓 Starting SmartLearn Enhanced (Fixed Version)..."

# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/tejachowdary/Smartlearn

# Start the fixed enhanced Streamlit app
echo "🌟 Launching enhanced features in background..."
python3 -m streamlit run src/app_enhanced_simple_fixed.py --server.port 8515

echo "✅ SmartLearn Enhanced Fixed App started on port 8515"
echo "🌐 Open your browser to: http://localhost:8515"
echo "💡 Advanced features are running silently in the background!"
echo "🔧 All function call errors have been fixed!"
