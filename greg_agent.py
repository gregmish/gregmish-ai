"""
GregMish AI - Single Entry Point
ONE script to rule them all
"""

import sys
import argparse
from core.agent_core import get_agent


def run_chat_mode():
    """Interactive chat mode"""
    agent = get_agent()
    
    print("=" * 60)
    print("🤖 GREGMISH AI - Chat Mode")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Later!")
                break
            
            if not user_input:
                continue
            
            result = agent.execute_command(user_input)
            
            if result['status'] == 'completed':
                print(f"\n✅ Done!")
                
                if result['results']:
                    last_result = result['results'][-1]
                    if 'data' in last_result and 'response' in last_result['data']:
                        print(f"\n{last_result['data']['response']}")
                    elif 'data' in last_result:
                        import json
                        print(f"\nResult: {json.dumps(last_result['data'], indent=2)[:500]}")
            else:
                print(f"\n⚠️ Partially completed")
                
                for i, r in enumerate(result['results']):
                    if r['status'] == 'error':
                        print(f"   Step {i+1} failed: {r.get('error', 'Unknown error')}")
            
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def run_web_mode():
    """Web dashboard mode"""
    print("🌐 Starting web dashboard...")
    import uvicorn
    from dashboard import app
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_test_command(command: str):
    """Test a single command and exit"""
    agent = get_agent()
    
    print(f"\n🧪 Testing: {command}\n")
    result = agent.execute_command(command)
    
    import json
    print("\n" + "=" * 60)
    print("RESULT:")
    print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(description="GregMish AI")
    parser.add_argument('--mode', choices=['chat', 'web'], default='chat')
    parser.add_argument('--test', type=str, help='Test a single command')
    
    args = parser.parse_args()
    
    if args.test:
        run_test_command(args.test)
    elif args.mode == 'chat':
        run_chat_mode()
    elif args.mode == 'web':
        run_web_mode()


if __name__ == "__main__":
    main()
