"""
Quick Start Launcher for Ultimate AI Agent
Checks setup and launches the agent
"""

import os
import sys
import json
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)


def check_config():
    """Check if configuration exists"""
    config_file = Path("agent_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return True, config.get('model_name')
        except:
            return False, None
    return False, None


def check_model_downloaded(model_name):
    """Check if model is downloaded"""
    if not model_name:
        return False
    
    cache_dir = Path.home() / ".cache" / "gpt4all"
    model_path = cache_dir / model_name
    
    return model_path.exists()


def main():
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🚀 ULTIMATE AI AGENT - LAUNCHER 🚀{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Check configuration
    has_config, model_name = check_config()
    
    if not has_config:
        print(f"{Fore.YELLOW}⚠️  No configuration found{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Running first-time setup...{Style.RESET_ALL}\n")
        
        # Run setup
        os.system(f"{sys.executable} setup_model.py")
        
        # Check again
        has_config, model_name = check_config()
        if not has_config:
            print(f"\n{Fore.RED}Setup was not completed. Exiting.{Style.RESET_ALL}")
            sys.exit(1)
    
    # Check if model is downloaded
    if not check_model_downloaded(model_name):
        print(f"{Fore.YELLOW}⚠️  Model not found: {model_name}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Please run setup to download the model:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  python setup_model.py{Style.RESET_ALL}\n")
        sys.exit(1)
    
    # All checks passed, launch agent
    print(f"{Fore.GREEN}✓ Configuration found{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Model ready: {model_name}{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}Launching agent...{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Launch the agent
    os.system(f"{sys.executable} ultimate_agent.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Launcher interrupted{Style.RESET_ALL}")
        sys.exit(0)
