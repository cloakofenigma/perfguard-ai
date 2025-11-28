#!/bin/bash
# PerfGuard AI - Dashboard Verification Script
# This script verifies the complete flow from analysis to dashboard display

set -e  # Exit on error

echo "========================================"
echo "🔍 PerfGuard AI - Dashboard Verification"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check environment
echo "Step 1: Checking environment..."
if [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${RED}❌ GOOGLE_API_KEY not set!${NC}"
    echo "   Run: export GOOGLE_API_KEY='your-key-here'"
    exit 1
fi
echo -e "${GREEN}✅ GOOGLE_API_KEY is set${NC}"

# Step 2: Check for existing reports (keep history)
echo ""
echo "Step 2: Checking existing reports..."
if [ -f "perfguard_score.json" ]; then
    echo -e "${YELLOW}ℹ️  Found existing perfguard_score.json (keeping for history)${NC}"
fi
if [ -f "dashboard/public/report.json" ]; then
    echo -e "${YELLOW}ℹ️  Found existing dashboard report (keeping for history)${NC}"
fi
echo -e "${GREEN}✅ Existing reports preserved${NC}"

# Step 3: Run PerfGuard AI
echo ""
echo "Step 3: Running PerfGuard AI analysis..."
echo "========================================"
./venv/bin/python3 perfguard/main.py || echo "Analysis completed with exit code: $?"
echo "========================================"

# Step 4: Verify root directory files
echo ""
echo "Step 4: Verifying root directory files..."
if [ ! -f "perfguard_score.json" ]; then
    echo -e "${RED}❌ perfguard_score.json not created!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ perfguard_score.json exists${NC}"

# Step 5: Verify dashboard files
echo ""
echo "Step 5: Verifying dashboard/public files..."
if [ ! -f "dashboard/public/report.json" ]; then
    echo -e "${RED}❌ dashboard/public/report.json not created!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ dashboard/public/report.json exists${NC}"

# Step 6: Verify file sizes
echo ""
echo "Step 6: Checking file sizes..."
ROOT_SIZE=$(stat -f%z perfguard_score.json 2>/dev/null || stat -c%s perfguard_score.json)
DASH_SIZE=$(stat -f%z dashboard/public/report.json 2>/dev/null || stat -c%s dashboard/public/report.json)

echo "   Root file size: $ROOT_SIZE bytes"
echo "   Dashboard file size: $DASH_SIZE bytes"

if [ "$ROOT_SIZE" -lt 100 ] || [ "$DASH_SIZE" -lt 100 ]; then
    echo -e "${YELLOW}⚠️  Warning: Files seem too small${NC}"
fi

# Step 7: Extract and compare scores
echo ""
echo "Step 7: Extracting scores..."
echo "----------------------------------------"

echo "Root file (perfguard_score.json):"
ROOT_SCORES=$(jq -r '"\(.previous_score) → \(.current_score) → \(.delta_score)"' perfguard_score.json)
echo "   Previous → Current → Delta: $ROOT_SCORES"

echo ""
echo "Dashboard file (dashboard/public/report.json):"
DASH_SCORES=$(jq -r '"\(.previous_score) → \(.current_score) → \(.delta_score)"' dashboard/public/report.json)
echo "   Previous → Current → Delta: $DASH_SCORES"

# Step 8: Verify scores match
echo ""
echo "Step 8: Verifying score consistency..."
if [ "$ROOT_SCORES" = "$DASH_SCORES" ]; then
    echo -e "${GREEN}✅ Scores match between root and dashboard!${NC}"
else
    echo -e "${RED}❌ Score mismatch detected!${NC}"
    echo "   Root:      $ROOT_SCORES"
    echo "   Dashboard: $DASH_SCORES"
    exit 1
fi

# Step 9: Validate JSON structure
echo ""
echo "Step 9: Validating JSON structure..."
jq -e '.previous_score, .current_score, .delta_score, .performance_score, .metrics, .ai_analysis' dashboard/public/report.json > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ JSON structure is valid${NC}"
else
    echo -e "${RED}❌ JSON structure is invalid!${NC}"
    exit 1
fi

# Step 10: Check file timestamps
echo ""
echo "Step 10: Checking file timestamps..."
ROOT_TIME=$(stat -f%m perfguard_score.json 2>/dev/null || stat -c%Y perfguard_score.json)
DASH_TIME=$(stat -f%m dashboard/public/report.json 2>/dev/null || stat -c%Y dashboard/public/report.json)

TIME_DIFF=$((DASH_TIME - ROOT_TIME))
if [ $TIME_DIFF -lt -5 ] || [ $TIME_DIFF -gt 5 ]; then
    echo -e "${YELLOW}⚠️  Warning: File timestamps differ by more than 5 seconds${NC}"
    echo "   This might indicate a synchronization issue"
else
    echo -e "${GREEN}✅ File timestamps are synchronized${NC}"
fi

# Summary
echo ""
echo "========================================"
echo "📊 Summary"
echo "========================================"
echo ""
echo "Scores: $DASH_SCORES"
echo ""
echo "File locations:"
echo "   ✓ perfguard_score.json ($(ls -lh perfguard_score.json | awk '{print $5}'))"
echo "   ✓ dashboard/public/report.json ($(ls -lh dashboard/public/report.json | awk '{print $5}'))"
echo ""
echo -e "${GREEN}✅ All verification checks passed!${NC}"
echo ""
echo "========================================"
echo "🚀 Next Steps"
echo "========================================"
echo ""
echo "1. If dashboard is running, stop it (Ctrl+C)"
echo "2. Restart dashboard:"
echo "   cd dashboard && npm start"
echo "3. Open: http://localhost:3000"
echo "4. Hard refresh browser: Ctrl+Shift+R"
echo "5. Check browser console (F12) for [PerfGuard] logs"
echo ""
echo "Expected scores in dashboard:"
echo "   Previous: $(jq -r '.previous_score' dashboard/public/report.json)"
echo "   Current:  $(jq -r '.current_score' dashboard/public/report.json)"
echo "   Delta:    $(jq -r '.delta_score' dashboard/public/report.json)"
echo ""
