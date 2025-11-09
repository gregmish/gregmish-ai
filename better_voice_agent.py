"""
Better Voice Agent - Natural British voices with Edge-TTS!
Much simpler - just press SPACE to talk, release to process
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

class BetterVoiceAgent:
    def __init__(self):
        print("\n" + "="*60)
        print("🎤 BETTER VOICE AGENT - PUSH TO TALK")
        print("="*60)
        print("\n✨ Natural British voice with Edge-TTS")
        print("✨ Press & hold SPACE to speak")
        print("✨ Release SPACE to process\n")
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for better recognition
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Load AI model
        model_path = os.path.join(os.path.expanduser("~"), ".cache", "gpt4all", "orca-mini-3b-gguf2-q4_0.gguf")
        print(f"📦 Loading AI model...")
        self.model = GPT4All(model_path)
        
        # Edge-TTS voice - British male
        self.voice = "en-GB-RyanNeural"  # Natural British male voice
        
        self.is_recording = False
        self.should_stop = False
        
        print("✅ Voice Agent Ready!")
        print("\n💡 Try saying:")
        print("   'What can you do?'")
        print("   'How many packages do we have?'")
        print("   'Tell me about yourself'\n")
    
    async def speak_async(self, text):
        """Make the AI speak using Edge-TTS"""
        print(f"🤖 AI: {text}")
        
        # Create unique temp file to avoid permission issues
        import time
        temp_file = os.path.join(tempfile.gettempdir(), f"ai_speech_{int(time.time()*1000)}.mp3")
        
        try:
            # Generate speech with Edge-TTS
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(temp_file)
            
            # Play audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
        finally:
            # Clean up
            try:
                pygame.mixer.music.unload()
                await asyncio.sleep(0.2)  # Brief pause before deletion
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
    
    def speak(self, text):
        """Synchronous wrapper for speak"""
        asyncio.run(self.speak_async(text))
    
    def listen_once(self):
        """Listen for one command"""
        with self.microphone as source:
            print("\n🎙️  RECORDING... (speak now)")
            
            # Adjust for ambient noise quickly
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            
            try:
                # Listen with longer timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("🔄 Processing your voice...")
                
                # Use Google with British English
                text = self.recognizer.recognize_google(audio, language="en-GB")
                print(f"👂 You said: '{text}'")
                return text.lower()
                
            except sr.WaitTimeoutError:
                print("⏰ No speech detected")
                return None
            except sr.UnknownValueError:
                print("❓ Couldn't understand that")
                return None
            except Exception as e:
                print(f"❌ Error: {e}")
                return None
    
    def process_command(self, command):
        """Get AI response"""
        if not command:
            return "Yes, how can I help?"
        
        print(f"🧠 Thinking...")
        
        # Generate response
        with self.model.chat_session():
            response = self.model.generate(
                f"You are a helpful Yorkshire AI assistant. User said: '{command}'. Respond briefly and helpfully:",
                max_tokens=150,
                temp=0.7
            )
        
        return response.strip()
    
    def on_press(self, key):
        """Handle key press"""
        try:
            if key == kb.Key.space and not self.is_recording:
                self.is_recording = True
                # Start listening in background thread
                thread = threading.Thread(target=self.handle_voice_input)
                thread.daemon = True
                thread.start()
            elif key == kb.Key.esc:
                print("\n👋 Exiting...")
                self.should_stop = True
                return False  # Stop listener
        except:
            pass
    
    def on_release(self, key):
        """Handle key release - does nothing now, using press only"""
        pass
    
    def handle_voice_input(self):
        """Handle one voice interaction"""
        # Listen
        text = self.listen_once()
        
        # Reset recording flag
        self.is_recording = False
        
        if text:
            # Check for exit
            if any(word in text for word in ["exit", "quit", "goodbye", "stop", "ta ra"]):
                self.speak("Ta ra, Master! See thee later!")
                self.should_stop = True
                os._exit(0)
                return
            
            # Process command
            response = self.process_command(text)
            
            # Speak response
            self.speak(response)
    
    def run(self):
        """Main loop"""
        self.speak("Ey up! I'm ready. Just press SPACE when you want to talk to me.")
        
        print("\n" + "="*60)
        print("📍 CONTROLS:")
        print("   SPACE = Talk (wait for beep, then speak)")
        print("   ESC = Exit")
        print("="*60 + "\n")
        
        # Start keyboard listener
        with kb.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    try:
        agent = BetterVoiceAgent()
        agent.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
