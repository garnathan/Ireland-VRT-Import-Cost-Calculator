#!/usr/bin/env python3
"""
Production runner for VRT Calculator Flask App
"""

import os
from app import app

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting VRT Calculator on {host}:{port}")
    print(f"Debug mode: {debug}")
    print("Access the calculator at: http://localhost:5000")
    
    app.run(host=host, port=port, debug=debug)
