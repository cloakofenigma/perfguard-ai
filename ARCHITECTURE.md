# PerfGuard AI - System Architecture

## 🏗️ Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PerfGuard AI Workflow                        │
└─────────────────────────────────────────────────────────────────┘

1. CODE CHANGES
   ├── Developer commits code
   ├── Git tracks changes
   └── Diff generated (optimized: --no-color --no-ext-diff --unified=2)

2. ANALYSIS ENGINE (perfguard/main.py)
   ├── Load baseline score (from dashboard/public/baseline_score.json)
   ├── Get git diff (smart truncation: 55MB → 5KB)
   ├── Run AI analysis (Google Gemini 2.5 Pro)
   │   ├── Safety settings: BLOCK_NONE (all categories)
   │   ├── Max tokens: 4096
   │   ├── Finish reason handling
   │   └── JSON extraction with balanced braces
   ├── Calculate metrics
   │   ├── Execution time
   │   ├── Memory usage
   │   ├── CPU usage
   │   ├── I/O operations
   │   ├── Code complexity
   │   └── AI risk score
   └── Generate scores
       ├── Previous score (baseline)
       ├── Current score (weighted metrics)
       └── Delta score (new code only)
           ├── AI risk (40% penalty)
           ├── Critical paths (5 pts each, max 20)
           └── File count (1 pt each, max 10)

3. FILE OUTPUT (Dual-location save)
   ├── Root directory
   │   ├── perfguard_score.json (backward compatibility)
   │   └── perfguard_report.md (human-readable)
   └── Dashboard directory
       ├── dashboard/public/report.json (dashboard source)
       └── dashboard/public/baseline_score.json (next run)

4. DASHBOARD SERVER (React + Custom Proxy)
   ├── setupProxy.js
   │   ├── Intercepts /report.json requests
   │   ├── Reads fresh data from disk
   │   ├── Sets cache-busting headers
   │   ├── Logs [Proxy] messages
   │   └── Returns JSON with proper Content-Type
   └── React Dev Server
       ├── Serves dashboard UI
       └── Proxies API requests

5. DASHBOARD UI (dashboard/src/App.js)
   ├── Fetch /report.json
   │   ├── Cache-busting query param (?t=timestamp)
   │   ├── Validation (status, content-type)
   │   ├── Logs [PerfGuard] messages
   │   └── Error handling (no mock fallback)
   ├── Display Components
   │   ├── ScoreCard (3 scores: Previous/Current/Delta)
   │   ├── MetricsCard (6 metrics with scores)
   │   ├── AIAnalysisCard (Gemini insights)
   │   ├── RecommendationsCard (actionable tips)
   │   └── PRScoreChart (historical trend)
   └── Auto-refresh (30s interval)

6. USER INTERACTION
   ├── Browser console (F12)
   │   └── [PerfGuard] logs for debugging
   ├── Server terminal
   │   └── [Proxy] logs for monitoring
   └── Dashboard UI
       ├── View scores
       ├── Read recommendations
       └── Manual refresh button
```

---

## 🔄 Data Flow Diagram

```
┌──────────────┐
│  Git Repo    │
│  (Changes)   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│  perfguard/main.py                           │
│  ┌─────────────────────────────────────┐    │
│  │ 1. Load baseline score              │    │
│  │ 2. Get git diff (smart truncate)    │    │
│  │ 3. AI analysis (Gemini 2.5 Pro)     │    │
│  │ 4. Calculate metrics                │    │
│  │ 5. Generate 3 scores                │    │
│  └─────────────────────────────────────┘    │
└───────────┬──────────────────────────────────┘
            │
            ├─────────────────┬────────────────┐
            ▼                 ▼                ▼
    ┌───────────────┐  ┌──────────────┐  ┌──────────────────┐
    │ Root Dir      │  │ Dashboard    │  │ Dashboard        │
    │               │  │ Public       │  │ Public           │
    │ perfguard_    │  │              │  │                  │
    │ score.json    │  │ report.json  │  │ baseline_        │
    │               │  │              │  │ score.json       │
    └───────────────┘  └──────┬───────┘  └──────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ setupProxy.js       │
                    │                     │
                    │ • Read from disk    │
                    │ • Cache-busting     │
                    │ • [Proxy] logs      │
                    │ • Proper headers    │
                    └──────┬──────────────┘
                           │
                           ▼
                    ┌─────────────────────┐
                    │ React App.js        │
                    │                     │
                    │ • Fetch JSON        │
                    │ • Validate response │
                    │ • [PerfGuard] logs  │
                    │ • Update UI         │
                    └──────┬──────────────┘
                           │
                           ▼
                    ┌─────────────────────┐
                    │ Dashboard UI        │
                    │                     │
                    │ • 3 Score Cards     │
                    │ • 6 Metrics         │
                    │ • AI Analysis       │
                    │ • Recommendations   │
                    └─────────────────────┘
