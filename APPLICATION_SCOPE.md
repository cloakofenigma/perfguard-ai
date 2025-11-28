# PerfGuard AI - Application Scope Configuration

## 🎯 Purpose

PerfGuard AI is designed to analyze **application code changes**, not the PerfGuard tool itself. This prevents polluted results and ensures accurate performance analysis of your actual application.

---

## 📁 Current Configuration

### Analyzed Directory
```
APPLICATION_PATH = "sample-app"
```

**Location:** `perfguard/config.py`

### What Gets Analyzed

✅ **Included:**
- All files in `sample-app/` directory
- Python code: `app.py`, `movies_data.py`, `slow_function.py`
- Tests: `tests/test_perf.py`
- Templates: `templates/*.html`
- Static files: `static/css/`, `static/images/`

❌ **Excluded:**
- `perfguard/` - Tool code itself
- `dashboard/` - Dashboard UI code
- Root configuration files
- Git/CI/CD files
- Documentation files

---

## 🔧 How It Works

### 1. Git Diff Scoping

```python
# Only gets diff for sample-app directory
git diff HEAD~1 -- sample-app/
```

### 2. Changed Files Detection

```python
# Only lists changed files in sample-app
git diff --name-only HEAD~1 -- sample-app/
```

### 3. Analysis Focus

PerfGuard analyzes:
1. **Code changes** in sample-app/
2. **Performance impact** of those changes
3. **Metrics** from sample-app tests
4. **AI risk assessment** for sample-app code only

---

## 🎯 Why This Matters

### Problem Without Scoping:
```
User edits: perfguard/ai_analyzer.py
PerfGuard analyzes: All files including its own code
Result: Irrelevant analysis about PerfGuard internals
         Dashboard shows metrics for tool code (not app)
         Confusing and meaningless scores
```

### Solution With Scoping:
```
User edits: perfguard/ai_analyzer.py
PerfGuard analyzes: Only sample-app/ (no changes found)
Result: "No changes detected in sample-app/"
         No misleading scores
         Clear feedback

User edits: sample-app/app.py
PerfGuard analyzes: Only app.py changes
Result: Accurate performance impact for the application
         Relevant metrics and scores
         Actionable insights
```

---

## 🔄 Changing the Application Path

### For Different Applications

Edit `perfguard/config.py`:

```python
# Example 1: Analyze a different app
APPLICATION_PATH = "my-web-app"

# Example 2: Analyze an API
APPLICATION_PATH = "api/src"

# Example 3: Analyze microservice
APPLICATION_PATH = "services/user-service"
```

### For Multiple Applications (Future)

Currently, PerfGuard analyzes one application at a time. For multiple apps:

**Option 1: Run separately**
```bash
# Analyze app 1
# Edit config.py: APPLICATION_PATH = "app1"
python perfguard/main.py

# Analyze app 2
# Edit config.py: APPLICATION_PATH = "app2"
python perfguard/main.py
```

**Option 2: Environment variable (future enhancement)**
```bash
export PERFGUARD_APP_PATH="app1"
python perfguard/main.py
```

---

## 📊 Expected Behavior

### Scenario 1: Changes in Application Directory

```bash
# Make changes to app
cd sample-app
echo "# Performance improvement" >> app.py
git add app.py
git commit -m "Optimize movie API"

# Run PerfGuard
cd ..
python perfguard/main.py
```

**Output:**
```
Getting git diff from HEAD~1 for sample-app/ only...
Found 1 changed files in sample-app/
Analyzing: sample-app/app.py
Previous: 100.0 → Current: 85.4 → Delta: 82.3
```

### Scenario 2: Changes Outside Application Directory

```bash
# Make changes to PerfGuard itself
echo "# New feature" >> perfguard/ai_analyzer.py
git add perfguard/ai_analyzer.py
git commit -m "Add new AI feature"

# Run PerfGuard
python perfguard/main.py
```

**Output:**
```
Getting git diff from HEAD~1 for sample-app/ only...
No changes detected in sample-app/ compared to HEAD~1
WARNING: No changes detected, nothing to analyze
```

### Scenario 3: Mixed Changes

```bash
# Make changes to both
echo "# Update" >> sample-app/app.py
echo "# Update" >> dashboard/src/App.js
git add .
git commit -m "Multiple changes"

# Run PerfGuard
python perfguard/main.py
```

**Output:**
```
Getting git diff from HEAD~1 for sample-app/ only...
Found 1 changed files in sample-app/
Analyzing: sample-app/app.py
(Dashboard changes are ignored)
```

---

## ✅ Verification

### Check Current Scope

```bash
# View config
grep APPLICATION_PATH perfguard/config.py

# Expected output:
# APPLICATION_PATH = "sample-app"
```

### Test Scoping

```bash
# 1. Clean old data
rm -f perfguard_score.json dashboard/public/report.json

# 2. Make test change
echo "# Test change" >> sample-app/app.py
git add sample-app/app.py
git commit -m "Test scoping"

# 3. Run analysis
python perfguard/main.py

# 4. Check logs for scope confirmation
# Should see: "Getting git diff from HEAD~1 for sample-app/ only..."
```

---

## 🎯 Best Practices

### 1. Separate Tool from Application

```
perfguard-ai/           # Tool repository
├── perfguard/          # Tool code (not analyzed)
├── dashboard/          # Dashboard (not analyzed)
└── sample-app/         # Application (ANALYZED)
```

### 2. One Application Per Analysis

- Each analysis run focuses on ONE application directory
- Prevents mixing unrelated changes
- Clear, focused results

### 3. Use Meaningful Commits

```bash
# Good: Specific to application
git commit -m "Optimize movie search algorithm"

# Avoid: Mixed concerns
git commit -m "Update tool and app"
```

### 4. Review Scope Before Analysis

```bash
# Always check what will be analyzed
git diff HEAD~1 -- sample-app/

# Verify changed files
git diff --name-only HEAD~1 -- sample-app/
```

---

## 🔮 Future Enhancements

### Planned Features:

1. **Environment Variable Support**
   ```bash
   export PERFGUARD_APP_PATH="my-app"
   python perfguard/main.py
   ```

2. **Multiple Application Support**
   ```bash
   python perfguard/main.py --app frontend
   python perfguard/main.py --app backend
   ```

3. **Auto-detection**
   ```python
   # Automatically detect application directories
   # Skip tool directories (perfguard/, dashboard/, etc.)
   ```

4. **Configuration File**
   ```yaml
   # .perfguardrc
   applications:
     - path: frontend/
       threshold: 85
     - path: backend/
       threshold: 80
   ```

---

## 📝 Summary

**Key Points:**
- ✅ PerfGuard analyzes **only** `sample-app/` directory by default
- ✅ Changes to PerfGuard itself are **ignored**
- ✅ Prevents polluted and irrelevant results
- ✅ Configurable via `APPLICATION_PATH` in `config.py`
- ✅ All old analysis records cleaned to start fresh

**Configuration Location:**
```
perfguard/config.py
Line 64: APPLICATION_PATH = "sample-app"
```

**Verification:**
```bash
# Confirm scoping works
grep -n "for sample-app/ only" perfguard/main.py
# Should show the scoped logging messages
```

---

**Last Updated:** November 27, 2025
**Status:** ✅ Implemented and Verified
