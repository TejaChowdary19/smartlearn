#!/bin/bash

# SmartLearn App Startup Script
echo "🚀 Starting SmartLearn with RAG Integration..."

# Activate virtual environment
source .venv/bin/activate

# Set Python path
export PYTHONPATH=/Users/tejachowdary/Smartlearn

# Run Streamlit app
echo "✅ Environment activated"
echo "🌐 Starting Streamlit app..."
echo "📱 Open http://localhost:8501 in your browser"
echo "🔍 RAG system is ready - enable it in the sidebar!"

python3 -m streamlit run src/app_streamlit.py
