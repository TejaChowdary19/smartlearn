#!/bin/bash

# SmartLearn Enhanced Simple App Startup Script
echo "🎓 Starting SmartLearn Enhanced (Clean Interface)..."

# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/tejachowdary/Smartlearn

# Start the enhanced simple Streamlit app
echo "🌟 Launching enhanced features in background..."
python3 -m streamlit run src/app_enhanced_simple.py --server.port 8514

echo "✅ SmartLearn Enhanced App started on port 8514"
echo "🌐 Open your browser to: http://localhost:8514"
echo "💡 Advanced features are running silently in the background!"
