# 🚨 SECURITY ALERT - IMMEDIATE ACTION REQUIRED

## ⚠️ API Keys Were Exposed in Code

### What Happened:
Your Anthropic API key and GitHub token were accidentally hardcoded in `perfguard/config.py` (lines 12-13).

**Exposed Keys:**
- Anthropic API Key: `sk-ant-api03-[REDACTED]`
- GitHub Token: `ghp_[REDACTED]`

**⚠️ CRITICAL:** The actual keys were removed from this file but were previously exposed in git history. You MUST rotate these keys immediately!

### ✅ What I Fixed:
- Removed hardcoded keys from `config.py`
- Changed to proper environment variable usage:
  ```python
  ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Correct
  GITHUB_TOKEN = os.getenv("GH_TOKEN")  # Correct
  ```

### ⚠️ IMMEDIATE ACTIONS YOU MUST TAKE:

#### 1. Rotate Your API Keys (URGENT!)
These keys are now compromised and should be rotated immediately:

**Anthropic API Key:**
- Go to: https://console.anthropic.com/settings/keys
- Delete the exposed key
- Generate a new key

**GitHub Token:**
- Go to: https://github.com/settings/tokens
- Revoke the exposed token
- Generate a new token

#### 2. Check Git History
```bash
# Check if keys were committed to git
git log --all --full-history --source -- perfguard/config.py

# If keys were committed, you need to:
# 1. Remove them from git history (use git filter-branch or BFG Repo-Cleaner)
# 2. Force push (⚠️ coordinate with team first)
# 3. Rotate keys immediately
```

#### 3. Set Up Environment Variables Properly

Create a `.env` file (DO NOT commit this file):
```bash
# .env file (add to .gitignore!)
export ANTHROPIC_API_KEY="your-new-anthropic-key"
export GH_TOKEN="your-new-github-token"
```

Or export directly:
```bash
export ANTHROPIC_API_KEY="your-new-anthropic-key"
export GH_TOKEN="your-new-github-token"
```

#### 4. Update .gitignore
Ensure these patterns are in `.gitignore`:
```
.env
.env.local
*.key
*.pem
secrets/
```

---

## 🔒 Best Practices Going Forward

### DO ✅
- Always use environment variables for secrets
- Add `.env` to `.gitignore`
- Use `os.getenv("VAR_NAME")` with variable NAMES, not values
- Use secrets management for production (AWS Secrets Manager, etc.)
- Rotate keys regularly

### DON'T ❌
- Never hardcode API keys in code
- Never commit `.env` files
- Never share keys in screenshots/logs
- Never use production keys in development

---

## 📝 Correct Usage Example

```python
# ❌ WRONG - This hardcodes the actual key
ANTHROPIC_API_KEY = os.getenv("sk-ant-api03-...")

# ✅ CORRECT - This reads from environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

Then set the actual key in your environment:
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-your-actual-key"
```

---

## 🆘 Need Help?

- Anthropic Security: security@anthropic.com
- GitHub Security: https://github.com/security/advisories

---

**Status:** ✅ Code fixed, but KEYS MUST BE ROTATED!
