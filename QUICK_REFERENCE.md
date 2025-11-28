# PerfGuard AI - Quick Reference Card

## ⚠️ IMPORTANT: Application Scope

**PerfGuard analyzes ONLY the `sample-app/` directory by default.**

- ✅ Changes to `sample-app/` → Analyzed
- ❌ Changes to `perfguard/` → Ignored
- ❌ Changes to `dashboard/` → Ignored

**Why?** To prevent polluted results from tool code. See [APPLICATION_SCOPE.md](APPLICATION_SCOPE.md) for details.

**Change it:** Edit `perfguard/config.py` → `APPLICATION_PATH = "your-app"`

---

## 🚀 Quick Start (30 seconds)

```bash
export GOOGLE_API_KEY="your-key"
./perfguard_complete.sh
# Select option 1
```

---

## 📋 Common Commands

### Run Analysis
```bash
# Full flow (analysis + verify + dashboard)
./perfguard_complete.sh

# Analysis only
python perfguard/main.py

# With verification
./verify_dashboard.sh
```

### Start Dashboard
```bash
# Quick start (recommended)
./start_dashboard.sh

# Manual start
cd dashboard && npm start
```

### View Results
```bash
# Terminal report
cat perfguard_report.md

# JSON scores
jq '{previous_score, current_score, delta_score}' dashboard/public/report.json

# Dashboard
# http://localhost:3000
```

### Troubleshooting
```bash
# Verify everything
./verify_dashboard.sh

# Check if report exists
ls -lh dashboard/public/report.json

# View report data
cat dashboard/public/report.json | jq '.'

# Clean and restart
rm -f dashboard/public/report.json perfguard_score.json
./perfguard_complete.sh
```

---

## 🔍 Debugging Guide

### Browser Console (F12)
Look for these logs:
```
[PerfGuard] Fetching report.json...
[PerfGuard] Response status: 200
[PerfGuard] Report data loaded: {...}
[PerfGuard] Dashboard updated successfully!
```

**If you see errors:**
- Check Network tab for `/report.json` request
- Verify response is JSON (not HTML)
- Check status code is 200
- Hard refresh: `Ctrl+Shift+R`

### Server Terminal
Look for these logs:
```
[Proxy] Request for /report.json
[Proxy] File found, size: 3656 bytes
[Proxy] Serving scores: { previous: 66.2, current: 79.3, delta: 76.0 }
```

**If you don't see logs:**
- Restart dev server: `Ctrl+C` then `./start_dashboard.sh`
- Check if port 3000 is in use: `lsof -i :3000`
- Kill and restart: `kill -9 $(lsof -ti:3000)`

---

## 🛠️ Common Issues

| Issue | Solution |
|-------|----------|
| **"GOOGLE_API_KEY not set"** | `export GOOGLE_API_KEY="your-key"` |
| **"report.json not found"** | Run `./verify_dashboard.sh` |
| **Dashboard shows 85, 85, 85** | Hard refresh browser: `Ctrl+Shift+R` |
| **Scores don't match terminal** | Restart dev server and hard refresh |
| **finish_reason=2 error** | Check git diff size, may need to commit binary files |
| **HTTP 404 error** | Re-run analysis: `python perfguard/main.py` |
| **Port 3000 already in use** | Kill existing: `kill -9 $(lsof -ti:3000)` |

---

## 📊 Understanding Scores

### Three Scores Explained

1. **Previous Score** (0-100)
   - Overall app performance BEFORE your changes
   - Loaded from previous run's baseline

2. **Current Score** (0-100)
   - Overall app performance AFTER your changes
   - Calculated from all 6 metrics

3. **Delta Score** (0-100)
   - Performance score for NEW code only
   - Calculated from:
     - AI risk score (40% penalty weight)
     - Critical paths (5 points each, max 20)
     - Changed files (1 point each, max 10)

### Score Interpretation

| Score | Verdict | Action |
|-------|---------|--------|
| 80-100 | ✅ PASS | Safe to merge |
| 60-79 | ⚠️ WARNING | Review recommendations |
| 0-59 | ❌ FAIL | Fix issues before merge |

---

## 🎯 Workflow Options

### perfguard_complete.sh Menu

