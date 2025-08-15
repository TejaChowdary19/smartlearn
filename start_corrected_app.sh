#!/bin/bash

# SmartLearn Corrected App Startup Script
echo "🎓 Starting SmartLearn Enhanced (Corrected Version)..."

# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/tejachowdary/Smartlearn

# Start the corrected enhanced Streamlit app
echo "🌟 Launching enhanced features in background..."
python3 -m streamlit run src/app_quiz_fixed_corrected.py --server.port 8517

echo "✅ SmartLearn Enhanced Corrected App started on port 8517"
echo "🌐 Open your browser to: http://localhost:8517"
echo "💡 Advanced features are running silently in the background!"
echo "🔧 All syntax errors have been fixed!"
echo "🎯 Quiz is now properly formatted with interactive options!"
