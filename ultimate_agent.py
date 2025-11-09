"""
Ultimate AI Agent - Main Agent Loop  
Autonomous laptop controller with GPT4All and custom tools
"""

import sys
import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from colorama import Fore, Style, init
from gpt4all import GPT4All

from agent_tools import get_all_tools
from agent_memory import AgentMemory
from agent_safety import SafetySystem

init(autoreset=True)


class UltimateAIAgent:
    """The Ultimate AI Agent - Autonomous laptop controller with learning capabilities"""
    
    def __init__(self, model_name: str = None):
        """Initialize the agent"""
        print(f"{Fore.CYAN}🤖 Initializing Ultimate AI Agent...{Style.RESET_ALL}")
        
        # Load config if exists
        if model_name is None:
            model_name = self._load_config()
        
        # Initialize components
        self.memory = AgentMemory()
        self.safety = SafetySystem()
        self.model_name = model_name
        self.llm = None
        self.agent = None
        self.tools = get_all_tools()
        
        print(f"{Fore.GREEN}✓ Memory system initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Safety system initialized{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ {len(self.tools)} tools loaded{Style.RESET_ALL}")
        
        self._initialize_llm()
        self._create_agent()
    
    def _initialize_llm(self):
        """Initialize the local LLM"""
        print(f"\n{Fore.CYAN}Loading AI model: {self.model_name}{Style.RESET_ALL}")
        
        try:
            # Load GPT4All model directly
            self.llm = GPT4All(self.model_name, device='cpu')
            print(f"{Fore.GREEN}✓ Model loaded successfully{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error loading model: {e}{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Available models in GPT4All cache:{Style.RESET_ALL}")
            
            # Try to list available models
            try:
                import os
                cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "gpt4all")
                if os.path.exists(cache_dir):
                    models = [f for f in os.listdir(cache_dir) if f.endswith('.gguf')]
                    if models:
                        for i, model in enumerate(models, 1):
                            print(f"  {i}. {model}")
                    else:
                        print(f"{Fore.RED}  No models found. You need to download a model first.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}  GPT4All cache directory not found.{Style.RESET_ALL}")
            except Exception as list_error:
                print(f"{Fore.RED}  Could not list models: {list_error}{Style.RESET_ALL}")
            
            raise
    
    def _create_agent(self):
        """Create the simple agent loop"""
        print(f"{Fore.GREEN}✓ Agent initialized{Style.RESET_ALL}")
    
    def _load_config(self) -> str:
        """Load configuration file"""
        config_file = Path("agent_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('model_name', 'mistral-7b-instruct-v0.2.Q4_0.gguf')
            except:
                pass
        return 'mistral-7b-instruct-v0.2.Q4_0.gguf'
    
    def _get_memory_context(self, query: str) -> str:
        """Get relevant memory context for the query"""
        similar_experiences = self.memory.recall_similar_experiences(query, n_results=3)
        successful_actions = self.memory.recall_successful_actions(query, n_results=2)
        
        context_parts = []
        
        if successful_actions:
            context_parts.append("Previous successful approaches:")
            for action in successful_actions:
                context_parts.append(f"- {action['content']}")
        
        if similar_experiences:
            context_parts.append("\nRelated past experiences:")
            for exp in similar_experiences:
                meta = exp['metadata']
                if meta.get('success'):
                    context_parts.append(f"✓ {meta.get('task', 'Unknown task')}")
                else:
                    context_parts.append(f"✗ {meta.get('task', 'Unknown task')} (failed)")
        
        return "\n".join(context_parts) if context_parts else "No previous experience with similar tasks."
    
    def _get_chat_history(self) -> str:
        """Get recent chat history"""
        history = self.memory.get_conversation_context(last_n=5)
        if not history:
            return "No previous conversation."
        
        chat_lines = []
        for msg in history:
            role = msg['role'].capitalize()
            content = msg['content'][:200]  # Truncate long messages
            chat_lines.append(f"{role}: {content}")
        
        return "\n".join(chat_lines)
    
    def execute_task(self, task: str) -> str:
        """Execute a task using the agent"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📋 Task: {task}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        # Store in conversation
        self.memory.add_to_conversation("user", task)
        
        # Get memory context
        memory_context = self._get_memory_context(task)
        
        # Build prompt for the AI
        prompt = f"""You are an autonomous AI agent controlling a Windows laptop.

Task: {task}

Previous similar experiences:
{memory_context}

Available Tools:
- file_operation: Create, read, write, delete files/folders
- terminal_command: Execute PowerShell commands
- web_search: Fetch content from URLs
- python_code: Execute Python code
- system_info: Check CPU, RAM, disk, processes

Instructions:
1. Think about what tool(s) you need to use
2. Respond with ONLY the tool name and parameters in this format:
   TOOL: tool_name
   PARAMS: {{parameter details}}
   
Example for "open Edge and go to gumroad":
TOOL: terminal_command
PARAMS: start msedge "https://gumroad.com"

Your response (tool name and params only):"""

        try:
            # Get AI response
            print(f"{Fore.CYAN}🤔 Agent thinking...{Style.RESET_ALL}\n")
            response = self.llm.generate(prompt, max_tokens=500, temp=0.7)
            
            print(f"{Fore.YELLOW}Agent's plan:{Style.RESET_ALL}")
            print(response)
            print()
            
            # Parse the response for tool usage
            tool_match = re.search(r'TOOL:\s*(\w+)', response, re.IGNORECASE)
            params_match = re.search(r'PARAMS?:\s*(.+)', response, re.IGNORECASE | re.DOTALL)
            
            if tool_match and params_match:
                tool_name = tool_match.group(1).strip()
                params_str = params_match.group(1).strip()
                
                # Find the tool
                tool = None
                for t in self.tools:
                    if t.name == tool_name:
                        tool = t
                        break
                
                if tool:
                    print(f"{Fore.GREEN}Using tool: {tool_name}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Parameters: {params_str}{Style.RESET_ALL}\n")
                    
                    # Execute the tool based on its type
                    result = self._execute_tool(tool, params_str)
                    
                    # Store success
                    self.memory.add_experience(
                        task=task,
                        action=f"{tool_name}: {params_str}",
                        result=result,
                        success="Error" not in result
                    )
                    
                    self.memory.add_to_conversation("assistant", result)
                    
                    print(f"\n{Fore.GREEN}✓ Task Complete{Style.RESET_ALL}\n")
                    return result
                else:
                    return f"Tool '{tool_name}' not found"
            else:
                # No tool specified, just return AI response
                self.memory.add_to_conversation("assistant", response)
                return response
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n{Fore.RED}✗ {error_msg}{Style.RESET_ALL}\n")
            return error_msg
    
    def _execute_tool(self, tool, params_str: str) -> str:
        """Execute a tool with given parameters"""
        try:
            # Parse parameters based on tool type
            if tool.name == "terminal_command":
                return tool._run(command=params_str, timeout=30)
            
            elif tool.name == "file_operation":
                # Parse file operation params
                lines = params_str.split('\n')
                operation = None
                path = None
                content = None
                
                for line in lines:
                    if 'operation' in line.lower() or 'op' in line.lower():
                        operation = line.split(':')[-1].strip().strip('"\'')
                    elif 'path' in line.lower():
                        path = line.split(':')[-1].strip().strip('"\'')
                    elif 'content' in line.lower():
                        content = line.split(':')[-1].strip().strip('"\'')
                
                if not operation:
                    # Try to infer from params
                    if 'read' in params_str.lower():
                        operation = 'read'
                    elif 'write' in params_str.lower():
                        operation = 'write'
                    elif 'create' in params_str.lower():
                        operation = 'create'
                    elif 'delete' in params_str.lower():
                        operation = 'delete'
                    elif 'list' in params_str.lower():
                        operation = 'list'
                
                return tool._run(operation=operation or 'read', path=path or '', content=content)
            
            elif tool.name == "web_search":
                # Extract URL
                url = params_str.strip().strip('"\'')
                if not url.startswith('http'):
                    url = 'https://' + url
                return tool._run(url=url)
            
            elif tool.name == "python_code":
                return tool._run(code=params_str)
            
            elif tool.name == "system_info":
                info_type = 'all'
                if 'cpu' in params_str.lower():
                    info_type = 'cpu'
                elif 'memory' in params_str.lower() or 'ram' in params_str.lower():
                    info_type = 'memory'
                elif 'disk' in params_str.lower():
                    info_type = 'disk'
                elif 'process' in params_str.lower():
                    info_type = 'processes'
                
                return tool._run(info_type=info_type)
            
            else:
                return f"Unknown tool: {tool.name}"
                
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
    def chat(self, message: str) -> str:
        """Simple chat without tool use"""
        self.memory.add_to_conversation("user", message)
        
        try:
            response = self.llm.invoke(message)
            self.memory.add_to_conversation("assistant", response)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def show_stats(self):
        """Show agent statistics"""
        print(f"\n{Fore.CYAN}📊 Agent Statistics{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        mem_stats = self.memory.get_stats()
        print(f"{Fore.YELLOW}Memory:{Style.RESET_ALL}")
        print(f"  Total Experiences: {mem_stats['total_experiences']}")
        print(f"  Successful Actions: {mem_stats['successful_actions']}")
        print(f"  Conversation Length: {mem_stats['conversation_length']}")
        
        print(f"\n{Fore.YELLOW}Safety:{Style.RESET_ALL}")
        safety_stats = self.safety.get_approval_stats()
        if isinstance(safety_stats, dict):
            print(f"  Total Approval Requests: {safety_stats['total_requests']}")
            print(f"  Approved: {safety_stats['approved']}")
            print(f"  Denied: {safety_stats['denied']}")
            print(f"  Auto-Approve: {safety_stats['auto_approve_enabled']}")
        else:
            print(f"  {safety_stats}")
        
        print(f"\n{Fore.YELLOW}Tools Available:{Style.RESET_ALL}")
        for tool in self.tools:
            print(f"  • {tool.name}: {tool.description.split('.')[0]}")
        
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def export_knowledge(self, filename: str = "agent_knowledge.json"):
        """Export learned knowledge"""
        result = self.memory.export_knowledge(filename)
        print(f"{Fore.GREEN}✓ {result}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  Saved to: {filename}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🚀 ULTIMATE AI AGENT 🚀{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  Autonomous Laptop Controller with Learning{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        agent = UltimateAIAgent()
        
        print(f"\n{Fore.GREEN}✓ Agent ready!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Available commands:{Style.RESET_ALL}")
        print(f"  Just type your request naturally!")
        print(f"  'stats' - Show agent statistics")
        print(f"  'export' - Export learned knowledge")
        print(f"  'quit' or 'exit' - Exit the agent")
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        while True:
            try:
                user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(f"{Fore.YELLOW}Goodbye! 👋{Style.RESET_ALL}")
                    break
                
                if user_input.lower() == 'stats':
                    agent.show_stats()
                    continue
                
                if user_input.lower() == 'export':
                    agent.export_knowledge()
                    continue
                
                # Execute the task
                response = agent.execute_task(user_input)
                print(f"\n{Fore.CYAN}Agent: {Style.RESET_ALL}{response}\n")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'quit' to exit{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}Failed to initialize agent: {e}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Please make sure you have a GPT4All model downloaded.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You can download models from: https://gpt4all.io/models.html{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