```

---

## 🧩 Component Architecture

### Backend Components

```
perfguard/
├── main.py                    # Entry point, orchestration
│   ├── load_baseline_score()  # Read previous baseline
│   ├── get_git_diff()         # Optimized diff extraction
│   ├── calculate_delta_score() # New code score calculation
│   └── save_results()         # Dual-location saves
│
├── config.py                  # Configuration management
│   ├── GOOGLE_API_KEY         # Required env var
│   ├── GEMINI_MODEL           # gemini-2.5-pro
│   └── MAX_TOKENS             # 4096
│
├── ai_analyzer.py             # Gemini integration
│   ├── _call_gemini()         # API calls with safety settings
│   ├── _smart_truncate_diff() # 55MB → 5KB optimization
│   ├── _extract_json()        # Balanced brace matching
│   └── _get_default_response() # Graceful fallback
│
├── rules_engine.py            # Metrics calculation
│   ├── evaluate_performance() # 6-metric scoring
│   ├── calculate_scores()     # Individual metric scores
│   └── enrich_metrics()       # Add score fields
│
└── prompts.py                 # AI prompts
    └── diff_analysis          # JSON-only prompt
```

### Frontend Components

```
dashboard/src/
├── App.js                     # Main application
│   ├── fetchData()            # Enhanced fetch with validation
│   ├── useCallback()          # Auto-refresh logic (30s)
│   └── Error UI               # Troubleshooting steps
│
├── setupProxy.js              # Custom proxy middleware
│   ├── Route: /report.json    # Explicit handler
│   ├── File existence check   # 404 if missing
│   ├── Cache-busting headers  # Prevent caching
│   └── [Proxy] logging        # Server-side logs
│
└── components/
    ├── ScoreCard.js           # 3 scores (Previous/Current/Delta)
    ├── MetricsCard.js         # 6 metrics with scores
    │   └── Field compatibility # change_percent ?? change
    ├── AIAnalysisCard.js      # Gemini insights
    ├── RecommendationsCard.js # Actionable tips
    └── PRScoreChart.js        # Historical trends
```

### Automation Scripts

```
Root directory/
├── perfguard_complete.sh      # Master menu script
│   ├── Option 1: Full flow    # Analysis + Verify + Dashboard
│   ├── Option 2: Analysis     # Score generation only
│   ├── Option 3: Verify       # Validation checks
│   ├── Option 4: Dashboard    # Start UI only
│   └── Option 5: Clean        # Reset everything
│
├── verify_dashboard.sh        # 10-step verification
│   ├── Step 1: Check API key  # Env validation
│   ├── Step 2: Clean reports  # Remove old files
│   ├── Step 3: Run analysis   # Generate new reports
│   ├── Step 4-5: Verify files # Existence checks
│   ├── Step 6: Check sizes    # File validation
│   ├── Step 7-8: Compare      # Score consistency
│   ├── Step 9: Validate JSON  # Structure check
│   └── Step 10: Timestamps    # Sync verification
│
└── start_dashboard.sh         # Quick start with checks
    ├── Check report exists    # Pre-flight validation
    ├── Show current scores    # Display before start
    ├── Check port 3000        # Availability check
    └── Start npm server       # Launch dashboard
```

---

## 🔐 Security & Safety

### API Safety Settings (Gemini)

```python
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
```

**Why BLOCK_NONE?**
- Code analysis may contain keywords triggering false positives
- Performance code may reference sensitive topics (attacks, exploits)
- We need unfiltered analysis for accurate security assessment

### Data Privacy

- **No external data sharing**: All analysis stays local
- **API key security**: Stored in environment variables only
- **Git safety**: Binary files and secrets excluded from diff
- **No telemetry**: Zero tracking or analytics

---

## 📊 Scoring Algorithm

### Current Score (Overall Performance)

```
Current Score = (
    execution_score * 0.25 +
    memory_score * 0.20 +
    cpu_score * 0.15 +
    io_score * 0.15 +
    complexity_score * 0.15 +
    ai_risk_score * 0.10
)

Where each metric score = 100 - penalty
```

### Delta Score (New Code Only)

```
Delta Score = 100 - penalties

Penalties:
  - AI risk score: risk_score * 40  (0-40 points)
  - Critical paths: min(count * 5, 20)  (0-20 points)
  - Changed files: min(count * 1, 10)  (0-10 points)
  - Complexity: 30 points for high complexity

Maximum penalty: 100 points (score = 0)
```

### Previous Score (Baseline)

```
Previous Score = baseline_score from last run

