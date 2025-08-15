#!/bin/bash

# SmartLearn Metrics Dashboard Startup Script
# This script starts the comprehensive analytics and performance monitoring dashboard

echo "🚀 Starting SmartLearn Metrics Dashboard..."
echo "=========================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "   Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements_metrics.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if required packages are installed
echo "📦 Checking required packages..."
python3 -c "import plotly, altair, psutil, streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required packages not found. Installing..."
    pip install -r requirements_metrics.txt
fi

# Set environment variables for optimal performance
export STREAMLIT_SERVER_PORT=8505
export STREAMLIT_SERVER_ADDRESS=localhost
export STREAMLIT_SERVER_HEADLESS=false
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Start the metrics dashboard
echo "📊 Launching SmartLearn Metrics Dashboard..."
echo "🌐 Dashboard will be available at: http://localhost:8505"
echo "🔄 Press Ctrl+C to stop the dashboard"
echo ""

# Run the dashboard
python3 -m streamlit run src/app_metrics_dashboard.py --server.port 8505 --server.address localhost

echo ""
echo "👋 Metrics Dashboard stopped."
