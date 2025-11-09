"""
Demo Script - Examples of what the Ultimate AI Agent can do
Run this to see the agent in action!
"""

from colorama import Fore, Style, init
import time

init(autoreset=True)

DEMO_TASKS = [
    {
        "category": "📁 File Operations",
        "tasks": [
            "Create a folder called 'test_agent' on my Desktop",
            "Create a file called 'hello.txt' in that folder with the text 'Hello from AI Agent!'",
            "Read the contents of that file back to me",
            "List all files in the test_agent folder",
        ]
    },
    {
        "category": "💻 System Information",
        "tasks": [
            "Check my current CPU and memory usage",
            "Show me the top 5 processes using the most CPU",
            "How much disk space do I have available?",
        ]
    },
    {
        "category": "🐍 Python Execution",
        "tasks": [
            "Calculate the factorial of 10",
            "Generate the first 15 fibonacci numbers",
            "Create a function that checks if a number is prime and test it with 17",
        ]
    },
    {
        "category": "🌐 Web & Research",
        "tasks": [
            "Fetch the content from example.com and summarize it",
            "Get information about the Python requests library",
        ]
    },
    {
        "category": "🔧 Advanced Tasks",
        "tasks": [
            "Create a Python script that counts words in a text file",
            "Write a batch file that prints 'Hello World'",
            "Check if Python is installed and show me the version",
        ]
    }
]


def print_header():
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🎯 ULTIMATE AI AGENT - DEMO EXAMPLES 🎯{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def print_category(category):
    print(f"\n{Fore.YELLOW}{category}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'-'*len(category)}{Style.RESET_ALL}\n")


def main():
    print_header()
    
    print(f"{Fore.GREEN}Here are some example tasks you can give to the AI Agent:{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}These examples demonstrate the agent's capabilities.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}You can copy any of these and use them when talking to the agent!{Style.RESET_ALL}\n")
    
    for section in DEMO_TASKS:
        print_category(section["category"])
        
        for i, task in enumerate(section["tasks"], 1):
            print(f"  {Fore.GREEN}{i}.{Style.RESET_ALL} {task}")
        
        print()
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}💡 Tips for Best Results:{Style.RESET_ALL}\n")
    print(f"  • Be specific about what you want")
    print(f"  • Break complex tasks into smaller steps")
    print(f"  • The agent learns from experience - it gets better over time!")
    print(f"  • Check 'stats' to see what the agent has learned")
    print(f"  • Use 'export' to save all learned knowledge\n")
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}Ready to try? Run:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  python start_agent.py{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Or go straight to the agent:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  python ultimate_agent.py{Style.RESET_ALL}\n")
    
    # Interactive option
    choice = input(f"{Fore.GREEN}Want to start the agent now? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if choice == 'y':
        print(f"\n{Fore.CYAN}Launching agent...{Style.RESET_ALL}\n")
        import os
        import sys
        os.system(f"{sys.executable} start_agent.py")


if __name__ == "__main__":
    main()
