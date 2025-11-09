"""
OVERSEER - Your All-Seeing AI Assistant
- Constantly monitors your screen
- Always listening for "Overseer" 
- Fast responses, knows everything you're doing
"""

import speech_recognition as sr
import edge_tts
import asyncio
import os
import pygame
import tempfile
import threading
import time
from PIL import ImageGrab, Image
import pygetwindow as gw
from datetime import datetime
from openai import OpenAI
import anthropic

class Overseer:
    def __init__(self):
        print("\n" + "="*70)
        print("👁️  OVERSEER - ALL-SEEING AI ASSISTANT")
        print("="*70)
        print("\n⚡ OVERSEER is now:")
        print("   📸 Monitoring your screen every 2 seconds")
        print("   🎤 Listening for 'Overseer' commands")
        print("   🧠 Tracking everything you do")
        print("   ⚡ Fast response mode enabled\n")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recognizer.energy_threshold = 200  # Lower = more sensitive
        self.recognizer.pause_threshold = 0.8   # Wait 0.8 seconds of silence
        self.recognizer.dynamic_energy_threshold = False  # Consistent sensitivity
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Load SMARTER LOCAL AI - try better models
        print("🧠 Loading OVERSEER AI brain...")
        print("   Checking for smarter local models...")
        
        from gpt4all import GPT4All
        
        # Try to use smarter models (all free and local)
        smart_models = [
            "Meta-Llama-3-8B-Instruct.Q4_0.gguf",  # Llama 3 - MUCH smarter
            "Phi-3-mini-4k-instruct.Q4_0.gguf",     # Microsoft Phi-3 - smart and fast
            "orca-mini-3b-gguf2-q4_0.gguf"          # Fallback to what you have
        ]
        
        model_loaded = False
        for model_name in smart_models:
            try:
                print(f"   Trying {model_name}...")
                self.model = GPT4All(model_name)
                print(f"✅ Loaded {model_name} - OVERSEER is now smarter!")
                self.model_name = model_name
                model_loaded = True
                break
            except Exception as e:
                print(f"   ❌ {model_name} not found")
                continue
        
        if not model_loaded:
            print("⚠️ No models found! Downloading Llama 3.2 3B (free, smarter)...")
            self.model = GPT4All("Llama-3.2-3B-Instruct-Q4_0.gguf")
            self.model_name = "Llama-3.2-3B-Instruct"
            print("✅ Llama 3.2 downloaded and loaded!")
        
        self.use_smart_ai = False  # Using local AI only
        
        # British voice
        self.voice = "en-GB-RyanNeural"
        
        # Surveillance data
        self.current_window = ""
        self.recent_windows = []
        self.is_listening = True
        self.is_processing = False
        
        # Wake words - LOTS of variations for Yorkshire accent
        self.wake_words = ["overseer", "over seer", "hey overseer", "oversee", "over see", "oi overseer", "hey over"]
        
        print("✅ OVERSEER Online!")
        print("\n💡 Say 'Overseer' or 'Hey Overseer' + your command")
        print("💡 I can see everything you're doing\n")
    
    async def speak_async(self, text):
        """Speak quickly"""
        print(f"\n🗣️ OVERSEER: {text}\n")
        
        temp_file = os.path.join(tempfile.gettempdir(), f"overseer_{int(time.time()*1000)}.mp3")
        
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(temp_file)
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
        finally:
            try:
                pygame.mixer.music.unload()
                await asyncio.sleep(0.1)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
    
    def speak(self, text):
        asyncio.run(self.speak_async(text))
    
    def get_active_window(self):
        """Get current window"""
        try:
            active = gw.getActiveWindow()
            return active.title if active else "Unknown"
        except:
            return "Unknown"
    
    def screen_monitor(self):
        """Monitor screen changes"""
        print("📸 Screen monitoring active...")
        
        while self.is_listening:
            try:
                window = self.get_active_window()
                
                if window != self.current_window:
                    self.current_window = window
                    self.recent_windows.append(window)
                    
                    # Keep last 10
                    if len(self.recent_windows) > 10:
                        self.recent_windows.pop(0)
                    
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"👁️ [{timestamp}] {window}")
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                time.sleep(2)
    
    def voice_monitor(self):
        """Listen for commands - FAST MODE"""
        print("🎤 Voice monitoring active...")
        print("🎤 Testing microphone... Speak now to test!\n")
        
        while self.is_listening:
            if self.is_processing:
                time.sleep(0.3)
                continue
            
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    
                    # Longer listen time for Yorkshire accent
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=12)
                    
                    try:
                        text = self.recognizer.recognize_google(audio, language="en-GB")
                        text_lower = text.lower()
                        
                        # ALWAYS show what we heard
                        print(f"👂 Heard: '{text}'")
                        
                        # Check for wake word
                        if any(wake in text_lower for wake in self.wake_words):
                            print(f"🔔 OVERSEER ACTIVATED!")
                            
                            # Remove wake words
                            command = text_lower
                            for wake in self.wake_words:
                                command = command.replace(wake, "").strip()
                            
                            # Process immediately
                            if command:
                                threading.Thread(target=self.process_command, args=(command,), daemon=True).start()
                            else:
                                self.speak("Yes, Master?")
                        else:
                            print("   (No wake word detected)")
                        
                    except sr.UnknownValueError:
                        print("👂 [Could not understand]")
                    except sr.RequestError as e:
                        print(f"❌ Recognition error: {e}")
                        time.sleep(1)
                        
            except sr.WaitTimeoutError:
                pass  # Normal timeout
            except Exception as e:
                print(f"❌ Voice error: {e}")
                time.sleep(0.5)
    
    def process_command(self, command):
        """Process command with LOCAL SMART AI"""
        self.is_processing = True
        
        try:
            # Build context
            context = f"Currently viewing: {self.current_window}. "
            if len(self.recent_windows) > 1:
                context += f"Recent activity: {', '.join(self.recent_windows[-3:])}"
            
            print(f"⚡ OVERSEER thinking with {self.model_name}...")
            
            # Use LOCAL AI with better prompting for smarter responses
            system_prompt = f"""You are OVERSEER, Greg's intelligent AI assistant with full surveillance capabilities.

CONTEXT: {context}

RULES:
- Call the user "Greg", never "Master"
- Be concise, helpful, and intelligent
- You can see what Greg is doing on his screen
- Give direct, actionable answers
- Be friendly but professional"""

            full_prompt = f"""{system_prompt}

GREG'S COMMAND: {command}

YOUR RESPONSE (brief and helpful):"""
            
            with self.model.chat_session():
                response = self.model.generate(
                    full_prompt,
                    max_tokens=200,
                    temp=0.7
                )
            
            # Clean up response
            answer = response.strip()
            
            # Remove any "Master" mentions
            answer = answer.replace("Master", "Greg")
            answer = answer.replace("master", "Greg")
            
            self.speak(answer)
            
        except Exception as e:
            print(f"❌ AI error: {e}")
            self.speak("Sorry Greg, I encountered an error processing that.")
        finally:
            self.is_processing = False
    
    def run(self):
        """Activate OVERSEER"""
        self.speak("OVERSEER online. All systems active. I am watching and listening, Master.")
        
        # Start monitoring
        screen_thread = threading.Thread(target=self.screen_monitor, daemon=True)
        voice_thread = threading.Thread(target=self.voice_monitor, daemon=True)
        
        screen_thread.start()
        voice_thread.start()
        
        print("\n" + "="*70)
        print("✅ OVERSEER ACTIVE - ALL SYSTEMS ONLINE")
        print("="*70)
        print("\n📊 Status: Monitoring screen + listening for commands")
        print("🛑 Press CTRL+C to deactivate OVERSEER\n")
        
        try:
            while self.is_listening:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Deactivating OVERSEER...")
            self.is_listening = False
            self.speak("OVERSEER offline. Goodbye, Master.")


if __name__ == "__main__":
    try:
        overseer = Overseer()
        overseer.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 OVERSEER deactivated!")
    except Exception as e:
        print(f"\n❌ OVERSEER Error: {e}")
        import traceback
        traceback.print_exc()