Default: 100.0 (first run)
Persisted in: dashboard/public/baseline_score.json
```

---

## 🔧 Configuration Points

### Environment Variables

```bash
# Required
GOOGLE_API_KEY="your-google-api-key"

# Optional
GH_TOKEN="ghp-your-github-token"  # For PR comments
```

### Config File (perfguard/config.py)

```python
# LLM Configuration
GEMINI_MODEL = "gemini-2.5-pro"
MAX_TOKENS = 4096
TEMPERATURE = 0.2

# Thresholds
PASS_THRESHOLD = 80
WARNING_THRESHOLD = 60

# Paths
RESULTS_PATH = Path("perfguard_score.json")
REPORT_PATH = Path("perfguard_report.md")
DASHBOARD_REPORT_PATH = Path("dashboard/public/report.json")
BASELINE_SCORE_PATH = Path("dashboard/public/baseline_score.json")
```

### React Config (dashboard/src/App.js)

```javascript
// Auto-refresh interval
const REFRESH_INTERVAL = 30000  // 30 seconds

// Cache-busting
const url = `/report.json?t=${Date.now()}`

// Fetch headers
headers: {
  'Cache-Control': 'no-cache, no-store, must-revalidate',
  'Pragma': 'no-cache'
}
```

---

## 🚦 Error Handling Flow

```
┌─────────────────────────────────────────┐
│  Gemini API Call                        │
└────────────┬────────────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ Check finish_reason│
    └────────┬───────────┘
             │
    ┌────────┴────────────────────────┐
    │                                 │
    ▼                                 ▼
┌───────────┐                   ┌──────────┐
│ reason=1  │                   │ reason≠1 │
│ (STOP)    │                   │ (ERROR)  │
└─────┬─────┘                   └─────┬────┘
      │                               │
      ▼                               ▼
┌──────────────┐            ┌──────────────────┐
│ Extract JSON │            │ Handle Error     │
└──────┬───────┘            │ - MAX_TOKENS: 2  │
       │                    │ - SAFETY: 3      │
       ▼                    │ - OTHER: 4       │
┌──────────────┐            └────────┬─────────┘
│ Validate     │                     │
│ Structure    │                     ▼
└──────┬───────┘            ┌──────────────────┐
       │                    │ Retry (max 3)    │
       ▼                    │ or Fallback      │
┌──────────────┐            └──────────────────┘
│ Return Data  │
└──────────────┘
```

---

## 📈 Performance Optimizations

### 1. Git Diff Optimization
- **Before**: 55MB unoptimized diff
- **After**: ~5KB smart truncation
- **Method**: Extract only meaningful changes (±, @@, diff headers)

### 2. JSON Extraction
- **Before**: Regex-based (unreliable with nested objects)
- **After**: Balanced brace matching
- **Benefit**: Handles complex nested JSON

### 3. Caching Strategy
- **Client-side**: Query param timestamp
- **Server-side**: Cache-Control headers
- **Result**: Always fresh data, no stale UI

### 4. Dual-location Saves
- **Before**: Manual `cp` command
- **After**: Automatic atomic writes
- **Benefit**: Eliminates race conditions

---

## 🎯 Key Design Decisions

1. **Why Custom Proxy?**
   - React dev server's static file serving is unreliable
   - Need server-side logging for debugging
   - Require custom cache-busting headers

2. **Why No Mock Data Fallback?**
   - Silent failures hide real issues
   - Users need to know when fetch fails
   - Better to show error with troubleshooting

3. **Why Three Scores?**
   - Previous: Establish baseline
   - Current: Overall quality
   - Delta: Isolate new code impact

4. **Why Gemini-Only?**
   - Simplified architecture
   - Reduced dependencies
   - Lower cost (vs. multiple providers)

5. **Why Smart Truncation?**
   - API token limits (4096)
   - Safety filter triggers on large diffs
   - Focus on meaningful changes only

---

## 🔮 Extension Points

### Adding New Metrics
```python
# In rules_engine.py
def calculate_new_metric(changed_files, diff):
    # Your logic here
    return score, details

# Add to evaluate_performance()
new_metric_score, new_metric_details = calculate_new_metric(...)
```

### Custom Scoring Weights
```python
# In rules_engine.py
final_score = (
    execution_score * 0.25 +
    memory_score * 0.20 +
    cpu_score * 0.15 +
    io_score * 0.15 +
    complexity_score * 0.15 +
    ai_risk_score * 0.10 +
    new_metric_score * 0.05  # Add here
)
```

### New Dashboard Components
```javascript
// In dashboard/src/components/
// Create NewCard.js
export function NewCard({ data }) {
  return <div>{/* Your UI */}</div>
}

// In App.js
import { NewCard } from './components/NewCard'
<NewCard data={data} />
```

---

**Last Updated**: November 27, 2025
**Version**: 3.0
**Status**: Production Ready
