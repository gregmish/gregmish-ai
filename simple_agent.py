"""
Simple AI Agent - Works immediately without complex dependencies  
"""

import subprocess
from gpt4all import GPT4All
from colorama import Fore, Style, init
import re

init(autoreset=True)

class SimpleAgent:
    def __init__(self, model_name="orca-mini-3b-gguf2-q4_0.gguf"):
        print(f"{Fore.CYAN}Loading AI model...{Style.RESET_ALL}")
        self.llm = GPT4All(model_name, device='cpu')
        print(f"{Fore.GREEN}✓ Model loaded!{Style.RESET_ALL}\n")
    
    def run_task(self, task):
        print(f"{Fore.YELLOW}Task: {task}{Style.RESET_ALL}\n")
        
        prompt = f"""You are an AI that controls a Windows laptop.

Task: {task}

Think about what you need to do and respond with a PowerShell command to execute.

Examples:
- To open Edge and go to a website: start msedge "https://example.com"
- To check CPU usage: Get-Process | Sort-Object CPU -Descending | Select-Object -First 5
- To create a folder: New-Item -ItemType Directory -Path "C:\\Users\\folder_name"

Respond with ONLY the PowerShell command, nothing else:"""

        print(f"{Fore.CYAN}🤔 Thinking...{Style.RESET_ALL}\n")
        response = self.llm.generate(prompt, max_tokens=200, temp=0.7)
        
        # Clean up the response
        command = response.strip()
        # Remove common prefixes
        command = re.sub(r'^(Command:|PowerShell:|PS>|>)\s*', '', command, flags=re.IGNORECASE)
        command = command.split('\n')[0].strip()  # Take first line only
        
        print(f"{Fore.GREEN}Command to execute:{Style.RESET_ALL}")
        print(f"  {command}\n")
        
        choice = input(f"{Fore.YELLOW}Execute this command? (y/n): {Style.RESET_ALL}").strip().lower()
        
        if choice == 'y':
            try:
                result = subprocess.run(
                    ['powershell', '-Command', command],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                print(f"\n{Fore.GREEN}✓ Executed!{Style.RESET_ALL}\n")
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Cancelled{Style.RESET_ALL}")

def main():
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🚀 SIMPLE AI AGENT 🚀{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    agent = SimpleAgent()
    
    print(f"{Fore.GREEN}Ready! Type your commands:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Example: 'Open Edge and go to Gumroad'{Style.RESET_ALL}\n")
    
    while True:
        try:
            task = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            
            if not task:
                continue
            
            if task.lower() in ['quit', 'exit', 'q']:
                print(f"{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}")
                break
            
            agent.run_task(task)
            print()
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Use 'quit' to exit{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
