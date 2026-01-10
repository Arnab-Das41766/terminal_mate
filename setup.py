"""
TerminalMate Setup Script
Run this to set up the project automatically
"""
import os
import sys
import subprocess


def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✓ Created directory: {path}")
    else:
        print(f"• Directory already exists: {path}")


def create_file(path, content=""):
    """Create file with content"""
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ Created file: {path}")


def check_ollama():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Ollama is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ Ollama is NOT installed")
    print("  Please install from: https://ollama.ai/download")
    return False


def check_qwen_model():
    """Check if Qwen model is available"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True)
        if 'qwen2.5-coder:7b' in result.stdout:
            print("✓ Qwen 2.5 Coder model is available")
            return True
        else:
            print("✗ Qwen 2.5 Coder model NOT found")
            print("  Run: ollama pull qwen2.5-coder:7b")
            return False
    except Exception:
        return False


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def main():
    print("""
╔═══════════════════════════════════════╗
║   TerminalMate Setup Script 🤖       ║
╚═══════════════════════════════════════╝
""")
    
    # Check prerequisites
    print("1️⃣ Checking prerequisites...\n")
    ollama_ok = check_ollama()
    model_ok = check_qwen_model()
    
    if not ollama_ok or not model_ok:
        print("\n⚠️  Please install missing prerequisites and run setup again")
        return
    
    # Create project structure
    print("\n2️⃣ Creating project structure...\n")
    
    # Create directories
    create_directory('core')
    create_directory('safety')
    create_directory('utils')
    create_directory('ui')
    
    # Create __init__.py files
    create_file('core/__init__.py', '# Core module\n')
    create_file('safety/__init__.py', '# Safety module\n')
    create_file('utils/__init__.py', '# Utils module\n')
    create_file('ui/__init__.py', '# UI module\n')
    
    # Create requirements.txt if it doesn't exist
    if not os.path.exists('requirements.txt'):
        requirements = """ollama>=0.1.0
rich>=13.7.0
prompt-toolkit>=3.0.43
psutil>=5.9.0
colorama>=0.4.6
"""
        create_file('requirements.txt', requirements)
    
    # Install dependencies
    print("\n3️⃣ Installing dependencies...\n")
    if install_dependencies():
        print("\n✅ Setup complete!")
        print("\n🚀 To start TerminalMate, run:")
        print("   python main.py")
    else:
        print("\n⚠️  Setup incomplete. Please install dependencies manually:")
        print("   pip install -r requirements.txt")


if __name__ == "__main__":
    main()