#!/usr/bin/env python3
"""
AdaptivePhish - Single Command Launcher
Opens backend and frontend automatically
"""

import os
import sys
import time
import webbrowser
import subprocess
import signal
from pathlib import Path
import requests

# Colors for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_color(text, color=Colors.ENDC):
    print(f"{color}{text}{Colors.ENDC}")

def check_backend_health():
    """Check if backend is responding"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    print("=" * 60)
    print_color("🛡️  AdaptivePhish - Intelligent Phishing Detector", Colors.BOLD)
    print("=" * 60)
    print()

    # Check Python version
    if sys.version_info < (3, 11):
        print_color("⚠️  Warning: Python 3.11+ recommended", Colors.YELLOW)
        print(f"   Current version: {sys.version_info.major}.{sys.version_info.minor}")
        print()

    backend_process = None

    try:
        # Start backend
        print_color("[1/3] Starting Backend Server...", Colors.BLUE)
        print()

        backend_dir = script_dir / 'backend'
        backend_script = backend_dir / 'app.py'

        if not backend_script.exists():
            print_color(f"❌ Error: Backend not found at {backend_script}", Colors.RED)
            return 1

        # Start backend process
        backend_process = subprocess.Popen(
            [sys.executable, 'app.py'],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8',
            errors='replace',  # Replace unencodable characters
            bufsize=1
        )

        print(f"   Backend PID: {backend_process.pid}")
        print()
        print_color("⏳ Waiting for AI models to load (30-60 seconds)...", Colors.YELLOW)
        print("   This is normal on first run - models are downloading/loading")
        print()

        # Wait for backend to be ready (max 120 seconds)
        start_time = time.time()
        max_wait = 120
        ready = False

        while time.time() - start_time < max_wait:
            if check_backend_health():
                print()
                print_color("✅ Backend is ready!", Colors.GREEN)
                ready = True
                break

            elapsed = int(time.time() - start_time)
            if elapsed > 0 and elapsed % 10 == 0:
                print(f"   ⏳ Still loading... ({elapsed} seconds elapsed)")

            time.sleep(2)

        if not ready:
            print()
            print_color("⚠️  Warning: Backend took longer than expected", Colors.YELLOW)
            print("   The backend may still be starting. Check console for errors.")
            print()

        # Open frontend in browser
        print()
        print_color("[2/3] Opening Frontend in Browser...", Colors.BLUE)
        print()

        frontend_url = "http://localhost:5000"

        print(f"   Opening: {frontend_url}")

        # Try to open browser
        try:
            webbrowser.open(frontend_url, new=2)  # new=2 opens in new tab
            print_color("✅ Browser opened successfully!", Colors.GREEN)
        except Exception as e:
            print_color(f"⚠️  Could not auto-open browser: {e}", Colors.YELLOW)
            print(f"   Please manually open: {frontend_url}")

        print()
        print("=" * 60)
        print_color("🎉 AdaptivePhish is Running!", Colors.GREEN + Colors.BOLD)
        print("=" * 60)
        print()
        print(f"🌐 Frontend:     http://localhost:5000")
        print(f"📖 API Docs:     http://localhost:5000/docs")
        print(f"📍 API Info:     http://localhost:5000/api/info")
        print()
        print_color("[3/3] System Ready!", Colors.GREEN)
        print()
        print("💡 Tips:")
        print("   • Click the 'Quick Test' buttons to test instantly")
        print("   • Try the 'Text Content' tab for text analysis")
        print("   • Check 'Technical Details' to see how AI works")
        print()
        print_color("Press Ctrl+C to stop all services", Colors.YELLOW)
        print()

        # Keep running and show backend output
        try:
            while True:
                try:
                    line = backend_process.stdout.readline()
                    if line:
                        print(f"[Backend] {line.rstrip()}")
                except UnicodeDecodeError as e:
                    # Skip lines that can't be decoded
                    pass

                if backend_process.poll() is not None:
                    print_color("⚠️  Backend process stopped unexpectedly", Colors.RED)
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print()
            print_color("🛑 Shutting down...", Colors.YELLOW)

    except Exception as e:
        print_color(f"❌ Error: {e}", Colors.RED)
        return 1

    finally:
        # Cleanup
        if backend_process:
            print("   Stopping backend server...")
            try:
                backend_process.terminate()
                backend_process.wait(timeout=5)
            except:
                backend_process.kill()
            print_color("✅ Shutdown complete", Colors.GREEN)

    return 0

if __name__ == '__main__':
    sys.exit(main())
