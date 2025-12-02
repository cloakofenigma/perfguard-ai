# 🔥 Junk Code Testing Guide

This guide shows how to test PerfGuard with intentionally bad code that **WILL BLOCK MERGES**.

## 📁 Files Created

### 1. `sample-app/junk_performance_killer.py`
Junk code with ALL performance anti-patterns:
- ❌ **Recursive Fibonacci**: O(2^n) exponential complexity
- ❌ **Memory Bomb**: 100MB+ wasted memory allocation
- ❌ **Blocking I/O**: 2+ seconds of file operations
- ❌ **Nested Loops**: O(n³) with 8 million iterations
- ❌ **String Concatenation**: 50k inefficient string ops
- ❌ **Redundant JSON**: 100 unnecessary parse/serialize cycles
- ❌ **List Operations**: Repeated large list copies

### 2. `sample-app/tests/test_junk_performance.py`
Pytest benchmarks that run the junk code:
- 8 performance tests with `@pytest.mark.perf`
- Tests ALL anti-patterns individually
- `test_combined_killer_benchmark()` - runs EVERYTHING

### 3. `perfguard_complete.sh` (Updated)
Added **Option 6: Test with Junk Code**

---

## 🧪 Local Testing Steps

### Method 1: Using perfguard_complete.sh (Easiest)

```bash
# Set API key
export GOOGLE_API_KEY='your-google-gemini-api-key'

# Run the script
./perfguard_complete.sh

# Select option 6
# Output will show:
# ❌ Score: < 50
# ❌ Verdict: FAIL
# ❌ Merge: BLOCKED
```

### Method 2: Manual Step-by-Step

```bash
# 1. Set API key
export GOOGLE_API_KEY='your-key-here'

# 2. Run pytest with junk tests
./venv/bin/pytest sample-app/tests/test_junk_performance.py \
  -m perf \
  --benchmark-only \
  --benchmark-json=benchmark_results.json \
  -v

# 3. Run PerfGuard analysis
./venv/bin/python3 perfguard/main.py

# 4. Check results
cat perfguard_report.md
cat perfguard_score.json
```

### Method 3: Quick Test (Single Function)

```bash
# Activate venv
source venv/bin/activate

# Test single junk function
cd sample-app
python3 -c "
from junk_performance_killer import combined_performance_killer
result = combined_performance_killer()
print(result)
"
```

---

## 🌐 GitHub Testing Steps

### Step 1: Create Test Branch

```bash
# Create and checkout new branch
git checkout -b test/junk-code-blocker

# Stage the junk files
git add sample-app/junk_performance_killer.py
git add sample-app/tests/test_junk_performance.py
git add perfguard_complete.sh
git add JUNK_CODE_TEST_GUIDE.md

# Commit
git commit -m "Add junk code for merge blocking test

- Added junk_performance_killer.py with terrible performance
- Added test_junk_performance.py pytest benchmarks
- Updated perfguard_complete.sh with junk test option
- Expected: Score < 50, FAIL verdict, BLOCKED merge

Testing PerfGuard's ability to block bad code."

# Push to GitHub
git push origin test/junk-code-blocker
```

### Step 2: Create Pull Request

1. Go to: `https://github.com/cloakofenigma/perfguard-ai/pulls`
2. Click **"New pull request"**
3. Set:
   - Base: `main`
   - Compare: `test/junk-code-blocker`
4. Title: `Test: Junk Code Should Block Merge`
5. Description:
   ```markdown
   ## Purpose
   Testing PerfGuard's merge blocking with intentionally terrible code.

   ## Changes
   - Added `junk_performance_killer.py` with 7 performance anti-patterns
   - Added pytest benchmarks for junk code
   - Updated test script

   ## Expected PerfGuard Results
   - ❌ Score: 30-50 (catastrophic)
   - ❌ Verdict: FAIL
   - ❌ Merge Status: BLOCKED
   - 🚫 PR should NOT be mergeable

   ## Performance Impact
   - Execution time: 10x-50x slower
   - Memory: +100MB waste
   - CPU: 90%+ utilization
   - I/O: 2+ second blocking
   - Complexity: O(2^n) + O(n³)
   ```
6. Click **"Create pull request"**

### Step 3: Monitor GitHub Actions

1. Go to **"Actions"** tab
2. Click on running **"PerfGuard Analysis"** workflow
3. Watch for logs showing:
   ```
   Running pytest with junk tests...
   ❌ Execution Time Score: 5.0 (catastrophic)
   ❌ Memory RSS Score: 10.0 (terrible)
   ❌ CPU Utilization Score: 15.0 (very high)
   ❌ Final Score: 42.0/100 - FAIL
   ❌ MERGE: BLOCKED
   ```

### Step 4: Check PR Comment

After workflow completes:
- Scroll to PR comments
- Look for PerfGuard bot comment:
  ```
  📊 Performance Score: 42.0/100
  Previous: 87.0
  Current: 42.0

  🚫 Verdict: FAIL
  🚫 Merge Status: BLOCKED

  ⚠️ Performance Degradation Detected
  - Execution Time: 2000% worse
  - Memory Usage: 500% worse
  - AI Risk: CRITICAL
  ```

### Step 5: Verify Merge Blocking

1. Check PR status at top:
   - Should show ❌ red X
   - "Some checks have failed"
2. Try to click **"Merge pull request"**:
   - Button should be disabled OR
   - Warning message appears
3. Branch protection working! ✅

