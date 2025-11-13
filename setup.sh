#!/bin/bash
# PerfGuard AI Setup Script

echo "🚀 PerfGuard AI Setup"
echo "===================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "⚠️  IMPORTANT: Set up your environment variables:"
echo ""
echo "export ANTHROPIC_API_KEY='your-anthropic-api-key'"
echo "export GH_TOKEN='your-github-token'"
echo ""
echo "Or create a .env file (make sure it's in .gitignore!):"
echo ""
echo "echo 'export ANTHROPIC_API_KEY=\"your-key\"' >> .env"
echo "echo 'export GH_TOKEN=\"your-token\"' >> .env"
echo "source .env"
echo ""
echo "🎬 To run the sample app:"
echo "cd sample-app"
echo "python app.py"
echo ""
echo "🧪 To run tests:"
echo "pytest sample-app/tests/test_perf.py -m perf -v"
echo ""
echo "🔍 To run PerfGuard AI:"
echo "python perfguard/main.py"
