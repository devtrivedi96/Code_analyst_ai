#!/bin/bash

# AI Code Analyst - Quick Start Guide
# This script helps you set up and run the AI Code Analyst

set -e  # Exit on error

echo "🚀 AI Code Analyst - Setup & Quick Start"
echo "========================================"
echo ""

# Check if in correct directory
if [ ! -f "src/app.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check Python version
python3 --version

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "✅ Virtual environment ready"
echo ""

# Activate venv
source venv/bin/activate

echo "📝 API Key Setup:"
echo "================"
echo ""
echo "Choose your AI model:"
echo "1. Google Gemini (Free - Recommended)"
echo "2. OpenAI GPT-4 (Paid)"
echo "3. Anthropic Claude (Paid)"
echo ""

# Check for existing API keys
if [ ! -z "$GEMINI_API_KEY" ]; then
    echo "✅ GEMINI_API_KEY already set"
fi

if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "✅ OPENAI_API_KEY already set"
fi

if [ ! -z "$ANTHROPIC_API_KEY" ]; then
    echo "✅ ANTHROPIC_API_KEY already set"
fi

echo ""
echo "📚 Full setup instructions are in: AI_SETUP_GUIDE.md"
echo ""
echo "🚀 Starting Flask Development Server..."
echo "========================================"
echo ""

# Start the Flask app
python3 src/app.py
