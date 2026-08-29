import os
import sys

# Ensure root directory is on python path for Vercel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app
