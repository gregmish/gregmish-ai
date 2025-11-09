"""
Model Downloader and Configuration for Ultimate AI Agent
Helps download and configure GPT4All models
"""

import os
import sys
from pathlib import Path
from colorama import Fore, Style, init
from gpt4all import GPT4All

init(autoreset=True)


# Recommended models (sorted by size/performance)
RECOMMENDED_MODELS = [
    {
        "name": "Mistral 7B Instruct v0.2 (Q4_0)",
        "filename": "mistral-7b-instruct-v0.2.Q4_0.gguf",
        "size": "4.1 GB",
        "description": "Best balance of performance and speed. Recommended!",
        "recommended": True
    },
    {
        "name": "Llama 3 8B Instruct (Q4_0)",
        "filename": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
        "size": "4.3 GB",
        "description": "Meta's latest model, excellent for following instructions",
        "recommended": True
    },
    {
        "name": "GPT4All Falcon (Q4_0)",
        "filename": "gpt4all-falcon-newbpe-q4_0.gguf",
        "size": "3.9 GB",
        "description": "Fast and efficient, good for quick tasks",
        "recommended": False
    },
    {
        "name": "Nous Hermes 2 Mistral DPO (Q4_0)",
        "filename": "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf",
        "size": "4.1 GB",
        "description": "Fine-tuned for following instructions precisely",
        "recommended": True
    },
]


def get_gpt4all_cache_dir():
    """Get the GPT4All cache directory"""
    return Path.home() / ".cache" / "gpt4all"


def list_downloaded_models():
    """List models already downloaded"""
    cache_dir = get_gpt4all_cache_dir()
    
    if not cache_dir.exists():
        return []
    
    models = []
    for file in cache_dir.glob("*.gguf"):
        size_gb = file.stat().st_size / (1024**3)
        models.append({
            "filename": file.name,
            "size": f"{size_gb:.1f} GB",
            "path": str(file)
        })
    
    return models


def download_model(model_filename: str):
    """Download a GPT4All model"""
    print(f"\n{Fore.CYAN}Downloading model: {model_filename}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This may take several minutes depending on your internet speed...{Style.RESET_ALL}\n")
    
    try:
        # GPT4All will automatically download to cache
        model = GPT4All(model_filename)
        print(f"\n{Fore.GREEN}✓ Model downloaded successfully!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  Location: {get_gpt4all_cache_dir() / model_filename}{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error downloading model: {e}{Style.RESET_ALL}")
        return False


def interactive_model_setup():
    """Interactive model setup"""
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  🤖 AI MODEL SETUP 🤖{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Check for existing models
    downloaded = list_downloaded_models()
    
    if downloaded:
        print(f"{Fore.GREEN}✓ Found {len(downloaded)} model(s) already downloaded:{Style.RESET_ALL}\n")
        for i, model in enumerate(downloaded, 1):
            print(f"  {i}. {Fore.YELLOW}{model['filename']}{Style.RESET_ALL} ({model['size']})")
        
        print(f"\n{Fore.CYAN}Do you want to:{Style.RESET_ALL}")
        print(f"  [1] Use an existing model")
        print(f"  [2] Download a new model")
        print(f"  [q] Quit")
        
        choice = input(f"\n{Fore.GREEN}Your choice: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            if len(downloaded) == 1:
                selected = downloaded[0]
            else:
                model_choice = input(f"{Fore.GREEN}Select model number (1-{len(downloaded)}): {Style.RESET_ALL}").strip()
                try:
                    selected = downloaded[int(model_choice) - 1]
                except:
                    print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
                    return None
            
            print(f"\n{Fore.GREEN}✓ Using model: {selected['filename']}{Style.RESET_ALL}")
            return selected['filename']
        
        elif choice == 'q':
            return None
        
        # Fall through to download
    
    # Show recommended models
    print(f"\n{Fore.CYAN}Recommended Models:{Style.RESET_ALL}\n")
    
    for i, model in enumerate(RECOMMENDED_MODELS, 1):
        star = f"{Fore.YELLOW}⭐{Style.RESET_ALL}" if model['recommended'] else "  "
        print(f"{star} {i}. {Fore.CYAN}{model['name']}{Style.RESET_ALL}")
        print(f"     Size: {model['size']}")
        print(f"     {model['description']}\n")
    
    print(f"{Fore.YELLOW}Note: Models are downloaded once and cached locally{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Recommended: Option 1 (Mistral 7B) for best results{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.GREEN}Select model to download (1-{len(RECOMMENDED_MODELS)}) or 'q' to quit: {Style.RESET_ALL}").strip()
    
    if choice.lower() == 'q':
        return None
    
    try:
        model_idx = int(choice) - 1
        if 0 <= model_idx < len(RECOMMENDED_MODELS):
            selected_model = RECOMMENDED_MODELS[model_idx]
            
            if download_model(selected_model['filename']):
                return selected_model['filename']
        else:
            print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
    
    return None


def create_config(model_name: str):
    """Create configuration file"""
    config = {
        "model_name": model_name,
        "auto_approve": False,
        "max_iterations": 15,
        "temperature": 0.7,
        "max_tokens": 2048
    }
    
    config_file = Path("agent_config.json")
    import json
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"{Fore.GREEN}✓ Configuration saved to {config_file}{Style.RESET_ALL}")


def main():
    """Main setup function"""
    model_name = interactive_model_setup()
    
    if model_name:
        create_config(model_name)
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Setup complete!{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}To start the agent, run:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  python ultimate_agent.py{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.YELLOW}Setup cancelled{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
