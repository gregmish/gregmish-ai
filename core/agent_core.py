"""
Core Agent - ONE brain that does everything
No more scattered scripts - this is the single orchestrator
"""

from typing import Dict, List, Optional, Any
import json
import time
from pathlib import Path


class AgentCore:
    """
    The ONE brain - coordinates everything
    - Planning multi-step tasks
    - Executing tools
    - Managing memory
    - Verifying results
    """
    
    def __init__(self):
        self.tools = {}  # Will load from tool_registry
        self.memory = None  # Will load from memory_service
        self.llm = None  # Will load from llm_client
        self.task_history = []
        
    def execute_command(self, user_input: str) -> Dict[str, Any]:
        """
        Main entry point - user says something, we DO it
        
        This is the planning loop:
        1. Understand what they want
        2. Break into steps
        3. Execute each step
        4. Verify it worked
        5. Return result
        """
        
        print(f"\n🧠 Processing: {user_input}")
        
        # Step 1: Understand the intent
        intent = self._parse_intent(user_input)
        print(f"💭 Intent: {intent['action']} - {intent['target']}")
        
        # Step 2: Create a plan
        plan = self._create_plan(intent)
        print(f"📋 Plan: {len(plan['steps'])} steps")
        for i, step in enumerate(plan['steps']):
            print(f"   {i+1}. {step['description']}")
        
        # Step 3: Execute the plan
        results = []
        for i, step in enumerate(plan['steps']):
            print(f"\n⚡ Executing step {i+1}: {step['description']}")
            
            result = self._execute_step(step)
            results.append(result)
            
            if result.get('status') == 'error':
                print(f"❌ Step failed: {result.get('error', 'Unknown error')}")
                # Try to recover
                retry_result = self._retry_step(step, result.get('error', 'Unknown error'))
                if retry_result.get('status') == 'success':
                    print(f"✅ Retry succeeded!")
                    results[-1] = retry_result
                else:
                    print(f"❌ Retry failed - aborting plan")
                    break
            else:
                print(f"✅ Step completed: {result.get('summary', 'Done')}")
        
        # Step 4: Summarize
        final_result = {
            'status': 'completed' if all(r['status'] == 'success' for r in results) else 'partial',
            'plan': plan,
            'results': results,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to task history
        self.task_history.append(final_result)
        
        return final_result
    
    def _parse_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Figure out what the user actually wants
        Uses LLM but structured, not hallucinating
        """
        
        # Common patterns
        if any(word in user_input.lower() for word in ['post', 'upload', 'publish']):
            if 'pinterest' in user_input.lower():
                return {
                    'action': 'post_to_pinterest',
                    'target': self._extract_product_name(user_input),
                    'platform': 'pinterest'
                }
            elif 'twitter' in user_input.lower() or 'tweet' in user_input.lower():
                return {
                    'action': 'post_to_twitter',
                    'target': user_input,
                    'platform': 'twitter'
                }
        
        if any(word in user_input.lower() for word in ['check', 'get', 'scrape', 'fetch']):
            if 'gumroad' in user_input.lower():
                return {
                    'action': 'check_gumroad',
                    'target': 'sales',
                    'platform': 'gumroad'
                }
        
        if any(word in user_input.lower() for word in ['learn', 'explore', 'figure out']):
            platform = None
            if 'pinterest' in user_input.lower():
                platform = 'pinterest'
            elif 'twitter' in user_input.lower():
                platform = 'twitter'
            elif 'instagram' in user_input.lower():
                platform = 'instagram'
            
            return {
                'action': 'learn_platform',
                'target': platform,
                'platform': platform
            }
        
        # Default: just respond
        return {
            'action': 'respond',
            'target': user_input,
            'platform': None
        }
    
    def _extract_product_name(self, text: str) -> str:
        """Extract product name from user input"""
        import re
        
        # Look for quotes
        quoted = re.search(r'["\']([^"\']+)["\']', text)
        if quoted:
            return quoted.group(1)
        
        # Pattern: "post X to pinterest" - extract X
        pattern = r'post\s+(.+?)\s+to\s+(pinterest|twitter|instagram)'
        match = re.search(pattern, text.lower())
        if match:
            product = match.group(1).strip()
            # Capitalize properly
            return ' '.join(word.capitalize() for word in product.split())
        
        # Look for keywords
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ['product', 'item', 'about']:
                if i + 1 < len(words):
                    return ' '.join(words[i+1:])
        
        return ''
    
    def _create_plan(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Break down the intent into executable steps
        No LLM needed - hardcoded logic for known patterns
        """
        
        plan = {
            'intent': intent,
            'steps': []
        }
        
        if intent['action'] == 'post_to_pinterest':
            # Agent should use its learned knowledge, not hardcoded steps
            plan['steps'] = [
                {
                    'tool': 'browser_tool',
                    'function': 'execute_learned_task',
                    'description': f"Use learned Pinterest knowledge to post '{intent['target']}'",
                    'args': {
                        'platform': 'pinterest',
                        'task': 'create_post',
                        'product_name': intent['target']
                    }
                }
            ]
        
        elif intent['action'] == 'post_to_twitter':
            # Same - use learned knowledge
            plan['steps'] = [
                {
                    'tool': 'browser_tool',
                    'function': 'execute_learned_task',
                    'description': f"Use learned Twitter knowledge to post '{intent['target']}'",
                    'args': {
                        'platform': 'twitter',
                        'task': 'create_post',
                        'product_name': intent['target']
                    }
                }
            ]
        
        elif intent['action'] == 'check_gumroad':
            plan['steps'] = [
                {
                    'tool': 'browser_tool',
                    'function': 'check_gumroad_sales',
                    'description': 'Scrape Gumroad sales data',
                    'args': {}
                }
            ]
        
        elif intent['action'] == 'learn_platform':
            # Agent explores and learns the platform
            platform_urls = {
                'pinterest': 'https://www.pinterest.com/pin-builder/',
                'twitter': 'https://twitter.com/compose/tweet',
                'instagram': 'https://www.instagram.com/create/style/'
            }
            url = platform_urls.get(intent['platform'], f"https://{intent['platform']}.com")
            
            plan['steps'] = [
                {
                    'tool': 'browser_tool',
                    'function': 'learn_platform',
                    'description': f"Explore and learn how to use {intent['platform']}",
                    'args': {
                        'platform': intent['platform'],
                        'url': url
                    }
                }
            ]
        
        else:
            # Simple response
            plan['steps'] = [
                {
                    'tool': 'llm_tool',
                    'function': 'respond',
                    'description': 'Generate response',
                    'args': {'message': intent['target']}
                }
            ]
        
        return plan
    
    def _execute_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute one step of the plan
        This is where we call the actual tools
        """
        
        try:
            # Get the tool
            tool_name = step['tool']
            function_name = step['function']
            args = step['args']
            
            # Import and execute
            if tool_name == 'browser_tool':
                from tools.browser_tool import BrowserTool
                browser = BrowserTool()
                
                # Call the requested function
                func = getattr(browser, function_name)
                result = func(**args)
                
                # Keep browser open for next steps
                # browser.close()
                
                return {
                    'status': result.get('status', 'error'),
                    'summary': f"{function_name} completed",
                    'data': result
                }
            
            elif tool_name == 'gumroad_tool':
                # Load products from file
                with open('minions/commerce_core/data/sales.json', 'r') as f:
                    products = json.load(f)
                
                return {
                    'status': 'success',
                    'summary': f"Loaded {len(products)} products",
                    'data': products
                }
            
            elif tool_name == 'ai_tool':
                from gpt4all import GPT4All
                brain = GPT4All("Llama-3.2-3B-Instruct-Q4_0.gguf")
                
                # Get product data from previous step
                product_name = args['product_name']
                
                # Load products
                with open('minions/commerce_core/data/sales.json', 'r') as f:
                    products = json.load(f)
                
                # Find the product
                product = None
                for p in products:
                    if product_name.lower() in p['name'].lower():
                        product = p
                        break
                
                if not product:
                    return {
                        'status': 'error',
                        'error': f"Product '{product_name}' not found"
                    }
                
                # Create content
                prompt = f"""Create Pinterest pin content for this product:
Product: {product['name']}
Price: £{product['price']}

Give me:
TITLE: [catchy title under 100 chars]
DESCRIPTION: [engaging description with hashtags]"""

                with brain.chat_session():
                    content = brain.generate(prompt, max_tokens=200, temp=0.8)
                
                return {
                    'status': 'success',
                    'summary': 'Created Pinterest content',
                    'data': {
                        'product': product,
                        'content': content
                    }
                }
            
            elif tool_name == 'llm_tool':
                # Simple response - no hallucination
                return {
                    'status': 'success',
                    'summary': 'Responded',
                    'data': {
                        'response': f"Understood: {args['message']}"
                    }
                }
            
            else:
                return {
                    'status': 'error',
                    'error': f"Unknown tool: {tool_name}"
                }
        
        except Exception as e:
            import traceback
            return {
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    def _retry_step(self, step: Dict[str, Any], error: str) -> Dict[str, Any]:
        """
        Try to recover from a failed step
        """
        print(f"🔄 Retrying with adjusted approach...")
        
        # For now, just try once more with same params
        # TODO: Smarter retry logic based on error type
        time.sleep(2)
        return self._execute_step(step)


# Singleton instance
_agent_instance = None

def get_agent() -> AgentCore:
    """Get the single agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = AgentCore()
    return _agent_instance