```
1) Run Analysis + Verify + Start Dashboard (Full Flow)
   → Best for: First-time use, testing changes

2) Run Analysis Only
   → Best for: Quick score check

3) Verify Existing Reports
   → Best for: Debugging mismatches

4) Start Dashboard (requires existing report)
   → Best for: Viewing previous results

5) Clean All Reports and Start Fresh
   → Best for: Resetting everything
```

---

## 📁 File Locations

### Generated Files
```
perfguard_score.json                    # Root directory (backward compatibility)
perfguard_report.md                     # Human-readable report
dashboard/public/report.json            # Dashboard data source
dashboard/public/baseline_score.json    # Baseline for next run
```

### Key Source Files
```
perfguard/main.py                       # Entry point
perfguard/config.py                     # Configuration
perfguard/ai_analyzer.py                # Gemini integration
dashboard/src/App.js                    # Dashboard main component
dashboard/src/setupProxy.js             # Custom proxy for JSON serving
```

### Automation Scripts
```
perfguard_complete.sh                   # Master menu script
verify_dashboard.sh                     # 10-step verification
start_dashboard.sh                      # Quick dashboard start
```

---

## 🔧 Environment Variables

### Required
```bash
export GOOGLE_API_KEY="your-google-api-key"
```

### Optional
```bash
export GH_TOKEN="ghp-your-github-token"  # For PR comments
```

### Verify
```bash
echo $GOOGLE_API_KEY  # Should show your key
echo $GH_TOKEN        # Should show token or empty
```

---

## 🎬 Sample Workflows

### First Time Setup
```bash
git clone https://github.com/cloakofenigma/perfguard-ai.git
cd perfguard-ai
pip install -r requirements.txt
cd dashboard && npm install && cd ..
export GOOGLE_API_KEY="your-key"
./perfguard_complete.sh  # Select option 1
```

### After Making Changes
```bash
# Make code changes
git add .
git commit -m "Your changes"

# Run analysis
./verify_dashboard.sh

# View dashboard
./start_dashboard.sh
```

### Troubleshooting Flow
```bash
# Clean everything
./perfguard_complete.sh  # Select option 5

# Re-run analysis
./perfguard_complete.sh  # Select option 1

# Check results
jq '{previous_score, current_score, delta_score}' dashboard/public/report.json
```

---

## 💡 Pro Tips

1. **Always verify first**: Run `./verify_dashboard.sh` before starting dashboard
2. **Use hard refresh**: `Ctrl+Shift+R` to bypass browser cache
3. **Check both consoles**: Browser (F12) and server terminal
4. **Monitor auto-refresh**: Dashboard updates every 30 seconds
5. **Use menu script**: `./perfguard_complete.sh` for all common tasks
6. **Read the logs**: `[PerfGuard]` and `[Proxy]` logs tell you everything
7. **Commit binaries**: Large git diffs cause API errors
8. **Clean restarts**: Option 5 in menu script fixes most issues

---

## 🆘 Getting Help

### In Order of Usefulness

1. **Run verification**: `./verify_dashboard.sh`
2. **Check browser console**: F12 → Console tab
3. **Check server terminal**: Look for `[Proxy]` logs
4. **Read DASHBOARD_FIX_COMPLETE.md**: Comprehensive guide
5. **Check SESSION_SUMMARY.md**: Overview of all changes
6. **Check README.md**: Full documentation

### Key Documentation Files
- `QUICK_REFERENCE.md` - This file (quick commands)
- `DASHBOARD_FIX_COMPLETE.md` - Detailed troubleshooting
- `SESSION_SUMMARY.md` - Complete change log
- `README.md` - Full project documentation

---

## ✅ Success Checklist

After running `./perfguard_complete.sh` (option 1):

- [ ] No errors in terminal
- [ ] Dashboard opens at http://localhost:3000
- [ ] Three scores displayed correctly
- [ ] Scores match terminal output
- [ ] Browser console shows `[PerfGuard] Dashboard updated successfully!`
- [ ] Server shows `[Proxy] Serving scores: {...}`
- [ ] No error banner on dashboard
- [ ] Metrics show varied scores
- [ ] AI Analysis section populated

**If all checked → You're ready to go! 🎉**

---

**Last Updated**: November 27, 2025
**Quick Access**: Keep this file open for reference while using PerfGuard AI
