#!/usr/bin/env python3
"""
Personal Finance Chatbot - Frontend Launcher
Interactive launcher to choose and run different Python frontends
"""

import sys
import os
import subprocess
import importlib.util

def check_module(module_name):
    """Check if a module is available"""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🐍 Personal Finance Chatbot - Python Frontend Launcher")
    print("=" * 60)
    print()

def check_dependencies():
    """Check which frontends are available"""
    available = {}
    
    # Tkinter (built-in)
    available['tkinter'] = check_module('tkinter')
    
    # FastAPI
    available['fastapi'] = check_module('fastapi') and check_module('uvicorn')
    
    # Kivy
    available['kivy'] = check_module('kivy')
    
    # Streamlit
    available['streamlit'] = check_module('streamlit')
    
    return available

def print_menu(available):
    """Print the frontend selection menu"""
    print("📋 Available Frontends:")
    print()
    
    # Tkinter Desktop App
    status = "✅" if available['tkinter'] else "❌"
    print(f"1. {status} Tkinter Desktop App")
    print("   🖥️  Professional native desktop interface")
    if not available['tkinter']:
        print("   📦 Install: Usually included with Python")
    print()
    
    # FastAPI Web App
    status = "✅" if available['fastapi'] else "❌"
    print(f"2. {status} FastAPI Web App")
    print("   🌐 Modern responsive web interface")
    if not available['fastapi']:
        print("   📦 Install: pip install fastapi uvicorn jinja2")
    print()
    
    # Kivy Mobile App
    status = "✅" if available['kivy'] else "❌"
    print(f"3. {status} Kivy Mobile App")
    print("   📱 Touch-friendly mobile-style interface")
    if not available['kivy']:
        print("   📦 Install: pip install kivy")
    print()
    
    # Streamlit (Original)
    status = "✅" if available['streamlit'] else "❌"
    print(f"4. {status} Streamlit Interface (Original)")
    print("   🎨 Data science focused interface")
    if not available['streamlit']:
        print("   📦 Install: pip install streamlit")
    print()
    
    print("0. ❌ Exit")
    print()

def run_frontend(choice, available):
    """Run the selected frontend"""
    if choice == '1' and available['tkinter']:
        print("🚀 Launching Tkinter Desktop App...")
        try:
            subprocess.run([sys.executable, 'frontend/tkinter_app.py'])
        except KeyboardInterrupt:
            print("\n👋 Tkinter app closed.")
        return True
        
    elif choice == '2' and available['fastapi']:
        print("🚀 Launching FastAPI Web App...")
        print("📱 Open your browser to: http://localhost:8000")
        try:
            subprocess.run([sys.executable, 'frontend/fastapi_frontend.py'])
        except KeyboardInterrupt:
            print("\n👋 FastAPI server stopped.")
        return True
        
    elif choice == '3' and available['kivy']:
        print("🚀 Launching Kivy Mobile App...")
        try:
            subprocess.run([sys.executable, 'frontend/kivy_mobile_app.py'])
        except KeyboardInterrupt:
            print("\n👋 Kivy app closed.")
        return True
        
    elif choice == '4' and available['streamlit']:
        print("🚀 Launching Streamlit Interface...")
        print("📱 Open your browser to: http://localhost:8501")
        try:
            subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py'])
        except KeyboardInterrupt:
            print("\n👋 Streamlit app stopped.")
        return True
        
    elif choice == '0':
        print("👋 Goodbye!")
        return False
        
    else:
        print("❌ Invalid choice or frontend not available!")
        print("💡 Install missing dependencies and try again.")
        return True

def install_suggestions():
    """Print installation suggestions"""
    print()
    print("💡 Quick Installation Commands:")
    print()
    print("For FastAPI Web Frontend:")
    print("  pip install fastapi uvicorn jinja2 python-multipart")
    print()
    print("For Kivy Mobile Frontend:")
    print("  pip install kivy")
    print()
    print("For Streamlit Interface:")
    print("  pip install streamlit")
    print()
    print("Install all optional frontends:")
    print("  pip install fastapi uvicorn jinja2 kivy streamlit")
    print()

def main():
    """Main launcher function"""
    try:
        print_banner()
        
        # Check available frontends
        available = check_dependencies()
        
        # Check if any frontend is available
        if not any(available.values()):
            print("❌ No frontends available!")
            print("📦 Please install at least one frontend framework.")
            install_suggestions()
            return
        
        while True:
            print_menu(available)
            
            try:
                choice = input("🔢 Select a frontend (0-4): ").strip()
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            
            if not run_frontend(choice, available):
                break
            
            # Ask if user wants to try another frontend
            try:
                print()
                again = input("🔄 Try another frontend? (y/N): ").strip().lower()
                if again not in ['y', 'yes']:
                    print("👋 Thanks for using Personal Finance Chatbot!")
                    break
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            
            print("\n" + "="*60 + "\n")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you're running this from the project root directory.")

if __name__ == "__main__":
    main()
