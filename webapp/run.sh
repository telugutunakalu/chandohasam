#!/bin/bash
# Run the Telugu Meter Analyzer webapp

set -e

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "Starting Telugu Meter Analyzer..."
echo "Open http://127.0.0.1:5000/ in your browser"
echo ""

PYTHONPATH=.. python app.py
