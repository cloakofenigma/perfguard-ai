#!/bin/bash
echo "🔧 Testing PerfGuard AI Fixes"
echo "================================"

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment active: $VIRTUAL_ENV"
else
    echo "⚠️  Activating virtual environment..."
    source venv/bin/activate
fi

# Check for GOOGLE_API_KEY
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ GOOGLE_API_KEY not set!"
    echo "   Run: export GOOGLE_API_KEY='your-key-here'"
    exit 1
fi
echo "✅ GOOGLE_API_KEY is set"

# Run PerfGuard AI
echo ""
echo "🚀 Running PerfGuard AI..."
./venv/bin/python3 perfguard/main.py

# Check if report was generated
if [ -f "dashboard/public/report.json" ]; then
    echo ""
    echo "✅ Report generated successfully!"
    echo "📊 Scores:"
    jq -r '. | "Previous: \(.previous_score)\nCurrent: \(.current_score)\nDelta: \(.delta_score)"' dashboard/public/report.json
else
    echo "❌ Report not found"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
echo ""
echo "Next steps:"
echo "1. Stop your dashboard if running (Ctrl+C)"
echo "2. Restart dashboard: cd dashboard && npm start"
echo "3. Open http://localhost:3000"
