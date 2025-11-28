#!/bin/bash
# PerfGuard AI - Quick Start Dashboard Script

echo "🛡️  PerfGuard AI - Starting Dashboard"
echo "========================================"

# Check if report exists
if [ ! -f "dashboard/public/report.json" ]; then
    echo "⚠️  No report found. Please run analysis first:"
    echo "   ./verify_dashboard.sh"
    exit 1
fi

# Show current scores
echo ""
echo "Current scores in report.json:"
jq -r '"Previous: \(.previous_score)\nCurrent:  \(.current_score)\nDelta:    \(.delta_score)"' dashboard/public/report.json
echo ""

# Check if dashboard is already running
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Dashboard is already running on port 3000"
    echo "   Stop it first (Ctrl+C in the terminal where it's running)"
    echo "   Or kill it: kill -9 \$(lsof -ti:3000)"
    exit 1
fi

echo "Starting React development server..."
echo "========================================"
echo ""
echo "Dashboard will open at: http://localhost:3000"
echo ""
echo "🔍 Troubleshooting tips:"
echo "   1. Check browser console (F12) for [PerfGuard] logs"
echo "   2. Hard refresh: Ctrl+Shift+R (Linux/Win) or Cmd+Shift+R (Mac)"
echo "   3. If data doesn't load, check Network tab for /report.json"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

cd dashboard && npm start