### Step 6: View Dashboard

```
https://cloakofenigma.github.io/perfguard-ai/
```

Should show:
- **Baseline Score**: 87.0 (green)
- **Overall Score**: 42.0 (red)
- **Trend**: ⬇️ DOWN (red arrow)
- **Verdict**: ❌ FAIL (red)
- **Merge Status**: 🚫 BLOCKED (red)

---

## 📊 Expected Results

### Local Test Results

```bash
Performance Score Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Previous Overall Score:  87.0/100
Current Overall Score:   42.0/100
New Code Changes Score:  15.0/100

VERDICT: FAIL
MERGE: BLOCKED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Metric Breakdown:
- Execution Time:    5.0/100  (2000% slower)
- Memory RSS:       10.0/100  (500% worse)
- CPU Utilization:  15.0/100  (high usage)
- I/O Latency:      20.0/100  (very slow)
- Complexity:       30.0/100  (high complexity)
- AI Risk:           0.0/100  (critical risk detected)
```

### GitHub PR Results

```markdown
## PerfGuard Analysis Results

❌ **PERFORMANCE CHECK FAILED**

### Scores
- **Performance Score**: 42.0/100 ⬇️ -45.0 points
- **Previous**: 87.0/100
- **Verdict**: FAIL
- **Merge Status**: BLOCKED

### Issues Detected
1. 🔴 Execution time increased by 2000%
2. 🔴 Memory usage increased by 500%
3. 🔴 O(2^n) exponential complexity detected
4. 🔴 Blocking I/O operations (2+ seconds)
5. 🔴 Nested loops O(n³) detected

### Recommendation
**DO NOT MERGE** - Fix performance issues before merging.

[View Dashboard](https://cloakofenigma.github.io/perfguard-ai/)
```

---

## 🎯 What This Tests

### PerfGuard Capabilities

✅ **Detects execution time explosion** (O(2^n) fibonacci)
✅ **Catches memory leaks** (100MB+ allocation)
✅ **Identifies blocking I/O** (slow file operations)
✅ **Spots high complexity** (O(n³) nested loops)
✅ **AI analysis finds anti-patterns** (Gemini detects issues)
✅ **Blocks merge when score < 80** (42 < 80 = BLOCKED)
✅ **pytest benchmarks MANDATORY** (90% of score)
✅ **90/10 split enforced** (pytest 90%, AI 10%)

### GitHub Integration

✅ **Workflow triggers on PR**
✅ **Runs pytest + AI analysis**
✅ **Posts comment with results**
✅ **Blocks merge via status check**
✅ **Deploys dashboard to GitHub Pages**
✅ **Shows historical trends**

---

## 🔧 Troubleshooting

### If Score is Not Low Enough

The junk code is EXTREME - if score > 50, check:

```bash
# Verify junk tests ran
grep "test_junk" benchmark_results.json

# Check pytest actually executed
ls -lh benchmark_results.json  # Should be >100KB

# Verify mandatory pytest is enabled
grep "REQUIRE_PYTEST_TESTS" perfguard/config.py
# Should show: REQUIRE_PYTEST_TESTS = True
```

### If Merge Not Blocked

1. Check branch protection rules:
   - Settings → Branches → Branch protection rules
   - ✅ Require status checks to pass
   - ✅ "PerfGuard Analysis" must be checked

2. Verify workflow completed:
   - Actions tab → check for green/red status
   - If red, check error logs

### If pytest Fails

```bash
# Test junk code directly
cd sample-app
python3 -c "from junk_performance_killer import memory_bomb; print(memory_bomb())"

# Run single test
pytest tests/test_junk_performance.py::test_memory_bomb_benchmark -v
```

---

## 🎓 Learning Points

### Performance Anti-Patterns Demonstrated

1. **Exponential Complexity**: Never use pure recursion for fibonacci
2. **Memory Waste**: Don't create unnecessary large objects
3. **Blocking I/O**: Avoid synchronous file ops in loops
4. **Nested Loops**: Watch for O(n²) and O(n³) patterns
5. **String Concatenation**: Use list.join() instead of +=
6. **Redundant Operations**: Cache parsed results
7. **List Copies**: Use generators or in-place operations

### PerfGuard Features Tested

1. ✅ Mandatory pytest enforcement
2. ✅ Real-time performance measurement
3. ✅ AI-powered code analysis (Gemini)
4. ✅ Weighted scoring (90/10 split)
5. ✅ Merge blocking on failure
6. ✅ Dashboard visualization
7. ✅ Historical tracking
8. ✅ GitHub Actions integration

---

## 🚀 Next Steps After Testing

### If Test Succeeds (Merge Blocked)

1. **Verify PerfGuard is working** ✅
2. **Remove junk code**:
   ```bash
   git checkout main
   git branch -D test/junk-code-blocker
   git push origin --delete test/junk-code-blocker
   ```
3. **Keep the test files** for future testing
4. **Use PerfGuard on real PRs** with confidence!

### If Test Fails (Merge Not Blocked)

1. Check logs in GitHub Actions
2. Verify `REQUIRE_PYTEST_TESTS = True`
3. Ensure branch protection enabled
4. Check API key is set correctly
5. Review troubleshooting section above

---

## 📝 Summary

This junk code is **GUARANTEED** to:
- ❌ Score < 50 points
- ❌ Get FAIL verdict
- ❌ BLOCK the merge
- ✅ Prove PerfGuard works!

**Use this to validate your PerfGuard setup before production use!**
