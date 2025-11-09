"""
System Check - Verify Ultimate AI Agent Setup
Checks all dependencies and system requirements
"""

import sys
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"{Fore.GREEN}✓ Python {version.major}.{version.minor}.{version.micro}{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}✗ Python {version.major}.{version.minor}.{version.micro} (need 3.10+){Style.RESET_ALL}")
        return False


def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"{Fore.GREEN}✓ {package_name}{Style.RESET_ALL}")
        return True
    except ImportError:
        print(f"{Fore.RED}✗ {package_name} (not installed){Style.RESET_ALL}")
        return False


def check_files():
    """Check if all required files exist"""
    required_files = [
        'ultimate_agent.py',
        'agent_tools.py',
        'agent_memory.py',
        'agent_safety.py',
        'setup_model.py',
        'start_agent.py',
        'requirements.txt',
        'README.md',
        'GETTING_STARTED.md'
    ]
    
    all_exist = True
    for filename in required_files:
        if Path(filename).exists():
            print(f"{Fore.GREEN}✓ {filename}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {filename}{Style.RESET_ALL}")
            all_exist = False
    
    return all_exist


def check_model():
    """Check if any model is downloaded"""
    cache_dir = Path.home() / ".cache" / "gpt4all"
    
    if not cache_dir.exists():
        print(f"{Fore.YELLOW}! No models downloaded yet{Style.RESET_ALL}")
        return False
    
    models = list(cache_dir.glob("*.gguf"))
    if models:
        print(f"{Fore.GREEN}✓ {len(models)} model(s) found:{Style.RESET_ALL}")
        for model in models:
            size_gb = model.stat().st_size / (1024**3)
            print(f"  • {model.name} ({size_gb:.1f} GB)")
        return True
    else:
        print(f"{Fore.YELLOW}! No models downloaded yet{Style.RESET_ALL}")
        return False


def main():
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🔍 SYSTEM CHECK - Ultimate AI Agent 🔍{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    checks = []
    
    # Check Python version
    print(f"{Fore.YELLOW}Python Version:{Style.RESET_ALL}")
    checks.append(check_python_version())
    print()
    
    # Check packages
    print(f"{Fore.YELLOW}Required Packages:{Style.RESET_ALL}")
    packages = [
        ('gpt4all', 'gpt4all'),
        ('langchain', 'langchain'),
        ('langchain-core', 'langchain_core'),
        ('langchain-community', 'langchain_community'),
        ('chromadb', 'chromadb'),
        ('beautifulsoup4', 'bs4'),
        ('requests', 'requests'),
        ('psutil', 'psutil'),
        ('colorama', 'colorama'),
    ]
    
    for package, import_name in packages:
        checks.append(check_package(package, import_name))
    print()
    
    # Check files
    print(f"{Fore.YELLOW}Required Files:{Style.RESET_ALL}")
    checks.append(check_files())
    print()
    
    # Check models
    print(f"{Fore.YELLOW}AI Models:{Style.RESET_ALL}")
    has_model = check_model()
    print()
    
    # Summary
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    if all(checks):
        print(f"{Fore.GREEN}✓ ALL CHECKS PASSED!{Style.RESET_ALL}\n")
        
        if has_model:
            print(f"{Fore.GREEN}🎉 You're ready to use the agent!{Style.RESET_ALL}\n")
            print(f"{Fore.CYAN}Run:{Style.RESET_ALL}")
            print(f"  python start_agent.py\n")
        else:
            print(f"{Fore.YELLOW}⚠️  You need to download a model first{Style.RESET_ALL}\n")
            print(f"{Fore.CYAN}Run:{Style.RESET_ALL}")
            print(f"  python setup_model.py\n")
    else:
        print(f"{Fore.RED}✗ SOME CHECKS FAILED{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Missing packages? Try:{Style.RESET_ALL}")
        print(f"  pip install -r requirements.txt\n")
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
