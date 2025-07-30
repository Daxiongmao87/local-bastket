#!/usr/bin/env python3
"""
Development Server with CSS Hot Reload for Local Basket
Provides live reloading of CSS changes during development
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webbrowser
from flask import Flask
import logging

class CSSChangeHandler(FileSystemEventHandler):
    """Handle CSS file changes and trigger rebuilds"""
    
    def __init__(self, rebuild_callback):
        self.rebuild_callback = rebuild_callback
        self.last_rebuild = 0
        self.rebuild_delay = 1  # Minimum seconds between rebuilds
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if event.src_path.endswith('.css'):
            current_time = time.time()
            if current_time - self.last_rebuild > self.rebuild_delay:
                print(f"🔄 CSS file changed: {event.src_path}")
                self.rebuild_callback()
                self.last_rebuild = current_time

class DevServer:
    """Development server with CSS hot reload capabilities"""
    
    def __init__(self, css_dir="static/css", app_module="app"):
        self.css_dir = Path(css_dir)
        self.app_module = app_module
        self.observer = None
        self.flask_process = None
        
    def rebuild_css(self):
        """Rebuild CSS bundle when files change"""
        try:
            print("🏗️  Rebuilding CSS bundle...")
            result = subprocess.run(['python', 'build_css.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ CSS rebuild complete")
                # Run quick analysis
                self.quick_analysis()
            else:
                print(f"❌ CSS rebuild failed: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error rebuilding CSS: {e}")
    
    def quick_analysis(self):
        """Run quick CSS analysis after rebuild"""
        try:
            result = subprocess.run(['python', 'analyze_css.py'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                # Extract key metrics from output
                output_lines = result.stdout.split('\n')
                for line in output_lines:
                    if 'TOTAL' in line and 'KB' in line:
                        print(f"📊 {line.strip()}")
                        break
        except subprocess.TimeoutExpired:
            print("⚠️  CSS analysis timeout - skipping")
        except Exception:
            pass  # Silent fail for quick analysis
    
    def start_css_watcher(self):
        """Start watching CSS files for changes"""
        print(f"👀 Watching {self.css_dir} for CSS changes...")
        
        handler = CSSChangeHandler(self.rebuild_css)
        self.observer = Observer()
        self.observer.schedule(handler, str(self.css_dir), recursive=True)
        self.observer.start()
    
    def start_flask_app(self):
        """Start Flask application in development mode"""
        try:
            print("🚀 Starting Flask development server...")
            
            # Set Flask development environment variables
            env = os.environ.copy()
            env['FLASK_ENV'] = 'development'
            env['FLASK_DEBUG'] = '1'
            env['FLASK_APP'] = self.app_module
            
            # Start Flask with hot reload
            self.flask_process = subprocess.Popen([
                'python', '-m', 'flask', 'run', 
                '--host=0.0.0.0', 
                '--port=5000',
                '--reload'
            ], env=env)
            
            # Wait a moment for server to start
            time.sleep(2)
            print("✅ Flask server started on http://localhost:5000")
            
        except Exception as e:
            print(f"❌ Error starting Flask server: {e}")
    
    def open_browser(self):
        """Open browser to development server"""
        try:
            time.sleep(3)  # Wait for server to be fully ready
            webbrowser.open('http://localhost:5000')
            print("🌐 Opened browser to http://localhost:5000")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
    
    def run(self, open_browser=True):
        """Run the complete development server"""
        print("🎯 LOCAL BASKET DEVELOPMENT SERVER")
        print("="*50)
        
        try:
            # Initial CSS build
            print("🔧 Building initial CSS bundle...")
            self.rebuild_css()
            
            # Start CSS file watcher
            self.start_css_watcher()
            
            # Start Flask app in separate thread
            flask_thread = threading.Thread(target=self.start_flask_app)
            flask_thread.daemon = True
            flask_thread.start()
            
            # Open browser if requested
            if open_browser:
                browser_thread = threading.Thread(target=self.open_browser)
                browser_thread.daemon = True
                browser_thread.start()
            
            print("\n📝 Development server is running!")
            print("   • CSS files are being watched for changes")
            print("   • Flask app is running with hot reload")
            print("   • Press Ctrl+C to stop")
            print("   • Edit CSS files to see live updates")
            print("\n" + "="*50)
            
            # Keep main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down development server...")
                self.stop()
                
        except Exception as e:
            print(f"❌ Error running development server: {e}")
            self.stop()
    
    def stop(self):
        """Stop all development server components"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            
        if self.flask_process:
            self.flask_process.terminate()
            self.flask_process.wait()
        
        print("✅ Development server stopped")

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Local Basket Development Server')
    parser.add_argument('--no-browser', action='store_true', 
                       help='Do not open browser automatically')
    parser.add_argument('--css-dir', default='static/css',
                       help='CSS directory to watch (default: static/css)')
    parser.add_argument('--app', default='app',
                       help='Flask app module (default: app)')
    
    args = parser.parse_args()
    
    # Check if required files exist
    if not Path('build_css.py').exists():
        print("❌ build_css.py not found. Run from project root directory.")
        sys.exit(1)
    
    if not Path(args.css_dir).exists():
        print(f"❌ CSS directory {args.css_dir} not found.")
        sys.exit(1)
    
    # Start development server
    dev_server = DevServer(args.css_dir, args.app)
    dev_server.run(open_browser=not args.no_browser)

if __name__ == "__main__":
    main()