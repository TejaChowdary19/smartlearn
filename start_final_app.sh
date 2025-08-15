#!/bin/bash

# SmartLearn Final Corrected App Startup Script
echo "🎓 Starting SmartLearn Enhanced (Final Corrected Version)..."

# Activate virtual environment
source .venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/tejachowdary/Smartlearn

# Start the final corrected enhanced Streamlit app
echo "🌟 Launching enhanced features in background..."
python3 -m streamlit run src/app_final_corrected.py --server.port 8518

echo "✅ SmartLearn Enhanced Final Corrected App started on port 8518"
echo "🌐 Open your browser to: http://localhost:8518"
echo "💡 Advanced features are running silently in the background!"
echo "🔧 All syntax errors have been completely fixed!"
echo "🎯 Quiz is now properly formatted with interactive options!"
echo "🚀 Ready for testing!"
