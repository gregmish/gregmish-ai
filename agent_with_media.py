"""
AI Agent with Media Creation Powers
Can create images, videos, and social media content!
"""

from gpt4all import GPT4All
from colorama import Fore, Style, init
import subprocess
import re
from media_creator import MediaCreator

init(autoreset=True)

class MediaAIAgent:
    def __init__(self, model_name="orca-mini-3b-gguf2-q4_0.gguf"):
        print(f"{Fore.CYAN}Loading AI model...{Style.RESET_ALL}")
        self.llm = GPT4All(model_name, device='cpu')
        self.media = MediaCreator()
        print(f"{Fore.GREEN}✓ AI Model loaded{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Media Creator ready{Style.RESET_ALL}\n")
    
    def run_task(self, task):
        print(f"{Fore.YELLOW}Task: {task}{Style.RESET_ALL}\n")
        
        # Check if it's a media creation task
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["image", "picture", "graphic", "photo", "instagram", "thumbnail", "post"]):
            return self._handle_media_task(task)
        else:
            return self._handle_system_task(task)
    
    def _handle_media_task(self, task):
        """Handle image/video creation tasks"""
        
        print(f"{Fore.CYAN}🎨 Media creation task detected{Style.RESET_ALL}\n")
        
        prompt = f"""Task: {task}

Analyze this task and extract:
1. Platform (instagram_post, instagram_story, youtube_thumbnail, tiktok, twitter_post)
2. Main text to display
3. Subtitle (if any)
4. Type (text_image, thumbnail, gradient)

Respond in this format:
PLATFORM: platform_name
TEXT: main text
SUBTITLE: subtitle text (or NONE)
TYPE: type_name

Your response:"""

        response = self.llm.generate(prompt, max_tokens=200)
        
        # Parse response
        platform = "instagram_post"
        text = "Your Content Here"
        subtitle = None
        task_type = "text_image"
        
        # Extract from AI response
        platform_match = re.search(r'PLATFORM:\s*(.+)', response, re.IGNORECASE)
        text_match = re.search(r'TEXT:\s*(.+)', response, re.IGNORECASE)
        subtitle_match = re.search(r'SUBTITLE:\s*(.+)', response, re.IGNORECASE)
        type_match = re.search(r'TYPE:\s*(.+)', response, re.IGNORECASE)
        
        if platform_match:
            platform = platform_match.group(1).strip()
        if text_match:
            text = text_match.group(1).strip()
        if subtitle_match and "NONE" not in subtitle_match.group(1).upper():
            subtitle = subtitle_match.group(1).strip()
        if type_match:
            task_type = type_match.group(1).strip()
        
        print(f"{Fore.GREEN}Creating content:{Style.RESET_ALL}")
        print(f"  Platform: {platform}")
        print(f"  Text: {text}")
        if subtitle:
            print(f"  Subtitle: {subtitle}")
        print()
        
        # Create the content
        try:
            if "thumbnail" in task_type.lower() or "youtube" in platform.lower():
                output = self.media.create_thumbnail(text, subtitle or "", filename=None)
            elif "gradient" in task_type.lower():
                output = self.media.create_gradient_background(platform)
            else:
                output = self.media.create_text_image(text, platform)
            
            print(f"{Fore.GREEN}✓ Created: {output}{Style.RESET_ALL}\n")
            
            # Open the file
            subprocess.run(['start', output], shell=True)
            print(f"{Fore.CYAN}Opening the image...{Style.RESET_ALL}")
            
            return f"Created and opened: {output}"
        
        except Exception as e:
            return f"Error creating media: {e}"
    
    def _handle_system_task(self, task):
        """Handle regular system tasks"""
        
        prompt = f"""You are an AI that controls a Windows laptop via PowerShell commands.

Task: {task}

Respond with ONLY the PowerShell command, nothing else:"""

        print(f"{Fore.CYAN}🤔 AI is thinking...{Style.RESET_ALL}\n")
        response = self.llm.generate(prompt, max_tokens=150, temp=0.7)
        
        command = response.strip()
        command = re.sub(r'^(Command:|PowerShell:|PS>|>)\s*', '', command, flags=re.IGNORECASE)
        command = command.split('\n')[0].strip()
        
        print(f"{Fore.GREEN}Command:{Style.RESET_ALL} {command}\n")
        
        choice = input(f"{Fore.YELLOW}Execute? (y/n): {Style.RESET_ALL}").strip().lower()
        
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
                return "Task completed"
            except Exception as e:
                return f"Error: {e}"
        else:
            return "Cancelled"

def main():
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🤖 AI AGENT + MEDIA CREATOR 🎨{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Control your laptop + Create social media content!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    agent = MediaAIAgent()
    
    print(f"{Fore.GREEN}Ready! Try these commands:{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Media Creation:{Style.RESET_ALL}")
    print(f"  - 'Create an Instagram post saying Hello World'")
    print(f"  - 'Make a YouTube thumbnail for my AI video'")
    print(f"  - 'Create a gradient background for Instagram story'")
    print(f"\n{Fore.YELLOW}System Control:{Style.RESET_ALL}")
    print(f"  - 'Open Edge and go to Gumroad'")
    print(f"  - 'Check my CPU usage'")
    print(f"  - 'Create a folder called MyVideos'")
    print()
    
    while True:
        try:
            task = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            
            if not task:
                continue
            
            if task.lower() in ['quit', 'exit', 'q']:
                print(f"{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}")
                break
            
            agent.run_task(task)
            print(f"\n{Fore.CYAN}{'-'*70}{Style.RESET_ALL}\n")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Use 'quit' to exit{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
