import sys
import os

# Add the project root to the sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import app

# This is for Vercel
handler = app
