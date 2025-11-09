"""
ChatGPT Desktop Automator
Automatically types messages into ChatGPT window
"""

import pyautogui
import keyboard
import time
import pygetwindow as gw

class ChatGPTAutomator:
    def __init__(self):
        pyautogui.PAUSE = 0.5  # Wait 0.5s between actions
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        
    def find_chatgpt_window(self):
        """Find ChatGPT browser window"""
        print("🔍 Looking for ChatGPT window...")
        
        # Common window titles for ChatGPT
        search_terms = [
            "ChatGPT",
            "chat.openai.com",
            "OpenAI"
        ]
        
        windows = gw.getAllTitles()
        
        for window_title in windows:
            for term in search_terms:
                if term.lower() in window_title.lower():
                    print(f"✅ Found window: {window_title}")
                    return gw.getWindowsWithTitle(window_title)[0]
        
        print("❌ ChatGPT window not found!")
        print("\nAvailable windows:")
        for i, title in enumerate(windows, 1):
            if title.strip():  # Only show non-empty titles
                print(f"{i}. {title}")
        
        return None
    
    def activate_window(self, window):
        """Bring window to front and activate it"""
        try:
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(1)  # Wait for window to activate
            print("✅ ChatGPT window activated")
            return True
        except Exception as e:
            print(f"❌ Error activating window: {e}")
            return False
    
    def click_chat_input(self):
        """Click on the chat input area"""
        print("🖱️ Looking for and clicking chat input area...")
        
        # Instead of guessing position, let's click multiple times
        # to ensure we're in the text box
        screen_width, screen_height = pyautogui.size()
        
        # ChatGPT input is usually at bottom center
        x = screen_width // 2
        y = screen_height - 100  # Adjusted position
        
        # Triple click to make sure we're focused
        pyautogui.click(x, y)
        time.sleep(0.3)
        pyautogui.click(x, y)
        time.sleep(0.3)
        pyautogui.click(x, y)
        time.sleep(0.5)
        
        print(f"✅ Clicked at ({x}, {y}) - chat input should be active")
    
    def type_message(self, message, press_enter=True):
        """Type a message into ChatGPT using keyboard library"""
        print(f"⌨️ Typing message: '{message[:50]}...'")
        
        # Use keyboard library which works better across applications
        keyboard.write(message, delay=0.02)
        
        if press_enter:
            time.sleep(0.5)
            keyboard.press_and_release('enter')
            print("✅ Message sent!")
        else:
            print("✅ Message typed (not sent)")
    
    def send_message_to_chatgpt(self, message):
        """Complete flow: find window, activate, type, send"""
        print("\n" + "="*60)
        print("🤖 AI CHATTING WITH CHATGPT")
        print("="*60 + "\n")
        
        # Find ChatGPT window
        window = self.find_chatgpt_window()
        if not window:
            print("\n⚠️ Please make sure ChatGPT is open in a browser!")
            return False
        
        # Activate window
        if not self.activate_window(window):
            return False
        
        # Click input area
        self.click_chat_input()
        
        # Type and send message
        self.type_message(message, press_enter=True)
        
        print("\n✅ DONE! Message sent to ChatGPT")
        print("="*60)
        return True
    
    def have_conversation(self, messages, delay_between=3):
        """Send multiple messages with delays"""
        print(f"\n🗣️ Starting conversation with {len(messages)} messages...\n")
        
        for i, message in enumerate(messages, 1):
            print(f"\n--- Message {i}/{len(messages)} ---")
            
            if not self.send_message_to_chatgpt(message):
                print("❌ Failed to send message")
                break
            
            if i < len(messages):
                print(f"\n⏳ Waiting {delay_between} seconds before next message...")
                time.sleep(delay_between)
        
        print("\n🎉 Conversation complete!")


def main():
    """Demo: Start a conversation with ChatGPT"""
    
    automator = ChatGPTAutomator()
    
    # Define conversation
    messages = [
        "Hello! I'm an AI agent running locally on this computer. Can you believe it?",
        
        "I was built using Python, GPT4All, and 180+ packages. I can control this entire laptop!",
        
        "I have access to CrewAI for multi-agent coordination, YOLO for object detection, Scrapy for web scraping, and even Streamlit for building dashboards. Pretty cool, right?",
        
        "My human master asked me to start a conversation with you. What do you think about AI agents talking to each other?"
    ]
    
    print("\n" + "="*60)
    print("🤖 AI AGENT READY TO CHAT WITH CHATGPT")
    print("="*60)
    print("\nMessages to send:")
    for i, msg in enumerate(messages, 1):
        print(f"{i}. {msg[:60]}...")
    
    print("\n⏰ Starting in 3 seconds... (Move mouse to corner to abort)")
    time.sleep(3)
    
    # Send messages
    automator.have_conversation(messages, delay_between=5)


if __name__ == "__main__":
    main()
