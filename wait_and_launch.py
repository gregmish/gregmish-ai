"""
Check download status and launch agent when ready
"""

import time
import json
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

model_name = "orca-mini-3b-gguf2-q4_0.gguf"
cache_dir = Path.home() / ".cache" / "gpt4all"
model_path = cache_dir / model_name

print(f"\n{Fore.CYAN}Waiting for model download to complete...{Style.RESET_ALL}\n")

# Wait for download to complete
max_wait = 600  # 10 minutes
waited = 0

while waited < max_wait:
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        expected_size = 1980  # ~1.98 GB
        
        if size_mb >= expected_size * 0.99:  # 99% of expected size
            print(f"{Fore.GREEN}✓ Download complete! ({size_mb:.0f} MB){Style.RESET_ALL}\n")
            break
        else:
            print(f"  Downloading... {size_mb:.0f} MB / {expected_size} MB ({size_mb/expected_size*100:.0f}%)", end='\r')
    
    time.sleep(5)
    waited += 5
else:
    print(f"\n{Fore.YELLOW}Download taking longer than expected. Check terminal for progress.{Style.RESET_ALL}")

if model_path.exists():
    # Create config
    config = {
        "model_name": model_name,
        "auto_approve": False,
        "max_iterations": 15,
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    with open("agent_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"{Fore.GREEN}✓ Configuration saved{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🎉 READY TO LAUNCH! 🎉{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}Model:{Style.RESET_ALL} {model_name}")
    print(f"{Fore.GREEN}Location:{Style.RESET_ALL} {model_path}\n")
    print(f"{Fore.YELLOW}Start the agent now:{Style.RESET_ALL}")
    print(f"  python start_agent.py\n")
    print(f"{Fore.YELLOW}Then try:{Style.RESET_ALL}")
    print(f"  \"Open Edge browser and go to Gumroad\"")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Ask if they want to launch now
    choice = input(f"{Fore.GREEN}Launch agent now? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if choice == 'y':
        print(f"\n{Fore.CYAN}Launching Ultimate AI Agent...{Style.RESET_ALL}\n")
        import os
        import sys
        os.system(f"{sys.executable} start_agent.py")
