#!/bin/bash
# PerfGuard AI - Complete Workflow Script
# Runs analysis and launches dashboard in one command

set -e

clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║             🛡️  PerfGuard AI - Complete Flow            ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check API key
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ Error: GOOGLE_API_KEY not set!"
    echo ""
    echo "Please set your Google Gemini API key:"
    echo "  export GOOGLE_API_KEY='your-api-key-here'"
    echo ""
    exit 1
fi

# Menu
echo "Select an option:"
echo ""
echo "  1) Run Analysis + Verify + Start Dashboard (Full Flow)"
echo "  2) Run Analysis Only"
echo "  3) Verify Existing Reports"
echo "  4) Start Dashboard (requires existing report)"
echo "  5) Clean All Reports and Start Fresh"
echo "  6) Test with Junk Code (Should BLOCK merge)"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Full Flow..."
        echo "========================================"

        # Run verification (includes analysis)
        ./verify_dashboard.sh

        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Verification passed! Starting dashboard..."
            echo ""
            echo "Dashboard will open at: http://localhost:3000"
            echo "Browser console will show [PerfGuard] logs"
            echo "Server terminal will show [Proxy] logs"
            echo ""
            read -p "Press Enter to start dashboard..."

            ./start_dashboard.sh
        else
            echo "❌ Verification failed. Please fix errors above."
            exit 1
        fi
        ;;

    2)
        echo ""
        echo "🔬 Running PerfGuard AI Analysis..."
        echo "========================================"
        ./venv/bin/python3 perfguard/main.py

        echo ""
        echo "✅ Analysis complete!"
        echo ""
        echo "View results:"
        echo "  • Text report: cat perfguard_report.md"
        echo "  • JSON scores: jq '.' perfguard_score.json"
        echo "  • Dashboard: ./start_dashboard.sh"
        ;;

    3)
        echo ""
        echo "🔍 Verifying Reports..."
        echo "========================================"
        ./verify_dashboard.sh
        ;;

    4)
        echo ""
        echo "🌐 Starting Dashboard..."
        echo "========================================"
        ./start_dashboard.sh
        ;;

    5)
        echo ""
        echo "🧹 Cleaning All Reports..."
        rm -f perfguard_score.json perfguard_report.md
        rm -f dashboard/public/report.json dashboard/public/baseline_score.json
        echo "✅ All reports cleaned!"
        echo ""
        echo "Run analysis: ./venv/bin/python3 perfguard/main.py"
        ;;

    6)
        echo ""
        echo "🔥 Testing with Junk Performance Code..."
        echo "========================================"
        echo ""
        echo "This will run pytest with junk_performance_killer tests"
        echo "Expected results:"
        echo "  ❌ Score: < 50 (FAIL)"
        echo "  ❌ Verdict: FAIL"
        echo "  ❌ Merge: BLOCKED"
        echo ""
        read -p "Press Enter to continue..."

        # Run pytest with only junk tests
        echo ""
        echo "Step 1: Running junk performance tests..."
        ./venv/bin/pytest sample-app/tests/test_junk_performance.py -m perf --benchmark-only --benchmark-json=benchmark_results.json -v

        echo ""
        echo "Step 2: Running PerfGuard analysis..."
        ./venv/bin/python3 perfguard/main.py

        echo ""
        echo "Step 3: Results summary..."
        if [ -f "perfguard_score.json" ]; then
            echo ""
            echo "📊 Performance Score:"
            cat perfguard_score.json | grep -A 2 "performance_score"
            echo ""
            echo "🚦 Verdict:"
            cat perfguard_score.json | grep -A 1 "verdict"
            echo ""
            echo "🚫 Merge Status:"
            cat perfguard_score.json | grep -A 1 "block_merge"
            echo ""
            echo "Full report: cat perfguard_report.md"
            echo "Dashboard: ./start_dashboard.sh"
        else
            echo "❌ No results file found!"
        fi
        ;;

    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Done! 🎉"
