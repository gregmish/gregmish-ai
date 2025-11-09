"""
Demo: How the agent will open Edge and navigate to Gumroad
This shows the exact flow without needing the AI model
"""

from colorama import Fore, Style, init
import subprocess

init(autoreset=True)

print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
print(f"{Fore.CYAN}  DEMO: Opening Edge Browser and Navigating to Gumroad{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

print(f"{Fore.YELLOW}You say:{Style.RESET_ALL} \"Open Edge browser and go to Gumroad\"\n")

print(f"{Fore.CYAN}Agent thinks:{Style.RESET_ALL}")
print(f"  💭 I need to open Microsoft Edge")
print(f"  💭 I should navigate to gumroad.com")
print(f"  💭 I'll use the terminal_command tool\n")

print(f"{Fore.CYAN}Agent prepares command:{Style.RESET_ALL}")
command = 'start msedge "https://gumroad.com"'
print(f"  📝 PowerShell: {Fore.GREEN}{command}{Style.RESET_ALL}\n")

print(f"{Fore.CYAN}Safety Check:{Style.RESET_ALL}")
print(f"  ✓ Opening browser is safe")
print(f"  ✓ Navigating to gumroad.com is safe")
print(f"  ✓ No approval needed\n")

print(f"{Fore.YELLOW}Do you want me to execute this now? (y/n):{Style.RESET_ALL} ", end='')
choice = input().strip().lower()

if choice == 'y':
    print(f"\n{Fore.GREEN}Executing...{Style.RESET_ALL}\n")
    
    try:
        # Actually open Edge and go to Gumroad
        subprocess.run(['powershell', '-Command', command], check=True)
        
        print(f"{Fore.GREEN}✓ Success!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  Edge browser opened{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  Navigated to https://gumroad.com{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Agent learns:{Style.RESET_ALL}")
        print(f"  📚 Stored in memory: 'Open Edge + URL' → use 'start msedge [url]'")
        print(f"  📚 Next time this will be even faster!\n")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}(Edge might not be installed or path not found){Style.RESET_ALL}\n")
else:
    print(f"\n{Fore.YELLOW}Demo cancelled. No action taken.{Style.RESET_ALL}\n")

print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
print(f"\n{Fore.YELLOW}This is EXACTLY what the full agent will do when you:{Style.RESET_ALL}")
print(f"  1. Download a model with: {Fore.GREEN}python setup_model.py{Style.RESET_ALL}")
print(f"  2. Launch the agent with: {Fore.GREEN}python start_agent.py{Style.RESET_ALL}")
print(f"  3. Say: {Fore.GREEN}\"Open Edge and go to Gumroad\"{Style.RESET_ALL}\n")

print(f"{Fore.CYAN}The agent can also do:{Style.RESET_ALL}")
print(f"  • \"Open Edge and search Google for AI models\"")
print(f"  • \"Open Edge with multiple tabs: YouTube, Gmail, and Twitter\"")
print(f"  • \"Close all Edge windows\"")
print(f"  • \"Open Chrome/Firefox/any browser with any URL\"\n")

print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
