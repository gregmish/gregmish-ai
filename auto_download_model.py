"""
Automatic Model Downloader
Downloads Mistral 7B model without interaction
"""

from gpt4all import GPT4All
from colorama import Fore, Style, init
from pathlib import Path
import json

init(autoreset=True)

print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
print(f"{Fore.CYAN}  🤖 AUTOMATIC MODEL DOWNLOAD 🤖{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

# Recommended model
model_name = "mistral-7b-instruct-v0.2.Q4_0.gguf"

print(f"{Fore.YELLOW}Downloading:{Style.RESET_ALL} {model_name}")
print(f"{Fore.YELLOW}Size:{Style.RESET_ALL} ~4.1 GB")
print(f"{Fore.YELLOW}This will take 5-10 minutes...{Style.RESET_ALL}\n")

try:
    print(f"{Fore.CYAN}Starting download...{Style.RESET_ALL}\n")
    
    # GPT4All will automatically download to cache
    model = GPT4All(model_name)
    
    cache_dir = Path.home() / ".cache" / "gpt4all"
    model_path = cache_dir / model_name
    
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ SUCCESS! Model downloaded!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}Location:{Style.RESET_ALL} {model_path}")
    
    # Create config
    config = {
        "model_name": model_name,
        "auto_approve": False,
        "max_iterations": 15,
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    config_file = Path("agent_config.json")
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"{Fore.GREEN}✓ Configuration saved{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🎉 READY TO GO! 🎉{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}Launch the agent:{Style.RESET_ALL}")
    print(f"  python start_agent.py\n")
    print(f"{Fore.GREEN}Then say:{Style.RESET_ALL}")
    print(f"  \"Open Edge browser and go to Gumroad\"")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
except Exception as e:
    print(f"\n{Fore.RED}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.RED}✗ Download failed: {e}{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Alternative: Manual download{Style.RESET_ALL}")
    print(f"1. Visit: https://gpt4all.io/models/gguf/")
    print(f"2. Download: {model_name}")
    print(f"3. Place in: {Path.home() / '.cache' / 'gpt4all'}\n")
