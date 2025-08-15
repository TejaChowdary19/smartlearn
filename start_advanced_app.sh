#!/bin/bash

# SmartLearn Advanced App Startup Script
echo "🚀 Starting SmartLearn Advanced App..."

# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/tejachowdary/Smartlearn

# Start the advanced Streamlit app
echo "🌟 Launching advanced features..."
python3 -m streamlit run src/app_advanced_streamlit.py --server.port 8510

echo "✅ SmartLearn Advanced App started on port 8510"
echo "🌐 Open your browser to: http://localhost:8510"
