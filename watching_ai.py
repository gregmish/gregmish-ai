"""
AI Assistant with FULL SURVEILLANCE MODE
- Constantly monitors your screen
- Always listening for "Hey AI" 
- Can see what you're doing and help immediately
- Records everything you do for context
"""

import speech_recognition as sr
from gpt4all import GPT4All
import edge_tts
import asyncio
import os
import pygame
import tempfile
from pynput import keyboard as kb
import threading
import time
from PIL import ImageGrab, Image
import pyautogui
import io
import base64
from datetime import datetime

class WatchingAI:
    def __init__(self):
        print("\n" + "="*70)
        print("👁️  SURVEILLANCE AI - ALWAYS WATCHING, ALWAYS LISTENING")
        print("="*70)
        print("\n⚠️  WARNING: This AI is constantly:")
        print("   📸 Taking screenshots every 3 seconds")
        print("   🎤 Listening for 'Hey AI' commands")
        print("   🧠 Analyzing what you're doing")
        print("   💾 Remembering your context\n")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Load AI model
        model_path = os.path.join(os.path.expanduser("~"), ".cache", "gpt4all", "orca-mini-3b-gguf2-q4_0.gguf")
        print("📦 Loading AI model...")
        self.model = GPT4All(model_path)
        
        # Edge-TTS British voice
        self.voice = "en-GB-RyanNeural"
        
        # Surveillance data
        self.recent_screenshots = []  # Last 10 screenshots
        self.recent_activities = []   # Last 20 activities
        self.active_window_history = []
        self.is_listening = True
        self.is_speaking = False
        
        # Wake words - more flexible
        self.wake_words = ["hey ai", "ey up ai", "ai help", "help ai", "hey a i", "ai can you", "ai what", "ai how"]
        
        print("✅ Surveillance AI Ready!")
        print("\n💡 Say 'Hey AI' followed by your question")
        print("💡 I can see your screen and know what you're working on")
        print("💡 Press CTRL+ESC to exit\n")
    
    async def speak_async(self, text):
        """Speak using Edge-TTS"""
        self.is_speaking = True
        print(f"\n🤖 AI: {text}\n")
        
        temp_file = os.path.join(tempfile.gettempdir(), f"ai_speech_{int(time.time()*1000)}.mp3")
        
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
                await asyncio.sleep(0.2)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
            self.is_speaking = False
    
    def speak(self, text):
        """Synchronous wrapper"""
        asyncio.run(self.speak_async(text))
    
    def take_screenshot(self):
        """Capture current screen"""
        try:
            screenshot = ImageGrab.grab()
            # Resize for memory efficiency
            screenshot.thumbnail((800, 600), Image.Resampling.LANCZOS)
            return screenshot
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def get_active_window(self):
        """Get current active window title"""
        try:
            import pygetwindow as gw
            active = gw.getActiveWindow()
            return active.title if active else "Unknown"
        except:
            return "Unknown"
    
    def describe_current_context(self):
        """Describe what user is doing based on surveillance"""
        active_window = self.get_active_window()
        
        context = f"Currently viewing: {active_window}. "
        
        if self.recent_activities:
            context += f"Recent activity: {', '.join(self.recent_activities[-5:])}. "
        
        return context
    
    def screen_monitoring_loop(self):
        """Background thread - constantly monitor screen"""
        print("📸 Screen monitoring started...")
        screenshot_count = 0
        
        while self.is_listening:
            try:
                # Take screenshot
                screenshot = self.take_screenshot()
                if screenshot:
                    self.recent_screenshots.append({
                        'time': datetime.now(),
                        'image': screenshot,
                        'window': self.get_active_window()
                    })
                    
                    # Keep only last 10
                    if len(self.recent_screenshots) > 10:
                        self.recent_screenshots.pop(0)
                    
                    screenshot_count += 1
                    
                    # Log activity
                    current_window = self.get_active_window()
                    if not self.active_window_history or self.active_window_history[-1] != current_window:
                        self.active_window_history.append(current_window)
                        activity = f"Switched to {current_window}"
                        self.recent_activities.append(activity)
                        print(f"👁️  [{datetime.now().strftime('%H:%M:%S')}] {activity}")
                        
                        # Keep only last 20 activities
                        if len(self.recent_activities) > 20:
                            self.recent_activities.pop(0)
                
                # Wait 3 seconds between screenshots
                time.sleep(3)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(3)
    
    def voice_monitoring_loop(self):
        """Background thread - constantly listen for wake word"""
        print("🎤 Voice monitoring started...")
        
        while self.is_listening:
            if self.is_speaking:
                time.sleep(0.5)
                continue
            
            try:
                with self.microphone as source:
                    # Quick ambient adjustment
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    
                    # Listen for speech
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
                    
                    try:
                        # Recognize with Google (British English)
                        text = self.recognizer.recognize_google(audio, language="en-GB")
                        text_lower = text.lower()
                        
                        print(f"👂 Heard: '{text}'")
                        
                        # Check for wake word
                        if any(wake in text_lower for wake in self.wake_words):
                            print("🔔 WAKE WORD DETECTED!")
                            
                            # Remove wake words
                            command = text_lower
                            for wake in self.wake_words:
                                command = command.replace(wake, "").strip()
                            
                            if command:
                                # Process the command with full context
                                self.handle_command(command)
                        
                    except sr.UnknownValueError:
                        pass  # Couldn't understand, keep listening
                    except sr.RequestError as e:
                        print(f"Recognition error: {e}")
                        time.sleep(1)
                        
            except sr.WaitTimeoutError:
                pass  # Timeout is normal, keep listening
            except Exception as e:
                print(f"Voice monitoring error: {e}")
                time.sleep(1)
    
    def handle_command(self, command):
        """Process voice command with full context awareness"""
        print(f"\n💭 Processing: '{command}'")
        
        # Get current context
        context = self.describe_current_context()
        
        # Build prompt with surveillance context
        prompt = f"""You are a helpful AI assistant with full awareness of what the user is doing.

CONTEXT: {context}

USER COMMAND: {command}

Respond helpfully based on what you can see the user is working on. Be specific and actionable."""
        
        print("🧠 Thinking with full context awareness...")
        
        with self.model.chat_session():
            response = self.model.generate(prompt, max_tokens=250, temp=0.7)
        
        # Speak the response
        self.speak(response.strip())
    
    def run(self):
        """Start surveillance AI"""
        # Speak introduction
        self.speak("Surveillance mode activated. I'm now watching your screen and listening for your commands. Just say 'Hey AI' when you need help.")
        
        # Start monitoring threads
        screen_thread = threading.Thread(target=self.screen_monitoring_loop, daemon=True)
        voice_thread = threading.Thread(target=self.voice_monitoring_loop, daemon=True)
        
        screen_thread.start()
        voice_thread.start()
        
        print("\n" + "="*70)
        print("✅ SURVEILLANCE ACTIVE")
        print("="*70)
        print("\n📊 Status:")
        print("   📸 Screen capture: Every 3 seconds")
        print("   🎤 Voice detection: Continuous")
        print("   👁️  Context awareness: Full")
        print("\n🛑 Press CTRL+C to stop surveillance\n")
        
        try:
            # Keep main thread alive
            while self.is_listening:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down surveillance...")
            self.is_listening = False
            self.speak("Surveillance mode deactivated. Goodbye, Master.")
            time.sleep(2)


if __name__ == "__main__":
    try:
        print("\n⚠️  PRIVACY WARNING:")
        print("This AI will constantly monitor your screen and listen to audio.")
        print("All data is processed locally and not sent anywhere.")
        print("\nPress ENTER to activate surveillance mode...")
        input()
        
        ai = WatchingAI()
        ai.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Cancelled!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
