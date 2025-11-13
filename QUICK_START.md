# 🚀 Quick Start Guide - PerfGuard AI

## 🚨 CRITICAL: Security Issue Fixed!

**Your API keys were exposed in the code!** I've fixed it, but you need to:

1. **IMMEDIATELY rotate your keys:**
   - Anthropic: https://console.anthropic.com/settings/keys
   - GitHub: https://github.com/settings/tokens

2. **Read SECURITY_ALERT.md** for full details

---

## ✅ Issues Fixed

1. ✅ **Config.py** - Removed hardcoded API keys
2. ✅ **Requirements.txt** - Fixed memory-profiler version
3. ✅ **Virtual Environment** - Created and installing dependencies

---

## 📦 Installation (Choose One Method)

### Method 1: Automated Setup (Recommended)
```bash
./setup.sh
```

### Method 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔑 Set Up Environment Variables

### Option A: Export directly
```bash
export ANTHROPIC_API_KEY="sk-ant-your-new-key"
export GH_TOKEN="ghp_your-new-token"
```

### Option B: Create .env file (recommended)
```bash
# Create .env file (make sure it's in .gitignore!)
cat > .env << 'EOF'
export ANTHROPIC_API_KEY="sk-ant-your-new-key"
export GH_TOKEN="ghp_your-new-token"
EOF

# Source it
source .env
```

### Option C: Add to your shell profile
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="sk-ant-your-new-key"' >> ~/.bashrc
echo 'export GH_TOKEN="ghp_your-new-token"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🎬 Run the Sample Movie App

```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Set environment variables (if not done already)
export ANTHROPIC_API_KEY="your-new-key"

# Run the app
cd sample-app
python app.py

# Open browser to http://localhost:5000
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## 🧪 Run Performance Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
cd sample-app
pytest tests/test_perf.py -m perf -v

# Run with benchmarks
pytest tests/test_perf.py -m perf --benchmark-only
```

---

## 🔍 Run PerfGuard AI Analysis

```bash
# Activate virtual environment
source venv/bin/activate

# Set API key
export ANTHROPIC_API_KEY="your-new-key"

# Run analysis
python perfguard/main.py

# View results
cat perfguard_report.md
```

---

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
**Solution:** Virtual environment not activated
```bash
source venv/bin/activate
```

### Error: "ANTHROPIC_API_KEY not set"
**Solution:** Set environment variable
```bash
export ANTHROPIC_API_KEY="your-key"
```

### Error: "No changes detected"
**Solution:** Make some changes or commit code first
```bash
# Make a test change
echo "# test" >> sample-app/app.py
git add .
git commit -m "test"
```

### Installation taking too long (pandas building)
**Solution:** Skip pandas (it's optional)
```bash
# Edit requirements.txt and comment out pandas line
# Or install without pandas:
pip install anthropic requests pytest pytest-benchmark pytest-flask memory-profiler psutil radon Flask Flask-Cors Werkzeug
```

---

## 📋 Checklist Before Demo

- [ ] Rotated API keys
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Sample app runs (http://localhost:5000)
- [ ] Tests pass (`pytest -m perf`)
- [ ] PerfGuard AI runs successfully

---

## 🆘 Still Having Issues?

1. Check you're in the correct directory
2. Verify virtual environment is activated (`which python` should show `venv/bin/python`)
3. Verify API key is set (`echo $ANTHROPIC_API_KEY` should show your key)
4. Read the error message carefully
5. Check SECURITY_ALERT.md for key rotation steps

---

## 🎯 Next Steps

Once everything works:
1. Test the sample movie app in browser
2. Run performance tests to establish baselines
3. Create a test PR with slow code
4. Watch PerfGuard AI analyze it
5. Prepare for competition demo!

---

**Remember:** Always keep your API keys secure! Never commit them to git!
