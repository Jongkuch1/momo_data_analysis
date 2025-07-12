#!/usr/bin/env python3
"""
MoMo Data Analysis - Application Runner
This script processes the data and starts the API server
"""

import os
import sys
import subprocess
import time

def run_data_processor():
    """Run the data processor to parse XML and populate database"""
    print("🔄 Processing XML data and populating database...")
    
    os.chdir('backend')
    
    try:
        result = subprocess.run([sys.executable, 'data_processor.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Data processing completed successfully!")
            print(result.stdout)
        else:
            print("❌ Data processing failed!")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running data processor: {e}")
        return False
    
    return True

def start_api_server():
    """Start the Flask API server"""
    print("🚀 Starting Flask API server...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🌐 Open frontend/index.html in your browser to view the dashboard")
    print("\n⚠️  Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, 'api.py'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function to run the complete application"""
    print("🏦 MoMo Data Analysis Dashboard")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('backend') or not os.path.exists('frontend'):
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Process data first
    if not run_data_processor():
        print("❌ Cannot start API server without processed data")
        sys.exit(1)
    
    # Start API server
    start_api_server()

if __name__ == "__main__":
    main()