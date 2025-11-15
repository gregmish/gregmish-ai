""""""

Single Entry Point - No More ChaosQuick Start Launcher for Ultimate AI Agent

Start the agent in any mode from ONE placeChecks setup and launches the agent

""""""



import sysimport os

import argparseimport sys

from core.agent_core import get_agentimport json

from pathlib import Path

from colorama import Fore, Style, init

def run_chat_mode():

    """Interactive chat mode"""init(autoreset=True)

    agent = get_agent()

    

    print("=" * 60)def check_config():

    print("🤖 GREGMISH AI - Chat Mode")    """Check if configuration exists"""

    print("=" * 60)    config_file = Path("agent_config.json")

    print("Type 'quit' to exit\n")    if config_file.exists():

            try:

    while True:            with open(config_file, 'r') as f:

        try:                config = json.load(f)

            user_input = input("You: ").strip()                return True, config.get('model_name')

                    except:

            if user_input.lower() in ['quit', 'exit', 'bye']:            return False, None

                print("👋 Later!")    return False, None

                break

            

            if not user_input:def check_model_downloaded(model_name):

                continue    """Check if model is downloaded"""

                if not model_name:

            # Execute command through the core agent        return False

            result = agent.execute_command(user_input)    

                cache_dir = Path.home() / ".cache" / "gpt4all"

            # Display result    model_path = cache_dir / model_name

            if result['status'] == 'completed':    

                print(f"\n✅ Done!")    return model_path.exists()

                

                # Show any data from the last step

                if result['results']:def main():

                    last_result = result['results'][-1]    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")

                    if 'data' in last_result and 'response' in last_result['data']:    print(f"{Fore.CYAN}  🚀 ULTIMATE AI AGENT - LAUNCHER 🚀{Style.RESET_ALL}")

                        print(f"\n{last_result['data']['response']}")    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

                    elif 'data' in last_result:    

                        import json    # Check configuration

                        print(f"\nResult: {json.dumps(last_result['data'], indent=2)[:500]}")    has_config, model_name = check_config()

            else:    

                print(f"\n⚠️ Partially completed")    if not has_config:

                        print(f"{Fore.YELLOW}⚠️  No configuration found{Style.RESET_ALL}\n")

                # Show what failed        print(f"{Fore.CYAN}Running first-time setup...{Style.RESET_ALL}\n")

                for i, r in enumerate(result['results']):        

                    if r['status'] == 'error':        # Run setup

                        print(f"   Step {i+1} failed: {r.get('error', 'Unknown error')}")        os.system(f"{sys.executable} setup_model.py")

                    

            print()        # Check again

                has_config, model_name = check_config()

        except KeyboardInterrupt:        if not has_config:

            print("\n\n👋 Interrupted")            print(f"\n{Fore.RED}Setup was not completed. Exiting.{Style.RESET_ALL}")

            break            sys.exit(1)

        except Exception as e:    

            print(f"\n❌ Error: {e}")    # Check if model is downloaded

            import traceback    if not check_model_downloaded(model_name):

            traceback.print_exc()        print(f"{Fore.YELLOW}⚠️  Model not found: {model_name}{Style.RESET_ALL}\n")

        print(f"{Fore.CYAN}Please run setup to download the model:{Style.RESET_ALL}")

        print(f"{Fore.CYAN}  python setup_model.py{Style.RESET_ALL}\n")

def run_web_mode():        sys.exit(1)

    """Web dashboard mode"""    

    print("🌐 Starting web dashboard...")    # All checks passed, launch agent

        print(f"{Fore.GREEN}✓ Configuration found{Style.RESET_ALL}")

    # Import and run the server    print(f"{Fore.GREEN}✓ Model ready: {model_name}{Style.RESET_ALL}\n")

    import uvicorn    print(f"{Fore.CYAN}Launching agent...{Style.RESET_ALL}\n")

    from vivian_server import app    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

        

    uvicorn.run(app, host="0.0.0.0", port=8000)    # Launch the agent

    os.system(f"{sys.executable} ultimate_agent.py")



def run_test_command(command: str):

    """Test a single command and exit"""if __name__ == "__main__":

    agent = get_agent()    try:

            main()

    print(f"\n🧪 Testing: {command}\n")    except KeyboardInterrupt:

            print(f"\n{Fore.YELLOW}Launcher interrupted{Style.RESET_ALL}")

    result = agent.execute_command(command)        sys.exit(0)

    
    import json
    print("\n" + "=" * 60)
    print("RESULT:")
    print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(
        description="GregMish AI - Your Virtual Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_agent.py                    # Interactive chat (default)
  python start_agent.py --mode chat        # Chat mode
  python start_agent.py --mode web         # Web dashboard
  python start_agent.py --test "check gumroad"  # Test single command
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['chat', 'web'],
        default='chat',
        help='Mode to run (default: chat)'
    )
    
    parser.add_argument(
        '--test',
        type=str,
        help='Test a single command and exit'
    )
    
    args = parser.parse_args()
    
    # Test mode
    if args.test:
        run_test_command(args.test)
        return
    
    # Run selected mode
    if args.mode == 'chat':
        run_chat_mode()
    elif args.mode == 'web':
        run_web_mode()


if __name__ == "__main__":
    main()
