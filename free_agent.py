"""
FREE ChatGPT Agent Alternative
Unlimited screen control + chat using local Ollama
No usage limits, no $20/month, works forever
"""

import requests
import json
import time
from vivian_screen import VivianScreenAgent
from tools.browser_tool import BrowserTool

class FreeAgent:
    def __init__(self):
        self.model = "qwen2.5:latest"
        self.ollama_url = "http://localhost:11434/api/generate"
        self.screen = VivianScreenAgent()
        self.browser = BrowserTool()
        self.conversation_history = []
        
    def chat(self, user_message: str) -> str:
        """Send message to AI and get response"""
        # Build context from conversation history
        context = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in self.conversation_history[-10:]  # Last 10 messages
        ])
        
        prompt = f"""You are a helpful AI assistant with computer control abilities.

Previous conversation:
{context if context else "No previous conversation"}

User: {user_message}

You can use these tools:
1. SCREEN_CONTROL: Control the computer screen (open apps, type, click)
2. CHECK_GUMROAD: Check Gumroad sales data
3. CHAT: Just respond with text

Think about what the user wants. If they want you to DO something on the computer, use SCREEN_CONTROL or CHECK_GUMROAD. Otherwise just CHAT.

Respond in this format:
TOOL: [SCREEN_CONTROL or CHECK_GUMROAD or CHAT]
ACTION: [what to do if using a tool]
RESPONSE: [your message to the user]

Example 1:
User: "Open notepad and write hello"
TOOL: SCREEN_CONTROL
ACTION: open notepad and type hello
RESPONSE: I'll open notepad and type hello for you.

Example 2:
User: "How much have I made on Gumroad?"
TOOL: CHECK_GUMROAD
ACTION: scrape sales
RESPONSE: Let me check your Gumroad sales.

Example 3:
User: "What's the weather like?"
TOOL: CHAT
ACTION: none
RESPONSE: I don't have access to weather data, but you could check weather.com or ask me to open it for you.

Your response:"""
        
        response = requests.post(
            self.ollama_url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        
        return response.json()['response']
    
    def parse_response(self, ai_response: str) -> dict:
        """Parse AI response into tool, action, and message"""
        lines = ai_response.strip().split('\n')
        tool = "CHAT"
        action = ""
        response = ai_response  # Default to full response if parsing fails
        
        for line in lines:
            if line.startswith("TOOL:"):
                tool = line.replace("TOOL:", "").strip()
            elif line.startswith("ACTION:"):
                action = line.replace("ACTION:", "").strip()
            elif line.startswith("RESPONSE:"):
                response = line.replace("RESPONSE:", "").strip()
        
        return {"tool": tool, "action": action, "response": response}
    
    def execute_tool(self, tool: str, action: str) -> str:
        """Execute the requested tool"""
        if tool == "SCREEN_CONTROL":
            print(f"\n🖥️  Executing screen control: {action}")
            self.screen.run(action)
            return f"✅ Completed: {action}"
        
        elif tool == "CHECK_GUMROAD":
            print(f"\n📊 Checking Gumroad sales...")
            result = self.browser.check_gumroad_sales()
            revenue = result.get('total_revenue', 0)
            products = result.get('product_count', 0)
            return f"📊 Gumroad Sales:\n💰 Revenue: £{revenue}\n📦 Products: {products}"
        
        return ""
    
    def run(self):
        """Main chat loop - like ChatGPT interface"""
        print("\n" + "="*70)
        print("🤖 FREE CHATGPT AGENT ALTERNATIVE")
        print("="*70)
        print("Unlimited usage • Screen control • No $20/month")
        print("Powered by Ollama Qwen 2.5 (100% free)")
        print("\nType 'quit' to exit")
        print("="*70 + "\n")
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n👋 Later!")
                break
            
            if not user_input:
                continue
            
            # Add to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get AI response
            print("\n🤖 Thinking...")
            ai_response = self.chat(user_input)
            
            # Parse what to do
            parsed = self.parse_response(ai_response)
            
            # Execute tool if needed
            if parsed['tool'] != "CHAT":
                tool_result = self.execute_tool(parsed['tool'], parsed['action'])
                if tool_result:
                    parsed['response'] += f"\n\n{tool_result}"
            
            # Show response
            print(f"\nAssistant: {parsed['response']}\n")
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": parsed['response']
            })


if __name__ == "__main__":
    agent = FreeAgent()
    agent.run()
