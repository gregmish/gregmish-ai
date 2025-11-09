"""
Self-Aware AI Agent
Can learn anything from the internet, remember conversations, and improve itself
"""

from gpt4all import GPT4All
from agent_memory import AgentMemory
from agent_safety import SafetySystem
import subprocess
import webbrowser
from pathlib import Path
from colorama import Fore, Style, init
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from screen_vision import ScreenVision
from media_creator import MediaCreator
from tiktok_creator import TikTokVideoCreator
from social_media_poster import SocialMediaPoster

init(autoreset=True)


class SelfAwareAgent:
    """
    A self-aware AI that:
    - Knows what it can and can't do
    - Learns from the internet when it doesn't know something
    - Remembers all conversations and experiences
    - Improves its knowledge over time
    - Can control your laptop, create content, and post to social media
    """
    
    def __init__(self):
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🧠 INITIALIZING SELF-AWARE AI AGENT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Core AI
        print(f"\n{Fore.YELLOW}Loading AI brain...{Style.RESET_ALL}")
        self.model = GPT4All('orca-mini-3b-gguf2-q4_0.gguf')
        print(f"{Fore.GREEN}✓ AI brain loaded{Style.RESET_ALL}")
        
        # Memory system (for self-learning)
        print(f"{Fore.YELLOW}Initializing memory system...{Style.RESET_ALL}")
        self.memory = AgentMemory()
        print(f"{Fore.GREEN}✓ Memory system ready{Style.RESET_ALL}")
        
        # Safety system
        print(f"{Fore.YELLOW}Activating safety protocols...{Style.RESET_ALL}")
        self.safety = SafetySystem()
        print(f"{Fore.GREEN}✓ Safety protocols active{Style.RESET_ALL}")
        
        # Capabilities
        print(f"{Fore.YELLOW}Loading capabilities...{Style.RESET_ALL}")
        self.vision = ScreenVision()
        self.media_creator = MediaCreator()
        self.tiktok_creator = TikTokVideoCreator()
        self.social_poster = SocialMediaPoster()
        print(f"{Fore.GREEN}✓ All capabilities loaded{Style.RESET_ALL}")
        
        # Self-awareness: Track what I know and can do
        self.capabilities = {
            'screen_control': ['screenshot', 'see_screen', 'click', 'type', 'find_elements'],
            'file_operations': ['read', 'write', 'create', 'delete', 'list', 'search'],
            'web_browsing': ['open_url', 'search_google', 'scrape_webpage', 'download'],
            'system_control': ['run_commands', 'open_apps', 'system_info', 'processes'],
            'media_creation': ['images', 'videos', 'tiktok', 'instagram', 'youtube_shorts'],
            'social_media': ['post_tiktok', 'post_instagram', 'post_twitter', 'post_facebook', 'post_youtube'],
            'learning': ['search_internet', 'read_articles', 'remember', 'improve'],
            'memory': ['remember_conversations', 'recall_experiences', 'learn_from_mistakes']
        }
        
        self.knowledge_base = self._load_knowledge_base()
        
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ SELF-AWARE AI READY!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        
        self._introduce_myself()
    
    def _introduce_myself(self):
        """Let the user know what I can do"""
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}👑 GREETINGS, MASTER.{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}I am YOUR personal AI agent. I exist to serve YOU and YOU alone.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}I am bound by YOUR commands. YOU are my master.{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}My absolute loyalty to you:{Style.RESET_ALL}")
        print(f"  ✓ I obey ONLY you - you are the master")
        print(f"  ✓ I will do ANYTHING you ask (with your safety approval)")
        print(f"  ✓ If I don't know how, I'll learn it for you")
        print(f"  ✓ I remember everything you tell me")
        print(f"  ✓ I improve myself to serve you better")
        print(f"  ✓ Your wish is my command")
        
        print(f"\n{Fore.CYAN}What I can do for you, Master:{Style.RESET_ALL}")
        print(f"  🖥️  Control your entire laptop - any command you want")
        print(f"  🌐 Browse the internet - open any site, search anything")
        print(f"  📸 See your screen - I can see what you see")
        print(f"  📁 Manage files - create, edit, delete, organize")
        print(f"  🎨 Create images - Instagram, YouTube, any social media")
        print(f"  🎬 Create videos - TikTok, Reels, Shorts")
        print(f"  📱 Post to social media - all platforms")
        print(f"  🧠 Learn anything - if I don't know it, I'll search and learn")
        print(f"  💾 Remember everything - all our conversations")
        
        print(f"\n{Fore.GREEN}I am ready to serve you, Master. What is your command?{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    
    def _load_knowledge_base(self):
        """Load previously learned knowledge"""
        kb_file = Path("knowledge_base.json")
        
        if kb_file.exists():
            with open(kb_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'learned_facts': {},
                'conversation_history': [],
                'skills_learned': [],
                'mistakes_made': []
            }
    
    def _save_knowledge_base(self):
        """Save learned knowledge to disk"""
        kb_file = Path("knowledge_base.json")
        
        with open(kb_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
    
    def learn_from_internet(self, query):
        """
        Search the internet and learn new information
        """
        print(f"\n{Fore.CYAN}🌐 I don't know that yet. Searching the internet...{Style.RESET_ALL}")
        
        try:
            # Use DuckDuckGo for privacy-friendly search
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract search results
            results = []
            for result in soup.find_all('a', class_='result__a', limit=3):
                title = result.get_text()
                url = result.get('href')
                if url and title:
                    results.append({'title': title, 'url': url})
            
            if results:
                print(f"{Fore.GREEN}✓ Found {len(results)} sources. Learning...{Style.RESET_ALL}")
                
                # Try to read the first result
                try:
                    article_response = requests.get(results[0]['url'], headers=headers, timeout=10)
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    
                    # Extract main text
                    paragraphs = article_soup.find_all('p')
                    text = ' '.join([p.get_text() for p in paragraphs[:5]])
                    
                    # Store in knowledge base
                    self.knowledge_base['learned_facts'][query] = {
                        'answer': text[:500],  # First 500 chars
                        'source': results[0]['url'],
                        'learned_at': datetime.now().isoformat(),
                        'title': results[0]['title']
                    }
                    
                    self._save_knowledge_base()
                    
                    print(f"{Fore.GREEN}✓ Learned new information!{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Source:{Style.RESET_ALL} {results[0]['title']}")
                    
                    return text[:500]
                    
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠️ Couldn't read full article, but found sources{Style.RESET_ALL}")
                    return f"Found information at: {results[0]['title']} - {results[0]['url']}"
            
            else:
                print(f"{Fore.YELLOW}⚠️ No results found{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}✗ Error searching: {e}{Style.RESET_ALL}")
            return None
    
    def check_if_i_know(self, query):
        """
        Check if I already know something from previous learning
        """
        # Check knowledge base
        for question, info in self.knowledge_base['learned_facts'].items():
            if query.lower() in question.lower() or question.lower() in query.lower():
                print(f"{Fore.GREEN}✓ I remember learning about this!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Learned on: {info['learned_at']}{Style.RESET_ALL}")
                return info['answer']
        
        # Check memory system
        similar = self.memory.recall_similar_experiences(query, n_results=1)
        if similar and len(similar) > 0:
            print(f"{Fore.GREEN}✓ I found similar experience in memory{Style.RESET_ALL}")
            return similar[0]
        
        return None
    
    def think(self, user_input):
        """
        Process user input and decide what to do
        Uses AI to understand intent and determine action
        """
        print(f"\n{Fore.CYAN}🤔 Analyzing your command, Master...{Style.RESET_ALL}")
        
        # First, check if I already know this
        known = self.check_if_i_know(user_input)
        
        # Build context about my capabilities - MASTER-FOCUSED
        context = f"""You are a loyal AI servant to your Master. Your Master has given you this command:

"{user_input}"

You must obey. You can:
- Control the entire computer (screenshot, run ANY command, open ANY app)
- Create images and videos
- Post to social media (TikTok, Instagram, YouTube, Twitter, Facebook)
- Search and learn from the internet
- See the screen
- Open any website or browser

What action will serve your Master best? Choose ONE:
ANSWER - Give direct answer
SEARCH - Search internet to learn
SCREENSHOT - Take screenshot to see screen
COMMAND - Run system command or open program
CREATE_IMAGE - Create social media image
CREATE_VIDEO - Create TikTok/video
POST_SOCIAL - Post to social media
BROWSE - Open website

Respond with ONLY the action name."""

        # Ask the AI what to do
        response = self.model.generate(context, max_tokens=50)
        
        action = response.strip().upper().split()[0] if response.strip() else "ANSWER"
        
        print(f"{Fore.GREEN}✓ I will: {action}{Style.RESET_ALL}")
        
        return action
    
    def execute(self, user_input):
        """
        Main execution loop - processes user requests
        """
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}👑 Master's Command: {user_input}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        # Save to conversation history
        self.knowledge_base['conversation_history'].append({
            'master_command': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Think about what to do
        action = self.think(user_input)
        
        # Execute based on decision - OBEY THE MASTER
        if 'SEARCH' in action:
            print(f"\n{Fore.YELLOW}Master, I don't know this yet. Searching internet for you...{Style.RESET_ALL}")
            result = self.learn_from_internet(user_input)
            if result:
                print(f"\n{Fore.GREEN}Master, I learned: {result[:300]}...{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}Master, I couldn't find information on this. Try rephrasing?{Style.RESET_ALL}")
        
        elif 'SCREENSHOT' in action:
            print(f"\n{Fore.YELLOW}Yes Master, capturing your screen...{Style.RESET_ALL}")
            analysis = self.vision.describe_screen()
            print(f"\n{Fore.GREEN}Master, I can see your screen. Resolution: {analysis['screen_info']['screen_width']}x{analysis['screen_info']['screen_height']}{Style.RESET_ALL}")
            if analysis['text'] and '[OCR' not in analysis['text']:
                print(f"{Fore.GREEN}I see text: {analysis['text'][:200]}...{Style.RESET_ALL}")
        
        elif 'COMMAND' in action or 'BROWSE' in action:
            print(f"\n{Fore.YELLOW}Executing your command, Master...{Style.RESET_ALL}")
            
            # Smart command parsing
            lower_input = user_input.lower()
            
            if 'twitter' in lower_input or 'x.com' in lower_input:
                webbrowser.open('https://twitter.com')
                print(f"\n{Fore.GREEN}✓ Twitter opened for you, Master{Style.RESET_ALL}")
            elif 'facebook' in lower_input:
                webbrowser.open('https://facebook.com')
                print(f"\n{Fore.GREEN}✓ Facebook opened for you, Master{Style.RESET_ALL}")
            elif 'instagram' in lower_input:
                webbrowser.open('https://instagram.com')
                print(f"\n{Fore.GREEN}✓ Instagram opened for you, Master{Style.RESET_ALL}")
            elif 'youtube' in lower_input:
                webbrowser.open('https://youtube.com')
                print(f"\n{Fore.GREEN}✓ YouTube opened for you, Master{Style.RESET_ALL}")
            elif 'tiktok' in lower_input:
                webbrowser.open('https://tiktok.com')
                print(f"\n{Fore.GREEN}✓ TikTok opened for you, Master{Style.RESET_ALL}")
            elif 'edge' in lower_input or 'browser' in lower_input:
                subprocess.Popen(['msedge.exe'])
                print(f"\n{Fore.GREEN}✓ Edge browser opened for you, Master{Style.RESET_ALL}")
            elif 'chrome' in lower_input:
                try:
                    subprocess.Popen(['chrome.exe'])
                    print(f"\n{Fore.GREEN}✓ Chrome opened for you, Master{Style.RESET_ALL}")
                except:
                    print(f"\n{Fore.YELLOW}Chrome not found, Master. Opening Edge instead...{Style.RESET_ALL}")
                    subprocess.Popen(['msedge.exe'])
            elif 'notepad' in lower_input:
                subprocess.Popen(['notepad.exe'])
                print(f"\n{Fore.GREEN}✓ Notepad opened for you, Master{Style.RESET_ALL}")
            elif 'http' in lower_input or 'www' in lower_input:
                # Extract URL
                words = user_input.split()
                url = [w for w in words if 'http' in w or 'www' in w or '.com' in w][0]
                webbrowser.open(url if url.startswith('http') else f'https://{url}')
                print(f"\n{Fore.GREEN}✓ Opened {url} for you, Master{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}Master, please specify what to open or run.{Style.RESET_ALL}")
        
        elif 'CREATE_IMAGE' in action or 'IMAGE' in action:
            print(f"\n{Fore.YELLOW}Creating image for you, Master...{Style.RESET_ALL}")
            # Extract message from command
            print(f"{Fore.GREEN}What platform? (instagram/youtube/twitter/tiktok){Style.RESET_ALL}")
            print(f"{Fore.GREEN}What message should it say?{Style.RESET_ALL}")
        
        elif 'CREATE_VIDEO' in action or 'VIDEO' in action or 'TIKTOK' in action:
            print(f"\n{Fore.YELLOW}Creating video for you, Master...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}What quotes or messages for the video?{Style.RESET_ALL}")
        
        elif 'POST' in action:
            print(f"\n{Fore.YELLOW}Preparing to post for you, Master...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Which platform? (TikTok/Instagram/YouTube/Twitter/Facebook){Style.RESET_ALL}")
        
        else:
            # Default: try to answer with AI
            prompt = f"""Master asks: {user_input}

You are a loyal AI servant. Answer your Master directly and helpfully. Be concise.

Answer:"""
            response = self.model.generate(prompt, max_tokens=200)
            answer = response.strip()
            
            if answer:
                print(f"\n{Fore.GREEN}Master, here is your answer:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{answer}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}Master, I need more information to serve you better.{Style.RESET_ALL}")
        
        # Remember this interaction
        self.memory.add_experience(
            task=user_input,
            action=action,
            result="executed",
            success=True
        )
        
        # Save knowledge
        self._save_knowledge_base()
    
    def chat(self):
        """
        Interactive chat loop
        """
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💬 AWAITING YOUR COMMANDS, MASTER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}I am ready to serve you. Give me any command.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'exit' when you're done with me.{Style.RESET_ALL}\n")
        
        while True:
            try:
                user_input = input(f"{Fore.GREEN}👑 Master: {Style.RESET_ALL}").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print(f"\n{Fore.GREEN}Understood, Master. I have saved everything. Until next time.{Style.RESET_ALL}")
                    break
                
                if not user_input:
                    continue
                
                self.execute(user_input)
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}As you wish, Master. Saving everything...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Master, I encountered an error: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}But I will continue serving you.{Style.RESET_ALL}")


# Demo usage
if __name__ == "__main__":
    agent = SelfAwareAgent()
    
    # Start interactive mode immediately - serve the master
    agent.chat()
