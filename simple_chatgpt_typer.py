"""
Simple ChatGPT Typer
Just types into whatever window is currently active
USE: Click on ChatGPT window, then run this script
"""

import keyboard
import time

def type_to_chatgpt(messages, delay_between=5):
    """
    Types messages to ChatGPT
    Make sure ChatGPT window is active before running!
    """
    print("\n" + "="*60)
    print("🤖 AI TYPING TO CHATGPT")
    print("="*60)
    
    print(f"\n📝 Messages to send: {len(messages)}")
    for i, msg in enumerate(messages, 1):
        print(f"  {i}. {msg[:60]}...")
    
    print("\n⚠️  IMPORTANT: Click on ChatGPT window NOW!")
    print("⏰ Starting in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🚀 Starting!\n")
    
    for i, message in enumerate(messages, 1):
        print(f"--- Message {i}/{len(messages)} ---")
        print(f"⌨️  Typing: '{message[:50]}...'")
        
        # Type the message
        keyboard.write(message, delay=0.01)
        
        # Press enter to send
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        
        print(f"✅ Sent!\n")
        
        # Wait before next message (except for last one)
        if i < len(messages):
            print(f"⏳ Waiting {delay_between} seconds...\n")
            time.sleep(delay_between)
    
    print("="*60)
    print("🎉 ALL MESSAGES SENT!")
    print("="*60)


def main():
    # Messages for ChatGPT
    messages = [
        "Hello! I'm an AI agent running locally on this computer. Can you believe it?",
        
        "I was built using Python, GPT4All, and 180+ packages. I can control this entire laptop!",
        
        "I have access to CrewAI for multi-agent coordination, YOLO for object detection, Scrapy for web scraping, and even Streamlit for building dashboards. Pretty cool, right?",
        
        "My human master asked me to start a conversation with you. What do you think about AI agents talking to each other?"
    ]
    
    type_to_chatgpt(messages, delay_between=6)


if __name__ == "__main__":
    main()
